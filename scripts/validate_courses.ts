/**
 * Проверка курсов (courses/): структура, понятия по порядку, выполнение уроков в Pyodide и в CPython, экспорт
 * в .ipynb. Формат и правила — docs/COURSES_PLAN.md.
 *
 *   node scripts/validate_courses.ts                  # все курсы
 *   node scripts/validate_courses.ts numpy np-first-array   # курс или урок
 *   node scripts/validate_courses.ts --update         # записать сохранённый вывод (output.json) из Pyodide
 *   node scripts/validate_courses.ts --strict         # программа полная: модуль кончается мини-проектом и т.д.
 *   node scripts/validate_courses.ts --python путь    # CPython с пакетами requirements-dev.txt (по умолчанию .venv)
 *
 * Каждый урок выполняется целиком, как ноутбук, в одном сеансе (runtime/lesson_exec.py):
 *   - с эталонами: демонстрации без ошибок (кроме [raises]), все проверки упражнений проходят, ответы на
 *     вопросы с ячейкой [quiz] совпадают с верным вариантом;
 *   - с заготовкой каждого упражнения (выше — эталоны): проверка не проходит;
 *   - с каждым «другим решением»: проверка проходит, и все ячейки ниже работают;
 *   - с каждой «ошибкой»: проверка не проходит понятным сообщением (assert, а не падение теста).
 * Так — в Pyodide (Node.js, то же ядро, что у сайта) и в CPython с версиями из requirements-dev.txt.
 * Сохранённый вывод — из Pyodide: ровно то, что человек увидит в браузере. Вывод CPython обязан совпадать,
 * если у ячейки нет флага [platform] (32-битный Python в браузере: int32, номера ошибок ОС и т.п.).
 * Ноутбук с эталонами выполняется в CPython без ошибок, все проверки в нём — «Прошло N из N».
 */
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { availableParallelism } from 'node:os';
import { join } from 'node:path';
import { type Block, type CodeCell, type ExerciseCell, type OutputFile, type StoredOutput } from '../src/lib/courses/format.ts';
import { courseLessons, DATA_DIR, lessonFiles, lessonPackages, loadCourses, type CourseSource, type LessonSource } from '../src/lib/courses/load.ts';
import { buildNotebook } from '../src/lib/courses/notebook.ts';
import { PYODIDE_VERSION } from '../src/lib/python/config.ts';
import type { LessonDone, TestResult } from '../src/lib/python/protocol.ts';
import { NodePython, pool } from './node-python.ts';

const root = join(import.meta.dirname, '..');
const read = (path: string) => readFileSync(path, 'utf-8');

/** Python-минимум: встроенные функции и методы встроенных типов считаются известными с начала курса. */
const PYTHON_KNOWN = new Set([
  ...['append', 'extend', 'insert', 'pop', 'remove', 'index', 'count', 'sort', 'reverse', 'copy', 'clear'],
  ...['keys', 'values', 'items', 'get', 'update', 'setdefault'],
  ...['split', 'join', 'strip', 'lstrip', 'rstrip', 'lower', 'upper', 'replace', 'startswith', 'endswith', 'format', 'find', 'title', 'isdigit'],
  ...['add', 'discard', 'union', 'intersection'],
  ...['real', 'imag', 'is_integer'],
].map((m) => `.${m}`));
const PYTHON_KEYWORDS = new Set(['sep=', 'end=', 'key=', 'reverse=', 'start=', 'default=']);
const FORBIDDEN_WARNINGS = ['DeprecationWarning', 'PendingDeprecationWarning', 'FutureWarning'];

// ─── Отчёт ──────────────────────────────────────────────────────────────────

class Report {
  errors = new Map<string, string[]>();
  warnings = new Map<string, string[]>();
  error(where: string, message: string): void {
    (this.errors.get(where) ?? this.errors.set(where, []).get(where)!).push(message);
  }
  warn(where: string, message: string): void {
    (this.warnings.get(where) ?? this.warnings.set(where, []).get(where)!).push(message);
  }
}

