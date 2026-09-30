/// <reference lib="webworker" />
/**
 * Web Worker с Python (Pyodide). Один на вкладку, создаёт его src/lib/python/client.ts.
 * Pyodide грузится с jsDelivr — версия закреплена в package.json (см. config.ts).
 */
import coursePrelude from '../../../courses/prelude.py?raw';
import prelude from '../../../reference/prelude.py?raw';
import driver from '../../../runtime/pyodide_driver.py?raw';
import lessonExec from '../../../runtime/lesson_exec.py?raw';
import referenceExec from '../../../runtime/reference_exec.py?raw';
import runner from '../../../runtime/runner.py?raw';
import { MICROPIP_PACKAGES, PYODIDE_INDEX_URL, PYTHON_CONFIG } from './config.ts';
import { Engine } from './engine.ts';
import type { RunRequest } from './protocol.ts';

declare const self: DedicatedWorkerGlobalScope;

const engine = new Engine({
  loadPyodide: async (options) => {
    const { loadPyodide } = await import(/* @vite-ignore */ `${PYODIDE_INDEX_URL}pyodide.mjs`);
    return loadPyodide(options);
  },
  indexURL: PYODIDE_INDEX_URL,
  modules: { pyodide_driver: driver, reference_exec: referenceExec, lesson_exec: lessonExec, runner },
  prelude,
  coursePrelude,
  fetchFile: async (url) => {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`файл данных ${url} не загрузился (HTTP ${response.status})`);
    return new Uint8Array(await response.arrayBuffer());
  },
  maxLines: PYTHON_CONFIG.maxLines,
  maxChars: PYTHON_CONFIG.maxChars,
  memoryLimitMB: PYTHON_CONFIG.memoryLimitMB,
  micropip: MICROPIP_PACKAGES,
  post: (message) => self.postMessage(message),
});

let queue: Promise<void> = Promise.resolve();
self.onmessage = (event: MessageEvent<{ type: 'run'; request: RunRequest }>) => {
  if (event.data?.type !== 'run') return;
  queue = queue.then(() => engine.run(event.data.request)).catch(() => {});
};
