/**
 * Урок курса как ноутбук Jupyter: одно пространство имён Python на урок (сеанс в воркере), ячейки
 * выполняются по нажатию. Устройство — docs/COURSES_PLAN.md, «Ячейки и состояние».
 *
 * - Сеанс: id выбирает страница; «Перезапустить» — новый id (новое пространство имён). Если воркер
 *   пересоздан (таймаут, падение), состояние потеряно — python.generation сменился.
 * - Ячейка «готова», если выполнена в текущем сеансе: демонстрация — без ошибки (или с ожидаемой
 *   [raises]), упражнение — проверка пройдена или выполнен эталон.
 * - Перед запуском ячейки невыполненные ячейки выше выполняются сами, по порядку. Упражнение выше, где
 *   ученик что-то написал, проверяется; не решённое (или пропущенное) заменяется эталонным решением —
 *   следующие ячейки не ломаются, а код ученика остаётся в редакторе.
 * - Код упражнений сохраняется в localStorage, изменённый код демонстраций — нет.
 * Код выполняется только по нажатию — никогда из ссылки или параметров URL.
 */
import { python, type RunEnd } from '../../lib/python/client';
import { PYTHON_CONFIG } from '../../lib/python/config';
import type { LessonDone, LessonRun, TestInfo, TestResult } from '../../lib/python/protocol';
import type { DemoData, ExerciseData, LessonPageData } from '../../lib/courses/site';
import type * as EditorApi from '../python/editor';
import * as progress from './progress';


const isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);
let editorModule: Promise<typeof EditorApi> | null = null;
const loadEditor = () => (editorModule ??= import('../python/editor'));

function el<K extends keyof HTMLElementTagNameMap>(tag: K, className?: string, text?: string): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

const newSession = () => Math.random().toString(36).slice(2, 10);

/** Текст ошибки запуска (не ошибки Python-кода): таймаут, падение, загрузка. */
function failureText(end: Exclude<RunEnd, { type: 'done' }>): string {
  if (end.type === 'timeout') return `Ячейка выполнялась дольше ${end.seconds} с и была остановлена — возможно, бесконечный цикл. Python перезапущен, состояние урока сброшено.`;
  if (end.type === 'crash') {
    if (end.message === 'остановлено') return 'Выполнение остановлено. Python перезапущен, состояние урока сброшено.';
    return /call stack|stack size|too much recursion/i.test(end.message)
      ? 'Кончился стек браузера — слишком глубокая рекурсия. Python перезапущен, состояние урока сброшено.'
      : `Python в браузере аварийно остановился (${end.message}). Он перезапущен, состояние урока сброшено.`;
  }
  const what = end.type === 'package-error' ? 'пакеты' : 'Python';
  return `Не удалось загрузить ${what}: ${end.message}. Проверьте подключение и попробуйте ещё раз — или скачайте урок как .ipynb и выполните в Jupyter.`;
}

// ─── Урок ───────────────────────────────────────────────────────────────────

abstract class CellView {
  readonly index: number;
  protected readonly root: HTMLElement;
  protected readonly lesson: Lesson;
  private readonly counter: HTMLElement;
  protected readonly live: HTMLElement;

  constructor(lesson: Lesson, root: HTMLElement, index: number) {
    this.lesson = lesson;
    this.root = root;
    this.index = index;
    this.counter = root.querySelector('[data-count]')!;
    this.live = root.querySelector('[data-live]')!;
    root.querySelector('[data-above]')?.addEventListener('click', () => void lesson.runAbove(this));
  }

  abstract readonly id: string;
  /** Выполнить так, чтобы ячейки ниже могли на неё опираться. */
  abstract prepare(): Promise<boolean>;
  /** Сбросить отображение после «Перезапустить». */
  abstract clear(): void;

  setCount(value: number | '*' | null): void {
    this.counter.textContent = `[${value ?? ' '}]`;
    this.counter.classList.toggle('is-run', value !== null);
  }

