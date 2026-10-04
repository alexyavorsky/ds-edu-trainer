/**
 * Проверка Python в настоящих браузерах: Chromium, Firefox и WebKit (движок Safari) через Playwright.
 * Запускает production-сборку сайта (dist/, сначала npm run build) — тот же воркер, что на страницах задач.
 *
 *   node scripts/validate_browsers.ts                      # все три браузера
 *   node scripts/validate_browsers.ts webkit firefox       # выбранные
 *   node scripts/validate_browsers.ts --only ga-tile-ways,ga-typo-distance   # выбранные задачи и уроки (по id)
 *   node scripts/validate_browsers.ts webkit --shard 2/3   # часть 2 из 3 (как в CI): каждая третья задача и урок
 *   node scripts/validate_browsers.ts chromium --pages 2   # две вкладки параллельно (по умолчанию — по ядру, до 8)
 *   node scripts/validate_browsers.ts chromium --only pd-project-clean --lesson-timeout 5   # свой лимит на урок, с
 *
 * --only можно задать и переменной CHECK_ONLY. Пробы глубины — только в части 1: с --probes всегда, без него —
 * если проверяется всё (без --only); --no-probes — без них.
 *
 * Зачем, если есть scripts/validate_pyodide.ts: стек WebAssembly в браузерах разный, и рекурсия, которая идёт
 * через C (functools.cache / lru_cache, sum(генератор), map), в Safari выдерживает всего ~60 уровней, а в
 * Node.js — сотни. Проверка выполняет все эталоны и альтернативные эталоны в каждом браузере и пробы глубины:
 *   plain   — обычная рекурсия: 990 уровней работают, 5000 дают RecursionError (а не падение Python);
 *   cache   — рекурсия через @cache: должна выдерживать MEMO_DEPTH уровней — это бюджет глубины для тестов
 *             задач, где подходит рекурсия с запоминанием (docs/ARCHITECTURE.md, «Приёмы в тестах»);
 *   остальное — для отчёта: где именно в этом браузере кончается стек.
 * Нужны браузеры Playwright: npx playwright install chromium firefox webkit.
 *
 * Как выполняется (docs/ARCHITECTURE.md, «CI»):
 *   - задачи и уроки — пачками по BATCH, каждая пачка в новом контексте браузера (свой процесс страницы):
 *     у каждой задачи и урока свой воркер, как на сайте, но в одной странице их не больше BATCH — WebKit
 *     после сотни-другой воркеров в одном процессе страницы падает (подробности — у BATCH);
 *   - пачки выполняются в нескольких вкладках параллельно (--pages);
 *   - Pyodide и пакеты для задач и уроков — из локального зеркала (/__pyodide/): ядро — из npm-пакета pyodide
 *     той же версии (побайтно совпадает с jsDelivr), пакеты — из кэша PYODIDE_CACHE, при промахе скачиваются
 *     с jsDelivr с повторами и сверкой sha256 по pyodide-lock.json. Сбой сети не роняет проверку, а
 *     проверяемый код тот же. Пробы глубины грузят Pyodide с jsDelivr, как сайт (повторы запуска — с паузой).
 *
 * Урок курса ограничен LESSON_TIMEOUT (5 минут, вместе с запуском Python и пакетов): зависший урок
 * останавливается, в ошибке — браузер, урок, последняя начатая ячейка и сколько прошло; остальные уроки
 * проверяются дальше, итог — ненулевой код выхода.
 *
 * Повторы — только страховка, и каждый виден (строка «повтор» и ::warning в CI, итог «повторов: N»):
 * упала вкладка или браузер — пачка выполняется заново один раз в новом контексте; не запустился
 * воркер Python — до двух повторов (browser-check.html, startPython); скачивание файла Pyodide — до 6 попыток.
 * Журнал каждой вкладки пишется по мере выполнения в browser-logs/ (в CI — артефакт), конец журнала упавшей
 * вкладки печатается в ошибке.
 */
