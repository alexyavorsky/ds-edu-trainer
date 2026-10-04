/**
 * Диагностика сбоя JavaScriptCore (docs/ARCHITECTURE.md, «CI», «Почему падал WebKit»): тысячи запусков воркера
 * Pyodide в браузере — частота сбоев запуска. Не входит в CI; запускать при обновлении Playwright (новый WebKit),
 * локально или временным workflow на macos-latest (там сбой и проявляется: ~0,1–0,3 % запусков).
 *
 *   node scripts/stress_webkit.ts --minutes 25 --pages 3          # 25 минут, три вкладки (как раннер)
 *   node scripts/stress_webkit.ts --starts 3000 --pages 6         # заданное число запусков
 *   [--batch 25] [--term-delay мс] [--delay мс] [--browser webkit|chromium|firefox] [--packages numpy,pandas]
 *
 * Запуск: new Worker (воркер сайта, Pyodide с зеркала из npm-пакета) → ready → print(1) → terminate; --batch
 * запусков на вкладку (новый контекст — новый процесс страницы). Сбой печатается сразу, в конце — итог.
 * Нужна сборка dist/ (npm run build).
 */
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import type { AddressInfo } from 'node:net';
import { extname, join } from 'node:path';
import { chromium, firefox, webkit } from 'playwright';
import { PYODIDE_INDEX_URL } from '../src/lib/python/config.ts';

const opt = (n: string, d: string) => (process.argv.includes(n) ? process.argv[process.argv.indexOf(n) + 1] : d);
const pages = Number(opt('--pages', '3'));
const starts = Number(opt('--starts', '300'));
const delay = Number(opt('--delay', '0'));
const termDelay = Number(opt('--term-delay', '0'));
const packages = opt('--packages', '');
const batch = Number(opt('--batch', '25'));
const minutes = Number(opt('--minutes', '0'));
const engine = { chromium, firefox, webkit }[opt('--browser', 'webkit')]!;
const root = join(import.meta.dirname, '..');
const dist = join(root, 'dist');
const npm = join(root, 'node_modules', 'pyodide');
const cache = process.env.PYODIDE_CACHE || join(root, '.pyodide-cache');
const worker = readdirSync(join(dist, '_astro')).find((n) => /^worker-.*\.js$/.test(n))!;
const types: Record<string, string> = { '.js': 'text/javascript', '.mjs': 'text/javascript', '.wasm': 'application/wasm', '.json': 'application/json' };

const page = `<!doctype html><meta charset="utf-8"><script type="module">
const p = new URLSearchParams(location.search); const n = +p.get('n'), delay = +p.get('delay'), termDelay = +p.get('td'), pk = p.get('pk') ? p.get('pk').split(',') : [];
const stats = { starts: 0, ok: 0, loadError: [], crash: [], timeout: 0 };
for (let i = 0; i < n; i++) {
  const w = new Worker('/__mirror/_astro/${worker}', { type: 'module' });
  stats.starts++;
  const r = await new Promise((res) => {
    const t = setTimeout(() => res({ k: 'timeout' }), 60000);
    w.onerror = (e) => { e.preventDefault(); clearTimeout(t); res({ k: 'crash', m: e.message }); };
    w.onmessage = (e) => {
      const m = e.data;
      if (m.type === 'ready') w.postMessage({ type: 'run', request: { kind: 'example', packages: pk, setup: '', code: 'print(1)', filename: 'x.py', cell: 'x', runId: 1 } });
      if (m.type === 'load-error') { clearTimeout(t); res({ k: 'loadError', m: m.message }); }
      if (m.type === 'fatal') { clearTimeout(t); res({ k: 'crash', m: m.message }); }
      if (m.type === 'done') { clearTimeout(t); res({ k: m.lines && m.lines[0] === '1' ? 'ok' : 'crash', m: JSON.stringify(m.error) }); }
      if (m.type === 'package-error') { clearTimeout(t); res({ k: 'crash', m: 'package-error ' + m.message }); }
    };
  });
  if (termDelay) await new Promise((r) => setTimeout(r, termDelay));
  w.terminate();
  if (r.k === 'ok') stats.ok++; else if (r.k === 'timeout') stats.timeout++; else { stats[r.k].push(i + ': ' + r.m); console.log('FAIL ' + r.k + ' #' + i + ' ' + r.m); }
  if (delay) await new Promise((r) => setTimeout(r, delay));
  if ((i + 1) % 100 === 0) console.log('PROGRESS ' + (i + 1));
}
window.__stats = stats;
</script>`;