  scrollIntoView(): void {
    this.root.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  /** Строка состояния: «сначала выполняются ячейки выше…». */
  abstract status(text: string, isError?: boolean): void;

  protected request(op: LessonRun['op'], code: string, extra: Partial<LessonRun> = {}): Omit<LessonRun, 'runId'> {
    return { ...this.lesson.base(), op, cell: this.id, code, ...extra };
  }

  /** Живой вывод ячейки: печать, значение (таблица DataFrame — HTML), ошибка. */
  protected renderOutput(d: LessonDone, label: string, markError: (line: number) => void): Node[] {
    const children: Node[] = [];
    const head = el('div', 'live-head');
    const seconds = d.elapsed < 0.01 ? '<0,01' : d.elapsed.toFixed(2).replace('.', ',');
    const title = el('span', `out-label${d.error ? ' is-error' : ''}`, d.error ? 'Ошибка' : label);
    title.append(el('span', 'out-hint', `в браузере, ${seconds} с`));
    head.append(title);
    children.push(head);
    if (d.lines.length) children.push(el('pre', 'out-text', d.lines.join('\n')));
    if (d.html) {
      const table = el('div', 'out-table');
      table.innerHTML = d.html; // таблицу собрал pandas (значения экранированы) из данных этого же сеанса
      children.push(table);
    } else if (d.result) children.push(el('pre', 'out-text', d.result.join('\n')));
    if (d.error) {
      const pre = el('pre', 'out-text out-error', d.error.text);
      if (d.error.line) {
        const link = el('button', 'line-link', `строка ${d.error.line}`);
        link.type = 'button';
        link.addEventListener('click', () => markError(d.error!.line!));
        pre.append(' ', link);
      }
      children.push(pre);
    }
    if (d.truncated) children.push(el('p', 'live-note', `Вывод обрезан: больше ${PYTHON_CONFIG.maxLines.toLocaleString('ru')} строк или 1 МБ.`));
    for (const svg of d.plots) {
      const img = el('img');
      img.src = URL.createObjectURL(new Blob([svg], { type: 'image/svg+xml' }));
      img.alt = 'График, построенный в браузере';
      children.push(img);
    }
    if (!d.lines.length && !d.result && !d.html && !d.error && !d.plots.length) children.push(el('p', 'live-empty', 'Нет вывода — ячейка выполнена.'));
    return children;
  }
}

class DemoView extends CellView {
  readonly id: string;
  private readonly data: DemoData;
  private readonly runButton: HTMLButtonElement;
  private readonly editButton: HTMLButtonElement;
  private readonly codeBox: HTMLElement;
  private readonly stored: HTMLElement | null;
  private view: EditorApi.EditorView | null = null;
  private editor: typeof EditorApi | null = null;

  constructor(lesson: Lesson, root: HTMLElement, index: number, data: DemoData) {
    super(lesson, root, index);
    this.id = data.id;
    this.data = data;
    this.runButton = root.querySelector('[data-run]')!;
    this.editButton = root.querySelector('[data-edit]')!;
    this.codeBox = root.querySelector('[data-code]')!;
    this.stored = root.querySelector('[data-stored]');
    this.runButton.addEventListener('click', () => void lesson.run(this));
    this.editButton.addEventListener('click', () => void this.toggleEdit());
  }

  private get edited(): boolean {
    return !!this.view && !!this.editor && this.editor.getCode(this.view) !== this.data.code;
  }

  code(): string {
    return this.view && this.editor ? this.editor.getCode(this.view) : this.data.code;
  }

  private async toggleEdit(): Promise<void> {
    const label = this.root.querySelector<HTMLElement>('[data-edit-label]')!;
    const staticCode = this.codeBox.firstElementChild as HTMLElement;
    if (this.view) {
      // «Вернуть»: исходный код и сохранённый вывод
      this.view.destroy();
      this.view = null;
      staticCode.hidden = false;
      label.textContent = 'Изменить';
      this.editButton.title = 'Изменить код и выполнить свой вариант';
      this.showStored();
      return;
    }
    this.editor = await loadEditor();
    staticCode.hidden = true;
    this.view = this.editor.createEditor({ parent: this.codeBox, doc: this.data.code, label: 'Код ячейки', onRun: () => void this.lesson.run(this) });
    this.view.focus();
    label.textContent = 'Вернуть';
    this.editButton.title = 'Вернуть исходный код ячейки';
  }

