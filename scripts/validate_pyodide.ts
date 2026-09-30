/**
 * Проверка в Python для браузера: Pyodide из npm (та же версия, что грузит сайт) и то же ядро
 * (src/lib/python/engine.ts), те же таймауты (лимит теста × коэффициент браузера, лимит примера).
 *
 *   node scripts/validate_pyodide.ts                        # задачи и справочник
 *   node scripts/validate_pyodide.ts --tasks                # только задачи
 *   node scripts/validate_pyodide.ts --reference            # только справочник
 *   node scripts/validate_pyodide.ts ga-find-term numpy/broadcasting pandas   # выбранное: id задачи, статья, тема
 *   node scripts/validate_pyodide.ts --update               # переписать reference/browser.json
 *   node scripts/validate_pyodide.ts --report отчёт.md      # подробности: расхождения, время
 *
 * Задачи: эталон и альтернативные эталоны проходят все тесты, заготовка — нет. Время тестов эталона
 * сравнивается с лимитом браузера: больше половины — в отчёт.
 * Справочник: каждый пример выполняется; [raises] падает с нужной ошибкой. Что в браузере работает иначе,
 * записано в reference/browser.json (по нему сайт ставит пометки и отключает кнопку «Запустить»):
 *   differs      — вывод или график отличается от показанного (другая версия библиотеки);
 *   unavailable  — пример в браузере не работает (нет пакета или возможности), кнопка неактивна.
 * Расхождение с browser.json — ошибка: обновите файл (--update) и посмотрите, что изменилось.
 */
import { existsSync, readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import { availableParallelism } from 'node:os';
import { join, relative } from 'node:path';
import { parse as parseToml } from 'smol-toml';
import { bundleFooter } from '../src/lib/bundle.ts';
import { parseExamples, type ExampleCell } from '../src/lib/examples.ts';
import { MICROPIP_PACKAGES, PYODIDE_VERSION, PYTHON_CONFIG } from '../src/lib/python/config.ts';
import { examplePackages } from '../src/lib/python/packages.ts';
import type { ExampleDone, TaskDone, TestResult } from '../src/lib/python/protocol.ts';
import { NodePython, pool, type RunEnd } from './node-python.ts';

const root = join(import.meta.dirname, '..');
const read = (path: string) => readFileSync(path, 'utf-8');
const dirs = (path: string) =>
  existsSync(path) ? readdirSync(path).filter((n) => !/^[._]/.test(n) && statSync(join(path, n)).isDirectory()).sort() : [];
const STATUS_PATH = join(root, 'reference', 'browser.json');
const factor = PYTHON_CONFIG.timeoutFactor;

// ─── Задачи ─────────────────────────────────────────────────────────────────

interface Task {
  id: string;
  dir: string;
  type: string;
  packages: string[];
  footer: string;
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
        tasks.push({ id: meta.id, dir, type: meta.type, packages: bookMeta.packages ?? [], footer: bundleFooter(read(join(dir, 'tests.py')), runner) });
      }
    }
  }
  return tasks;
}

interface TaskReport {
  id: string;
  errors: string[];
  notes: string[];
  slow: { variant: string; test: string; elapsed: number; limit: number }[];
  total: number; // секунд на все тесты эталона
}

function describe(end: RunEnd): string {
  if (end.type === 'timeout') {
    const test = end.testIndex !== null ? end.tests?.[end.testIndex]?.title : null;
    return `завис (${end.seconds} с)${test ? ` на тесте «${test}»` : ' до тестов'}`;
  }
  if (end.type !== 'done') return `${end.type}: ${end.message}`;
  const d = end.data as TaskDone;
  if (d.phase !== 'tests') return `${d.phase}: ${d.error?.message} (строка ${d.error?.line})`;
  const failed = (d.results ?? []).filter((r) => r.status !== 'passed');
  return failed.map((r: TestResult) => `«${r.title}»: ${r.message}`).join('; ');
}

function passedAll(end: RunEnd): boolean {
  if (end.type !== 'done') return false;
  const d = end.data as TaskDone;
  return d.phase === 'tests' && (d.results ?? []).length > 0 && d.results!.every((r) => r.status === 'passed');
}

