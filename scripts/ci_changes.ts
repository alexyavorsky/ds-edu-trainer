/**
 * План прогона CI: какие задания запускать и что именно в них проверять — по изменённым файлам.
 * Единственное место с правилами «путь → раздел → задание» (.github/workflows/tasks.yml читает вывод).
 *
 *   node scripts/ci_changes.ts --base origin/main         # изменения ветки: git diff merge-base..HEAD
 *   node scripts/ci_changes.ts --files courses/numpy/01-start/02-first-array/lesson.py README.md
 *   node scripts/ci_changes.ts --full                     # полный прогон: всё, полная матрица, три браузера
 *
 * Уровни (docs/ARCHITECTURE.md, «CI»):
 *   полный   — push в main, ночной прогон, workflow_dispatch с scope = full: все задания, все id, матрица
 *              Python 3 ОС × 3.10–3.14, браузеры Chromium + Firefox + WebKit, по частям;
 *   ветка/PR — только задания затронутых разделов и только изменённые задачи, уроки; минимальная матрица
 *              Python; браузеры Chromium + WebKit. Изменены общие части раздела (раннер, валидатор) — все id
 *              раздела; изменены общие части всего (GLOBAL) — все задания и все id (матрицы остаются минимальными).
 *
 * Путь, который не подходит ни под одно правило и не в IGNORED, считается общим: лучше лишний прогон, чем
 * пропущенная проверка нового раздела. Новый раздел — новая запись в AREAS и в JOBS (см. docs/reports/ci-speedup.md).
 *
 * Вывод: таблица в консоль, в GitHub Actions — ключи в $GITHUB_OUTPUT и сводка в $GITHUB_STEP_SUMMARY:
 *   full=true|false, run_<задание>=true|false, ids_<задание>=id1,id2 (пусто — все),
 *   bundles_matrix, browsers_matrix — JSON для strategy.matrix, browser_pages — страниц в задании браузера.
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

/** Изменение здесь — всё проверяется заново (runtime, воркер, зависимости, сам CI). */
const GLOBAL = [
  'package.json',
  'package-lock.json',
  'requirements-dev.txt',
  '.github/workflows/',
  'scripts/ci_changes.ts',
  'src/lib/python/',
  'runtime/pyodide_driver.py',
  'scripts/node-python.ts',
  'scripts/pyodide-worker.ts',
];

/** Не влияет ни на одну проверку. */
const IGNORED = ['docs/', '.claude/', 'README.md', 'LICENSE', '.gitignore', '.vscode/', '.editorconfig'];

const AREAS: Record<string, Area> = {
  tasks: {
    content: ['challenges/'],
    shared: ['runtime/runner.py', 'scripts/validate.py', 'scripts/run_bundles.py', 'src/lib/bundle.ts', 'scripts/check-bundles.ts'],
    item: taskId,
  },
  reference: {
    content: ['reference/', 'public/reference/'],
    shared: ['runtime/reference_exec.py', 'scripts/validate_reference.py', 'reference/prelude.py', 'reference/browser.json', 'src/lib/examples.ts'],
    item: articleId,
  },
  courses: {
    content: ['courses/', 'public/course-plots/'],
    shared: ['runtime/lesson_exec.py', 'scripts/validate_courses.ts', 'scripts/course_cpython.py', 'src/lib/courses/', 'courses/prelude.py', 'courses/data/'],
    item: lessonId,
  },
  site: {
    content: ['src/', 'public/', 'astro.config.mjs', 'tsconfig.json'],
    shared: [],
  },
};

/**
 * Задания CI: от каких разделов зависят и какие файлы, кроме общих частей разделов, заставляют проверить всё.
 * ids — передавать ли заданию список id (иначе при запуске проверяется весь раздел: задание быстрое).
 */
const JOBS: Record<string, { areas: string[]; shared?: string[]; ids?: boolean }> = {
  tasks: { areas: ['tasks'] }, // валидатор и файлы задач на матрице ОС × Python: быстрые, всегда целиком
  reference: { areas: ['reference'] },
  pyodide: { areas: ['tasks', 'reference'], shared: ['scripts/validate_pyodide.ts'], ids: true },
  courses: { areas: ['courses'], ids: true },
  browsers: { areas: ['tasks', 'courses'], shared: ['scripts/validate_browsers.ts', 'scripts/browser-check.html'], ids: true },
  site: { areas: ['tasks', 'reference', 'courses', 'site'] },
};

/** Матрица «файлов задач»: полная и минимальная (границы поддерживаемых версий + Windows — пути, кодировка). */
const BUNDLES_FULL = ['ubuntu-latest', 'macos-latest', 'windows-latest'].flatMap((os) =>
  ['3.10', '3.11', '3.12', '3.13', '3.14'].map((python) => ({ os, python })),
);
const BUNDLES_MIN = [
  { os: 'ubuntu-latest', python: '3.10' },
  { os: 'ubuntu-latest', python: '3.14' },
  { os: 'windows-latest', python: '3.12' },
];

/** Браузеры: полный прогон — три, ветка — Chromium и WebKit (Safari: самый маленький стек). */
const BROWSERS_FULL = ['chromium', 'firefox', 'webkit'];
const BROWSERS_MIN = ['chromium', 'webkit'];
/** На сколько заданий делить проверку одного браузера, если проверяется всё (замеры — docs/reports/ci-speedup.md). */
const BROWSER_SHARDS = 3;
/** Страниц браузера параллельно в одном задании (validate_browsers.ts --pages): у раннера macOS 3 ядра. */
const BROWSER_PAGES = 1;
/** Выбрано меньше стольких задач и уроков — одна часть на браузер. */
const ONE_SHARD_LIMIT = 12;

