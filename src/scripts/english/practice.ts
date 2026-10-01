/**
 * Упражнения по английскому на странице урока (docs/ENGLISH_PLAN.md, 0.3 «Интерфейс»). Разметку со всеми
 * полями собирает Practice.astro; здесь — ввод, проверка тем же check.ts, что у валидатора, объяснения,
 * прогресс (edu:drill:v1, edu:test:v1, edu:course:v1) и режим контрольной.
 *
 * Урок (kind = lesson/review): у каждого пункта «Проверить»; верно → объяснение и «Также верно»; неверно →
 * предусмотренное объяснение или подсказка; после второй неверной попытки — «Показать ответ» (поле очищается,
 * пункт засчитается, когда ученик впишет ответ сам). Упражнение решено, когда каждый пункт хоть раз введён верно.
 * Контрольная (test/placement): проверки по ходу нет; «Завершить» → балл, у каждого пункта — ответ ученика,
 * верный ответ и объяснение; зачёт — 80 %, хранится лучший результат.
 */
import { check, displayAnswers, type Exercise, type Input, type Item, type Result } from '../../lib/english/check';
import { inlineMarkdown as md } from '../../lib/english/markdown';
import * as progress from '../course/progress';
import { loadDrill, loadTest, saveDrill, saveTest, type ItemState } from './store';

export interface PracticeData extends Exercise {
  hash: string;
}

export interface EnglishPageData {
  lesson: string;
  course: string;
  mode: 'drill' | 'test' | 'placement';
  exercises: PracticeData[];
  /** Входная проверка: уровень статьи у каждой ссылки и модули курса по уровням — для рекомендации. */
  placement?: { cefr: Record<string, string>; modules: { level: string; number: number; title: string; href: string }[] };
}

export const PASS_PERCENT = 80;

const $ = <T extends Element = HTMLElement>(root: ParentNode, sel: string) => root.querySelector<T>(sel);
const $$ = <T extends Element = HTMLElement>(root: ParentNode, sel: string) => [...root.querySelectorAll<T>(sel)];
const escape = (s: string) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]!);
const en = (s: string) => `<span lang="en">${escape(s)}</span>`;

/** Поле ввода пункта: чтение, запись, фокус. Своё у каждого вида упражнения. */
interface Control {
  get(): Input;
  set(value: Input | null): void;
  focus(): void;
  /** Отметки у пропусков (gap) или у выбранного варианта (choice). */
  mark?(result: Result | null): void;
  /** Только для показа в разборе контрольной: как ученик ответил. */
  show(value: Input): string;
}

// ─── Поля по видам ──────────────────────────────────────────────────────────

function gapControl(root: HTMLElement): Control {
  const inputs = $$<HTMLInputElement>(root, '[data-gap]');
  const fit = (i: HTMLInputElement) => (i.style.width = `${Math.max(4, i.value.length + 1)}ch`);
  inputs.forEach((i) => {
    fit(i);
    i.addEventListener('input', () => fit(i));
  });
  return {
    get: () => inputs.map((i) => i.value),
    set: (v) => inputs.forEach((i, k) => ((i.value = Array.isArray(v) ? (v[k] ?? '') : ''), fit(i))),
    focus: () => (inputs.find((i) => !i.value) ?? inputs[0])?.focus(),
    mark: (r) =>
      inputs.forEach((i, k) => {
        i.classList.toggle('is-ok', !!r && (r.status === 'ok' || !!r.gaps?.[k]));
        i.classList.toggle('is-bad', !!r && r.status !== 'ok' && r.status !== 'empty' && r.gaps?.[k] === false);
      }),
    show: (v) => (Array.isArray(v) ? v.map((x) => x.trim() || '…').join(' … ') : String(v)),
  };
}

