/**
 * Страница задачи: редактор, запуск тестов в браузере, сохранение кода в localStorage (scripts/code-store.ts).
 * Код выполняется только по нажатию «Запустить» (или Ctrl/Cmd+Enter) — никогда из ссылки или URL.
 */
import { joinBundle } from '../../lib/bundle';
import { python, type RunEnd } from '../../lib/python/client';
import { PYTHON_CONFIG } from '../../lib/python/config';
import type { TaskDone, TestInfo, TestResult } from '../../lib/python/protocol';
import { loadCode as loadSaved, saveCode as store, watchRemoteCode } from '../code-store';
import { setSolved } from '../progress';
import type * as EditorApi from './editor';

interface WorkbenchData {
  taskId: string;
  starter: string;
  starterHash: string;
  header: string;
  footer: string;
  packages: string[];
  filename: string;
}

const isMac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent);

function el<K extends keyof HTMLElementTagNameMap>(tag: K, className?: string, text?: string): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

export function initWorkbench(root: HTMLElement): void {
  const data = JSON.parse(root.querySelector('[data-workbench-data]')!.textContent!) as WorkbenchData;
  const q = <T extends HTMLElement = HTMLElement>(selector: string) => root.querySelector<T>(selector)!;
  const runButton = q<HTMLButtonElement>('[data-run]');
  const runLabel = q('[data-run-label]');
  const engineStatus = q('[data-engine-status]');
  const results = q('[data-results]');
  const summary = q('[data-summary]');
  const testList = q('[data-test-list]');
  const output = q('[data-output]');
  const outputText = q('[data-output-text]');
  const outputTruncated = q('[data-output-truncated]');
  const copied = q('[data-copied]');
  q('[data-shortcut]').textContent = isMac ? '⌘ Enter' : 'Ctrl+Enter';

  // ─── Редактор и сохранение ────────────────────────────────────────────────
  const saved = loadSaved(data.taskId);
  let code = saved?.code ?? data.starter;
  let opened = code; // код при открытии или последний пришедший с другого устройства
  let editor: typeof EditorApi | null = null;
  let view: EditorApi.EditorView | null = null;
  let saveTimer: ReturnType<typeof setTimeout> | undefined;

  const save = () => {
    clearTimeout(saveTimer);
    const current = loadSaved(data.taskId);
    store(data.taskId, code === data.starter ? null : { code, starter: current?.starter ?? data.starterHash });
  };
  const setEditorCode = (text: string) => {
    code = text;
    if (view && editor) editor.setCode(view, text);
  };

  const changed = q('[data-starter-changed]');
  if (saved && saved.starter !== data.starterHash && saved.code !== data.starter) changed.hidden = false;
  // код с другого устройства (после входа) — подставляем, пока здесь ничего не правили
  watchRemoteCode(data.taskId, () => code === opened, (remote) => {
    clearTimeout(saveTimer);
    opened = remote?.code ?? data.starter;
    setEditorCode(opened);
    changed.hidden = !(remote && remote.starter !== data.starterHash && remote.code !== data.starter);
  });
  q('[data-keep-mine]').addEventListener('click', () => {
    store(data.taskId, { code, starter: data.starterHash });
    changed.hidden = true;
  });
  q('[data-take-new]').addEventListener('click', () => {
    setEditorCode(data.starter);
    store(data.taskId, null);
    changed.hidden = true;
  });

  import('./editor').then((api) => {
    editor = api;
    const parent = q('[data-editor]');
    q('[data-editor-placeholder]').remove();
    view = api.createEditor({
      parent,
      doc: code,
      label: 'Код решения',
      onRun: () => void run(),
      onChange: (text) => {
        code = text;
        clearTimeout(saveTimer);
        saveTimer = setTimeout(save, PYTHON_CONFIG.saveDelay);
      },
    });
  });
  window.addEventListener('pagehide', save);

  // ─── Кнопки ───────────────────────────────────────────────────────────────
  const confirmBox = q('[data-reset-confirm]');
  q('[data-reset]').addEventListener('click', () => (confirmBox.hidden = false));
  q('[data-reset-no]').addEventListener('click', () => (confirmBox.hidden = true));
  q('[data-reset-yes]').addEventListener('click', () => {
    confirmBox.hidden = true;
    changed.hidden = true;
    setEditorCode(data.starter);
    store(data.taskId, null);
    if (view && editor) editor.markLine(view, null);
  });

  const testsSource = q('[data-tests-source]');
  const toggleTests = q('[data-toggle-tests]');
  toggleTests.addEventListener('click', () => {
    testsSource.hidden = !testsSource.hidden;
    toggleTests.setAttribute('aria-expanded', String(!testsSource.hidden));
    q('[data-toggle-label]').textContent = testsSource.hidden ? 'Показать тесты' : 'Скрыть тесты';
  });

  const copy = async (text: string, done: string) => {
    try {
      await navigator.clipboard.writeText(text);
      copied.textContent = done;
    } catch {
      copied.textContent = 'Буфер обмена недоступен — выделите код вручную';
    }
    setTimeout(() => (copied.textContent = ''), 2200);
  };
  q('[data-copy-full]').addEventListener('click', () =>
    copy(joinBundle(data.header, code, data.footer), `Скопирован файл с тестами — сохраните как ${data.filename}`),
  );
  q('[data-copy-mine]').addEventListener('click', () => copy(code, 'Код скопирован'));

  // ─── Состояние Python ─────────────────────────────────────────────────────
  let running = false;
  python.subscribe((state, text) => {
    runButton.classList.toggle('is-waiting', state === 'loading' && !running);
    runButton.setAttribute('aria-disabled', String(state === 'loading'));
    if (!running) {
      engineStatus.classList.remove('is-error');
      engineStatus.textContent = state === 'loading' ? `${text} Запуск можно нажать — он начнётся сам.` : '';
    }
  });
  python.preloadWhenIdle();
  runButton.addEventListener('click', () => void run());

  // ─── Результаты ───────────────────────────────────────────────────────────
  const lineLink = (line: number) => {
    const link = el('button', 'line-link', `строка ${line}`);
    link.type = 'button';
    link.addEventListener('click', () => view && editor?.goToLine(view, line));
    return link;
  };

  const renderTest = (item: HTMLLIElement, title: string, state: TestResult['status'] | 'pending' | 'running', message = '', line: number | null = null) => {
    const marks: Record<string, string> = { passed: '✓', not_run: '–', pending: '·', running: '…' };
    item.className = state === 'passed' ? 'passed' : state === 'not_run' ? 'skipped' : state === 'pending' ? 'pending' : state === 'running' ? 'running' : 'bad';
    item.replaceChildren(el('span', 'mark', marks[state] ?? '✗'), el('span', 'title', title));
    if (message || line) {
      const msg = el('span', 'message', message);
      if (line) msg.append(lineLink(line));
      item.append(msg);
    }
  };

  const setSummary = (text: string, tone: 'pass' | 'fail' | null, sub?: string, line?: number | null) => {
    summary.className = `summary${tone ? ` is-${tone}` : ''}`;
    summary.replaceChildren(text);
    if (sub || line) {
      const s = el('span', 'sub', sub ?? '');
      if (line) s.append(lineLink(line));
      summary.append(s);
    }
  };

  const markError = (line: number | null) => {
    if (view && editor) editor.markLine(view, line);
  };

  async function run(): Promise<void> {
    if (running) return;
    running = true;
    save();
    markError(null);
    runButton.classList.add('is-running');
    runButton.classList.remove('is-waiting');
    runLabel.textContent = python.state === 'ready' ? 'Выполняется…' : 'В очереди…';
    results.hidden = false;
    setSummary('Выполняется…', null);
    testList.replaceChildren();
    output.hidden = true;
    outputText.replaceChildren();
    outputTruncated.hidden = true;

    let tests: TestInfo[] = [];
    const items: HTMLLIElement[] = [];
    const got: (TestResult | undefined)[] = [];

    const end: RunEnd = await python.run(
      { kind: 'task', packages: data.packages, code, footer: data.footer },
      {
        onStatus: (text) => {
          engineStatus.textContent = text;
          if (text) runLabel.textContent = 'В очереди…';
        },
        onStarted: () => (runLabel.textContent = 'Выполняется…'),
        onOutput: (chunks, truncated) => {
          output.hidden = false;
          for (const [stream, text] of chunks) {
            if (stream === 'err') outputText.append(el('span', 'err', text));
            else outputText.append(text);
          }
          if (truncated) outputTruncated.hidden = false;
        },
        onTests: (list) => {
          tests = list;
          for (const t of list) {
            const item = el('li');
            renderTest(item, t.title, 'pending');
            items.push(item);
          }
          testList.replaceChildren(...items);
        },
        onTestStart: (i) => items[i] && renderTest(items[i], tests[i].title, 'running'),
        onTest: (i, r) => {
          got[i] = r;
          if (items[i]) renderTest(items[i], r.title, r.status, r.message, r.line);
        },
      },
    );

    running = false;
    runButton.classList.remove('is-running');
    runLabel.textContent = 'Запустить';
    engineStatus.textContent = '';
    finish(end, tests, items, got);
  }

  function finish(end: RunEnd, tests: TestInfo[], items: HTMLLIElement[], got: (TestResult | undefined)[]): void {
    const tail = (reason: string) => {
      // уже пройденные тесты видны; текущий и оставшиеся — помечены
      tests.forEach((t, i) => {
        if (got[i]) return;
        renderTest(items[i], t.title, 'not_run', reason);
      });
    };
    const passedSoFar = got.filter((r) => r?.status === 'passed').length;

    if (end.type === 'load-error' || end.type === 'package-error') {
      engineStatus.classList.add('is-error');
      const what = end.type === 'load-error' ? 'Python' : 'пакеты';
      setSummary(`Не удалось загрузить ${what} в браузере`, 'fail',
        `${end.message}. Проверьте подключение и запустите ещё раз — или нажмите «Скопировать с тестами» и запустите у себя: python3 ${data.filename}`);
      return;
    }
    if (end.type === 'crash') {
      tail('не запускался: Python остановился');
      const stack = /call stack|stack size|too much recursion/i.test(end.message);
      setSummary('Python в браузере аварийно остановился', 'fail', stack
        ? 'Кончился стек браузера. Рекурсия через @cache / lru_cache, sum(…) или map в браузере выдерживает меньше уровней, ' +
          'чем обычная (в Safari — около 60): замените её таблицей или обычной рекурсией со словарём — или запустите файл у себя. ' +
          'Python перезапущен.'
        : `Возможно, не хватило памяти (${end.message}). Python перезапущен — можно запускать снова.`);
      return;
    }
    if (end.type === 'timeout') {
      if (end.testIndex === null && !end.tests) {
        setSummary('Код выполнялся слишком долго ещё до запуска тестов', 'fail',
          `Остановлено через ${end.seconds} с — возможно, бесконечный цикл вне функции. Python перезапущен.`);
        return;
      }
      if (end.testIndex !== null && tests[end.testIndex]) {
        const t = tests[end.testIndex];
        got[end.testIndex] = { title: t.title, status: 'timeout', message: `${t.timeout_message} (в браузере ждали ${end.seconds} с)`, error_type: null, line: null };
        renderTest(items[end.testIndex], t.title, 'timeout', got[end.testIndex]!.message);
      }
      tail('не запускался: предыдущий тест завис');
      setSummary(`Прошло ${passedSoFar} из ${tests.length}`, 'fail', 'Выполнение остановлено: тест завис. Python перезапущен — следующий запуск работает.');
      return;
    }

    const done = end.data as TaskDone;
    if (done.truncated) outputTruncated.hidden = false;
    if (done.phase === 'syntax' || done.phase === 'load') {
      const e = done.error!;
      const text = done.phase === 'syntax' ? `${e.type}: ${e.message}` : e.message;
      setSummary(done.phase === 'syntax' ? 'Синтаксическая ошибка — тесты не запускались' : 'Ошибка при выполнении кода — тесты не запускались', 'fail', text, e.line);
      markError(e.line);
      return;
    }
    const list = done.results ?? [];
    const rendered = list.map((r, i) => {
      const item = items[i] ?? el('li');
      renderTest(item, r.title, r.status, r.message, r.line);
      return item;
    });
    testList.replaceChildren(...rendered);
    const passed = list.filter((r) => r.status === 'passed').length;
    const notWritten = list.some((r) => r.status === 'not_written');
    const all = passed === list.length && list.length > 0;
    setSummary(
      `Прошло ${passed} из ${list.length}${all ? ' — всё верно!' : ''}`,
      all ? 'pass' : 'fail',
      notWritten ? 'Функция ещё не написана — замените raise NotImplementedError своим кодом.' : all ? 'Задача отмечена как решённая.' : undefined,
    );
    markError(list.find((r) => r.line)?.line ?? null);
    if (all) setSolved(data.taskId, true);
  }
}
