/**
 * План прогона CI: какие задания запускать и что именно в них проверять — по изменённым файлам.
 * Единственное место с правилами «путь → раздел → задание» (.github/workflows/tasks.yml читает вывод).
 *
 *   node scripts/ci_changes.ts --base origin/main         # изменения ветки: git diff merge-base..HEAD
 *   node scripts/ci_changes.ts --files courses/numpy/01-start/02-first-array/lesson.py README.md
 *   node scripts/ci_changes.ts --full                     # полный прогон: всё
 *
 * Уровни (docs/ARCHITECTURE.md, «CI»):
 *   полный   — push в main, ночной прогон, ручной запуск «full»: все задания, все задачи, уроки и статьи;
 *   ветка    — только задания затронутых разделов; медленные (курсы, браузеры) — только изменённые уроки и
 *              задачи. Изменена общая часть раздела (раннер, валидатор, загрузчик курсов) — весь раздел;
 *              общая часть всего (GLOBAL: воркер, конфиг Pyodide, зависимости, сам CI) — всё, как в полном.
 * Матрица Python (3 ОС × 3.10–3.14) и три браузера — на любом уровне, если задание запускается: уровень
 * решает, ЧТО проверять, а не В ЧЁМ.
 *
 * Путь, который не подходит ни под одно правило и не в IGNORED, считается общим: лучше лишний прогон, чем
 * пропущенная проверка нового раздела. Новый раздел — запись в AREAS и в JOBS (docs/ARCHITECTURE.md, «CI»).
 *
 * Вывод: таблица в консоль, в GitHub Actions — ключи в $GITHUB_OUTPUT и сводка в $GITHUB_STEP_SUMMARY:
 *   full=true|false, run_<задание>=true|false, ids_<задание>=id1,id2 (пусто — все),
 *   browsers_matrix — JSON для strategy.matrix ({include: [{browser, shard}]}), browser_probes — пробы глубины рекурсии.
 */