  private showStored(): void {
    this.live.hidden = true;
    this.live.replaceChildren();
    if (this.stored) this.stored.hidden = false;
  }

  private showLive(children: Node[]): void {
    if (this.stored) this.stored.hidden = true;
    this.live.replaceChildren(...children);
    this.live.hidden = false;
  }

  status(text: string, isError = false): void {
    this.showLive([el('p', `live-status${isError ? ' is-error' : ''}`, text)]);
  }

  setRunning(running: boolean): void {
    this.runButton.classList.toggle('is-running', running);
    if (running) this.setCount('*');
  }

  /** Выполняет ячейку; true — ячейка готова (нет ошибки или ожидаемая ошибка [raises]). */
  async execute(): Promise<boolean> {
    const code = this.code();
    const edited = this.edited;
    if (this.view && this.editor) this.editor.markLine(this.view, null);
    this.setRunning(true);
    const end = await this.lesson.exec(this.request('cell', code), (text) => this.status(text || 'Выполняется…'));
    this.setRunning(false);
    if (end.type !== 'done') {
      this.setCount(null);
      this.showLive([el('p', 'live-status is-error', failureText(end))]);
      return false;
    }
    const d = end.data as LessonDone;
    this.setCount(this.lesson.nextCount());
    const expected = this.data.raises && !edited && d.error?.mro.includes(this.data.raises);
    const markError = (line: number) => {
      if (this.view && this.editor) this.editor.goToLine(this.view, line);
    };
    this.showLive(this.renderOutput(d, 'Вывод', markError));
    if (d.error && !expected && d.error.line && this.view && this.editor) this.editor.markLine(this.view, d.error.line);
    return !d.error || !!expected;
  }

  prepare(): Promise<boolean> {
    return this.execute();
  }

  clear(): void {
    this.setCount(null);
    this.showStored();
  }
}

class ExerciseView extends CellView {
  readonly id: string;
  private readonly data: ExerciseData;
  private readonly checkButton: HTMLButtonElement;
  private readonly statusLine: HTMLElement;
  private readonly results: HTMLElement;
  private readonly summary: HTMLElement;
  private readonly testList: HTMLElement;
  private readonly note: HTMLElement;
  private code: string;
  private view: EditorApi.EditorView | null = null;
  private editor: typeof EditorApi | null = null;
  private saveTimer: ReturnType<typeof setTimeout> | undefined;

  constructor(lesson: Lesson, root: HTMLElement, index: number, data: ExerciseData) {
    super(lesson, root, index);
    this.id = data.id;
    this.data = data;
    const q = <T extends HTMLElement = HTMLElement>(s: string) => root.querySelector<T>(s)!;
    this.checkButton = q('[data-check]');
    this.statusLine = q('[data-status]');
    this.results = q('[data-results]');
    this.summary = q('[data-summary]');
    this.testList = q('[data-tests]');
    this.note = q('[data-substituted]');
    q('[data-shortcut]').textContent = isMac ? '⌘ Enter' : 'Ctrl+Enter';

    // код: сохранённый или заготовка; заготовка могла измениться после сохранения
    const saved = progress.loadCode(lesson.id, data.id);
    this.code = saved?.code ?? data.starter;
    const changed = q('[data-starter-changed]');
    if (saved && saved.starter !== data.starterHash && saved.code !== data.starter) changed.hidden = false;
    q('[data-keep-mine]').addEventListener('click', () => {
      progress.saveCode(lesson.id, data.id, { code: this.code, starter: data.starterHash });
      changed.hidden = true;
    });
    q('[data-take-new]').addEventListener('click', () => {
      this.setCode(data.starter);
      progress.saveCode(lesson.id, data.id, null);
      changed.hidden = true;
    });

    const confirm = q('[data-reset-confirm]');
    q('[data-reset]').addEventListener('click', () => (confirm.hidden = false));
    q('[data-reset-no]').addEventListener('click', () => (confirm.hidden = true));
    q('[data-reset-yes]').addEventListener('click', () => {
      confirm.hidden = true;
      changed.hidden = true;
      this.setCode(data.starter);
      progress.saveCode(lesson.id, data.id, null);
    });

    this.checkButton.addEventListener('click', () => void lesson.run(this));
    this.initHints();
    const solution = q('[data-solution]');
    const toggle = q('[data-solution-toggle]');
    toggle.addEventListener('click', () => {
      solution.hidden = !solution.hidden;
      toggle.setAttribute('aria-expanded', String(!solution.hidden));
      q('[data-solution-label]').textContent = solution.hidden ? 'Решение' : 'Скрыть решение';
    });
    this.renderSolved();
    window.addEventListener('pagehide', () => this.save());
  }

