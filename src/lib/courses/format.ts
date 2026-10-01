/**
 * Формат урока курса: разбор lesson.py (ячейки кода) и структуры lesson.mdx (порядок ячеек, условия
 * упражнений, подсказки, вопросы). Общий для сайта, валидатора (scripts/validate_courses.ts) и экспорта
 * в .ipynb — без зависимостей от Astro. Формат описан в docs/COURSES_PLAN.md.
 */

// ─── lesson.py ─────────────────────────────────────────────────────────────

export const MARK = {
  starter: '# ─── заготовка ───',
  tests: '# ─── проверка ───',
  alt: '# ─── другое решение ───',
  mistake: '# ─── ошибка ───',
} as const;
const MARKS = new Map<string, keyof typeof MARK>(Object.entries(MARK).map(([k, v]) => [v, k as keyof typeof MARK]));
const CELL_RE = /^# %% ([a-z0-9]+(?:-[a-z0-9]+)*)(?: \[([^\]]*)\])?$/;
const TARGET_RE = /^([A-Za-z_]\w*)\s*=\s*\.\.\.\s*(#.*)?$/;

/** Флаги ячейки: exercise · quiz · raises=Ошибка · warns · platform (вывод в CPython и Pyodide разный). */
export const CELL_FLAGS = new Set(['exercise', 'quiz', 'raises', 'warns', 'platform']);

export interface DemoCell {
  kind: 'demo';
  id: string;
  flags: Record<string, string>;
  code: string;
  line: number;
}

export interface ExerciseCell {
  kind: 'exercise';
  id: string;
  flags: Record<string, string>;
  solution: string; // тело ячейки — эталон
  starter: string;
  tests: string;
  alts: string[]; // другие верные решения: проверка проходит, следующие ячейки работают
  mistakes: string[]; // типичные ошибки: проверка обязана их поймать
  targets: string[]; // переменные, которые заготовка задаёт как `x = ...`, и недописанные методы «Класс.метод»
  line: number;
}

/** Проверка ответа на вопрос: значение выражения должно совпасть с верным вариантом (не показывается). */
export interface QuizCell {
  kind: 'quiz';
  id: string;
  flags: Record<string, string>;
  code: string;
  line: number;
}

export type CodeCell = DemoCell | ExerciseCell | QuizCell;

export interface Parsed<T> {
  value: T;
  problems: string[];
}

function parseFlags(text: string | undefined): Record<string, string> {
  const flags: Record<string, string> = {};
  for (const part of (text ?? '').split(',').map((p) => p.trim()).filter(Boolean)) {
    const [key, value = ''] = part.split('=');
    flags[key.trim()] = value.trim();
  }
  return flags;
}

const trimBlock = (lines: string[]) => {
  const out = [...lines];
  while (out.length && !out[0].trim()) out.shift();
  while (out.length && !out[out.length - 1].trim()) out.pop();
  return out.join('\n');
};

/**
 * Что заготовка оставляет ученику: переменные `total = ...` на верхнем уровне и методы классов, тело которых —
 * только `...` (и комментарии): `class Product:` → `def total(self):` → `...` даёт цель «Product.total».
 */
export function starterTargets(starter: string): string[] {
  const targets: string[] = [];
  let cls: string | null = null;
  let method: string | null = null;
  let abstract = false;
  for (const line of starter.split('\n')) {
    const variable = TARGET_RE.exec(line)?.[1];
    if (variable) targets.push(variable);
    if (!line.trim() || line.trim().startsWith('#')) continue;
    const classMatch = /^class\s+([A-Za-z_]\w*)/.exec(line);
    if (classMatch) [cls, method] = [classMatch[1], null];
    else if (!/^\s/.test(line)) [cls, method] = [null, null];
    else if (cls && /^ {4}def\s+([A-Za-z_]\w*)/.test(line)) {
      method = abstract ? null : /^ {4}def\s+([A-Za-z_]\w*)/.exec(line)![1];
      abstract = false;
    } else if (cls && method && /^ {8}\.\.\.\s*(#.*)?$/.test(line)) {
      targets.push(`${cls}.${method}`);
      method = null;
    } else if (/^ {4}@/.test(line)) abstract ||= /^ {4}@abstractmethod\b/.test(line); // `...` абстрактного метода — не заготовка
    else method = null;
  }
  return targets;
}

export function parseLessonPy(text: string): Parsed<CodeCell[]> {
  const cells: CodeCell[] = [];
  const problems: string[] = [];
  type Raw = { id: string; flags: Record<string, string>; line: number; parts: [keyof typeof MARK | 'body', string[]][] };
  let current: Raw | null = null;

  const finish = () => {
    if (!current) return;
    const { id, flags, line, parts } = current;
    const kinds = ['exercise', 'quiz'].filter((k) => k in flags);
    const unknown = Object.keys(flags).filter((f) => !CELL_FLAGS.has(f));
    if (unknown.length) problems.push(`ячейка ${id}: неизвестные флаги ${unknown.join(', ')}`);
    if (kinds.length > 1) problems.push(`ячейка ${id}: флаги exercise и quiz вместе`);
    const body = trimBlock(parts[0][1]);
    const sections = parts.slice(1);
    if (kinds[0] === 'exercise') {
      const of = (k: keyof typeof MARK) => sections.filter(([s]) => s === k).map(([, l]) => trimBlock(l));
      const [starter] = of('starter');
      const [tests] = of('tests');
      for (const k of ['starter', 'tests'] as const) {
        if (of(k).length !== 1) problems.push(`упражнение ${id}: нужен ровно один раздел «${MARK[k]}»`);
      }
      if (!body) problems.push(`упражнение ${id}: нет эталона (код сразу под «# %% ${id} [exercise]»)`);
      cells.push({
        kind: 'exercise', id, flags, line, solution: body, starter: starter ?? '', tests: tests ?? '',
        alts: of('alt'), mistakes: of('mistake'), targets: starterTargets(starter ?? ''),
      });
    } else {
      if (sections.length) problems.push(`ячейка ${id}: разделы «заготовка/проверка/…» бывают только у [exercise]`);
      if (!body) problems.push(`ячейка ${id}: пустая`);
      cells.push({ kind: kinds[0] === 'quiz' ? 'quiz' : 'demo', id, flags, code: body, line });
    }
    current = null;
  };

  text.split(/\r?\n/).forEach((line, i) => {
    const m = CELL_RE.exec(line);
    if (m) {
      finish();
      if (cells.some((c) => c.id === m[1])) problems.push(`строка ${i + 1}: ячейка ${m[1]} уже есть`);
      current = { id: m[1], flags: parseFlags(m[2]), line: i + 1, parts: [['body', []]] };
      return;
    }
    if (line.startsWith('# %%')) {
      problems.push(`строка ${i + 1}: неверный заголовок ячейки «${line}» — нужно «# %% id» или «# %% id [флаги]»`);
      return;
    }
    if (!current) return; // шапка файла — комментарии
    const mark = MARKS.get(line.trim());
    if (mark) current.parts.push([mark, []]);
    else if (line.startsWith('# ───')) problems.push(`строка ${i + 1}: неизвестный раздел «${line.trim()}»`);
    else current.parts[current.parts.length - 1][1].push(line);
  });
  finish();
  return { value: cells, problems };
}

// ─── lesson.mdx ────────────────────────────────────────────────────────────

export interface QuizOption {
  text: string; // Markdown
  correct: boolean;
}

export type Block =
  | { type: 'text'; text: string; line: number }
  | { type: 'demo'; id: string; title: string; gate: string | null; line: number } // gate: "off" — не скрывать, "lesson" — до решения всех упражнений, id упражнения — до его решения
  | { type: 'exercise'; id: string; title: string; prompt: string; hints: string[]; line: number }
  | { type: 'quiz'; id: string; question: string; options: QuizOption[]; explain: string; line: number }
  | { type: 'component'; name: string; attrs: Record<string, string>; body: string | null; line: number };

/** Компоненты, которые можно писать в уроке (кроме Demo/Exercise/Quiz). Схемы — из справочника. */
export const TEXT_COMPONENTS = new Set(['Note', 'Mistake', 'After']);
export const DIAGRAMS = new Set(['AxisDiagram', 'BroadcastDiagram', 'GroupbyDiagram', 'MeltPivotDiagram', 'StackUnstackDiagram', 'MergeDiagram']);

const SELF_RE = /^<([A-Z]\w*)((?:\s+\w+="[^"]*")*)\s*\/>\s*$/;
const OPEN_RE = /^<([A-Z]\w*)((?:\s+\w+="[^"]*")*)\s*>\s*$/;
const ATTR_RE = /(\w+)="([^"]*)"/g;
const OPTION_RE = /^- \[( |x)\] (.+)$/;

export function splitFrontmatter(text: string): { frontmatter: string; body: string; offset: number } {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(text);
  if (!m) return { frontmatter: '', body: text, offset: 0 };
  return { frontmatter: m[1], body: text.slice(m[0].length), offset: m[0].split('\n').length - 1 };
}

const attrsOf = (text: string) => Object.fromEntries([...text.matchAll(ATTR_RE)].map((m) => [m[1], m[2]]));

/** Вынимает <Tag>…</Tag> (в одну строку или блоком) из текста: [найденное, остальной текст]. */
function extract(lines: string[], tag: string): [string[], string[]] {
  const found: string[] = [];
  const rest: string[] = [];
  let open: string[] | null = null;
  for (const line of lines) {
    const t = line.trim();
    if (open) {
      if (t === `</${tag}>`) {
        found.push(trimBlock(open));
        open = null;
      } else open.push(line);
      continue;
    }
    const single = new RegExp(`^<${tag}>(.*)</${tag}>$`).exec(t);
    if (single) found.push(single[1].trim());
    else if (t === `<${tag}>`) open = [];
    else rest.push(line);
  }
  return [found, rest];
}

export function parseLessonMdx(text: string): Parsed<Block[]> {
  const { body, offset } = splitFrontmatter(text);
  const lines = body.split(/\r?\n/);
  const blocks: Block[] = [];
  const problems: string[] = [];
  let textLines: string[] = [];
  let textStart = 0;
  let fence = false;

  const flushText = () => {
    const t = trimBlock(textLines);
    if (t) blocks.push({ type: 'text', text: t, line: textStart + offset + 1 });
    textLines = [];
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^\s*```/.test(line)) fence = !fence;
    const self = !fence && SELF_RE.exec(line);
    const open = !fence && !self && OPEN_RE.exec(line);
    if (!self && !open) {
      if (!textLines.length) textStart = i;
      textLines.push(line);
      if (!fence && /^\s*<[A-Z]/.test(line)) problems.push(`строка ${i + offset + 1}: компонент должен стоять на отдельной строке, атрибуты — только "строки"`);
      continue;
    }
    flushText();
    const tag = (self || open) as RegExpExecArray;
    const name = tag[1];
    const attrs = attrsOf(tag[2]);
    const at = i + offset + 1;
    let inner: string[] | null = null;
    if (open) {
      const end = lines.findIndex((l, j) => j > i && l.trim() === `</${name}>`);
      if (end < 0) {
        problems.push(`строка ${at}: нет закрывающего </${name}>`);
        break;
      }
      inner = lines.slice(i + 1, end);
      i = end;
    }
    if (name === 'Demo') {
      if (inner) problems.push(`строка ${at}: <Demo id="…" /> пишется без содержимого`);
      blocks.push({ type: 'demo', id: attrs.id ?? '', title: attrs.title ?? '', gate: attrs.gate ?? null, line: at });
    } else if (name === 'Exercise') {
      const [hints, prompt] = extract(inner ?? [], 'Hint');
      blocks.push({ type: 'exercise', id: attrs.id ?? '', title: attrs.title ?? '', prompt: trimBlock(prompt), hints, line: at });
    } else if (name === 'Quiz') {
      const [explain, rest] = extract(inner ?? [], 'Explain');
      const options: QuizOption[] = [];
      const question: string[] = [];
      for (const l of rest) {
        const m = OPTION_RE.exec(l.trim());
        if (m) options.push({ text: m[2].trim(), correct: m[1] === 'x' });
        else question.push(l);
      }
      blocks.push({ type: 'quiz', id: attrs.id ?? '', question: trimBlock(question), options, explain: explain.join('\n\n'), line: at });
    } else {
      if (!TEXT_COMPONENTS.has(name) && !DIAGRAMS.has(name)) problems.push(`строка ${at}: неизвестный компонент <${name}>`);
      blocks.push({ type: 'component', name, attrs, body: inner ? trimBlock(inner) : null, line: at });
    }
    if ((name === 'Demo' || name === 'Exercise' || name === 'Quiz') && !attrs.id) problems.push(`строка ${at}: у <${name}> нет id`);
  }
  if (!fence) flushText();
  else problems.push('незакрытый блок кода ```');
  return { value: blocks, problems };
}

// ─── Скрытие ответа до решения упражнения ────────────────────────────────────

export interface GateOwner {
  id: string;
  title: string;
}

/** Владелец скрытия «до решения всех упражнений урока» — data-gate="*". */
export const LESSON_GATE: GateOwner = { id: '*', title: '' };

/**
 * Упражнения, до решения которых скрыт сохранённый вывод демонстраций (docs/COURSES_PLAN.md, «Ячейки и
 * состояние»): демонстрация в разделе упражнения — после него и до ближайшего заголовка `#`/`##` или следующего
 * упражнения. Не скрываются демонстрации [raises] (показ ошибки, а не ответа) и помеченные gate="off".
 * gate="lesson" — итог урока: скрыт до решения всех упражнений (владелец LESSON_GATE); gate="<id упражнения
 * выше>" — скрыт до решения этого упражнения (график или таблица, повторяющие его ответ в другом разделе).
 * Возвращает id демонстрации → её упражнение.
 */
export function demoGates(blocks: Block[], raises: (demoId: string) => boolean): Map<string, GateOwner> {
  const gates = new Map<string, GateOwner>();
  let owner: GateOwner | null = null;
  const seen = new Map<string, GateOwner>();
  for (const b of blocks) {
    if (b.type === 'exercise') seen.set(b.id, (owner = { id: b.id, title: b.title }));
    else if (b.type === 'demo' && b.gate && seen.has(b.gate)) gates.set(b.id, seen.get(b.gate)!);
    else if (b.type === 'text' && /^#{1,2}\s/m.test(b.text)) owner = null;
    else if (b.type === 'demo' && b.gate === 'lesson') gates.set(b.id, LESSON_GATE);
    else if (b.type === 'demo' && owner && b.gate !== 'off' && !raises(b.id)) gates.set(b.id, owner);
  }
  return gates;
}

// ─── Сохранённый вывод (output.json — пишет валидатор) ───────────────────────

export interface StoredOutput {
  lines: string[];
  result: string[] | null;
  html: string | null;
  error: string | null; // «Тип: сообщение» — у ячеек [raises]
  plots?: number; // сколько графиков построила ячейка: public/course-plots/<курс>/<урок>/<ячейка>-<n>.svg
}

export interface OutputFile {
  generated: string; // «Pyodide 314.0.7 · NumPy 2.4.6»
  cells: Record<string, StoredOutput>;
}
