/**
 * Проверка Python в настоящих браузерах: Chromium, Firefox и WebKit (движок Safari) через Playwright.
 * Запускает production-сборку сайта (dist/, сначала npm run build) — тот же воркер, что на страницах задач.
 *
 *   node scripts/validate_browsers.ts                      # все три браузера
 *   node scripts/validate_browsers.ts webkit firefox       # выбранные
 *   node scripts/validate_browsers.ts --only ga-tile-ways,ga-typo-distance   # выбранные задачи и уроки (по id)
 *   node scripts/validate_browsers.ts webkit --shard 2/3   # часть 2 из 3 (как в CI): каждая n-я задача и урок
 *   node scripts/validate_browsers.ts chromium --pages 2   # две вкладки браузера параллельно
 *   node scripts/validate_browsers.ts --timings t.json     # время каждой задачи и урока — в файл
 *
 * Пробы глубины выполняет только часть 1, отдельной вкладкой (--no-probes — без них). --only можно задать и
 * переменной CHECK_ONLY. Упала вкладка — оставшиеся задачи и уроки выполняются на новой (один повтор).
 *
 * Зачем, если есть scripts/validate_pyodide.ts: стек WebAssembly в браузерах разный, и рекурсия, которая идёт
 * через C (functools.cache / lru_cache, sum(генератор), map), в Safari выдерживает всего ~60 уровней, а в
 * Node.js — сотни. Проверка выполняет все эталоны и альтернативные эталоны в каждом браузере и пробы глубины:
 *   plain   — обычная рекурсия: 990 уровней работают, 5000 дают RecursionError (а не падение Python);
 *   cache   — рекурсия через @cache: должна выдерживать MEMO_DEPTH уровней — это бюджет глубины для тестов
 *             задач, где подходит рекурсия с запоминанием (docs/ARCHITECTURE.md, «Приёмы в тестах»);
 *   остальное — для отчёта: где именно в этом браузере кончается стек.
 * Нужны браузеры Playwright: npx playwright install chromium firefox webkit (в CI — с --with-deps).
 */
import { existsSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { createServer } from 'node:http';
import type { AddressInfo } from 'node:net';
import { extname, join } from 'node:path';
import { chromium, firefox, webkit, type Browser, type BrowserType } from 'playwright';
import { parse as parseToml } from 'smol-toml';
import { bundleFooter } from '../src/lib/bundle.ts';
import { courseLessons, lessonFiles, lessonPackages, loadCourses } from '../src/lib/courses/load.ts';
import { PYTHON_CONFIG } from '../src/lib/python/config.ts';

/** Глубина рекурсии с запоминанием, которую тесты задач могут требовать (Safari падает на ~70). */
const MEMO_DEPTH = 40;

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
const read = (path: string) => readFileSync(path, 'utf-8');
const dirs = (path: string) => readdirSync(path).filter((n) => !/^[._]/.test(n) && statSync(join(path, n)).isDirectory()).sort();
const engines: Record<string, BrowserType> = { chromium, firefox, webkit };

function loadTasks() {
  const runner = read(join(root, 'runtime', 'runner.py'));
  const tasks = [];
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

function serve(tasks: unknown[], lessons: unknown[]): Promise<{ url: string; close: () => void }> {
  const worker = readdirSync(join(dist, '_astro')).find((n) => /^worker-.*\.js$/.test(n));
  if (!worker) throw new Error('в dist/ нет воркера — сначала npm run build');
  const routes: Record<string, [string, string]> = {
    '/__check/page.html': ['text/html; charset=utf-8', read(join(root, 'scripts', 'browser-check.html'))],
    '/__check/worker': ['text/plain', worker],
    '/__check/tasks.json': ['application/json', JSON.stringify(tasks)],
    '/__check/lessons.json': ['application/json', JSON.stringify(lessons)],
    '/__check/config.json': [
      'application/json',
      JSON.stringify({ timeoutFactor: PYTHON_CONFIG.timeoutFactor, defaultTestTimeout: PYTHON_CONFIG.defaultTestTimeout, probes: PROBES }),
    ],
  };
  const server = createServer((req, res) => {
    const path = new URL(req.url ?? '/', 'http://x').pathname;
    const route = routes[path];
    if (route) {
      res.setHeader('Content-Type', route[0]);
      res.end(route[1]);
      return;
    }
    const file = join(dist, decodeURIComponent(path));
    if (!file.startsWith(dist) || !existsSync(file) || statSync(file).isDirectory()) {
      res.statusCode = 404;
      res.end();
      return;
    }
    res.setHeader('Content-Type', extname(file) === '.js' ? 'text/javascript' : 'application/octet-stream');
    res.end(readFileSync(file));
  });
  return new Promise((resolve) =>
    server.listen(0, '127.0.0.1', () => resolve({ url: `http://127.0.0.1:${(server.address() as AddressInfo).port}`, close: () => server.close() })),
  );
}

interface CheckResult {
  probes: Record<string, Record<string, string>>;
  tasks: { id: string; variant: string; status: string }[];
  lessons: { id: string; cell: string; status: string }[];
  restarts?: string[]; // воркер Python запустился не с первого раза (browser-check.html: startPython)
  timings?: { probes: number; items: { kind: 'task' | 'lesson'; id: string; seconds: number }[] };
  userAgent: string;
  error?: string;
}

function annotate(title: string, message: string): void {
  if (process.env.GITHUB_ACTIONS === 'true') console.log(`::error title=${title}::${message.replaceAll('\n', '%0A')}`);
}


function warn(title: string, message: string): void {
  console.log(`  · ${message}`);
  if (process.env.GITHUB_ACTIONS === 'true') console.log(`::warning title=${title}::${message.replaceAll('\n', '%0A')}`);
}

/** Значение опции: --name значение или --name=значение. */
function option(argv: string[], name: string): string | null {
  const eq = argv.find((a) => a.startsWith(`${name}=`));
  if (eq) return eq.slice(name.length + 1);
  const i = argv.indexOf(name);
  return i >= 0 ? (argv[i + 1] ?? '') : null;
}

type Item = { kind: 'task' | 'lesson'; id: string; seconds: number; rows: { id: string; status: string; variant?: string; cell?: string }[] };

/**
 * Одна вкладка браузера: выполняет ids (null — только пробы). Готовые задачи и уроки приходят сразу (__itemDone),
 * поэтому, если вкладка упала (WebKit в CI изредка теряет процесс страницы: «Target page closed»), оставшиеся
 * выполняются на новой — один повтор; в лог (и ::warning в CI) — на какой задаче или ячейке урока это случилось.
 */
async function runTab(getBrowser: () => Promise<Browser>, url: string, name: string, ids: string[] | null, done: Item[]): Promise<Partial<CheckResult>> {
  let left = ids;
  let current = ids ? 'запуске' : 'пробах глубины'; // последняя начатая задача (вариант) или урок (ячейка)
  for (let attempt = 1; ; attempt++) {
    const context = await (await getBrowser()).newContext();
    try {
      const page = await context.newPage();
      await page.exposeFunction('__step', (where: string) => (current = where));
      await page.exposeFunction('__itemDone', (item: Item) => {
        done.push(item);
        if (left) left = left.filter((id) => id !== item.id);
      });
      const query = new URLSearchParams(left ? { probes: '0', only: left.join(',') } : { probes: '1', items: '0' });
      await page.goto(`${url}/__check/page.html?${query}`);
      await page.waitForFunction(() => (window as unknown as { __result?: unknown }).__result, null, { timeout: 30 * 60_000 });
      return (await page.evaluate(() => (window as unknown as { __result: unknown }).__result)) as CheckResult;
    } catch (error) {
      const message = `вкладка упала на ${current}, попытка ${attempt} (${String(error).split('\n')[0]})`;
      if (attempt === 2) return { error: message };
      if (left && !left.length) return {};
      warn(name, `${message} — повтор${left ? `, осталось задач и уроков: ${left.length}` : ''}`);
    } finally {
      await context.close().catch(() => {});
    }
  }
}

async function main(argv: string[]): Promise<number> {
  const valued = ['--only', '--shard', '--pages', '--timings'];
  const onlyArg = option(argv, '--only') ?? process.env.CHECK_ONLY ?? '';
  const only = onlyArg ? onlyArg.split(',') : null;
  const [shard, shards] = (option(argv, '--shard') ?? '1/1').split('/').map(Number);
  const pages = Number(option(argv, '--pages') ?? 1);
  const timingsPath = option(argv, '--timings');
  const withProbes = shard === 1 && !argv.includes('--no-probes');
  if (!(shards >= 1 && shard >= 1 && shard <= shards && pages >= 1)) throw new Error('--shard k/n: 1 ≤ k ≤ n; --pages — не меньше 1');
  const names = argv.filter((a, i) => !a.startsWith('--') && !valued.includes(argv[i - 1]));
  const chosen = names.length ? names : Object.keys(engines);

  // Части: список «задачи, затем уроки» (выбранные --only), элемент i — в части i mod n; внутри части — по вкладкам
  const tasks = loadTasks();
  const lessons = loadLessons();
  const selected = [...tasks, ...lessons].map((x) => x.id).filter((id) => !only || only.includes(id));
  const slot = (i: number) => i % (shards * pages);
  const tabs = Array.from({ length: pages }, (_, p) => selected.filter((_, i) => slot(i) === (shard - 1) * pages + p)).filter((ids) => ids.length);
  console.log(
    `Часть ${shard} из ${shards}: задач и уроков ${tabs.flat().length} из ${selected.length}, вкладок ${tabs.length}${withProbes ? ' + пробы глубины' : ''}` +
      (only ? ` · выбрано: ${onlyArg}` : ''),
  );

  const { url, close } = await serve(tasks, lessons);
  let failed = false;
  const timings: Record<string, unknown> = {};
  try {
    for (const name of chosen) {
      // браузер целиком тоже может упасть: следующая попытка вкладки запускает новый (один на все вкладки)
      let browser = engines[name].launch();
      const getBrowser = async () => {
        const current = await browser;
        if (current.isConnected()) return current;
        warn(name, 'браузер закрылся — запускаю заново');
        browser = engines[name].launch();
        return browser;
      };
      const started = performance.now();
      const done: Item[] = [];
      // пробы глубины — отдельной вкладкой параллельно с задачами (в CI ~70 с)
      const parts = await Promise.all([
        withProbes ? runTab(getBrowser, url, name, null, done) : Promise.resolve({} as Partial<CheckResult>),
        ...tabs.map((ids) => runTab(getBrowser, url, name, ids, done)),
      ]);
      await (await browser).close().catch(() => {});
      const seconds = ((performance.now() - started) / 1000).toFixed(0);
      const userAgent = parts.find((p) => p.userAgent)?.userAgent ?? '';
      console.log(`\n${name} — ${userAgent} (${seconds} с)`);
      const probeSeconds = parts[0].timings?.probes ?? 0;
      const sum = (kind: string) => done.filter((t) => t.kind === kind).reduce((a, t) => a + t.seconds, 0).toFixed(0);
      console.log(`  Время: пробы ${probeSeconds.toFixed(0)} с · задачи ${sum('task')} с · уроки ${sum('lesson')} с (сумма по вкладкам)`);
      const slowest = [...done].sort((a, b) => b.seconds - a.seconds).slice(0, 5);
      if (slowest.length) console.log(`  Дольше всего: ${slowest.map((t) => `${t.id} ${t.seconds.toFixed(0)} с`).join(', ')}`);
      timings[name] = { seconds: Number(seconds), probes: probeSeconds, items: done.map(({ kind, id, seconds: s }) => ({ kind, id, seconds: s })) };
      for (const restart of parts.flatMap((p) => p.restarts ?? [])) warn(name, `повторный запуск Python — ${restart}`);
      const problems: string[] = parts.flatMap((p) => (p.error ? [p.error] : []));
      const probeResults = parts[0].probes ?? {};
      const summary: string[] = [];
      for (const [probe, outcomes] of Object.entries(probeResults)) {
        const entries = Object.entries(outcomes);
        const last = entries[entries.length - 1];
        const works = entries.filter(([, o]) => o === 'ok').map(([d]) => d).pop() ?? '—';
        const line = `${probe}: работает до ${works}${last && last[1] !== 'ok' ? `, на ${last[0]} — ${last[1]}` : ''}`;
        console.log(`  · ${line}`);
        summary.push(line);
      }
      if (process.env.GITHUB_ACTIONS === 'true' && summary.length) console.log(`::notice title=${name}::${[userAgent, ...summary].join('%0A')}`);
      if (withProbes && !parts[0].error) {
        if (probeResults.plain?.['990'] !== 'ok') problems.push('обычная рекурсия на 990 уровней не работает');
        if (probeResults.plain?.['5000'] !== 'RecursionError') problems.push('рекурсия на 5000 уровней должна давать RecursionError, а не ронять Python');
        if (probeResults.cache?.[String(MEMO_DEPTH)] !== 'ok') problems.push(`рекурсия через @cache не выдерживает ${MEMO_DEPTH} уровней — уменьшите MEMO_DEPTH и тесты`);
      }
      const doneIds = new Set(done.map((d) => d.id));
      const missing = tabs.flat().filter((id) => !doneIds.has(id));
      if (missing.length) problems.push(`не выполнены: ${missing.join(', ')}`);
      for (const item of done) {
        for (const r of item.rows) {
          if (r.status === 'passed') continue;
          problems.push(item.kind === 'task' ? `${r.id} ${r.variant}: ${r.status}` : `урок ${r.id}, ячейка ${r.cell}: ${r.status}`);
        }
      }
      const of = (kind: string) => done.filter((d) => d.kind === kind);
      const good = (kind: string) => of(kind).filter((d) => d.rows.every((r) => r.status === 'passed')).length;
      const rows = (kind: string) => of(kind).reduce((a, d) => a + d.rows.length, 0);
      console.log(`  Задачи: прошли ${good('task')} из ${of('task').length} (вариантов ${rows('task')})`);
      console.log(`  Уроки курсов: прошли ${good('lesson')} из ${of('lesson').length} (ячеек ${rows('lesson')})`);
      for (const p of problems) {
        console.log(`  ✗ ${p}`);
        annotate(name, p);
      }
      failed ||= problems.length > 0;
    }
  } finally {
    close();
  }
  if (timingsPath) writeFileSync(timingsPath, `${JSON.stringify({ shard: `${shard}/${shards}`, pages, only: onlyArg || null, browsers: timings }, null, 2)}\n`);
  console.log(failed ? '\n✗ Есть ошибки' : '\n✓ Всё в порядке');
  return failed ? 1 : 0;
}

process.exitCode = await main(process.argv.slice(2));