  async mountEditor(api: typeof EditorApi): Promise<void> {
    this.editor = api;
    const parent = this.root.querySelector<HTMLElement>('[data-editor]')!;
    this.root.querySelector('[data-editor-placeholder]')?.remove();
    this.view = api.createEditor({
      parent,
      doc: this.code,
      label: 'Код упражнения',
      onRun: () => void this.lesson.run(this),
      onChange: (text) => {
        this.code = text;
        clearTimeout(this.saveTimer);
        this.saveTimer = setTimeout(() => this.save(), PYTHON_CONFIG.saveDelay);
      },
    });
  }

  private initHints(): void {
    const hints = [...this.root.querySelectorAll<HTMLElement>('[data-hint]')];
    hints.forEach((h, i) => (h.querySelector('[data-hint-n]')!.textContent = `Подсказка ${i + 1}`));
    const button = this.root.querySelector<HTMLButtonElement>('[data-hint-next]');
    if (!button) return;
    let shown = 0;
    button.addEventListener('click', () => {
      if (shown >= hints.length) return;
      hints[shown++].hidden = false;
      this.root.querySelector('[data-hint-counter]')!.textContent = `${shown} / ${hints.length}`;
      const label = this.root.querySelector('[data-hint-label]')!;
      if (shown === hints.length) {
        button.disabled = true;
        label.textContent = 'Подсказки закончились';
      } else label.textContent = 'Ещё подсказка';
    });
  }

  private save(): void {
    clearTimeout(this.saveTimer);
    const current = progress.loadCode(this.lesson.id, this.id);
    progress.saveCode(this.lesson.id, this.id, this.code === this.data.starter ? null : { code: this.code, starter: current?.starter ?? this.data.starterHash });
  }

  private setCode(text: string): void {
    this.code = text;
    if (this.view && this.editor) {
      this.editor.setCode(this.view, text);
      this.editor.markLine(this.view, null);
    }
  }

  /** Ученик что-то написал (код отличается от заготовки). */
  get written(): boolean {
    return this.code.trim() !== this.data.starter.trim();
  }

  renderSolved(): void {
    this.root.classList.toggle('is-solved', progress.isSolved(this.lesson.id, this.id));
  }

  status(text: string, isError = false): void {
    this.statusLine.textContent = text;
    this.statusLine.classList.toggle('is-error', isError);
  }

  private markError(line: number | null): void {
    if (this.view && this.editor) this.editor.markLine(this.view, line);
  }

  private lineLink(line: number): HTMLButtonElement {
    const link = el('button', 'line-link', `строка ${line}`);
    link.type = 'button';
    link.addEventListener('click', () => this.view && this.editor?.goToLine(this.view, line));
    return link;
  }