import { createHash } from 'node:crypto';
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import type { AddressInfo } from 'node:net';
import { availableParallelism } from 'node:os';
import { extname, join } from 'node:path';
import { chromium, firefox, webkit, type Browser, type BrowserType } from 'playwright';
import { parse as parseToml } from 'smol-toml';
import { bundleFooter } from '../src/lib/bundle.ts';
import { courseLessons, lessonFiles, lessonPackages, loadCourses } from '../src/lib/courses/load.ts';
import { PYODIDE_INDEX_URL, PYTHON_CONFIG } from '../src/lib/python/config.ts';

/** Глубина рекурсии с запоминанием, которую тесты задач могут требовать (Safari падает на ~70). */
const MEMO_DEPTH = 40;
/** Лимит на один урок курса в браузере, секунды (--lesson-timeout — свой, например для проверки самого лимита). */
const LESSON_TIMEOUT = 5 * 60;
/** Лимит на одну вкладку (пачку), секунды. */
const PAGE_TIMEOUT = 20 * 60;
/**
 * Задач и уроков на одну вкладку (новый контекст — новый процесс страницы). WebKit в одном процессе страницы
 * выдерживает около сотни воркеров Pyodide: дальше процесс страницы падает при запуске очередного воркера
 * (docs/ARCHITECTURE.md, «CI» — разбор). С запасом — 25 воркеров.
 */
const BATCH = 25;
/** Полные журналы вкладок (в CI — артефакт). */
const LOG_DIR = join(import.meta.dirname, '..', 'browser-logs');
/** Пакеты Pyodide, скачанные с jsDelivr (тот же кэш, что у scripts/validate_pyodide.ts в CI). */
const CACHE_DIR = process.env.PYODIDE_CACHE || join(import.meta.dirname, '..', '.pyodide-cache');
/** Попыток скачать файл Pyodide; пауза между ними растёт: 2, 4, 8, 16, 32 с — сеть может пропасть на минуту. */
const DOWNLOAD_ATTEMPTS = 6;

const PROBES: Record<string, { depths: number[]; code: string }> = {
  plain: { depths: [990, 5000], code: 'def f(n):\n    return 0 if n == 0 else f(n - 1) + 1\nprint(f(DEPTH))' },
  cache: {
    depths: [20, MEMO_DEPTH, 60, 80, 100, 150, 200, 300, 400],
    code: 'from functools import cache\n\n@cache\ndef f(n):\n    return 0 if n == 0 else f(n - 1) + 1\nprint(f(DEPTH))',
  },
  cache_min_generator: {
    depths: [20, 25, 30, 35, 40, 50, 60, 80, 100, 150, 200],
    code: 'from functools import cache\n\n@cache\ndef f(n):\n    return 0 if n == 0 else min(f(n - c) + 1 for c in (1, 2) if c <= n)\nprint(f(DEPTH))',
  },
  sum_generator: {
    depths: [20, 40, 60, 80, 100, 150, 200, 300, 400],
    code: 'def f(n):\n    return 0 if n == 0 else sum(f(n - 1) for _ in range(1)) + 1\nprint(f(DEPTH))',
  },
  nested_list_free: {
    depths: [500, 1000, 1500, 2000, 3000, 5000],
    code: 'x = [0]\nfor i in range(DEPTH):\n    x = [x, i]\ndel x\nprint("ok")',
  },
};

const root = join(import.meta.dirname, '..');
const dist = join(root, 'dist');
const npmPyodide = join(root, 'node_modules', 'pyodide');
const read = (path: string) => readFileSync(path, 'utf-8');
const dirs = (path: string) => readdirSync(path).filter((n) => !/^[._]/.test(n) && statSync(join(path, n)).isDirectory()).sort();
const engines: Record<string, BrowserType> = { chromium, firefox, webkit };
const inCI = process.env.GITHUB_ACTIONS === 'true';

interface Task {
  id: string;
  packages: string[];
  footer: string;
  variants: [string, string][];
}