function annotate(title: string, message: string): void {
  if (process.env.GITHUB_ACTIONS === 'true') console.log(`::error title=${title}::${message.replaceAll('\n', '%0A')}`);
}

// ─── CPython ────────────────────────────────────────────────────────────────

function cpython(python: string, task: object): unknown {
  const result = spawnSync(python, [join(root, 'scripts', 'course_cpython.py')], {
    input: JSON.stringify(task),
    encoding: 'utf-8',
    maxBuffer: 256 * 1024 * 1024,
    cwd: root,
  });
  if (result.status !== 0) throw new Error(`CPython (${python}) завершился с ошибкой:\n${result.stderr || result.error}`);
  return JSON.parse(result.stdout);
}

function pinned(): Record<string, string> {
  return Object.fromEntries(
    read(join(root, 'requirements-dev.txt'))
      .split('\n')
      .map((l) => /^([a-zA-Z0-9_-]+)==(\S+)/.exec(l.trim()))
      .filter((m): m is RegExpExecArray => !!m)
      .map((m) => [m[1].toLowerCase(), m[2]]),
  );
}

// ─── Структура ──────────────────────────────────────────────────────────────

const referenceExists = (id: string) => existsSync(join(root, 'reference', `${id}.mdx`));
const stripTicks = (text: string) => text.replace(/^`(.*)`$/, '$1').trim();

