/**
 * Python на странице: один воркер на вкладку, очередь запусков, таймауты и восстановление после падений.
 *
 * - Воркер создаётся лениво (preloadWhenIdle — когда браузер простаивает, или при первом запуске)
 *   и переиспользуется. Новый — только после таймаута, падения или нехватки памяти.
 * - Таймаут обеспечивает страница: в Pyodide нет потоков, поэтому зависший воркер завершается
 *   worker.terminate(). Тесту даётся его лимит × PYTHON_CONFIG.timeoutFactor, примеру — exampleTimeout.
 * - Код выполняется только по явному запуску пользователя — никогда из ссылки или параметров URL.
 */
import { PACKAGE_LABEL, PYTHON_CONFIG } from './config.ts';
import type { ExampleDone, FromWorker, RunInput, RunRequest, TaskDone, TestInfo, TestResult } from './protocol.ts';

export type EngineState = 'idle' | 'loading' | 'ready' | 'failed';

export interface RunHandlers {
  /** Индикатор: «Загружаем Python…», «Загружаем pandas…»; пустая строка — загрузка закончилась. */
  onStatus?(text: string): void;
  onStarted?(): void;
  onOutput?(chunks: [string, string][], truncated: boolean): void;
  onTests?(tests: TestInfo[]): void;
  onTestStart?(index: number): void;
  onTest?(index: number, result: TestResult): void;
}

export type RunEnd =
  | { type: 'done'; data: TaskDone | ExampleDone }
  | { type: 'timeout'; seconds: number; tests: TestInfo[] | null; testIndex: number | null }
  | { type: 'crash'; message: string }
  | { type: 'load-error'; message: string }
  | { type: 'package-error'; message: string };

export type { RunInput };

interface ActiveRun {
  id: number;
  request: RunRequest;
  kind: RunRequest['kind'];
  handlers: RunHandlers;
  finish(end: RunEnd): void;
  tests: TestInfo[] | null;
  testIndex: number | null;
  timer?: ReturnType<typeof setTimeout>;
}

const factor = PYTHON_CONFIG.timeoutFactor;

class PythonHost {
  state: EngineState = 'idle';
  statusText = '';
  private worker: Worker | null = null;
  private ready: Promise<void> | null = null;
  private resolveReady?: () => void;
  private rejectReady?: (error: Error) => void;
  private listeners = new Set<(state: EngineState, text: string) => void>();
  private active: ActiveRun | null = null;
  private queue: Promise<unknown> = Promise.resolve();
  private nextId = 1;

  subscribe(listener: (state: EngineState, text: string) => void): void {
    this.listeners.add(listener);
    listener(this.state, this.statusText);
  }

  private setState(state: EngineState, text = this.statusText): void {
    this.state = state;
    this.statusText = text;
    for (const listener of this.listeners) listener(state, text);
  }

  /** Фоновая загрузка Python, когда браузер простаивает (не при экономии трафика). */
  preloadWhenIdle(): void {
    const connection = (navigator as Navigator & { connection?: { saveData?: boolean } }).connection;
    if (connection?.saveData) return;
    const start = () => void this.start().catch(() => {});
    if ('requestIdleCallback' in window) requestIdleCallback(start, { timeout: 5000 });
    else setTimeout(start, 2000);
  }

  /** Создаёт воркер, если его ещё нет; промис — Python готов. */
  start(): Promise<void> {
    if (this.ready && this.state !== 'failed') return this.ready;
    this.ready = new Promise<void>((resolve, reject) => {
      this.resolveReady = resolve;
      this.rejectReady = reject;
    });
    this.ready.catch(() => {});
    this.setState('loading', 'Загружаем Python…');
    let worker: Worker;
    try {
      worker = new Worker(new URL('./worker.ts', import.meta.url), { type: 'module', name: 'python' });
    } catch (error) {
      this.fail(`браузер не смог запустить воркер (${String(error)})`);
      return this.ready;
    }
    worker.onmessage = (event: MessageEvent<FromWorker>) => this.handle(event.data);
    worker.onerror = (event) => {
      event.preventDefault();
      this.crash(event.message || 'воркер с Python завершился с ошибкой');
    };
    worker.onmessageerror = () => this.crash('сообщение от Python не удалось прочитать');
    this.worker = worker;
    return this.ready;
  }

  private fail(message: string): void {
    this.worker?.terminate();
    this.worker = null;
    this.setState('failed', '');
    this.rejectReady?.(new Error(message));
  }