  private renderTest(item: HTMLLIElement, title: string, state: TestResult['status'] | 'pending' | 'running', message = '', line: number | null = null): void {
    const marks: Record<string, string> = { passed: '✓', not_run: '–', pending: '·', running: '…' };
    item.className = state === 'passed' ? 'passed' : state === 'not_run' || state === 'pending' ? 'pending' : state === 'running' ? 'running' : 'bad';
    item.replaceChildren(el('span', 'mark', marks[state] ?? '✗'), el('span', 'title', title));
    if (message || line) {
      const msg = el('span', 'message', message);
      if (line) msg.append(' ', this.lineLink(line));
      item.append(msg);
    }
  }

  private setSummary(text: string, tone: 'pass' | 'fail' | null, sub?: string): void {
    this.results.hidden = false;
    this.summary.className = `summary${tone ? ` is-${tone}` : ''}`;
    this.summary.replaceChildren(text);
    if (sub) this.summary.append(el('span', 'sub', sub));
  }

  /** «Проверить»: код ученика как ячейка + тесты на состоянии урока. true — все проверки пройдены. */
  async check(): Promise<boolean> {
    this.save();
    this.markError(null);
    this.note.hidden = true;
    this.checkButton.classList.add('is-running');
    this.setCount('*');
    this.setSummary('Выполняется…', null);
    this.testList.replaceChildren();
    this.live.hidden = true;
    let tests: TestInfo[] = [];
    const items: HTMLLIElement[] = [];
    const got: (TestResult | undefined)[] = [];
    const code = this.code;
    const end = await this.lesson.exec(
      this.request('check', code, { tests: this.data.tests, targets: this.data.targets }),
      (text) => this.status(text),
      {
        onTests: (list) => {
          tests = list;
          for (const t of list) {
            const item = el('li');
            this.renderTest(item, t.title, 'pending');
            items.push(item);
          }
          this.testList.replaceChildren(...items);
        },
        onTestStart: (i) => items[i] && this.renderTest(items[i], tests[i].title, 'running'),
        onTest: (i, r) => {
          got[i] = r;
          if (items[i]) this.renderTest(items[i], r.title, r.status, r.message, r.line);
        },
      },
    );
    this.checkButton.classList.remove('is-running');
    this.status('');
    if (end.type !== 'done') {
      this.setCount(null);
      tests.forEach((t, i) => !got[i] && this.renderTest(items[i], t.title, 'not_run', 'не запускался'));
      this.setSummary('Проверка не завершилась', 'fail', failureText(end));
      return false;
    }
    const d = end.data as LessonDone;
    this.setCount(this.lesson.nextCount());
    const output = d.lines.length || d.result || d.html || d.error;
    if (output) {
      this.live.replaceChildren(...this.renderOutput(d, 'Вывод вашего кода', (line) => this.view && this.editor?.goToLine(this.view, line)));
      this.live.hidden = false;
    }
    if (d.phase === 'run') {
      this.setSummary('Код завершился с ошибкой — проверки не запускались', 'fail', d.error ? `${d.error.text}${d.error.line ? ` (строка ${d.error.line})` : ''}` : undefined);
      this.markError(d.error?.line ?? null);
      return false;
    }
    if (d.phase === 'missing') {
      this.setSummary('Упражнение ещё не выполнено', 'fail', d.results?.[0]?.title);
      this.testList.replaceChildren();
      return false;
    }
    const list = d.results ?? [];
    this.testList.replaceChildren(
      ...list.map((r, i) => {
        const item = items[i] ?? el('li');
        this.renderTest(item, r.title, r.status, r.message, r.line);
        return item;
      }),
    );
    const passed = list.filter((r) => r.status === 'passed').length;
    const all = list.length > 0 && passed === list.length;
    const notWritten = list.some((r) => r.status === 'not_written');
    this.setSummary(
      all ? `Все проверки пройдены — ${passed} из ${list.length}` : `Пройдено ${passed} из ${list.length}`,
      all ? 'pass' : 'fail',
      notWritten ? 'Функция ещё не написана — замените raise NotImplementedError своим кодом.' : undefined,
    );
    this.markError(list.find((r) => r.line)?.line ?? null);
    if (all) {
      progress.setSolved(this.lesson.id, this.id, await sha(code));
      this.renderSolved();
      this.lesson.onSolved();
    }
    return all;
  }