function taskJob(task: Task): () => (py: NodePython) => Promise<TaskReport> {
  return () => async (py) => {
    const report: TaskReport = { id: task.id, errors: [], notes: [], slow: [], total: 0 };
    const variants: [string, string][] = [['solution', read(join(task.dir, 'solution.py'))]];
    const altDir = join(task.dir, 'alt_solutions');
    if (existsSync(altDir)) {
      for (const f of readdirSync(altDir).filter((n) => n.endsWith('.py')).sort()) variants.push([`alt_solutions/${f}`, read(join(altDir, f))]);
    }
    for (const [name, code] of variants) {
      const end = await py.run({ kind: 'task', packages: task.packages, code, footer: task.footer });
      if (!passedAll(end)) {
        report.errors.push(`${name} не проходит в Pyodide: ${describe(end)}`);
        continue;
      }
      if (end.type !== 'done') continue;
      end.tests?.forEach((t, i) => {
        const elapsed = end.elapsed[i] ?? 0;
        const limit = t.timeout * factor;
        if (elapsed > limit / 2) report.slow.push({ variant: name, test: t.title, elapsed, limit });
      });
      if (name === 'solution') report.total = end.elapsed.reduce((a, b) => a + (b ?? 0), 0);
    }
    const starter = await py.run({ kind: 'task', packages: task.packages, code: read(join(task.dir, 'starter.py')), footer: task.footer });
    if (passedAll(starter)) report.errors.push('заготовка проходит все тесты в Pyodide');
    else if (starter.type === 'crash' || starter.type === 'load-error' || starter.type === 'package-error') {
      report.errors.push(`заготовка: ${describe(starter)}`);
    }
    return report;
  };
}

// ─── Справочник ─────────────────────────────────────────────────────────────

interface ExampleStatus {
  status: 'differs' | 'unavailable';
  reason?: string;
}

interface ExampleReport {
  id: string; // «numpy/sorting#descending»
  status: 'same' | ExampleStatus['status'];
  reason?: string;
  errors: string[];
  diff: string[];
  elapsed: number;
}

interface Article {
  id: string;
  topicPackage: string;
  setup: string;
  cells: ExampleCell[];
}

function loadArticles(): Article[] {
  const articles: Article[] = [];
  const base = join(root, 'reference');
  for (const topic of dirs(base)) {
    const meta = parseToml(read(join(base, topic, 'topic.toml'))) as { package: string; sections: { articles: string[] }[] };
    for (const slug of meta.sections.flatMap((s) => s.articles)) {
      const path = join(base, topic, `${slug}.py`);
      if (!existsSync(path)) continue;
      const cells = parseExamples(read(path));
      articles.push({
        id: `${topic}/${slug}`,
        topicPackage: meta.package,
        setup: cells.get('setup')?.code ?? '',
        cells: [...cells.values()].filter((c) => c.id !== 'setup' && !('norun' in c.flags)),
      });
    }
  }
  return articles;
}

const NUMBER_RE = /\d+(?:[.,]\d+)?/g;
const numberMask = (line: string) => line.replace(NUMBER_RE, '#').split(/\s+/).filter(Boolean).join(' ');

function plotPaths(articleId: string, cellId: string): string[] {
  const dir = join(root, 'public', 'reference', 'plots', articleId);
  if (!existsSync(dir)) return [];
  const order = (name: string) => Number(name.slice(cellId.length + 1, -4) || 1);
  return readdirSync(dir)
    .filter((n) => n === `${cellId}.svg` || new RegExp(`^${cellId}-\\d+\\.svg$`).test(n))
    .sort((a, b) => order(a) - order(b))
    .map((n) => join(dir, n));
}