  /** Завершает воркер и сразу начинает загружать новый — следующий запуск работает. */
  private restart(): void {
    this.worker?.terminate();
    this.worker = null;
    this.ready = null;
    this.setState('idle', '');
    void this.start().catch(() => {});
  }

  private crash(message: string): void {
    if (this.state === 'loading' && !this.active) {
      this.fail(message);
      return;
    }
    const active = this.active;
    this.restart();
    active?.finish({ type: 'crash', message });
  }

  private handle(message: FromWorker): void {
    if (message.type === 'status' && message.stage === 'python') return;
    if (message.type === 'ready') {
      this.setState('ready', '');
      this.resolveReady?.();
      return;
    }
    if (message.type === 'load-error') {
      this.fail(message.message);
      return;
    }
    const run = this.active;
    if (!run || !('runId' in message) || message.runId !== run.id) return;
    const h = run.handlers;
    switch (message.type) {
      case 'status':
        h.onStatus?.(`Загружаем ${PACKAGE_LABEL[message.name] ?? message.name}…`);
        break;
      case 'package-error':
        run.finish({ type: 'package-error', message: message.message });
        break;
      case 'started':
        h.onStatus?.('');
        h.onStarted?.();
        // до первого теста выполняется код решения вне функций; у примера — единый лимит
        this.arm(run, run.kind === 'task' ? PYTHON_CONFIG.defaultTestTimeout * factor : PYTHON_CONFIG.exampleTimeout);
        break;
      case 'retried':
        break;
      case 'restart':
        // Python нужно начать заново (pandas импортирован без pyarrow): новый воркер, тот же запуск
        h.onStatus?.('Перезапускаем Python…');
        this.worker?.terminate();
        this.worker = null;
        this.ready = null;
        this.start().then(
          () => this.active === run && this.worker!.postMessage({ type: 'run', request: run.request }),
          (error: Error) => run.finish({ type: 'load-error', message: error.message }),
        );
        break;
      case 'output':
        h.onOutput?.(message.chunks, message.truncated);
        break;
      case 'tests':
        run.tests = message.tests;
        h.onTests?.(message.tests);
        break;
      case 'test-start':
        run.testIndex = message.index;
        h.onTestStart?.(message.index);
        this.arm(run, (run.tests?.[message.index]?.timeout ?? PYTHON_CONFIG.defaultTestTimeout) * factor);
        break;
      case 'test':
        run.testIndex = null;
        h.onTest?.(message.index, message.result);
        this.arm(run, PYTHON_CONFIG.defaultTestTimeout * factor);
        break;
      case 'fatal':
        this.restart();
        run.finish({ type: 'crash', message: message.message });
        break;
      case 'done':
        run.finish({ type: 'done', data: message });
        if (message.memory) this.restart(); // WebAssembly не отдаёт память обратно — начинаем с чистого листа
        break;
    }
  }

  private arm(run: ActiveRun, seconds: number): void {
    clearTimeout(run.timer);
    run.timer = setTimeout(() => {
      if (this.active !== run) return;
      this.restart();
      run.finish({ type: 'timeout', seconds, tests: run.tests, testIndex: run.testIndex });
    }, seconds * 1000);
  }

  /** Ставит запуск в очередь: выполнится, когда Python загрузится и закончатся предыдущие запуски. */
  run(request: RunInput, handlers: RunHandlers = {}): Promise<RunEnd> {
    const result = this.queue.then(() => this.execute(request, handlers));
    this.queue = result.catch(() => {});
    return result;
  }

  private async execute(request: RunInput, handlers: RunHandlers): Promise<RunEnd> {
    if (this.state !== 'ready') handlers.onStatus?.('Загружаем Python…');
    try {
      await this.start();
    } catch (error) {
      handlers.onStatus?.('');
      return { type: 'load-error', message: (error as Error).message };
    }
    return new Promise<RunEnd>((resolve) => {
      const id = this.nextId++;
      const full = { ...request, runId: id } as RunRequest;
      const run: ActiveRun = {
        id,
        request: full,
        kind: request.kind,
        handlers,
        tests: null,
        testIndex: null,
        finish: (end) => {
          clearTimeout(run.timer);
          if (this.active === run) this.active = null;
          handlers.onStatus?.('');
          resolve(end);
        },
      };
      this.active = run;
      this.worker!.postMessage({ type: 'run', request: full });
    });
  }
}

export const python = new PythonHost();