function choiceControl(root: HTMLElement, onPick: () => void): Control {
  const options = $$<HTMLButtonElement>(root, '[data-option]');
  const slot = $(root, '[data-choice-slot]');
  let value = '';
  const render = () => {
    options.forEach((o) => {
      o.classList.toggle('is-selected', o.dataset.option === value);
      o.setAttribute('aria-pressed', String(o.dataset.option === value));
    });
    if (slot) slot.textContent = value || '____';
  };
  options.forEach((o) =>
    o.addEventListener('click', () => {
      value = o.dataset.option!;
      render();
      onPick();
    }),
  );
  return {
    get: () => value,
    set: (v) => ((value = typeof v === 'string' ? v : ''), render()),
    focus: () => options[0]?.focus(),
    mark: (r) =>
      options.forEach((o) => {
        const picked = o.dataset.option === value;
        o.classList.toggle('is-correct', picked && r?.status === 'ok');
        o.classList.toggle('is-wrong', picked && !!r && r.status !== 'ok');
      }),
    show: (v) => String(v),
  };
}

function orderControl(root: HTMLElement, item: Item, onChange: () => void): Control {
  const chips = $$<HTMLButtonElement>(root, '[data-chip]');
  const line = $(root, '[data-line]')!;
  const placeholder = line.querySelector('.pr-placeholder');
  const typed = $<HTMLInputElement>(root, '[data-typed]')!;
  const toggle = $<HTMLButtonElement>(root, '[data-type-toggle]')!;
  const final = /[.?!]$/.exec(item.answer[0]?.trim() ?? '')?.[0] ?? '';
  let seq: number[] = [];
  let typing = false;
  const words = (i: number) => item.words?.[i] ?? '';
  const sentence = () => {
    const s = seq.map(words).join(' ');
    return s ? s[0].toUpperCase() + s.slice(1) + final : '';
  };
  const render = () => {
    line.querySelectorAll('[data-picked]').forEach((n) => n.remove());
    for (const i of seq) {
      const b = Object.assign(document.createElement('button'), { type: 'button', className: 'pr-chip is-picked', textContent: words(i) });
      b.dataset.picked = String(i);
      b.setAttribute('aria-label', `Убрать «${words(i)}»`);
      b.addEventListener('click', () => {
        seq = seq.filter((x) => x !== i);
        render();
        onChange();
        (chips[i] ?? line).focus();
      });
      line.append(b);
    }
    if (placeholder) (placeholder as HTMLElement).hidden = seq.length > 0;
    chips.forEach((c, i) => (c.hidden = seq.includes(i)));
  };
  chips.forEach((c, i) =>
    c.addEventListener('click', () => {
      seq.push(i);
      render();
      onChange();
      const next = chips.find((x, j) => !seq.includes(j));
      (next ?? $<HTMLElement>(root, '[data-check]') ?? line).focus();
    }),
  );
  $(root, '[data-reset-line]')?.addEventListener('click', () => {
    seq = [];
    render();
    onChange();
    chips[0]?.focus();
  });
  const setTyping = (on: boolean) => {
    typing = on;
    typed.hidden = !on;
    toggle.setAttribute('aria-expanded', String(on));
    toggle.textContent = on ? 'Собрать из слов' : 'Набрать самому';
    $$(root, '.pr-bank, [data-line], [data-reset-line]').forEach((n) => (n.hidden = on));
    if (on) {
      typed.value ||= sentence();
      typed.focus();
    }
  };
  toggle.addEventListener('click', () => setTyping(!typing));
  typed.addEventListener('input', onChange);
  /** Восстановить фишки по предложению: слова по порядку, каждая фишка — один раз. */
  const rebuild = (text: string): number[] | null => {
    const tokens = text.toLowerCase().replace(/[.,!?;:"]/g, ' ').split(/\s+/).filter(Boolean);
    const out: number[] = [];
    let at = 0;
    while (at < tokens.length) {
      const i = (item.words ?? []).findIndex((w, j) => {
        if (out.includes(j)) return false;
        const parts = w.toLowerCase().replace(/[.,!?;:"]/g, ' ').split(/\s+/).filter(Boolean);
        return parts.every((p, k) => tokens[at + k] === p);
      });
      if (i < 0) return null;
      out.push(i);
      at += (item.words![i].trim().split(/\s+/).length);
    }
    return out;
  };
  return {
    get: () => (typing ? typed.value : sentence()),
    set: (v) => {
      const text = typeof v === 'string' ? v : '';
      const chipsSeq = text ? rebuild(text) : [];
      if (chipsSeq) {
        seq = chipsSeq;
        typed.value = '';
        if (typing) setTyping(false);
      } else {
        seq = [];
        typed.value = text;
        setTyping(true);
      }
      render();
    },
    focus: () => (typing ? typed : (chips.find((c) => !c.hidden) ?? line)).focus(),
    show: (v) => String(v),
  };
}

function transformControl(root: HTMLElement): Control {
  const area = $<HTMLTextAreaElement>(root, '[data-text]')!;
  const start = area.dataset.start ? `${area.dataset.start} ` : '';
  return {
    get: () => area.value,
    set: (v) => (area.value = typeof v === 'string' && v ? v : start),
    focus: () => {
      area.focus();
      area.setSelectionRange(area.value.length, area.value.length);
    },
    show: (v) => String(v),
  };
}

function findErrorControl(root: HTMLElement, item: Item, onChange: () => void): Control {
  const buttons = $$<HTMLButtonElement>(root, '[data-word]');
  const tokens = buttons.map((b) => b.textContent!.trim());
  const box = $(root, '[data-fix-box]')!;
  const fix = $<HTMLInputElement>(root, '[data-fix]')!;
  const preview = $(root, '[data-preview]')!;
  const whole = $<HTMLTextAreaElement>(root, '[data-whole]')!;
  const wholeToggle = $<HTMLButtonElement>(root, '[data-whole-toggle]')!;
  const noError = $<HTMLButtonElement>(root, '[data-no-error]');
  let sel: [number, number] | null = null;
  let wholeMode = false;
  let none = false;
  const result = () => (sel ? [...tokens.slice(0, sel[0]), fix.value.trim(), ...tokens.slice(sel[1] + 1)].filter(Boolean).join(' ') : '');
  const render = () => {
    buttons.forEach((b, i) => b.classList.toggle('is-selected', !!sel && i >= sel[0] && i <= sel[1]));
    buttons.forEach((b, i) => b.setAttribute('aria-pressed', String(!!sel && i >= sel[0] && i <= sel[1])));
    box.hidden = !sel || wholeMode;
    preview.textContent = sel ? result() : '';
    noError?.classList.toggle('is-selected', none);
    noError?.setAttribute('aria-pressed', String(none));
  };
  buttons.forEach((b, i) =>
    b.addEventListener('click', () => {
      none = false;
      if (sel && sel[0] === i && sel[1] === i) sel = null;
      else if (sel && (i === sel[0] - 1 || i === sel[1] + 1)) sel = [Math.min(sel[0], i), Math.max(sel[1], i)];
      else sel = [i, i];
      fix.value = sel ? tokens.slice(sel[0], sel[1] + 1).join(' ') : '';
      render();
      onChange();
      if (sel) fix.focus();
    }),
  );
  fix.addEventListener('input', () => {
    preview.textContent = result();
    onChange();
  });
  const setWhole = (on: boolean) => {
    wholeMode = on;
    whole.hidden = !on;
    wholeToggle.setAttribute('aria-expanded', String(on));
    wholeToggle.textContent = on ? 'Выбрать слово' : 'Исправить целиком';
    $$(root, '[data-words]').forEach((n) => (n.hidden = on));
    if (on) {
      none = false;
      whole.value = sel ? result() : whole.value || (item.text ?? '');
      whole.focus();
    }
    render();
  };
  wholeToggle.addEventListener('click', () => setWhole(!wholeMode));
  whole.addEventListener('input', onChange);
  noError?.addEventListener('click', () => {
    none = !none;
    sel = null;
    if (wholeMode) setWhole(false);
    render();
    onChange();
  });
  return {
    get: () => (none ? (item.text ?? '') : wholeMode ? whole.value : result()),
    set: (v) => {
      const text = typeof v === 'string' ? v : '';
      sel = null;
      fix.value = '';
      none = false;
      if (!text) {
        whole.value = item.text ?? '';
        if (wholeMode) setWhole(false);
      } else if (text === item.text && noError) {
        none = true;
      } else {
        whole.value = text;
        setWhole(true);
      }
      render();
    },
    focus: () => (wholeMode ? whole : (buttons[0] ?? whole)).focus(),
    show: (v) => String(v),
  };
}

// ─── Упражнение ─────────────────────────────────────────────────────────────

interface ItemView {
  item: Item;
  root: HTMLElement;
  control: Control;
  state: ItemState;
  feedback: HTMLElement;
  showButton: HTMLButtonElement | null;
}

const EMPTY_TEXT: Record<Exercise['kind'], string> = {
  gap: 'Впишите ответ — или «—», если ничего не нужно.',
  choice: 'Выберите вариант.',
  order: 'Соберите предложение из слов.',
  transform: 'Напишите предложение.',
  'find-error': 'Нажмите на слово с ошибкой и исправьте его.',
  match: 'Выберите конец для каждого начала.',
};

class PracticeView {
  readonly ex: PracticeData;
  readonly root: HTMLElement;
  readonly lesson: string;
  readonly test: boolean;
  readonly items: ItemView[] = [];
  private matchTries = 0;

  constructor(root: HTMLElement, ex: PracticeData, lesson: string, test: boolean) {
    this.root = root;
    this.ex = ex;
    this.lesson = lesson;
    this.test = test;
    const saved = loadDrill(lesson, ex.id);
    const fresh = saved && saved.hash === ex.hash ? saved : null;
    if (saved && !fresh) {
      $(root, '[data-updated]')!.hidden = false;
      saveDrill(lesson, ex.id, null);
    }
    for (const node of $$(root, '[data-item]')) {
      const item = ex.items.find((i) => String(i.n) === node.dataset.item)!;
      const state: ItemState = fresh?.items[item.n] ?? { ok: false, tries: 0, shown: false, input: null };
      const view: ItemView = {
        item,
        root: node,
        state,
        control: null as unknown as Control,
        feedback: $(node, '[data-feedback]')!,
        showButton: $<HTMLButtonElement>(node, '[data-show]'),
      };
      view.control = this.control(view);
      this.items.push(view);
      if (state.input !== null) view.control.set(state.input);
      if (!test && state.ok) this.renderOk(view, null, true);
      view.showButton?.addEventListener('click', () => this.reveal(view));
      $(node, '[data-check]')?.addEventListener('click', () => this.submit(view));
      node.addEventListener('keydown', (e) => {
        if (e.key !== 'Enter' || e.shiftKey || e.isComposing || !(e.target as HTMLElement).matches('input, textarea')) return;
        e.preventDefault();
        if (test) this.focusNext(view);
        else this.submit(view);
      });
    }
    if (ex.kind === 'match') {
      $(root, '[data-check]')?.addEventListener('click', () => this.submitMatch());
      $(root, '[data-show]')?.addEventListener('click', () => this.revealMatch());
      if (!test && this.items.every((v) => v.state.ok)) this.showMatchExplain();
    }
    root.classList.add('is-live');
    this.renderCount();
  }

  private control(view: ItemView): Control {
    const changed = () => this.changed(view);
    switch (this.ex.kind) {
      case 'gap':
        return gapControl(view.root);
      case 'choice':
        return choiceControl(view.root, () => (this.test ? changed() : this.submit(view)));
      case 'order':
        return orderControl(view.root, view.item, changed);
      case 'transform':
        return transformControl(view.root);
      case 'find-error':
        return findErrorControl(view.root, view.item, changed);
      case 'match': {
        const select = $<HTMLSelectElement>(view.root, '[data-select]')!;
        select.addEventListener('change', changed);
        return {
          get: () => select.value,
          set: (v) => (select.value = typeof v === 'string' ? v : ''),
          focus: () => select.focus(),
          show: (v) => String(v),
        };
      }
    }
  }

  /** Ввод изменился: в контрольной — сохранить ответ, в уроке — убрать устаревшую отметку. */
  private changed(view: ItemView): void {
    if (this.test) {
      view.state.input = view.control.get();
      this.save();
    } else {
      view.root.classList.remove('is-wrong', 'is-almost');
    }
  }

  private save(): void {
    const items = Object.fromEntries(this.items.map((v) => [v.item.n, v.state]));
    saveDrill(this.lesson, this.ex.id, { hash: this.ex.hash, items });
  }

  private renderCount(): void {
    const done = this.items.filter((v) => v.state.ok).length;
    const counter = $(this.root, '[data-done-count]');
    if (counter) counter.textContent = String(done);
    this.root.classList.toggle('is-solved', !this.test && progress.isSolved(this.lesson, this.ex.id));
  }

  private focusNext(view: ItemView): void {
    const i = this.items.indexOf(view);
    const next = this.items.slice(i + 1).find((v) => !v.state.ok) ?? this.items[i + 1];
    next?.control.focus();
  }

  /** Другие допустимые ответы — «Также верно». */
  private also(item: Item, matched: string | undefined): string[] {
    const shown = displayAnswers(this.ex, item);
    return shown.filter((a) => a !== matched).slice(0, 6);
  }

  private explainHtml(item: Item, matched?: string): string {
    const parts = [`<p>${md(item.explain)}</p>`];
    const also = this.also(item, matched);
    if (also.length && this.ex.kind !== 'choice' && this.ex.kind !== 'match') parts.push(`<p class="pr-also">Также верно: ${also.map(en).join(' · ')}</p>`);
    return parts.join('');
  }

  private renderOk(view: ItemView, result: Result | null, restored = false): void {
    view.root.classList.remove('is-wrong', 'is-almost');
    view.root.classList.add('is-ok');
    view.control.mark?.(result ?? { status: 'ok', notes: [] });
    if (this.ex.kind === 'match') {
      view.feedback.innerHTML = '<span class="pr-verdict is-ok">Верно</span>';
      return;
    }
    const notes = result?.notes.map((n) => `<p class="pr-soft">${escape(n)}</p>`).join('') ?? '';
    view.feedback.innerHTML = `<p class="pr-verdict is-ok">${restored ? 'Решено' : 'Верно'}</p>${notes}${this.explainHtml(view.item, result?.matched)}`;
    if (view.showButton) view.showButton.hidden = true;
  }

  submit(view: ItemView): void {
    if (this.ex.kind === 'match') return this.submitMatch();
    const input = view.control.get();
    const result = check(this.ex, view.item, input);
    view.root.classList.remove('is-ok', 'is-wrong', 'is-almost');
    if (result.status === 'empty') {
      view.control.mark?.(null);
      view.feedback.innerHTML = `<p class="pr-verdict">${EMPTY_TEXT[this.ex.kind]}</p>`;
      return;
    }
    view.state.input = input;
    if (result.status === 'ok') {
      view.state.ok = true;
      this.renderOk(view, result);
    } else if (result.status === 'almost') {
      view.root.classList.add('is-almost');
      view.control.mark?.(result);
      view.feedback.innerHTML = '<p class="pr-verdict is-almost">Проверьте написание: в одном слове опечатка.</p>';
    } else {
      view.state.tries++;
      view.root.classList.add('is-wrong');
      view.control.mark?.(result);
      const hint = view.item.hint ?? this.ex.hint;
      const why = result.why ?? (this.ex.kind === 'choice' ? view.item.why[String(input)] : undefined);
      view.feedback.innerHTML = why
        ? `<p class="pr-verdict is-wrong">Неверно</p><p>${md(why)}</p>`
        : `<p class="pr-verdict is-wrong">Не совсем${view.state.tries > 1 ? '' : ' — попробуйте ещё раз'}.</p>${hint ? `<p class="pr-hint">Подсказка: ${md(hint)}</p>` : ''}`;
      if (view.showButton && view.state.tries >= 2) view.showButton.hidden = false;
    }
    this.save();
    this.afterCheck(view, result);
  }

  private afterCheck(view: ItemView, result: Result): void {
    this.renderCount();
    if (this.items.every((v) => v.state.ok) && !progress.isSolved(this.lesson, this.ex.id)) {
      progress.setSolved(this.lesson, this.ex.id, this.ex.hash);
      this.renderCount();
    }
    if (result.status === 'ok') this.focusNext(view);
  }

  /** «Показать ответ»: ответ, допустимые варианты и объяснение; поле очищается — вписать нужно самому. */
  reveal(view: ItemView): void {
    view.state.shown = true;
    view.state.input = null;
    view.control.set(null);
    view.control.mark?.(null);
    view.root.classList.remove('is-wrong', 'is-almost');
    const [main, ...rest] = displayAnswers(this.ex, view.item);
    view.feedback.innerHTML =
      `<p class="pr-verdict">Ответ: ${en(main)}</p>` +
      (rest.length && this.ex.kind !== 'choice' ? `<p class="pr-also">Также верно: ${rest.slice(0, 6).map(en).join(' · ')}</p>` : '') +
      `<p>${md(view.item.explain)}</p><p class="pr-soft">Впишите ответ сами — так пункт засчитается.</p>`;
    if (view.showButton) view.showButton.hidden = true;
    this.save();
    view.control.focus();
  }

  submitMatch(): void {
    const filled = this.items.filter((v) => v.control.get());
    if (!filled.length) {
      this.items[0].feedback.textContent = EMPTY_TEXT.match;
      return;
    }
    let wrong = 0;
    for (const view of this.items) {
      const value = view.control.get();
      view.root.classList.remove('is-ok', 'is-wrong');
      if (!value) {
        view.feedback.textContent = '';
        continue;
      }
      view.state.input = value;
      const r = check(this.ex, view.item, value);
      if (r.status === 'ok') {
        view.state.ok = true;
        this.renderOk(view, r);
      } else {
        wrong++;
        view.root.classList.add('is-wrong');
        view.feedback.innerHTML = '<span class="pr-verdict is-wrong">Не та пара</span>';
      }
    }
    if (wrong) this.matchTries++;
    if (this.matchTries >= 2) $(this.root, '[data-show]')!.hidden = false;
    this.save();
    this.afterCheck(this.items[0], { status: 'wrong', notes: [] });
    if (this.items.every((v) => v.state.ok)) this.showMatchExplain();
  }

  private showMatchExplain(): void {
    const box = $(this.root, '[data-match-explain]');
    if (!box || !this.ex.explain) return;
    box.innerHTML = `<p class="pr-verdict is-ok">Все пары верны</p><p>${md(this.ex.explain)}</p>`;
    box.hidden = false;
  }

  revealMatch(): void {
    const box = $(this.root, '[data-match-explain]')!;
    box.innerHTML =
      `<p class="pr-verdict">Ответ:</p><ol>${this.items.map((v) => `<li>${en(v.item.text ?? '')} → ${en(v.item.answer[0])}</li>`).join('')}</ol>` +
      (this.ex.explain ? `<p>${md(this.ex.explain)}</p>` : '') +
      '<p class="pr-soft">Соберите пары сами — так упражнение засчитается.</p>';
    box.hidden = false;
    for (const v of this.items) {
      if (!v.state.ok) {
        v.control.set(null);
        v.state.shown = true;
        v.root.classList.remove('is-wrong');
        v.feedback.textContent = '';
      }
    }
    $(this.root, '[data-show]')!.hidden = true;
    this.save();
  }

  // ─── Контрольная ───

  /** Проверяет все пункты и показывает разбор; возвращает число верных. */
  grade(): number {
    let ok = 0;
    for (const view of this.items) {
      const input = view.control.get();
      const result = check(this.ex, view.item, input);
      const right = result.status === 'ok';
      if (right) ok++;
      view.root.classList.remove('is-ok', 'is-wrong', 'is-almost');
      view.root.classList.add(right ? 'is-ok' : 'is-wrong');
      view.control.mark?.(result.status === 'empty' ? null : result);
      const [main] = displayAnswers(this.ex, view.item);
      const answered = result.status === 'empty' ? '<i>нет ответа</i>' : en(view.control.show(input));
      const why = !right && (result.why ?? (this.ex.kind === 'choice' ? view.item.why[String(input)] : undefined));
      view.feedback.innerHTML =
        `<p class="pr-verdict ${right ? 'is-ok' : 'is-wrong'}">${right ? 'Верно' : 'Неверно'}</p>` +
        `<p class="pr-review">Ваш ответ: ${answered}${right ? '' : ` · верно: ${en(main)}`}</p>` +
        (why ? `<p>${md(why)}</p>` : '') +
        (this.ex.kind === 'match' ? '' : `<p>${md(view.item.explain)}</p>`);
      view.state.input = input;
    }
    if (this.ex.kind === 'match' && this.ex.explain) {
      const box = $(this.root, '[data-match-explain]')!;
      box.innerHTML = `<p>${md(this.ex.explain)}</p>`;
      box.hidden = false;
    }
    this.root.classList.add('is-graded');
    return ok;
  }

  resetTest(): void {
    for (const view of this.items) {
      view.state = { ok: false, tries: 0, shown: false, input: null };
      view.control.set(null);
      view.control.mark?.(null);
      view.feedback.innerHTML = '';
      view.root.classList.remove('is-ok', 'is-wrong', 'is-almost');
    }
    const box = $(this.root, '[data-match-explain]');
    if (box) box.hidden = true;
    this.root.classList.remove('is-graded');
    saveDrill(this.lesson, this.ex.id, null);
  }
}

// ─── Контрольная и входная проверка ─────────────────────────────────────────

/** Рекомендация входной проверки: первый уровень, где верно меньше 80 %, — с первого модуля этого уровня. */
export function placementAdvice(data: EnglishPageData, views: PracticeView[]): string {
  const p = data.placement;
  if (!p) return '';
  const byLevel = new Map<string, { ok: number; all: number }>();
  for (const view of views) {
    for (const v of view.items) {
      const ref = v.item.ref[0] ?? view.ex.ref[0];
      const level = (p.cefr[ref] ?? '').slice(0, 2);
      if (!level) continue;
      const s = byLevel.get(level) ?? { ok: 0, all: 0 };
      s.all++;
      if (check(view.ex, v.item, v.control.get()).status === 'ok') s.ok++;
      byLevel.set(level, s);
    }
  }
  const levels = [...byLevel.keys()].sort();
  const weak = levels.find((l) => byLevel.get(l)!.ok / byLevel.get(l)!.all < PASS_PERCENT / 100);
  const stats = levels.map((l) => `${l}: ${byLevel.get(l)!.ok} из ${byLevel.get(l)!.all}`).join(' · ');
  if (!weak) {
    const last = p.modules[p.modules.length - 1];
    return `<p>${stats}.</p><p>Темы проверки вы знаете уверенно. ${last ? `Можно начать с модуля ${last.number} <a href="${last.href}">«${escape(last.title)}»</a> или выбрать темы в программе.` : ''}</p>`;
  }
  const module = p.modules.find((m) => m.level.includes(weak));
  return `<p>${stats}.</p><p>Начните с уровня ${weak}${module ? `: модуль ${module.number} <a href="${module.href}">«${escape(module.title)}»</a>` : ''}. Уроки не блокируются — знакомые темы можно пролистать.</p>`;
}

function initTest(data: EnglishPageData, views: PracticeView[]): void {
  const panel = document.querySelector<HTMLElement>('[data-test-panel]');
  if (!panel) return;
  const finish = $<HTMLButtonElement>(panel, '[data-finish]')!;
  const again = $<HTMLButtonElement>(panel, '[data-again]')!;
  const result = $(panel, '[data-result]')!;
  const best = $(panel, '[data-best]')!;
  const total = views.reduce((n, v) => n + v.items.length, 0);
  const renderBest = () => {
    const saved = loadTest(data.lesson);
    best.textContent = saved ? `Лучший результат: ${saved.best} %${saved.best >= PASS_PERCENT ? ' — зачёт' : ''}.` : '';
  };
  panel.hidden = false;
  renderBest();
  finish.addEventListener('click', () => {
    const ok = views.reduce((n, v) => n + v.grade(), 0);
    const percent = Math.round((ok / total) * 100);
    const passed = percent >= PASS_PERCENT;
    saveTest(data.lesson, percent);
    if (data.mode === 'test' && passed) {
      for (const v of views) progress.setSolved(data.lesson, v.ex.id, v.ex.hash);
      progress.setDone(data.lesson, true);
    }
    if (data.mode === 'placement') {
      for (const v of views) progress.setSolved(data.lesson, v.ex.id, v.ex.hash);
      result.innerHTML = `<p class="pr-score">Верно ${ok} из ${total} (${percent} %)</p>${placementAdvice(data, views)}`;
    } else {
      result.innerHTML =
        `<p class="pr-score ${passed ? 'is-ok' : 'is-wrong'}">Верно ${ok} из ${total} — ${percent} %. ${passed ? 'Зачёт.' : `Для зачёта нужно ${PASS_PERCENT} %.`}</p>` +
        '<p class="pr-soft">Ниже у каждого пункта — ваш ответ, верный и объяснение.</p>';
    }
    result.hidden = false;
    finish.hidden = true;
    again.hidden = false;
    renderBest();
    result.focus();
  });
  again.addEventListener('click', () => {
    views.forEach((v) => v.resetTest());
    result.hidden = true;
    finish.hidden = false;
    again.hidden = true;
    views[0]?.root.scrollIntoView({ behavior: 'smooth', block: 'start' });
    views[0]?.items[0]?.control.focus();
  });
}

// ─── Страница ───────────────────────────────────────────────────────────────

export function initPractice(): void {
  const node = document.getElementById('english-data');
  if (!node) return;
  const data = JSON.parse(node.textContent!) as EnglishPageData;
  progress.setLast(data.course, data.lesson);
  const test = data.mode !== 'drill';
  const views = $$('[data-practice]').flatMap((root) => {
    const ex = data.exercises.find((e) => e.id === root.dataset.practice);
    return ex ? [new PracticeView(root, ex, data.lesson, test)] : [];
  });
  if (test) initTest(data, views);

  // отметка «Урок пройден»: вручную или сама, когда решены все упражнения (у контрольной — при зачёте)
  const toggle = document.querySelector<HTMLInputElement>('[data-lesson-done]');
  const exercises = data.exercises.map((e) => e.id);
  const sync = () => {
    if (toggle) toggle.checked = progress.isDone(data.lesson, exercises);
    const solved = exercises.filter((e) => progress.isSolved(data.lesson, e)).length;
    document.querySelectorAll<HTMLElement>('[data-lesson-solved]').forEach((el) => (el.textContent = String(solved)));
  };
  toggle?.addEventListener('change', () => progress.setDone(data.lesson, toggle.checked));
  document.addEventListener(progress.COURSE_EVENT, sync);
  sync();
}

