/**
 * Проверка Python в настоящих браузерах: Chromium, Firefox и WebKit (движок Safari) через Playwright.
 * Запускает production-сборку сайта (dist/, сначала npm run build) — тот же воркер, что на страницах задач.
 *
 *   node scripts/validate_browsers.ts                      # все три браузера
 *   node scripts/validate_browsers.ts webkit firefox       # выбранные
 *   node scripts/validate_browsers.ts --only ga-tile-ways,ga-typo-distance
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
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import type { AddressInfo } from 'node:net';
import { extname, join } from 'node:path';
import { chromium, firefox, webkit, type BrowserType } from 'playwright';
import { parse as parseToml } from 'smol-toml';
import { bundleFooter } from '../src/lib/bundle.ts';
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

function serve(): Promise<{ url: string; close: () => void }> {
  const worker = readdirSync(join(dist, '_astro')).find((n) => /^worker-.*\.js$/.test(n));
  if (!worker) throw new Error('в dist/ нет воркера — сначала npm run build');
  const routes: Record<string, [string, string]> = {
    '/__check/page.html': ['text/html; charset=utf-8', read(join(root, 'scripts', 'browser-check.html'))],
    '/__check/worker': ['text/plain', worker],
    '/__check/tasks.json': ['application/json', JSON.stringify(loadTasks())],
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
  userAgent: string;
  error?: string;
}

function annotate(title: string, message: string): void {
  if (process.env.GITHUB_ACTIONS === 'true') console.log(`::error title=${title}::${message.replaceAll('\n', '%0A')}`);
}

async function main(argv: string[]): Promise<number> {
  const onlyArg = argv.includes('--only') ? argv[argv.indexOf('--only') + 1] : '';
  const names = argv.filter((a, i) => !a.startsWith('--') && argv[i - 1] !== '--only');
  const chosen = names.length ? names : Object.keys(engines);
  const { url, close } = await serve();
  let failed = false;
  try {
    for (const name of chosen) {
      const browser = await engines[name].launch();
      const page = await (await browser.newContext()).newPage();
      const started = performance.now();
      await page.goto(`${url}/__check/page.html${onlyArg ? `?only=${onlyArg}` : ''}`);
      await page.waitForFunction(() => (window as unknown as { __result?: unknown }).__result, null, { timeout: 30 * 60_000 });
      const result = (await page.evaluate(() => (window as unknown as { __result: unknown }).__result)) as CheckResult;
      await browser.close();
      const seconds = ((performance.now() - started) / 1000).toFixed(0);
      console.log(`\n${name} — ${result.userAgent} (${seconds} с)`);
      if (result.error) {
        console.log(`  ✗ ${result.error}`);
        annotate(name, result.error);
        failed = true;
        continue;
      }
      for (const [probe, outcomes] of Object.entries(result.probes)) {
        const entries = Object.entries(outcomes);
        const last = entries[entries.length - 1];
        const works = entries.filter(([, o]) => o === 'ok').map(([d]) => d).pop() ?? '—';
        console.log(`  · ${probe}: работает до ${works}${last && last[1] !== 'ok' ? `, на ${last[0]} — ${last[1]}` : ''}`);
      }
      const problems: string[] = [];
      if (result.probes.plain?.['990'] !== 'ok') problems.push('обычная рекурсия на 990 уровней не работает');
      if (result.probes.plain?.['5000'] !== 'RecursionError') problems.push('рекурсия на 5000 уровней должна давать RecursionError, а не ронять Python');
      if (result.probes.cache?.[String(MEMO_DEPTH)] !== 'ok') problems.push(`рекурсия через @cache не выдерживает ${MEMO_DEPTH} уровней — уменьшите MEMO_DEPTH и тесты`);
      for (const t of result.tasks) if (t.status !== 'passed') problems.push(`${t.id} ${t.variant}: ${t.status}`);
      const passed = result.tasks.filter((t) => t.status === 'passed').length;
      console.log(`  Задачи: прошли ${passed} из ${result.tasks.length}`);
      for (const p of problems) {
        console.log(`  ✗ ${p}`);
        annotate(name, p);
      }
      failed ||= problems.length > 0;
    }
  } finally {
    close();
  }
  console.log(failed ? '\n✗ Есть ошибки' : '\n✓ Всё в порядке');
  return failed ? 1 : 0;
}

process.exitCode = await main(process.argv.slice(2));