  /** Эталон вместо нерешённого упражнения — чтобы ячейки ниже работали. Код ученика не трогается. */
  private async substitute(): Promise<boolean> {
    this.setCount('*');
    const end = await this.lesson.exec(this.request('cell', this.data.solution), (text) => this.status(text));
    this.status('');
    if (end.type !== 'done' || (end.data as LessonDone).error) {
      this.setCount(null);
      this.status(end.type === 'done' ? `Эталонное решение не выполнилось: ${(end.data as LessonDone).error?.text}` : failureText(end), true);
      return false;
    }
    this.setCount(this.lesson.nextCount());
    this.note.hidden = false;
    return true;
  }

  async prepare(): Promise<boolean> {
    const epoch = this.lesson.epoch;
    if (this.written && (await this.check())) return true;
    if (this.lesson.epoch !== epoch) return false; // проверка уронила Python — дальше выполнять нечего
    return this.substitute();
  }

  clear(): void {
    this.setCount(null);
    this.results.hidden = true;
    this.testList.replaceChildren();
    this.live.hidden = true;
    this.live.replaceChildren();
    this.note.hidden = true;
    this.status('');
    this.markError(null);
  }
}

async function sha(text: string): Promise<string> {
  try {
    const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
    return [...new Uint8Array(digest)].slice(0, 8).map((b) => b.toString(16).padStart(2, '0')).join('');
  } catch {
    return '';
  }
}

class Lesson {
  readonly id: string;
  private readonly data: LessonPageData;
  private readonly cells: CellView[] = [];
  private session = newSession();
  private generation = -1; // python.generation, при котором начат сеанс
  /** Растёт при каждом сбросе состояния: цепочка запусков, начатая до сброса, останавливается. */
  epoch = 0;
  private readonly ready = new Set<string>();
  private count = 0;
  private busy = false;
  private readonly bar: HTMLElement;
  private readonly barText: HTMLElement;
  private readonly notice: HTMLElement;

  constructor(data: LessonPageData) {
    this.id = data.lesson;
    this.data = data;
    this.bar = document.querySelector('[data-kernel]')!;
    this.barText = this.bar.querySelector('[data-kernel-text]')!;
    this.notice = document.querySelector('[data-kernel-notice]')!;
    for (const cell of data.cells) {
      const root = document.querySelector<HTMLElement>(`[data-cell="${cell.id}"]`);
      if (!root) continue;
      const i = this.cells.length;
      this.cells.push(cell.kind === 'demo' ? new DemoView(this, root, i, cell) : new ExerciseView(this, root, i, cell));
    }
    this.bar.querySelector('[data-run-all]')!.addEventListener('click', () => void this.runAll());
    this.bar.querySelector('[data-restart]')!.addEventListener('click', () => this.restart());
    python.subscribe(() => this.renderBar());
    this.renderBar();
  }

  base(): Omit<LessonRun, 'runId' | 'op' | 'cell' | 'code'> {
    return { kind: 'lesson', lesson: this.id, session: this.session, files: this.data.files, packages: this.data.packages };
  }

  nextCount(): number {
    return ++this.count;
  }

  /** Состояние потеряно: воркер пересоздан после таймаута или падения. */
  lost(): boolean {
    return this.generation !== -1 && python.generation !== this.generation;
  }

  private syncGeneration(): void {
    this.generation = python.generation;
  }

  private isReady(cell: CellView): boolean {
    return !this.lost() && this.ready.has(cell.id);
  }