function loadTasks(): Task[] {
  const runner = read(join(root, 'runtime', 'runner.py'));
  const tasks: Task[] = [];
  const base = join(root, 'challenges');
  for (const book of dirs(base)) {
    const bookMeta = parseToml(read(join(base, book, 'book.toml'))) as { packages?: string[] };
    for (const chapter of dirs(join(base, book))) {
      for (const slug of dirs(join(base, book, chapter))) {
        const dir = join(base, book, chapter, slug);
        const meta = parseToml(read(join(dir, 'meta.toml'))) as { id: string; type: string };
        if (meta.type === 'complexity') continue;
        const variants: [string, string][] = [['solution.py', read(join(dir, 'solution.py'))]];
        const alt = join(dir, 'alt_solutions');
        if (existsSync(alt)) for (const f of readdirSync(alt).filter((n) => n.endsWith('.py')).sort()) variants.push([`alt_solutions/${f}`, read(join(alt, f))]);
        tasks.push({ id: meta.id, packages: bookMeta.packages ?? [], footer: bundleFooter(read(join(dir, 'tests.py')), runner), variants });
      }
    }
  }
  return tasks;
}

/**
 * Уроки курсов: прогон с эталонами, как в scripts/validate_courses.ts, — все ячейки по порядку в одном сеансе.
 * Страница сверяет вывод демонстраций с сохранённым (output.json снят в Pyodide) и требует, чтобы проверки
 * упражнений проходили.
 */
function loadLessons() {
  return loadCourses().flatMap((course) =>
    courseLessons(course).map((lesson) => ({
      id: lesson.meta.id,
      packages: lessonPackages(course.meta, lesson.meta),
      files: lessonFiles(lesson.meta),
      steps: lesson.cells.map((c) =>
        c.kind === 'exercise'
          ? { op: 'check', cell: c.id, code: c.solution, tests: c.tests, targets: c.targets }
          : { op: c.kind === 'quiz' ? 'quiz' : 'cell', cell: c.id, code: c.code, raises: c.flags.raises ?? null, expected: lesson.output?.cells[c.id] ?? null },
      ),
    })),
  );
}

// ─── Зеркало Pyodide ────────────────────────────────────────────────────────

type Lock = { packages: Record<string, { file_name: string; sha256: string; depends: string[] }> };

/** Повторы и скачивания — в итог прогона: повторы должны быть видны. */
const network = { downloaded: 0, served: 0, retries: [] as string[] };

class PyodideMirror {
  private lock = JSON.parse(read(join(npmPyodide, 'pyodide-lock.json'))) as Lock;
  private sha = new Map(Object.values(this.lock.packages).map((p) => [p.file_name, p.sha256]));
  private pending = new Map<string, Promise<Buffer>>();

  /** Файл дистрибутива Pyodide: npm-пакет → кэш → jsDelivr (с повторами и сверкой sha256). */
  file(name: string): Promise<Buffer> {
    if (!/^[\w.+-]+$/.test(name)) return Promise.reject(new HttpError(404));
    let p = this.pending.get(name);
    if (!p) {
      p = this.load(name);
      this.pending.set(name, p);
      p.catch(() => this.pending.delete(name));
    }
    return p;
  }

  /** Пакеты с зависимостями — заранее, чтобы сбой сети проявился и вылечился до запуска браузеров. */
  async prefetch(names: string[]): Promise<void> {
    const all = new Set<string>();
    const add = (n: string) => {
      const key = n.toLowerCase();
      if (all.has(key) || !this.lock.packages[key]) return;
      all.add(key);
      for (const d of this.lock.packages[key].depends) add(d);
    };
    for (const n of names) add(n);
    const files = [...all].map((n) => this.lock.packages[n].file_name);
    for (let i = 0; i < files.length; i += 4) await Promise.all(files.slice(i, i + 4).map((f) => this.file(f)));
  }