const server = createServer((req, res) => {
  const path = new URL(req.url ?? '/', 'http://x').pathname;
  if (path === '/stress.html') { res.setHeader('Content-Type', 'text/html'); res.end(page); return; }
  if (path.startsWith('/__pyodide/')) {
    const name = path.slice(11);
    const f = [join(npm, name), join(cache, name)].find(existsSync);
    if (!f) { res.statusCode = 404; res.end(); return; }
    res.setHeader('Content-Type', types[extname(name)] ?? 'application/octet-stream');
    res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
    res.end(readFileSync(f)); return;
  }
  const mirrored = path.startsWith('/__mirror/');
  const file = join(dist, mirrored ? path.slice(9) : path);
  if (!existsSync(file) || statSync(file).isDirectory()) { res.statusCode = 404; res.end(); return; }
  res.setHeader('Content-Type', types[extname(file)] ?? 'application/octet-stream');
  res.end(mirrored && file.endsWith('.js') ? readFileSync(file, 'utf-8').replaceAll(PYODIDE_INDEX_URL, `http://127.0.0.1:${(server.address() as AddressInfo).port}/__pyodide/`) : readFileSync(file));
});
await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
const url = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
const browser = await engine.launch();
const t0 = performance.now();
const total = { starts: 0, ok: 0, loadError: [] as string[], crash: [] as string[], timeout: 0, pageCrash: 0 };
const deadline = minutes ? t0 + minutes * 60_000 : Infinity;
let budget = minutes ? Infinity : starts;
await Promise.all(Array.from({ length: pages }, async (_, k) => {
  while (performance.now() < deadline && budget > 0) {
    const n = Math.min(batch, budget);
    budget -= n;
    const ctx = await browser.newContext();
    const pg = await ctx.newPage();
    pg.on('console', (m) => /^FAIL/.test(m.text()) && console.log(`${new Date().toISOString().slice(11, 19)} [вкладка ${k}] ${m.text()}`));
    let crashed = false;
    pg.on('crash', () => (crashed = true));
    await pg.goto(`${url}/stress.html?n=${n}&delay=${delay}&td=${termDelay}&pk=${packages}`);
    const s = await pg.waitForFunction(() => (window as any).__stats, null, { timeout: 600_000, polling: 1000 }).then((h) => h.jsonValue()).catch(() => null);
    await ctx.close().catch(() => {});
    if (!s) { total.pageCrash++; total.starts += 1; console.log(`${new Date().toISOString().slice(11, 19)} [вкладка ${k}] FAIL page crash (crash=${crashed})`); continue; }
    total.starts += s.starts; total.ok += s.ok; total.timeout += s.timeout; total.loadError.push(...s.loadError); total.crash.push(...s.crash);
    if (Math.floor(total.starts / 500) !== Math.floor((total.starts - s.starts) / 500)) console.log(`${new Date().toISOString().slice(11, 19)} PROGRESS ${total.starts}`);
  }
}));
await browser.close(); server.close();
console.log(`ИТОГ: запусков ${total.starts}, ok ${total.ok}, load-error ${total.loadError.length}, crash ${total.crash.length}, timeout ${total.timeout}, падений вкладки ${total.pageCrash}, ${((performance.now() - t0) / 1000).toFixed(0)} с`);
for (const e of [...total.loadError, ...total.crash].slice(0, 10)) console.log('  ' + e);