  /** Запуск через общий воркер; после таймаута/падения состояние сбрасывается и об этом сообщается. */
  async exec(
    request: Omit<LessonRun, 'runId'>,
    onStatus: (text: string) => void,
    handlers: { onTests?(t: TestInfo[]): void; onTestStart?(i: number): void; onTest?(i: number, r: TestResult): void } = {},
  ): Promise<RunEnd> {
    const end = await python.run(request, { onStatus, onStarted: () => onStatus(''), ...handlers });
    if (end.type === 'done' && this.generation === -1) this.syncGeneration();
    if (end.type === 'done' && (end.data as LessonDone).memory) this.dropState('Python перезапущен после нехватки памяти — состояние урока сброшено.');
    else if (end.type === 'timeout' || end.type === 'crash') this.dropState(null);
    this.renderBar();
    return end;
  }

  /** Всё, что было выполнено, потеряно: номера ячеек гаснут, выводы остаются для чтения. */
  private dropState(message: string | null): void {
    this.epoch++;
    this.ready.clear();
    this.count = 0;
    this.session = newSession();
    this.generation = -1;
    for (const c of this.cells) c.setCount(null);
    this.showNotice(message ?? 'Python перезапущен — состояние урока сброшено: ячейки выше выполнятся заново при следующем запуске.');
  }

  private showNotice(text: string): void {
    this.notice.textContent = text;
    this.notice.hidden = false;
  }

  private renderBar(): void {
    const total = this.cells.length;
    const done = this.cells.filter((c) => this.isReady(c)).length;
    const state = python.state;
    this.bar.classList.toggle('is-busy', this.busy);
    this.barText.textContent =
      state === 'loading' ? python.statusText || 'Загружаем Python…'
      : state === 'failed' ? 'Python не загрузился'
      : state === 'idle' && !this.count ? 'Python запустится при первом выполнении'
      : `Выполнено ячеек: ${done} из ${total}`;
  }

  /** Выполняет ячейку; невыполненные ячейки выше — сначала, по порядку. */
  async run(target: CellView): Promise<void> {
    if (this.busy) {
      target.status('Дождитесь окончания — выполняется другая ячейка.');
      return;
    }
    this.busy = true;
    this.notice.hidden = true;
    if (this.lost()) this.dropState(null); // воркер пересоздан вне запусков урока
    try {
      const pending = this.cells.slice(0, target.index).filter((c) => !this.isReady(c));
      if (!(await this.prepareAll(pending, target))) return;
      const epoch = this.epoch;
      const ok = target instanceof ExerciseView ? await target.check() : await (target as DemoView).execute();
      if (ok && this.epoch === epoch) this.ready.add(target.id);
      else this.ready.delete(target.id);
    } finally {
      this.busy = false;
      this.renderBar();
    }
  }

  /** «Выполнить все выше» — заново, даже уже выполненные. */
  async runAbove(target: CellView): Promise<void> {
    if (this.busy) return;
    this.busy = true;
    this.notice.hidden = true;
    try {
      if (await this.prepareAll(this.cells.slice(0, target.index), target)) target.status('Ячейки выше выполнены.');
    } finally {
      this.busy = false;
      this.renderBar();
    }
  }

  /** «Выполнить всё»: каждая ячейка по порядку; упражнения — код ученика или эталон. */
  private async runAll(): Promise<void> {
    if (this.busy || !this.cells.length) return;
    this.busy = true;
    this.notice.hidden = true;
    try {
      await this.prepareAll(this.cells, null);
    } finally {
      this.busy = false;
      this.renderBar();
    }
  }

  private async prepareAll(cells: CellView[], target: CellView | null): Promise<boolean> {
    const epoch = this.epoch;
    for (const [i, cell] of cells.entries()) {
      target?.status(`Сначала выполняются ячейки выше: ${i + 1} из ${cells.length}…`);
      this.renderBar();
      const ok = await cell.prepare();
      if (this.epoch !== epoch) {
        target?.status('Python перезапущен — выполнение остановлено.', true);
        return false;
      }
      if (ok) {
        this.ready.add(cell.id);
        continue;
      }
      this.ready.delete(cell.id);
      if (target && target !== cell) {
        target.status('Ячейка выше завершилась с ошибкой — посмотрите её и выполните снова.', true);
        cell.scrollIntoView();
      }
      return false;
    }
    return true;
  }