function exampleJob(article: Article, cell: ExampleCell): () => (py: NodePython) => Promise<ExampleReport> {
  return () => async (py) => {
    const id = `${article.id}#${cell.id}`;
    const report: ExampleReport = { id, status: 'same', errors: [], diff: [], elapsed: 0 };
    const packages = examplePackages(article.topicPackage, `${article.setup}\n${cell.code}`);
    const end = await py.run({ kind: 'example', packages, setup: article.setup, code: cell.code, filename: `reference/${article.id}.py`, cell: cell.id });
    if (end.type === 'timeout') return { ...report, status: 'unavailable', reason: `выполняется дольше ${end.seconds} с` };
    if (end.type !== 'done') return { ...report, status: 'unavailable', reason: `Python остановился: ${end.message}` };
    const d = end.data as ExampleDone;
    report.elapsed = d.elapsed;
    if (end.retried) report.errors.push(`пакет ${end.retried} не распознан заранее — дополните правила в src/lib/python/packages.ts`);
    const expected = cell.flags.raises;
    if (d.error && !(expected && d.error.mro.includes(expected))) {
      const last = d.lines[d.lines.length - 1] ?? d.error.type;
      const reason = d.error.type === 'ModuleNotFoundError' ? `нет пакета — ${last}` : `пример падает — ${last}`;
      return { ...report, status: 'unavailable', reason };
    }
    if (expected && !d.error) return { ...report, status: 'differs', reason: `не возникает ${expected}` };
    const stored = cell.output === null ? [] : cell.output.split('\n');
    const same = 'timing' in cell.flags
      ? stored.map(numberMask).join('\n') === d.lines.map(numberMask).join('\n')
      : stored.join('\n') === d.lines.join('\n');
    if (!same) {
      report.status = 'differs';
      report.reason = 'вывод';
      for (let i = 0; i < Math.max(stored.length, d.lines.length); i++) {
        if (stored[i] !== d.lines[i]) report.diff.push(`- ${stored[i] ?? ''}`, `+ ${d.lines[i] ?? ''}`);
        if (report.diff.length >= 6) break;
      }
    }
    const svgs = plotPaths(article.id, cell.id).map(read);
    if (svgs.length !== d.plots.length || svgs.some((svg, i) => svg !== d.plots[i])) {
      report.status = 'differs';
      report.reason = report.reason ? `${report.reason} и график` : 'график';
    }
    return report;
  };
}

// ─── Точка входа ────────────────────────────────────────────────────────────