  private async load(name: string): Promise<Buffer> {
    for (const dir of [npmPyodide, CACHE_DIR]) {
      const path = join(dir, name);
      if (existsSync(path)) return readFileSync(path);
    }
    const expected = this.sha.get(name);
    for (let attempt = 1; ; attempt++) {
      try {
        const response = await fetch(`${PYODIDE_INDEX_URL}${name}`, { signal: AbortSignal.timeout(120_000) });
        if (response.status === 404) throw new HttpError(404);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const body = Buffer.from(await response.arrayBuffer());
        const got = createHash('sha256').update(body).digest('hex');
        if (expected && got !== expected) throw new Error(`sha256 ${got.slice(0, 12)}… не совпадает с pyodide-lock.json`);
        mkdirSync(CACHE_DIR, { recursive: true });
        writeFileSync(join(CACHE_DIR, name), body);
        network.downloaded++;
        return body;
      } catch (error) {
        if (error instanceof HttpError || attempt === DOWNLOAD_ATTEMPTS) throw error;
        const pause = 2 ** attempt;
        const message = `скачивание ${name}: попытка ${attempt} не удалась (${(error as Error).message}) — повтор через ${pause} с`;
        network.retries.push(message);
        warn('сеть', message);
        await new Promise((r) => setTimeout(r, pause * 1000));
      }
    }
  }
}

class HttpError extends Error {
  status: number;
  constructor(status: number) {
    super(`HTTP ${status}`);
    this.status = status;
  }
}

const TYPES: Record<string, string> = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.wasm': 'application/wasm', '.json': 'application/json' };

/**
 * Сервер проверки: страница, данные, dist/ и зеркало. /__mirror/_astro/… — файлы сборки, в которых адрес
 * Pyodide на jsDelivr заменён на /__pyodide/ этого сервера (больше в них ничего не меняется).
 */
function serve(lessonTimeout: number, tasks: Task[], lessons: unknown[], mirror: PyodideMirror): Promise<{ url: string; close: () => void }> {
  const worker = readdirSync(join(dist, '_astro')).find((n) => /^worker-.*\.js$/.test(n));
  if (!worker) throw new Error('в dist/ нет воркера — сначала npm run build');
  if (!read(join(dist, '_astro', worker)).includes(PYODIDE_INDEX_URL)) throw new Error(`в воркере нет адреса ${PYODIDE_INDEX_URL} — зеркалу нечего подменять`);
  const routes: Record<string, [string, string]> = {
    '/__check/page.html': ['text/html; charset=utf-8', read(join(root, 'scripts', 'browser-check.html'))],
    '/__check/worker': ['application/json', JSON.stringify({ cdn: `/_astro/${worker}`, mirror: `/__mirror/_astro/${worker}` })],
    '/__check/tasks.json': ['application/json', JSON.stringify(tasks)],
    '/__check/lessons.json': ['application/json', JSON.stringify(lessons)],
    '/__check/config.json': [
      'application/json',
      JSON.stringify({ timeoutFactor: PYTHON_CONFIG.timeoutFactor, defaultTestTimeout: PYTHON_CONFIG.defaultTestTimeout, probes: PROBES, lessonTimeout }),
    ],
  };
  let origin = '';
  const server = createServer(async (req, res) => {
    const path = new URL(req.url ?? '/', 'http://x').pathname;
    const route = routes[path];
    if (route) {
      res.setHeader('Content-Type', route[0]);
      res.end(route[1]);
      return;
    }
    if (path.startsWith('/__pyodide/')) {
      try {
        const body = await mirror.file(decodeURIComponent(path.slice('/__pyodide/'.length)));
        res.setHeader('Content-Type', TYPES[extname(path)] ?? 'application/octet-stream');
        res.setHeader('Cache-Control', 'public, max-age=31536000, immutable'); // как у jsDelivr: версия в адресе
        res.end(body);
        network.served++;
      } catch (error) {
        res.statusCode = error instanceof HttpError ? error.status : 502;
        res.end(String(error));
      }
      return;
    }
    const mirrored = path.startsWith('/__mirror/');
    const file = join(dist, decodeURIComponent(mirrored ? path.slice('/__mirror'.length) : path));
    if (!file.startsWith(dist) || !existsSync(file) || statSync(file).isDirectory()) {
      res.statusCode = 404;
      res.end();
      return;
    }
    res.setHeader('Content-Type', TYPES[extname(file)] ?? 'application/octet-stream');
    if (mirrored && extname(file) === '.js') res.end(read(file).replaceAll(PYODIDE_INDEX_URL, `${origin}/__pyodide/`));
    else res.end(readFileSync(file));
  });
  return new Promise((resolve) =>
    server.listen(0, '127.0.0.1', () => {
      origin = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
      resolve({ url: origin, close: () => server.close() });
    }),
  );
}