  /** «Перезапустить»: новое пространство имён; идущий запуск останавливается. */
  private restart(): void {
    if (this.busy) python.stop();
    this.epoch++;
    this.ready.clear();
    this.count = 0;
    this.session = newSession();
    this.generation = -1;
    for (const c of this.cells) c.clear();
    this.showNotice('Состояние урока сброшено: переменные удалены, файлы данных — исходные.');
    this.renderBar();
  }

  /** Решено упражнение: если решены все — урок отмечается пройденным (если его не отмечали вручную). */
  onSolved(): void {
    const exercises = this.data.cells.filter((c) => c.kind === 'exercise').map((c) => c.id);
    if (exercises.every((e) => progress.isSolved(this.id, e))) progress.setDone(this.id, true);
  }

  async mountEditors(): Promise<void> {
    const api = await loadEditor();
    for (const c of this.cells) if (c instanceof ExerciseView) await c.mountEditor(api);
  }

  /** Фоновая загрузка Python, пакетов и данных, когда браузер простаивает (не при экономии трафика). */
  preload(): void {
    const connection = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection;
    if (connection?.saveData) return;
    const start = () => void python.run({ ...this.base(), op: 'prepare', cell: '', code: '' }, { onStatus: () => this.renderBar() }).then(() => this.renderBar());
    if ('requestIdleCallback' in window) requestIdleCallback(start, { timeout: 5000 });
    else setTimeout(start, 2000);
  }
}

// ─── Вопросы ────────────────────────────────────────────────────────────────

function initQuiz(root: HTMLElement): void {
  const feedback = root.querySelector<HTMLElement>('[data-feedback]')!;
  const explain = root.querySelector<HTMLElement>('[data-explain]');
  const options = [...root.querySelectorAll<HTMLButtonElement>('[data-option]')];
  let wrong = 0;
  for (const option of options) {
    option.addEventListener('click', () => {
      const correct = option.hasAttribute('data-correct');
      option.classList.add(correct ? 'is-correct' : 'is-wrong');
      if (correct) {
        options.forEach((o) => (o.disabled = true));
        feedback.textContent = 'Верно!';
        feedback.className = 'quiz-feedback is-pass';
        if (explain) explain.hidden = false;
        return;
      }
      option.disabled = true;
      wrong++;
      feedback.textContent = wrong === 1 ? 'Не совсем — попробуйте ещё раз.' : 'Снова мимо. Подсказка — в тексте выше; или выберите другой вариант.';
      feedback.className = 'quiz-feedback is-fail';
    });
  }
}

// ─── Страница ───────────────────────────────────────────────────────────────

export function initLesson(): void {
  const node = document.getElementById('lesson-data');
  if (!node) return;
  const data = JSON.parse(node.textContent!) as LessonPageData;
  progress.setLast(data.course, data.lesson);
  const lesson = new Lesson(data);
  void lesson.mountEditors();
  lesson.preload();
  document.querySelectorAll<HTMLElement>('[data-quiz]').forEach(initQuiz);

  // отметка «Урок пройден»: вручную или сама, когда решены все упражнения
  const toggle = document.querySelector<HTMLInputElement>('[data-lesson-done]');
  const exercises = data.cells.filter((c) => c.kind === 'exercise').map((c) => c.id);
  const sync = () => {
    if (toggle) toggle.checked = progress.isDone(data.lesson, exercises);
    const solved = exercises.filter((e) => progress.isSolved(data.lesson, e)).length;
    document.querySelectorAll<HTMLElement>('[data-lesson-solved]').forEach((el) => (el.textContent = String(solved)));
  };
  toggle?.addEventListener('change', () => progress.setDone(data.lesson, toggle.checked));
  document.addEventListener(progress.COURSE_EVENT, sync);
  sync();
}
