/**
 * Python для проверок в Node.js: воркер с Pyodide (scripts/pyodide-worker.ts — то же ядро, что у сайта) и те же
 * таймауты, что у страницы (src/lib/python/client.ts). Общий для validate_pyodide.ts и validate_courses.ts.
 */
import { Worker } from 'node:worker_threads';
import { PYTHON_CONFIG } from '../src/lib/python/config.ts';
import type { ExampleDone, FromWorker, LessonDone, RunInput, TaskDone, TestInfo } from '../src/lib/python/protocol.ts';

const factor = PYTHON_CONFIG.timeoutFactor;

// ─── Воркер с таймаутами (как src/lib/python/client.ts) ─────────────────────

export type RunEnd =
  | { type: 'done'; data: TaskDone | ExampleDone | LessonDone; tests: TestInfo[] | null; elapsed: number[]; retried: string | null }
  | { type: 'timeout'; seconds: number; tests: TestInfo[] | null; testIndex: number | null; elapsed: number[] }
  | { type: 'crash' | 'package-error' | 'load-error'; message: string };

export class NodePython {
  private worker: Worker | null = null;
  private listener: ((m: FromWorker) => void) | null = null;
  private nextId = 1;

  private spawn(): Worker {
    const worker = new Worker(new URL('./pyodide-worker.ts', import.meta.url));
    worker.on('message', (m: FromWorker) => this.listener?.(m));
    worker.on('error', (e) => this.listener?.({ type: 'fatal', runId: -1, message: String(e) }));
    return worker;
  }

  stop(): void {
    void this.worker?.terminate();
    this.worker = null;
  }

  run(request: RunInput): Promise<RunEnd> {
    this.worker ??= this.spawn();
    const id = this.nextId++;
    return new Promise((resolve) => {
      let tests: TestInfo[] | null = null;
      let testIndex: number | null = null;
      let retried: string | null = null;
      const elapsed: number[] = [];
      let timer: ReturnType<typeof setTimeout> | undefined;
      const finish = (end: RunEnd) => {
        clearTimeout(timer);
        this.listener = null;
        if (end.type !== 'done' || (end.data as { memory?: boolean }).memory) this.stop();
        resolve(end);
      };
      const arm = (seconds: number) => {
        clearTimeout(timer);
        timer = setTimeout(() => finish({ type: 'timeout', seconds, tests, testIndex, elapsed }), seconds * 1000);
      };
      this.listener = (m) => {
        if (m.type === 'load-error') return finish({ type: 'load-error', message: m.message });
        if (m.type === 'fatal' && (m.runId === id || m.runId === -1)) return finish({ type: 'crash', message: m.message });
        if (!('runId' in m) || m.runId !== id) return;
        switch (m.type) {
          case 'package-error':
            return finish({ type: 'package-error', message: m.message });
          case 'started':
            return arm(request.kind === 'task' ? PYTHON_CONFIG.defaultTestTimeout * factor : PYTHON_CONFIG.exampleTimeout);
          case 'retried':
            retried = m.name;
            return;
          case 'restart':
            // как на сайте: новый Python и тот же запуск
            this.stop();
            this.worker = this.spawn();
            this.worker.postMessage({ type: 'run', request: { ...request, runId: id } });
            return;
          case 'tests':
            tests = m.tests;
            return;
          case 'test-start':
            testIndex = m.index;
            return arm((tests?.[m.index]?.timeout ?? PYTHON_CONFIG.defaultTestTimeout) * factor);
          case 'test':
            testIndex = null;
            elapsed[m.index] = m.elapsed;
            return arm(PYTHON_CONFIG.defaultTestTimeout * factor);
          case 'done':
            return finish({ type: 'done', data: m, tests, elapsed, retried });
        }
      };
      this.worker!.postMessage({ type: 'run', request: { ...request, runId: id } });
    });
  }
}

/** Пул воркеров: задания выполняются параллельно, у каждого воркера — по одному за раз. */
export async function pool<T>(jobs: (() => (py: NodePython) => Promise<T>)[], size: number): Promise<T[]> {
  const results: T[] = new Array(jobs.length);
  let next = 0;
  const workers = Array.from({ length: Math.min(size, jobs.length) }, async () => {
    const py = new NodePython();
    while (next < jobs.length) {
      const i = next++;
      results[i] = await jobs[i]()(py);
    }
    py.stop();
  });
  await Promise.all(workers);
  return results;
}