// ─── Вкладки ────────────────────────────────────────────────────────────────

interface CheckResult {
  probes: Record<string, Record<string, string>>;
  tasks: { id: string; variant: string; status: string }[];
  /** status 'lesson-timeout' — урок не уложился в лимит: cell/kind — последняя начатая ячейка, seconds — сколько прошло. */
  lessons: { id: string; cell: string; status: string; kind?: string; seconds?: number; limit?: number }[];
  restarts: string[]; // воркер Python запустился не с первого раза (browser-check.html: startPython)
  userAgent: string;
  error?: string;
}

/** Пачка: задачи и уроки одной вкладки или пробы глубины (имена из PROBES). */
interface Batch {
  label: string;
  ids: string[];
  probes: string[];
}

function warn(title: string, message: string): void {
  console.log(`  · ${message}`);
  if (inCI) console.log(`::warning title=${title}::${message.replaceAll('\n', '%0A')}`);
}

function annotate(title: string, message: string): void {
  if (inCI) console.log(`::error title=${title}::${message.replaceAll('\n', '%0A')}`);
}

/**
 * Одна вкладка в новом контексте. Журнал страницы (console, в том числе воркеров) собирается по мере
 * выполнения: если процесс страницы упадёт, в нём видно, что выполнялось.
 */
async function runPage(browser: Browser, url: string, batch: Batch, journal: string[]): Promise<CheckResult> {
  const started = performance.now();
  const note = (s: string) => journal.push(`${((performance.now() - started) / 1000).toFixed(1).padStart(7)} с  ${s}`);
  const context = await browser.newContext();
  try {
    const page = await context.newPage();
    page.on('console', (m) => note(m.text().replace(/^\[check\] /, '')));
    const gone = new Promise<never>((_, reject) => {
      page.on('crash', () => reject(new Error('процесс страницы упал (crash)')));
      page.on('close', () => reject(new Error(browser.isConnected() ? 'вкладка закрылась' : 'браузер отключился')));
      page.on('pageerror', (e) => reject(new Error(`ошибка страницы проверки: ${e.message}`)));
    });
    gone.catch(() => {});
    const query = new URLSearchParams({ probes: batch.probes.join(','), only: batch.ids.join(',') });
    await Promise.race([page.goto(`${url}/__check/page.html?${query}`), gone]);
    await Promise.race([page.waitForFunction(() => (window as unknown as { __result?: unknown }).__result, null, { timeout: PAGE_TIMEOUT * 1000, polling: 500 }), gone]);
    return (await page.evaluate(() => (window as unknown as { __result: unknown }).__result)) as CheckResult;
  } catch (error) {
    note(`✗ ${String(error).split('\n')[0]}`);
    throw error;
  } finally {
    await context.close().catch(() => {});
  }
}

const STEP_KIND: Record<string, string> = { start: 'запуске Python', check: 'упражнении', cell: 'ячейке', quiz: 'вопросе' };

function lessonProblem(browser: string, l: CheckResult['lessons'][number]): string {
  if (l.status !== 'lesson-timeout') return `урок ${l.id}, ячейка ${l.cell}: ${l.status}`;
  const limit = l.limit! % 60 ? `${l.limit} с` : `${l.limit! / 60} мин`;
  const where = l.kind === 'start' ? STEP_KIND.start : `${STEP_KIND[l.kind!] ?? 'ячейке'} «${l.cell}»`;
  return `${browser}: урок ${l.id} не уложился в ${limit} — остановлен на ${where} (последняя начатая), прошло ${l.seconds} с`;
}