async function main(argv: string[]): Promise<number> {
  let failedPins = false;
  const update = argv.includes('--update');
  const reportPath = argv.includes('--report') ? argv[argv.indexOf('--report') + 1] : null;
  const jobsArg = argv.includes('--jobs') ? Number(argv[argv.indexOf('--jobs') + 1]) : 0;
  const selected = argv.filter((a, i) => !a.startsWith('--') && !['--report', '--jobs'].includes(argv[i - 1]));
  const only = argv.includes('--tasks') ? 'tasks' : argv.includes('--reference') ? 'reference' : null;
  const size = jobsArg || Math.max(1, Math.min(4, availableParallelism() - 1));
  const matches = (...keys: string[]) => !selected.length || selected.some((s) => keys.includes(s));

  const npmVersion = (JSON.parse(read(join(root, 'node_modules', 'pyodide', 'package.json'))) as { version: string }).version;
  if (npmVersion !== PYODIDE_VERSION) {
    console.log(`✗ Сайт грузит Pyodide ${PYODIDE_VERSION} (src/lib/python/config.ts), а npm-пакет pyodide — ${npmVersion}: закрепите в package.json ту же версию`);
    return 1;
  }
  const pins = read(join(root, 'requirements-dev.txt'));
  for (const pin of Object.values(MICROPIP_PACKAGES)) {
    if (pins.split('\n').includes(pin)) continue;
    console.log(`✗ ${pin} (MICROPIP_PACKAGES в config.ts) не совпадает с requirements-dev.txt`);
    failedPins = true;
  }
  console.log(`Pyodide ${PYODIDE_VERSION} (Node.js ${process.version}), воркеров: ${size}, коэффициент лимита ×${factor}`);
  let failed = failedPins;
  const lines: string[] = [];

  if (only !== 'reference') {
    const tasks = loadTasks().filter((t) => matches(t.id, relative(join(root, 'challenges'), t.dir)));
    const started = performance.now();
    const reports = await pool(tasks.map(taskJob), size);
    const bad = reports.filter((r) => r.errors.length);
    for (const r of reports) {
      if (!r.errors.length) continue;
      console.log(`✗ ${r.id}`);
      for (const e of r.errors) console.log(`    ${e}`);
    }
    const slow = reports.flatMap((r) => r.slow.map((s) => ({ id: r.id, ...s })));
    console.log(`Задачи: прошли ${reports.length - bad.length} из ${reports.length} за ${((performance.now() - started) / 1000).toFixed(1)} с`);
    for (const s of slow) console.log(`  · ${s.id} ${s.variant} «${s.test}»: ${s.elapsed.toFixed(2)} с из ${s.limit} с`);
    failed ||= bad.length > 0;
    lines.push('## Задачи', '', `Прошли ${reports.length - bad.length} из ${reports.length}.`, '');
    lines.push('Самые долгие эталоны (сумма тестов):', '');
    for (const r of [...reports].sort((a, b) => b.total - a.total).slice(0, 10)) lines.push(`- ${r.id}: ${r.total.toFixed(2)} с`);
    lines.push('', 'Тесты дольше половины лимита браузера:', '');
    for (const s of slow) lines.push(`- ${s.id} (${s.variant}) «${s.test}»: ${s.elapsed.toFixed(2)} с из ${s.limit} с`);
    if (!slow.length) lines.push('- нет');
    lines.push('');
  }

  if (only !== 'tasks') {
    const articles = loadArticles().filter((a) => matches(a.id, a.id.split('/')[0]));
    const jobs = articles.flatMap((a) => a.cells.map((c) => exampleJob(a, c)));
    const started = performance.now();
    const reports = await pool(jobs, size);
    const stored = existsSync(STATUS_PATH) ? (JSON.parse(read(STATUS_PATH)) as { examples: Record<string, ExampleStatus> }) : { examples: {} };
    const fresh: Record<string, ExampleStatus> = {};
    for (const r of reports) if (r.status !== 'same') fresh[r.id] = { status: r.status, ...(r.reason ? { reason: r.reason } : {}) };
    const checkedIds = new Set(reports.map((r) => r.id));
    let mismatched = 0;
    for (const r of reports) {
      for (const e of r.errors) {
        console.log(`✗ ${r.id}: ${e}`);
        failed = true;
      }
      const was = stored.examples[r.id];
      const now = fresh[r.id];
      if (JSON.stringify(was ?? null) !== JSON.stringify(now ?? null)) {
        mismatched++;
        if (!update) console.log(`✗ ${r.id}: в browser.json ${JSON.stringify(was ?? 'работает')}, получено ${JSON.stringify(now ?? 'работает')}`);
      }
    }
    const counts = { differs: 0, unavailable: 0 };
    for (const r of reports) if (r.status !== 'same') counts[r.status]++;
    console.log(
      `Справочник: примеров ${reports.length} за ${((performance.now() - started) / 1000).toFixed(1)} с · ` +
        `как показано ${reports.length - counts.differs - counts.unavailable} · отличается ${counts.differs} · не работает ${counts.unavailable}`,
    );
    if (update) {
      const examples = { ...Object.fromEntries(Object.entries(stored.examples).filter(([id]) => !checkedIds.has(id))), ...fresh };
      const sorted = Object.fromEntries(Object.entries(examples).sort(([a], [b]) => a.localeCompare(b)));
      writeFileSync(STATUS_PATH, `${JSON.stringify({ pyodide: PYODIDE_VERSION, examples: sorted }, null, 2)}\n`);
      console.log(`reference/browser.json обновлён (изменений: ${mismatched})`);
    } else if (mismatched) {
      console.log('Состояние примеров в браузере изменилось — обновите: node scripts/validate_pyodide.ts --update');
      failed = true;
    }
    lines.push('## Справочник', '', `Примеров ${reports.length}: отличается ${counts.differs}, не работает ${counts.unavailable}.`, '');
    lines.push('### Не работают в браузере', '');
    for (const r of reports.filter((r) => r.status === 'unavailable')) lines.push(`- ${r.id}: ${r.reason}`);
    lines.push('', '### Вывод отличается', '');
    for (const r of reports.filter((r) => r.status === 'differs')) {
      lines.push(`- ${r.id}: ${r.reason}`);
      if (r.diff.length) lines.push('  ```', ...r.diff.map((l) => `  ${l}`), '  ```');
    }
    lines.push('', 'Самые долгие примеры:', '');
    for (const r of [...reports].sort((a, b) => b.elapsed - a.elapsed).slice(0, 10)) lines.push(`- ${r.id}: ${r.elapsed.toFixed(2)} с`);
  }

  if (reportPath) writeFileSync(reportPath, `# Проверка в Pyodide ${PYODIDE_VERSION}\n\n${lines.join('\n')}\n`);
  console.log(failed ? '✗ Есть ошибки' : '✓ Всё в порядке');
  return failed ? 1 : 0;
}

process.exitCode = await main(process.argv.slice(2));
