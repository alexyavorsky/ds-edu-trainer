/**
 * Воркер с Python для проверки в Node.js (worker_threads) — то же ядро, что у сайта (src/lib/python/engine.ts).
 * Pyodide — npm-пакет той же версии, что грузит сайт; пакеты он скачивает с jsDelivr и кэширует.
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { parentPort } from 'node:worker_threads';
import { loadPyodide } from 'pyodide';
import { MICROPIP_PACKAGES, PYTHON_CONFIG } from '../src/lib/python/config.ts';
import { Engine } from '../src/lib/python/engine.ts';
import type { RunRequest } from '../src/lib/python/protocol.ts';

const root = join(import.meta.dirname, '..');
const read = (path: string) => readFileSync(join(root, path), 'utf-8');

const engine = new Engine({
  loadPyodide: (options) => loadPyodide({ ...options, packageCacheDir: process.env.PYODIDE_CACHE || undefined }),
  modules: { pyodide_driver: read('runtime/pyodide_driver.py'), reference_exec: read('runtime/reference_exec.py') },
  prelude: read('reference/prelude.py'),
  maxLines: PYTHON_CONFIG.maxLines,
  maxChars: PYTHON_CONFIG.maxChars,
  memoryLimitMB: PYTHON_CONFIG.memoryLimitMB,
  micropip: MICROPIP_PACKAGES,
  post: (message) => parentPort!.postMessage(message),
});

let queue: Promise<void> = Promise.resolve();
parentPort!.on('message', (data: { type: 'run'; request: RunRequest }) => {
  if (data?.type !== 'run') return;
  queue = queue.then(() => engine.run(data.request)).catch(() => {});
});