/** Значение опции: --name значение или --name=значение; null — опции нет. */
function option(argv: string[], name: string): string | null {
  const eq = argv.find((a) => a.startsWith(`${name}=`));
  if (eq) return eq.slice(name.length + 1);
  const i = argv.indexOf(name);
  return i >= 0 ? (argv[i + 1] ?? '') : null;
}

interface BrowserReport {
  name: string;
  seconds: number;
  pages: number;
  retries: string[];
  restarts: string[];
  problems: string[];
  tasks: string;
  lessons: string;
}

/** Все пачки одного браузера: pages вкладок параллельно, упавшая вкладка — один повтор пачки. */
async function checkBrowser(name: string, url: string, batches: Batch[], pages: number): Promise<BrowserReport> {
  const started = performance.now();
  let browser = await engines[name].launch();
  let relaunch: Promise<Browser> | null = null;
  const alive = async () => {
    if (browser.isConnected()) return browser;
    relaunch ??= engines[name].launch().then((b) => ((browser = b), (relaunch = null), b));
    return relaunch;
  };
  const results: CheckResult[] = [];
  const retries: string[] = [];
  const errors: string[] = [];
  const log: string[] = [];
  const queue = [...batches];
  await Promise.all(
    Array.from({ length: Math.min(pages, batches.length) }, async () => {
      for (let batch = queue.shift(); batch; batch = queue.shift()) {
        for (let attempt = 1; ; attempt++) {
          const journal: string[] = [];
          try {
            results.push(await runPage(await alive(), url, batch, journal));
            log.push(`── ${batch.label}${attempt > 1 ? `, попытка ${attempt}` : ''}`, ...journal);
            break;
          } catch (error) {
            log.push(`── ${batch.label}, попытка ${attempt} — ✗`, ...journal);
            const where = journal.filter((l) => / · |урок |задача /.test(l)).slice(-1)[0]?.trim() ?? 'до первой задачи';
            const message = `${batch.label}: ${String(error).split('\n')[0]}; последнее в журнале: ${where}`;
            if (attempt === 2) {
              errors.push(`${message}\nконец журнала:\n${journal.slice(-25).join('\n')}`);
              break;
            }
            retries.push(message);
            warn(name, `повтор — ${message}`);
          }
        }
      }
    }),
  );
  await browser.close().catch(() => {});
  mkdirSync(LOG_DIR, { recursive: true });
  writeFileSync(join(LOG_DIR, `${name}.log`), `${log.join('\n')}\n`);

  const seconds = Math.round((performance.now() - started) / 1000);
  const userAgent = results.find((r) => r.userAgent)?.userAgent ?? name;
  console.log(`\n${name} — ${userAgent} (${seconds} с, вкладок ${batches.length}, параллельно ${Math.min(pages, batches.length)})`);
  const problems = [...errors];
  const probes: CheckResult['probes'] = Object.assign({}, ...results.map((r) => r.probes));
  if (Object.keys(probes).length) {
    const summary: string[] = [];
    for (const probe of Object.keys(PROBES).filter((n) => probes[n])) {
      const entries = Object.entries(probes[probe]);
      const last = entries[entries.length - 1];
      const works = entries.filter(([, o]) => o === 'ok').map(([d]) => d).pop() ?? '—';
      const line = `${probe}: работает до ${works}${last && last[1] !== 'ok' ? `, на ${last[0]} — ${last[1]}` : ''}`;
      console.log(`  · ${line}`);
      summary.push(line);
    }
    if (inCI) console.log(`::notice title=${name}::${[userAgent, ...summary].join('%0A')}`);
    if (probes.plain?.['990'] !== 'ok') problems.push('обычная рекурсия на 990 уровней не работает');
    if (probes.plain?.['5000'] !== 'RecursionError') problems.push('рекурсия на 5000 уровней должна давать RecursionError, а не ронять Python');
    if (probes.cache?.[String(MEMO_DEPTH)] !== 'ok') problems.push(`рекурсия через @cache не выдерживает ${MEMO_DEPTH} уровней — уменьшите MEMO_DEPTH и тесты`);
  }
  const lostProbes = batches.flatMap((b) => b.probes).filter((n) => !probes[n]);
  if (lostProbes.length && !errors.length) problems.push(`пробы глубины не выполнены: ${lostProbes.join(', ')}`);
  const restarts = results.flatMap((r) => r.restarts);
  for (const restart of restarts) warn(name, `повторный запуск Python — ${restart}`);
  const tasks = results.flatMap((r) => r.tasks);
  const lessons = results.flatMap((r) => r.lessons);
  for (const r of results) if (r.error) problems.push(`ошибка страницы проверки: ${r.error}`);
  for (const t of tasks) if (t.status !== 'passed') problems.push(`${t.id} ${t.variant}: ${t.status}`);
  for (const l of lessons) if (l.status !== 'passed') problems.push(lessonProblem(name, l));
  const expected = batches.flatMap((b) => b.ids);
  const seen = new Set([...tasks.map((t) => t.id), ...lessons.map((l) => l.id)]);
  const missing = expected.filter((id) => !seen.has(id));
  if (missing.length && !errors.length) problems.push(`не выполнены: ${missing.join(', ')}`);

  const taskIds = [...new Set(tasks.map((t) => t.id))];
  const lessonIds = [...new Set(lessons.map((l) => l.id))];
  const goodLessons = lessonIds.filter((id) => lessons.every((l) => l.id !== id || l.status === 'passed'));
  const stopped = lessons.filter((l) => l.status === 'lesson-timeout').length;
  const taskLine = `прошли ${tasks.filter((t) => t.status === 'passed').length} из ${tasks.length} (задач ${taskIds.length})`;
  const lessonLine = `прошли ${goodLessons.length} из ${lessonIds.length} (ячеек ${lessons.length - stopped}${stopped ? `, остановлено по времени: ${stopped}` : ''})`;
  console.log(`  Задачи: ${taskLine}`);
  console.log(`  Уроки курсов: ${lessonLine}`);
  console.log(`  Повторов: ${retries.length + restarts.length} (вкладок ${retries.length}, запусков Python ${restarts.length})`);
  for (const p of problems) {
    console.log(`  ✗ ${p}`);
    annotate(name, p);
  }
  return { name, seconds, pages: batches.length, retries, restarts, problems, tasks: taskLine, lessons: lessonLine };
}