const starts = (file: string, prefixes: string[]) => prefixes.some((p) => (p.endsWith('/') ? file.startsWith(p) : file === p));

function taskId(file: string): string | null {
  const parts = file.split('/'); // challenges/<книга>/<глава>/<задача>/…
  if (parts.length < 5) return null;
  const meta = join(root, ...parts.slice(0, 4), 'meta.toml');
  return existsSync(meta) ? String((parseToml(readFileSync(meta, 'utf-8')) as { id: string }).id) : '';
}

function articleId(file: string): string | null {
  const m = /^(?:public\/)?reference\/(?:plots\/)?([^/]+)\/([^/.]+)(?:\.(?:mdx|py)|\/)/.exec(file);
  return m ? `${m[1]}/${m[2]}` : null;
}

let lessonDirs: Map<string, string> | null = null;
function lessonId(file: string): string | null {
  lessonDirs ??= new Map(loadCourses().flatMap((c) => courseLessons(c).map((l) => [relative(root, l.dir), l.meta.id] as [string, string])));
  if (file.startsWith('public/course-plots/')) return null;
  for (let dir = dirname(file); dir !== '.' && dir !== 'courses'; dir = dirname(dir)) {
    const id = lessonDirs.get(dir);
    if (id) return id;
  }
  // файл урока, которого уже нет (удалён или переименован), — '' (ничего), файл курса или модуля — весь курс
  return /^courses\/[^/]+\/[^/]+\/[^/]+\//.test(file) ? '' : null;
}

interface Plan {
  full: boolean;
  reason: string;
  jobs: Record<string, { run: boolean; ids: string[] | null }>; // ids null — все
}

function plan(files: string[] | null): Plan {
  const jobs = Object.fromEntries(Object.keys(JOBS).map((j) => [j, { run: files === null, ids: null as string[] | null }]));
  if (files === null) return { full: true, reason: 'полный прогон', jobs };
  const global = files.filter((f) => starts(f, GLOBAL) || (!starts(f, IGNORED) && !Object.values(AREAS).some((a) => starts(f, a.content) || starts(f, a.shared))));
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
    const ids = spec.areas.flatMap((a) => [...(areaIds.get(a) ?? [])]).filter(Boolean);
    const touched = all || spec.areas.some((a) => areaIds.has(a));
    job.run = touched;
    // все id раздела, или только удалённые (id нет) — проверяется всё; иначе — только изменённое
    job.ids = !touched || all || !spec.ids || !ids.length ? null : [...new Set(ids)].sort();
  }
  const areas = [...new Set([...areaAll, ...areaIds.keys()])];
  return { full: false, reason: areas.length ? `изменены разделы: ${areas.join(', ')}` : 'проверять нечего', jobs };
}

function changedFiles(base: string): string[] {
  const git = (...args: string[]) => execFileSync('git', args, { cwd: root, encoding: 'utf-8' }).trim();
  const mergeBase = git('merge-base', base, 'HEAD');
  return git('diff', '--name-only', '--no-renames', mergeBase, 'HEAD').split('\n').filter(Boolean);
}

function main(argv: string[]): void {
  const baseArg = argv.includes('--base') ? argv[argv.indexOf('--base') + 1] : null;
  const files = argv.includes('--full') ? null : argv.includes('--files') ? argv.slice(argv.indexOf('--files') + 1) : changedFiles(baseArg ?? 'origin/main');
  const p = plan(files);
  const browsers = p.full ? BROWSERS_FULL : BROWSERS_MIN;
  const b = p.jobs.browsers;
  const shards = b.ids && b.ids.length < ONE_SHARD_LIMIT ? 1 : BROWSER_SHARDS;
  const out: Record<string, string> = {
    full: String(p.full),
    bundles_matrix: JSON.stringify({ include: p.full ? BUNDLES_FULL : BUNDLES_MIN }),
    browser_pages: String(BROWSER_PAGES),
    browsers_matrix: JSON.stringify({ browser: browsers, shard: Array.from({ length: shards }, (_, i) => `${i + 1}/${shards}`) }),
  };
  for (const [name, job] of Object.entries(p.jobs)) {
    out[`run_${name}`] = String(job.run);
    out[`ids_${name}`] = job.ids?.join(',') ?? '';
  }
  const lines = [
    `Уровень: ${p.full ? 'полный' : 'ветка/PR'} — ${p.reason}${files ? ` (файлов изменено: ${files.length})` : ''}`,
    ...Object.entries(p.jobs).map(([name, job]) => `  ${name.padEnd(9)} ${job.run ? (job.ids ? `только: ${job.ids.join(', ')}` : 'всё') : '—'}`),
    `  матрица Python: ${p.full ? BUNDLES_FULL.length : BUNDLES_MIN.length} заданий; браузеры: ${browsers.join(', ')} × частей ${shards}`,
  ];
  console.log(lines.join('\n'));
  if (process.env.GITHUB_OUTPUT) appendFileSync(process.env.GITHUB_OUTPUT, Object.entries(out).map(([k, v]) => `${k}=${v}\n`).join(''));
  if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, `### План прогона\n\n\`\`\`\n${lines.join('\n')}\n\`\`\`\n`);
}

main(process.argv.slice(2));