function checkStructure(courses: CourseSource[], strict: boolean, r: Report): void {
  const ids = new Map<string, string>();
  for (const course of courses) {
    const c = course.meta;
    for (const key of ['title', 'code', 'package', 'summary', 'audience', 'reference'] as const) {
      if (!c[key]) r.error(course.slug, `course.toml: нет поля ${key}`);
    }
    if (!c.prerequisites?.length) r.error(course.slug, 'course.toml: пустой prerequisites («что нужно знать»)');
    const slugs = new Set<string>();
    const lessonUrls = new Set(courses.flatMap((x) => courseLessons(x).map((l) => `/courses/${x.slug}/${l.slug}`)));
    const known = new Set([...lessonUrls, ...courses.map((x) => `/courses/${x.slug}`)]);
    const meta = [c.summary, c.audience, ...c.prerequisites, ...course.modules.flatMap((m) => [m.meta.summary, ...(m.meta.outcomes ?? [])])].join('\n');
    for (const [, href] of meta.matchAll(/href="(\/courses\/[^"#]*)"/g)) {
      if (!known.has(href.replace(/\/$/, ''))) r.error(course.slug, `course.toml / module.toml: ссылка ${href} — такой страницы нет`);
    }
    for (const module of course.modules) {
      const where = `${course.slug}/${module.slug}`;
      if (!module.meta.title || !module.meta.summary) r.error(where, 'module.toml: нужны title и summary');
      if (!module.meta.outcomes?.length) r.error(where, 'module.toml: пустой outcomes («что умеет после модуля»)');
      const last = module.lessons[module.lessons.length - 1];
      if (strict && last && last.meta.kind !== 'project') r.error(where, `модуль должен заканчиваться мини-проектом (kind: project), а последний урок — ${last.meta.id}`);
      if (!module.lessons.length) r.warn(where, 'в модуле нет уроков');
      for (const lesson of module.lessons) {
        const at = lesson.meta.id || `${where}/${lesson.slug}`;
        for (const p of lesson.problems) r.error(at, p);
        const m = lesson.meta;
        if (!/^[a-z]+-[a-z0-9]+(-[a-z0-9]+)*$/.test(m.id)) r.error(at, `id «${m.id}»: kebab-case с префиксом курса`);
        else if (!m.id.startsWith(`${c.code}-`)) r.error(at, `id должен начинаться с «${c.code}-»`);
        if (ids.has(m.id)) r.error(at, `id повторяется: ещё в ${ids.get(m.id)}`);
        ids.set(m.id, `${course.slug}/${module.slug}/${lesson.slug}`);
        if (slugs.has(lesson.slug)) r.error(at, `адрес /courses/${course.slug}/${lesson.slug} уже занят другим уроком`);
        slugs.add(lesson.slug);
        if (!m.title || !m.summary) r.error(at, 'frontmatter: нужны title и summary');
        if (!(m.minutes >= 5 && m.minutes <= 30)) r.error(at, `minutes: ${m.minutes} — урок рассчитан на 10–20 минут`);
        else if (m.minutes < 10 || m.minutes > 20) r.warn(at, `minutes: ${m.minutes} — ориентир 10–20 минут`);
        for (const ref of m.reference) if (!referenceExists(ref)) r.error(at, `reference: статьи ${ref} нет в справочнике`);
        for (const file of m.data) if (!existsSync(join(DATA_DIR, file))) r.error(at, `data: нет файла courses/data/${file}`);
        checkBlocks(lesson, lessonUrls, r);
      }
    }
  }
}

function checkBlocks(lesson: LessonSource, lessonUrls: Set<string>, r: Report): void {
  const at = lesson.meta.id;
  const blocks = lesson.blocks;
  const placed = blocks.filter((b): b is Extract<Block, { type: 'demo' | 'exercise' }> => b.type === 'demo' || b.type === 'exercise');
  const runnable = lesson.cells.filter((c) => c.kind !== 'quiz');
  // порядок ячеек в lesson.py = порядок в lesson.mdx
  const inMdx = placed.map((b) => b.id).join(' ');
  const inPy = runnable.map((c) => c.id).join(' ');
  if (inMdx !== inPy) r.error(at, `порядок ячеек в lesson.mdx (${inMdx || '—'}) и lesson.py (${inPy || '—'}) не совпадает`);
  for (const b of placed) {
    const cell = lesson.cells.find((c) => c.id === b.id);
    if (cell && cell.kind !== b.type) r.error(at, `<${b.type === 'demo' ? 'Demo' : 'Exercise'} id="${b.id}">: в lesson.py это ${cell.kind}`);
  }
  const exercises = blocks.filter((b) => b.type === 'exercise');
  const project = lesson.meta.kind === 'project';
  if (exercises.length < 3 || exercises.length > (project ? 8 : 6)) r.error(at, `упражнений ${exercises.length}, нужно 3–${project ? 8 : 6}`);
  for (const b of exercises) {
    if (b.type !== 'exercise') continue;
    if (!b.title) r.error(at, `упражнение ${b.id}: нет title`);
    if (!b.prompt) r.error(at, `упражнение ${b.id}: нет условия`);
    if (!b.hints.length) r.warn(at, `упражнение ${b.id}: нет подсказок`);
  }
  for (const b of blocks) {
    if (b.type === 'quiz') {
      if (b.options.length < 2) r.error(at, `вопрос ${b.id}: меньше двух вариантов`);
      if (b.options.filter((o) => o.correct).length !== 1) r.error(at, `вопрос ${b.id}: верным должен быть ровно один вариант «- [x]»`);
      if (!b.question) r.error(at, `вопрос ${b.id}: нет текста вопроса`);
    }
    if (b.type === 'component' && b.body && /<(Demo|Exercise|Quiz)\b/.test(b.body)) r.error(at, `строка ${b.line}: ячейки нельзя вкладывать в <${b.name}> — поставьте их рядом`);
    const text = b.type === 'text' ? b.text : b.type === 'exercise' ? `${b.prompt}\n${b.hints.join('\n')}` : b.type === 'quiz' ? `${b.question}\n${b.explain}` : b.type === 'component' ? b.body ?? '' : '';
    for (const [, href] of text.matchAll(/\]\((\/[^)\s#]*)/g)) {
      const clean = href.replace(/\/$/, '');
      if (clean.startsWith('/reference/') && !referenceExists(clean.slice('/reference/'.length))) r.error(at, `ссылка ${href}: статьи нет в справочнике`);
      if (clean.startsWith('/courses/') && clean.split('/').length === 4 && !lessonUrls.has(clean)) r.error(at, `ссылка ${href}: такого урока нет`);
    }
  }
  const quizIds = new Set(blocks.filter((b) => b.type === 'quiz').map((b) => b.type === 'quiz' && b.id));
  for (const c of lesson.cells) {
    if (c.kind === 'quiz' && !quizIds.has(c.id)) r.error(at, `ячейка ${c.id} [quiz]: в lesson.mdx нет <Quiz id="${c.id}">`);
    if (c.kind !== 'exercise') continue;
    if (!/^def test_\w+/m.test(c.tests)) r.error(at, `упражнение ${c.id}: в проверке нет функций test_*`);
    for (const t of c.targets) {
      if (!new RegExp(`^${t}\\s*[=,]|^\\s*${t}\\s*=|,\\s*${t}\\s*=`, 'm').test(c.solution)) r.error(at, `упражнение ${c.id}: заготовка задаёт ${t} = ..., а эталон её не присваивает`);
    }
    if (!c.alts.length) r.warn(at, `упражнение ${c.id}: нет «другого решения»`);
  }
}

// ─── Понятия по порядку ─────────────────────────────────────────────────────

function checkConcepts(courses: CourseSource[], python: string, r: Report): Map<string, string[]> {
  const snippets: Record<string, string> = {};
  for (const course of courses) {
    for (const lesson of courseLessons(course)) {
      for (const c of lesson.cells) {
        if (c.kind === 'demo') snippets[`${lesson.meta.id}#${c.id}`] = c.code;
        if (c.kind === 'exercise') {
          snippets[`${lesson.meta.id}#${c.id}#solution`] = c.solution;
          snippets[`${lesson.meta.id}#${c.id}#starter`] = c.starter;
        }
      }
    }
  }
  const found = cpython(python, { mode: 'concepts', snippets }) as Record<string, string[] | { error: string }>;
  const review = new Map<string, string[]>(); // урок → понятия прошлых уроков в его упражнениях (повторение)
  const introducedBy = (course: CourseSource) => new Map(courseLessons(course).flatMap((l) => l.meta.introduces.map((c) => [c, l.meta.id] as [string, string])));
  for (const course of courses) {
    // понятие → урок, где введено. Курс самостоятельный, если requires пуст: понятия других курсов (np.* в курсе
    // pandas) нужно ввести в нём самом, там, где они понадобились
    const known = new Map<string, string>();
    for (const dep of course.meta.requires) {
      const other = courses.find((c) => c.slug === dep);
      if (!other) r.error(course.slug, `course.toml: requires — нет курса ${dep}`);
      else for (const [c, id] of introducedBy(other)) known.set(c, id);
    }
    for (const lesson of courseLessons(course)) {
      const at = lesson.meta.id;
      const introduced = new Set(lesson.meta.introduces);
      for (const concept of introduced) {
        if (known.has(concept)) r.warn(at, `introduces: ${concept} уже введено в ${known.get(concept)}`);
      }
      const used = new Set<string>();
      const reviewed = new Set<string>();
      for (const [key, value] of Object.entries(found)) {
        if (!key.startsWith(`${at}#`)) continue;
        if (!Array.isArray(value)) {
          r.error(at, `${key.slice(at.length + 1)}: ${value.error}`);
          continue;
        }
        for (const concept of value) {
          used.add(concept);
          if (key.endsWith('#solution') && known.has(concept)) reviewed.add(concept);
          if (introduced.has(concept) || known.has(concept) || PYTHON_KNOWN.has(concept) || PYTHON_KEYWORDS.has(concept)) continue;
          r.error(at, `${key.slice(at.length + 1).replace('#', ' ')}: «${concept}» используется, но не введено ни в этом, ни в прошлых уроках (добавьте в introduces урока, где оно объясняется)`);
        }
      }
      for (const concept of introduced) {
        if (!used.has(concept)) r.error(at, `introduces: ${concept} не встречается в коде урока`);
        if (!known.has(concept)) known.set(concept, at);
      }
      review.set(at, [...reviewed].sort());
    }
  }
  return review;
}

// ─── Прогоны ────────────────────────────────────────────────────────────────

interface Step {
  op: 'cell' | 'quiz' | 'check';
  cell: string;
  code: string;
  tests?: string;
  targets?: string[];
}

interface Run {
  lesson: LessonSource;
  course: CourseSource;
  label: string; // «эталоны», «заготовка temps», «другое решение 1 fahrenheit»…
  steps: Step[];
  expect: ('ok' | 'fail' | 'mistake')[]; // для каждого шага: ok — работает, fail — проверка не проходит, mistake — не проходит сообщением
  from: number; // шаги до этого — те же, что в прогоне с эталонами: их ошибки уже показаны там
}

interface StepResult {
  lines: string[];
  result: string[] | null;
  html: string | null;
  error: { type: string; mro: string[]; text: string; line: number | null } | null;
  warnings: string[];
  truncated: boolean;
  phase?: 'run' | 'missing' | 'tests';
  results?: TestResult[];
}

const solutionStep = (c: CodeCell): Step =>
  c.kind === 'exercise' ? { op: 'check', cell: c.id, code: c.solution, tests: c.tests, targets: c.targets } : { op: c.kind === 'quiz' ? 'quiz' : 'cell', cell: c.id, code: c.code };

function planRuns(course: CourseSource, lesson: LessonSource): Run[] {
  const cells = lesson.cells;
  const runs: Run[] = [{ course, lesson, label: 'эталоны', steps: cells.map(solutionStep), expect: cells.map(() => 'ok'), from: 0 }];
  cells.forEach((cell, i) => {
    if (cell.kind !== 'exercise') return;
    const before = cells.slice(0, i).map(solutionStep);
    const after = cells.slice(i + 1).map(solutionStep);
    const check = (code: string): Step => ({ op: 'check', cell: cell.id, code, tests: cell.tests, targets: cell.targets });
    runs.push({ course, lesson, label: `заготовка ${cell.id}`, steps: [...before, check(cell.starter)], expect: [...before.map(() => 'ok' as const), 'fail'], from: i });
    cell.alts.forEach((alt, j) => {
      const steps = [...before, check(alt), ...after];
      runs.push({ course, lesson, label: `другое решение ${j + 1} ${cell.id}`, steps, expect: steps.map(() => 'ok'), from: i });
    });
    cell.mistakes.forEach((mistake, j) => {
      runs.push({ course, lesson, label: `ошибка ${j + 1} ${cell.id}`, steps: [...before, check(mistake)], expect: [...before.map(() => 'ok' as const), 'mistake'], from: i });
    });
  });
  return runs;
}

const passedAll = (s: StepResult) => s.phase === 'tests' && !!s.results?.length && s.results.every((t) => t.status === 'passed');

function describe(s: StepResult): string {
  if (s.error) return s.error.text + (s.error.line ? ` (строка ${s.error.line})` : '');
  if (s.phase === 'missing') return s.results?.[0]?.title ?? 'переменная не задана';
  const bad = (s.results ?? []).filter((t) => t.status !== 'passed');
  return bad.map((t) => `«${t.title}»: ${t.status}${t.message ? ` — ${t.message}` : ''}`).join('; ') || 'нет вывода';
}

/** Ошибки шага по ожиданию: работает / проверка не проходит / не проходит понятным сообщением. */
function judge(run: Run, i: number, s: StepResult | undefined, engine: string): string | null {
  const step = run.steps[i];
  const cell = run.lesson.cells.find((c) => c.id === step.cell)!;
  const where = `${engine}, ${run.label}, ячейка ${step.cell}`;
  if (!s) return `${where}: не выполнилась (прогон остановился раньше)`;
  const forbidden = s.warnings.filter((w) => FORBIDDEN_WARNINGS.includes(w));
  if (forbidden.length) return `${where}: ${forbidden.join(', ')} — устаревший API в уроке недопустим`;
  if (s.warnings.length && !('warns' in cell.flags)) return `${where}: предупреждения ${s.warnings.join(', ')} — уберите их или поставьте флаг [warns]`;
  const expect = run.expect[i];
  if (step.op === 'check') {
    if (expect === 'ok' && !passedAll(s)) return `${where}: проверка не проходит — ${describe(s)}`;
    if (expect !== 'ok' && passedAll(s)) return `${where}: проверка проходит, а должна ловить ${expect === 'fail' ? 'заготовку' : 'эту ошибку'}`;
    if (expect === 'mistake' && s.phase === 'tests') {
      const raw = s.results!.filter((t) => t.status === 'error');
      if (raw.length || !s.results!.some((t) => t.status === 'failed' && t.message)) {
        return `${where}: тест падает с исключением вместо понятного сообщения (${describe(s)}) — добавьте assert с текстом до этого места`;
      }
    }
    return null;
  }
  const raises = cell.flags.raises;
  if (raises && !(s.error?.mro.includes(raises))) return `${where}: ожидалась ошибка ${raises}, получено ${s.error?.text ?? 'без ошибки'}`;
  if (!raises && s.error) return `${where}: ${s.error.text}${s.error.line ? ` (строка ${s.error.line})` : ''}`;
  if (step.op === 'quiz') {
    const block = run.lesson.blocks.find((b) => b.type === 'quiz' && b.id === step.cell);
    const correct = block?.type === 'quiz' ? block.options.find((o) => o.correct) : undefined;
    const got = (s.result ?? s.lines).join('\n');
    if (correct && stripTicks(correct.text) !== got) return `${where}: код вопроса даёт «${got}», а верный вариант — «${stripTicks(correct.text)}»`;
  }
  return null;
}

async function runPyodide(runs: Run[], size: number): Promise<(StepResult[] | string)[]> {
  return pool(
    runs.map((run, n) => () => async (py: NodePython) => {
      const results: StepResult[] = [];
      const session = `v${n}`;
      for (const step of run.steps) {
        const end = await py.run({
          kind: 'lesson',
          packages: lessonPackages(run.course.meta, run.lesson.meta),
          lesson: run.lesson.meta.id,
          session,
          files: lessonFiles(run.lesson.meta),
          ...step,
        });
        if (end.type !== 'done') return `Pyodide, ${run.label}, ячейка ${step.cell}: ${end.type === 'timeout' ? `дольше ${end.seconds} с` : `${end.type}: ${end.message}`}`;
        results.push(end.data as LessonDone as StepResult);
      }
      return results;
    }),
    size,
  );
}

function stored(s: StepResult): StoredOutput {
  return { lines: s.lines, result: s.result, html: s.html, error: s.error?.text ?? null };
}

const sameOutput = (a: StoredOutput, b: StoredOutput) => JSON.stringify([a.lines, a.result, a.error]) === JSON.stringify([b.lines, b.result, b.error]);

function diffText(a: StoredOutput, b: StoredOutput): string {
  const text = (o: StoredOutput) => [...o.lines, ...(o.result ?? []), ...(o.error ? [o.error] : [])];
  const x = text(a);
  const y = text(b);
  const out: string[] = [];
  for (let i = 0; i < Math.max(x.length, y.length) && out.length < 6; i++) if (x[i] !== y[i]) out.push(`- ${x[i] ?? ''}`, `+ ${y[i] ?? ''}`);
  return out.join('\n');
}

// ─── Точка входа ────────────────────────────────────────────────────────────

async function main(argv: string[]): Promise<number> {
  const update = argv.includes('--update');
  const strict = argv.includes('--strict');
  const pythonArg = argv.includes('--python') ? argv[argv.indexOf('--python') + 1] : null;
  const selected = argv.filter((a, i) => !a.startsWith('--') && argv[i - 1] !== '--python');
  const python = pythonArg ?? (existsSync(join(root, '.venv', 'bin', 'python')) ? join(root, '.venv', 'bin', 'python') : 'python3');
  const r = new Report();
  const started = performance.now();

  const all = loadCourses();
  checkStructure(all, strict, r);
  const versions = cpython(python, { mode: 'versions' }) as Record<string, string>;
  const pins = pinned();
  for (const name of ['numpy', 'pandas']) {
    if (versions[name] !== pins[name]) r.error('окружение', `CPython: ${name} ${versions[name]}, а в requirements-dev.txt ${pins[name]} — поставьте зафиксированные версии`);
  }
  const review = checkConcepts(all, python, r);

  const chosen = all.flatMap((course) =>
    courseLessons(course)
      .filter((l) => !selected.length || selected.includes(course.slug) || selected.includes(l.meta.id))
      .map((lesson) => ({ course, lesson })),
  );
  const runs = chosen.filter(({ lesson }) => !lesson.problems.length).flatMap(({ course, lesson }) => planRuns(course, lesson));
  const size = Math.max(1, Math.min(4, availableParallelism() - 1));
  console.log(`Pyodide ${PYODIDE_VERSION} · CPython ${versions.python}, NumPy ${versions.numpy}, pandas ${versions.pandas} · уроков ${chosen.length}, прогонов ${runs.length}`);

  const [pyodide, cpy] = await Promise.all([
    runPyodide(runs, size),
    Promise.resolve().then(() => cpython(python, { mode: 'run', runs: runs.map((x) => ({ lesson: x.lesson.meta.id, files: x.lesson.meta.data, steps: x.steps })) }) as StepResult[][]),
  ]);

  const lock = JSON.parse(read(join(root, 'node_modules', 'pyodide', 'pyodide-lock.json'))) as { packages: Record<string, { version: string }> };
  const npVersion = (name: string) => lock.packages[name]?.version ?? '?';
  for (const { course, lesson } of chosen) {
    const at = lesson.meta.id;
    const lessonRuns = runs.map((run, i) => ({ run, i })).filter(({ run }) => run.lesson === lesson);
    for (const { run, i } of lessonRuns) {
      const p = pyodide[i];
      for (let k = run.from; k < run.steps.length; k++) {
        const problems = [typeof p === 'string' ? (k === run.from ? p : null) : judge(run, k, p[k], 'Pyodide'), judge(run, k, cpy[i][k], 'CPython')];
        for (const problem of problems) if (problem) r.error(at, problem);
      }
    }
    // сохранённый вывод — из прогона с эталонами в Pyodide; CPython должен совпадать, кроме [platform]
    const main = lessonRuns.find(({ run }) => run.label === 'эталоны');
    if (!main || typeof pyodide[main.i] === 'string') continue;
    const fresh: OutputFile = { generated: `Pyodide ${PYODIDE_VERSION} · ${course.meta.title} ${npVersion(course.meta.package)}`, cells: {} };
    main.run.steps.forEach((step, k) => {
      const cell = lesson.cells.find((c) => c.id === step.cell)!;
      if (cell.kind !== 'demo') return;
      const out = stored((pyodide[main.i] as StepResult[])[k]);
      fresh.cells[cell.id] = out;
      const c = cpy[main.i][k];
      if (c && !('platform' in cell.flags) && !sameOutput(out, stored(c))) {
        r.error(at, `ячейка ${cell.id}: вывод в CPython и в браузере разный — сделайте его независимым от платформы или поставьте [platform]\n${diffText(out, stored(c))}`);
      }
      if (c && 'platform' in cell.flags && sameOutput(out, stored(c))) r.warn(at, `ячейка ${cell.id}: вывод одинаковый — флаг [platform] не нужен`);
    });
    const path = join(lesson.dir, 'output.json');
    const text = `${JSON.stringify(fresh, null, 2)}\n`;
    if (update) {
      if (!existsSync(path) || read(path) !== text) writeFileSync(path, text);
    } else if (!existsSync(path)) r.error(at, 'нет output.json — запустите с --update');
    else {
      const old = JSON.parse(read(path)) as OutputFile;
      for (const id of new Set([...Object.keys(old.cells), ...Object.keys(fresh.cells)])) {
        if (!old.cells[id] || !fresh.cells[id] || JSON.stringify(old.cells[id]) !== JSON.stringify(fresh.cells[id])) {
          r.error(at, `ячейка ${id}: сохранённый вывод устарел — запустите с --update`);
        }
      }
      if (old.generated !== fresh.generated) r.error(at, `output.json снят в «${old.generated}», сейчас «${fresh.generated}» — запустите с --update`);
    }
    // ноутбук с эталонами выполняется в Jupyter-подобном режиме без ошибок
    const notebook = buildNotebook(course, lesson, { root, siteUrl: null, solutions: true });
    const nbIds = (notebook as { cells: { id: string }[] }).cells.map((c) => c.id);
    const dupIds = nbIds.filter((id, k) => nbIds.indexOf(id) !== k);
    if (dupIds.length) r.error(at, `ноутбук: id ячеек повторяются (${dupIds.join(', ')}) — переименуйте ячейки урока`);
    const nb = cpython(python, { mode: 'notebook', notebook }) as { outputs: { cell: string; stdout: string }[]; error: { cell: string; traceback: string } | null };
    if (nb.error) r.error(at, `ноутбук: ячейка ${nb.error.cell} падает\n${nb.error.traceback}`);
    for (const cell of lesson.cells) {
      const raises = cell.kind === 'demo' ? cell.flags.raises : undefined;
      const out = nb.outputs.find((o) => o.cell === cell.id);
      if (raises && out && !out.stdout.includes(`${raises}: `)) r.error(at, `ноутбук: ячейка ${cell.id} должна напечатать перехваченную ошибку ${raises}`);
    }
    const checkCells = new Set(lesson.cells.filter((c) => c.kind === 'exercise').map((c) => `${c.id}-check`));
    for (const out of nb.outputs.filter((o) => checkCells.has(o.cell))) {
      if (!/Прошло (\d+) из \1 — всё верно!/.test(out.stdout)) r.error(at, `ноутбук: проверка ${out.cell} с эталоном не проходит:\n${out.stdout.trim()}`);
    }
  }

  // ─── Итог ─────────────────────────────────────────────────────────────────
  for (const { lesson } of chosen) {
    const at = lesson.meta.id;
    const exercises = lesson.cells.filter((c): c is ExerciseCell => c.kind === 'exercise');
    const errors = r.errors.get(at) ?? [];
    console.log(`${errors.length ? '✗' : '✓'} ${at}: ${exercises.length} упр., ${lesson.cells.filter((c) => c.kind === 'demo').length} демонстраций · повторение: ${review.get(at)?.join(' ') || '—'}`);
  }
  for (const [where, list] of r.warnings) for (const w of list) console.log(`  · ${where}: ${w}`);
  for (const [where, list] of r.errors) {
    for (const e of list) {
      console.log(`  ✗ ${where}: ${e}`);
      annotate(where, e);
    }
  }
  const count = [...r.errors.values()].reduce((a, l) => a + l.length, 0);
  console.log(`${count ? `✗ Ошибок: ${count}` : '✓ Всё в порядке'} (${((performance.now() - started) / 1000).toFixed(1)} с)`);
  return count ? 1 : 0;
}

process.exitCode = await main(process.argv.slice(2));