async function main(argv: string[]): Promise<number> {
  const valued = ['--only', '--shard', '--pages', '--lesson-timeout'];
  const onlyArg = option(argv, '--only') ?? process.env.CHECK_ONLY ?? '';
  const only = onlyArg ? new Set(onlyArg.split(',')) : null;
  const [shard, shards] = (option(argv, '--shard') ?? '1/1').split('/').map(Number);
  // по вкладке на ядро: раннер macOS (3 ядра) с тремя вкладками проходит WebKit за ~3–5 мин, с двумя — за ~6–7
  const pages = Number(option(argv, '--pages') ?? Math.min(8, availableParallelism()));
  const lessonTimeout = Number(option(argv, '--lesson-timeout') ?? LESSON_TIMEOUT);
  if (!(shards >= 1 && shard >= 1 && shard <= shards && pages >= 1)) throw new Error('--shard k/n: 1 ≤ k ≤ n; --pages — не меньше 1');
  // пробы — только в части 1 (--probes в CI передаётся всем частям)
  const probes = shard === 1 && (argv.includes('--probes') || (!argv.includes('--no-probes') && !only));
  const names = argv.filter((a, i) => !a.startsWith('--') && !valued.includes(argv[i - 1]));
  const chosen = names.length ? names : Object.keys(engines);
  for (const n of chosen) if (!engines[n]) throw new Error(`неизвестный браузер ${n}: ${Object.keys(engines).join(', ')}`);

  // Часть: список «задачи, затем уроки» (выбранные --only), элемент i — в часть i mod n; дальше — пачки по BATCH
  const tasks = loadTasks();
  const lessons = loadLessons();
  const all = [...tasks, ...lessons];
  if (only) {
    const unknown = [...only].filter((id) => !all.some((x) => x.id === id));
    if (unknown.length) console.log(`  · нет таких задач и уроков (удалены?): ${unknown.join(', ')}`);
  }
  const mine = all.filter((x) => !only || only.has(x.id)).filter((_, i) => i % shards === shard - 1);
  // пробы — каждая своей вкладкой: в них воркеры падают от переполнения стека намеренно
  const batches: Batch[] = probes ? Object.keys(PROBES).map((name) => ({ label: `проба ${name}`, ids: [], probes: [name] })) : [];
  // пачек — кратно числу вкладок, иначе в конце одна вкладка работает, а остальные ждут
  const count = Math.min(mine.length, Math.ceil(Math.ceil(mine.length / BATCH) / pages) * pages);
  for (let b = 0; b < count; b++) {
    // элементы через один по всем пачкам: в каждой и задачи, и уроки — пачки примерно равны по времени
    const ids = mine.filter((_, i) => i % count === b).map((x) => x.id);
    batches.push({ label: `вкладка ${b + 1}/${count} (${ids[0]} … ${ids.at(-1)})`, ids, probes: [] });
  }
  console.log(
    `Часть ${shard} из ${shards}: задач и уроков ${mine.length}${only ? ` (выбрано ${only.size})` : ''}, вкладок ${count}${probes ? ' + пробы глубины' : ''}, параллельно ${pages}`,
  );
  if (!batches.length) {
    console.log('Проверять нечего');
    return 0;
  }

  const mirror = new PyodideMirror();
  const t0 = performance.now();
  const needed = new Set(mine.flatMap((x) => x.packages));
  try {
    await mirror.prefetch([...needed]);
  } catch (error) {
    const message = `пакеты Pyodide не скачались за ${DOWNLOAD_ATTEMPTS} попыток (около минуты): ${(error as Error).message}`;
    console.log(`✗ ${message}`);
    annotate('сеть', message);
    return 1;
  }
  console.log(`Пакеты Pyodide (${[...needed].join(', ') || 'без пакетов'}): готовы за ${((performance.now() - t0) / 1000).toFixed(0)} с, скачано ${network.downloaded}`);

  const { url, close } = await serve(lessonTimeout, tasks, lessons, mirror);
  const reports: BrowserReport[] = [];
  try {
    for (const name of chosen) reports.push(await checkBrowser(name, url, batches, pages));
  } finally {
    close();
  }
  const failed = reports.some((r) => r.problems.length);
  console.log(`\nЗеркало Pyodide: отдано файлов ${network.served}, скачано с jsDelivr ${network.downloaded}, повторов скачивания ${network.retries.length}`);
  if (process.env.GITHUB_STEP_SUMMARY) {
    const row = (r: BrowserReport) =>
      `| ${r.name} | ${r.problems.length ? '✗' : '✓'} | ${r.seconds} с | ${r.tasks} | ${r.lessons} | ${r.retries.length + r.restarts.length} |`;
    const lines = [
      `### Браузеры, часть ${shard} из ${shards}`,
      '',
      '| Браузер | Итог | Время | Задачи | Уроки | Повторы |',
      '| --- | --- | --- | --- | --- | --- |',
      ...reports.map(row),
      '',
      ...reports.flatMap((r) => [...r.retries, ...r.restarts].map((m) => `- повтор, ${r.name}: ${m}`)),
      ...network.retries.map((m) => `- повтор, сеть: ${m}`),
      '',
    ];
    appendFileSync(process.env.GITHUB_STEP_SUMMARY, `${lines.join('\n')}\n`);
  }
  console.log(failed ? '\n✗ Есть ошибки' : '\n✓ Всё в порядке');
  return failed ? 1 : 0;
}

process.exitCode = await main(process.argv.slice(2));