import { execFileSync } from 'node:child_process';
import { appendFileSync, existsSync, readFileSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { parse as parseToml } from 'smol-toml';
import { courseLessons, loadCourses } from '../src/lib/courses/load.ts';

const root = join(import.meta.dirname, '..');
process.chdir(root); // loadCourses читает courses/ относительно текущей папки

/** Раздел содержимого: изменение в content — только затронутые id; в shared — весь раздел. */
interface Area {
  content: string[];
  shared: string[];
  /** id изменённого элемента по пути файла; null — файл уровня раздела (книга, курс, модуль): весь раздел. */
  item?: (file: string) => string | null;
}

/** Изменение здесь — всё проверяется заново (воркер и ядро Python, зависимости, сборка, сам CI). */
export const GLOBAL = [
  'package.json',
  'package-lock.json',
  'requirements-dev.txt',
  'astro.config.mjs',
  'tsconfig.json',
  '.github/workflows/',
  'scripts/ci_changes.ts',
  'src/lib/python/',
  'runtime/pyodide_driver.py',
  'scripts/node-python.ts',
  'scripts/pyodide-worker.ts',
];

/** Не влияет ни на одну проверку. */
export const IGNORED = ['docs/', '.claude/', 'README.md', 'LICENSE', 'CONTENT-LICENSE.md', 'changes.txt', '.gitignore'];

export const AREAS: Record<string, Area> = {
  tasks: {
    content: ['challenges/'],
    shared: ['runtime/runner.py', 'scripts/validate.py', 'scripts/run_bundles.py', 'src/lib/bundle.ts', 'src/lib/challenges.ts', 'scripts/check-bundles.ts'],
    item: taskId,
  },
  reference: {
    content: ['reference/', 'public/reference/'],
    shared: ['runtime/reference_exec.py', 'scripts/validate_reference.py', 'reference/prelude.py', 'reference/browser.json', 'src/lib/examples.ts', 'src/lib/browser-runs.ts'],
    item: articleId,
  },
  courses: {
    content: ['courses/', 'public/course-plots/'],
    shared: ['runtime/lesson_exec.py', 'scripts/validate_courses.ts', 'scripts/course_cpython.py', 'src/lib/courses/', 'courses/prelude.py', 'courses/data/'],
    item: lessonId,
  },
  site: {
    content: ['src/', 'public/', 'supabase/', 'scripts/test_supabase_sql.ts', 'scripts/mock_supabase.ts'],
    shared: [],
  },
};

/**
 * Задания CI: от каких разделов зависят и какие ещё файлы заставляют проверить в них всё.
 * ids — получает ли задание список id (медленные: курсы, браузеры); остальные быстрые и проверяют раздел целиком.
 */
export const JOBS: Record<string, { areas: string[]; shared?: string[]; ids?: boolean }> = {
  tasks: { areas: ['tasks'] }, // валидатор и файлы задач на матрице ОС × Python
  reference: { areas: ['reference'] },
  pyodide: { areas: ['tasks', 'reference'], shared: ['scripts/validate_pyodide.ts'] },
  courses: { areas: ['courses'], ids: true },
  browsers: { areas: ['tasks', 'courses'], shared: ['scripts/validate_browsers.ts', 'scripts/browser-check.html'], ids: true },
  site: { areas: ['tasks', 'reference', 'courses', 'site'] },
};

/**
 * На сколько заданий делится проверка каждого браузера, если проверяется всё (замеры — docs/ARCHITECTURE.md, «CI»).
 * Всего 5 заданий — столько раннеров macOS у аккаунта одновременно. Chromium целиком быстрее Firefox и WebKit
 * (у WebKit ещё и пробы глубины дольше).
 */
export const BROWSER_SHARDS: Record<string, number> = { chromium: 1, firefox: 2, webkit: 2 };
/** Выбрано не больше стольких задач и уроков — одна часть на браузер. */
const ONE_SHARD_LIMIT = 40;

const starts = (file: string, prefixes: string[]) => prefixes.some((p) => (p.endsWith('/') ? file.startsWith(p) : file === p));

function taskId(file: string): string | null {
  const parts = file.split('/'); // challenges/<книга>/<глава>/<задача>/…
  if (parts.length < 5) return null; // book.toml, файл главы — вся книга
  const meta = join(root, ...parts.slice(0, 4), 'meta.toml');
  return existsSync(meta) ? String((parseToml(readFileSync(meta, 'utf-8')) as { id: string }).id) : '';
}

function articleId(file: string): string | null {
  const m = /^(?:public\/)?reference\/(?:plots\/)?([^/]+)\/([^/.]+)(?:\.(?:mdx|py)|\/)/.exec(file);
  return m ? `${m[1]}/${m[2]}` : null;
}

let lessonDirs: Map<string, string> | null = null;
let lessonPlots: Map<string, string> | null = null;
function lessonId(file: string): string | null {
  if (!lessonDirs || !lessonPlots) {
    const lessons = loadCourses().flatMap((c) => courseLessons(c).map((l) => ({ c, l })));
    lessonDirs = new Map(lessons.map(({ l }) => [relative(root, l.dir), l.meta.id]));
    lessonPlots = new Map(lessons.map(({ c, l }) => [`${c.slug}/${l.slug}`, l.meta.id]));
  }
  if (file.startsWith('public/course-plots/')) {
    const m = /^public\/course-plots\/([^/]+\/[^/]+)\//.exec(file); // графики урока: public/course-plots/<курс>/<урок>/…
    return m ? (lessonPlots.get(m[1]) ?? '') : null;
  }
  for (let dir = dirname(file); dir !== '.' && dir !== 'courses'; dir = dirname(dir)) {
    const id = lessonDirs.get(dir);
    if (id) return id;
  }
  // файл урока, которого уже нет (удалён или переименован), — '' (проверять нечего), файл курса или модуля — весь курс
  return /^courses\/[^/]+\/[^/]+\/[^/]+\//.test(file) ? '' : null;
}

export interface Plan {
  full: boolean;
  reason: string;
  jobs: Record<string, { run: boolean; ids: string[] | null }>; // ids null — все
}

export function plan(files: string[] | null): Plan {
  const jobs = Object.fromEntries(Object.keys(JOBS).map((j) => [j, { run: files === null, ids: null as string[] | null }]));
  if (files === null) return { full: true, reason: 'полный прогон', jobs };
  const known = (f: string) => starts(f, IGNORED) || Object.values(AREAS).some((a) => starts(f, a.content) || starts(f, a.shared)) || Object.values(JOBS).some((j) => starts(f, j.shared ?? []));
  const global = files.filter((f) => starts(f, GLOBAL) || !known(f));
  if (global.length) {
    for (const job of Object.values(jobs)) job.run = true;
    return { full: false, reason: `общие части: ${global.slice(0, 5).join(', ')}${global.length > 5 ? '…' : ''}`, jobs };
  }
  const areaAll = new Set<string>();
  const areaIds = new Map<string, Set<string>>();
  for (const file of files) {
    for (const [name, area] of Object.entries(AREAS)) {
      if (starts(file, area.shared)) areaAll.add(name);
      else if (starts(file, area.content)) {
        const id = area.item ? area.item(file) : null;
        if (id === null) areaAll.add(name);
        else (areaIds.get(name) ?? areaIds.set(name, new Set()).get(name)!).add(id);
      }
    }
  }
  for (const [name, spec] of Object.entries(JOBS)) {
    const job = jobs[name];
    const all = files.some((f) => starts(f, spec.shared ?? [])) || spec.areas.some((a) => areaAll.has(a));
    const ids = [...new Set(spec.areas.flatMap((a) => [...(areaIds.get(a) ?? [])]).filter(Boolean))].sort();
    job.run = all || ids.length > 0 || (!spec.ids && spec.areas.some((a) => areaIds.has(a)));
    job.ids = all || !spec.ids ? null : ids;
    if (job.ids && !job.ids.length) job.run = false; // только удалённые уроки или задачи — выполнять нечего
  }
  const areas = [...new Set([...areaAll, ...areaIds.keys()])];
  return { full: false, reason: areas.length ? `изменены разделы: ${areas.join(', ')}` : 'проверять нечего', jobs };
}

function changedFiles(base: string): string[] {
  const git = (...args: string[]) => execFileSync('git', args, { cwd: root, encoding: 'utf-8' }).trim();
  const mergeBase = git('merge-base', base, 'HEAD');
  return git('diff', '--name-only', '--no-renames', mergeBase, 'HEAD').split('\n').filter(Boolean);
}

/** Ключи для GitHub Actions. */
export function outputs(p: Plan): Record<string, string> {
  const b = p.jobs.browsers;
  const few = b.ids !== null && b.ids.length <= ONE_SHARD_LIMIT;
  const include = Object.entries(BROWSER_SHARDS).flatMap(([browser, n]) =>
    Array.from({ length: few ? 1 : n }, (_, i) => ({ browser, shard: `${i + 1}/${few ? 1 : n}` })),
  );
  const out: Record<string, string> = {
    full: String(p.full),
    // пробы глубины проверяют воркер и браузер, а не содержимое: только если проверяется всё
    browser_probes: String(b.run && b.ids === null),
    browsers_matrix: JSON.stringify({ include }),
  };
  for (const [name, job] of Object.entries(p.jobs)) {
    out[`run_${name}`] = String(job.run);
    out[`ids_${name}`] = job.ids?.join(',') ?? '';
  }
  return out;
}

function main(argv: string[]): void {
  const baseArg = argv.includes('--base') ? argv[argv.indexOf('--base') + 1] : null;
  const files = argv.includes('--full') ? null : argv.includes('--files') ? argv.slice(argv.indexOf('--files') + 1) : changedFiles(baseArg ?? 'origin/main');
  const p = plan(files);
  const out = outputs(p);
  const parts = (JSON.parse(out.browsers_matrix) as { include: { browser: string; shard: string }[] }).include;
  const lines = [
    `Уровень: ${p.full ? 'полный' : 'ветка'} — ${p.reason}${files ? ` (файлов изменено: ${files.length})` : ''}`,
    ...Object.entries(p.jobs).map(([name, job]) => `  ${name.padEnd(9)} ${job.run ? (job.ids ? `только: ${job.ids.join(', ')}` : 'всё') : '—'}`),
    `  браузеры: ${Object.keys(BROWSER_SHARDS).map((n) => `${n} × ${parts.filter((x) => x.browser === n).length}`).join(', ')}${out.browser_probes === 'true' ? ', с пробами глубины' : ''}`,
  ];
  console.log(lines.join('\n'));
  if (process.env.GITHUB_OUTPUT) appendFileSync(process.env.GITHUB_OUTPUT, Object.entries(out).map(([k, v]) => `${k}=${v}\n`).join(''));
  if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, `### План прогона\n\n\`\`\`\n${lines.join('\n')}\n\`\`\`\n`);
}

if (import.meta.main) main(process.argv.slice(2));
