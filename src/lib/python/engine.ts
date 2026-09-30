/**
 * Ядро воркера: загружает Pyodide, ставит пакеты и выполняет запуски через runtime/pyodide_driver.py.
 * Не зависит от окружения — его используют и Web Worker сайта (worker.ts), и проверка в Node.js
 * (scripts/validate_pyodide.ts), поэтому в Node код выполняется ровно так же, как в браузере.
 */
import type { PyodideAPI } from 'pyodide';
import type { FromWorker, RunRequest } from './protocol.ts';

export interface EngineOptions {
  loadPyodide: (options: Record<string, unknown>) => Promise<PyodideAPI>;
  indexURL?: string;
  /** Исходники Python: имя модуля → код (pyodide_driver, reference_exec). */
  modules: Record<string, string>;
  prelude: string;
  maxLines: number;
  maxChars: number;
  memoryLimitMB: number;
  micropip: Record<string, string>;
  post: (message: FromWorker) => void;
}

interface Driver {
  run_task(payload: string): void;
  run_example(payload: string): void;
}

/**
 * Ограничивает рост памяти WebAssembly: Emscripten растит кучу через WebAssembly.Memory.grow, и отказ
 * превращается в MemoryError в Python — вместо того чтобы съесть всю память вкладки.
 */
export function limitWasmMemory(limitMB: number): void {
  const proto = WebAssembly.Memory.prototype as WebAssembly.Memory & { eduLimited?: boolean };
  if (proto.eduLimited) return;
  const grow = proto.grow;
  const limit = limitMB * 1024 * 1024;
  proto.grow = function (this: WebAssembly.Memory, delta: number) {
    if (this.buffer.byteLength + delta * 65536 > limit) throw new RangeError(`память ограничена ${limitMB} МБ`);
    return grow.call(this, delta);
  };
  proto.eduLimited = true;
}

export class Engine {
  readonly ready: Promise<void>;
  private options: EngineOptions;
  private pyodide?: PyodideAPI;
  private driver?: Driver;
  private loaded = new Set<string>();
  private runId = 0;
  /** Перехват сообщений Python: вернуть false — сообщение не уходит странице. */
  private intercept: ((message: FromWorker) => boolean) | null = null;

  constructor(options: EngineOptions) {
    this.options = options;
    this.ready = this.init();
    this.ready.catch(() => {}); // ошибка загрузки уходит странице сообщением load-error
  }

  private emit(message: FromWorker): void {
    if (!this.intercept || this.intercept(message)) this.options.post(message);
  }

  private async init(): Promise<void> {
    const o = this.options;
    limitWasmMemory(o.memoryLimitMB);
    o.post({ type: 'status', stage: 'python' });
    try {
      const pyodide = await o.loadPyodide({
        ...(o.indexURL ? { indexURL: o.indexURL } : {}),
        env: { PYTHONHASHSEED: '0' }, // как у валидатора справочника: порядок элементов set постоянный
        stdout: () => {},
        stderr: () => {},
      });
      pyodide.setStdin({ error: true });
      const dir = '/home/pyodide/edu';
      pyodide.FS.mkdirTree(dir);
      for (const [name, source] of Object.entries(o.modules)) pyodide.FS.writeFile(`${dir}/${name}.py`, source);
      pyodide.runPython(`import sys; sys.path.insert(0, ${JSON.stringify(dir)})`);
      const driver = pyodide.pyimport('pyodide_driver') as unknown as Driver & { setup(post: unknown, config: string): void };
      const config = JSON.stringify({ maxLines: o.maxLines, maxChars: o.maxChars, prelude: o.prelude });
      driver.setup((json: string) => this.emit({ ...JSON.parse(json), runId: this.runId }), config);
      this.pyodide = pyodide;
      this.driver = driver;
      o.post({ type: 'ready' });
    } catch (error) {
      o.post({ type: 'load-error', message: errorText(error) });
      throw error;
    }
  }

  /** Загружает недостающие пакеты; индикатор — по каждому запрошенному пакету. */
  private async ensurePackages(names: string[]): Promise<void> {
    const pyodide = this.pyodide!;
    const quiet = { messageCallback: () => {}, errorCallback: () => {} };
    for (const name of names) {
      if (this.loaded.has(name)) continue;
      this.options.post({ type: 'status', stage: 'package', name, runId: this.runId });
      const pin = this.options.micropip[name];
      if (pin) {
        await pyodide.loadPackage('micropip', quiet);
        await pyodide.pyimport('micropip').install(pin);
      } else {
        await pyodide.loadPackage(name, quiet);
        if (!pyodide.loadedPackages[name]) throw new Error(`пакет ${name} не загрузился`);
      }
      this.loaded.add(name);
    }
  }

  /** Пакет Pyodide (или из списка micropip), дающий модуль, — для повтора после ModuleNotFoundError. */
  private packageFor(module: string): string | null {
    const top = module.split('.')[0];
    if (this.options.micropip[top]) return top;
    for (const [name, info] of Object.entries(this.pyodide!.lockfile.packages)) {
      if ((info as { imports?: string[] }).imports?.includes(top)) return name;
    }
    return null;
  }

  async run(request: RunRequest): Promise<void> {
    await this.ready;
    this.runId = request.runId;
    const post = this.options.post;
    try {
      // pandas проверяет pyarrow при импорте: если pandas уже импортирован без него, нужен новый Python
      if (request.packages.includes('pyarrow') && !this.loaded.has('pyarrow') && this.pyodide!.runPython("'pandas' in __import__('sys').modules")) {
        post({ type: 'restart', runId: request.runId, reason: 'pyarrow' });
        return;
      }
      try {
        await this.ensurePackages(request.packages);
        if (request.kind === 'example') {
          await this.pyodide!.loadPackagesFromImports(`${request.setup}\n${request.code}`, { messageCallback: () => {} });
        }
      } catch (error) {
        post({ type: 'package-error', runId: request.runId, message: errorText(error) });
        return;
      }
      post({ type: 'started', runId: request.runId });
      if (request.kind === 'task') {
        this.driver!.run_task(JSON.stringify({ code: request.code, footer: request.footer }));
        return;
      }
      const payload = JSON.stringify({ setup: request.setup, code: request.code, filename: request.filename, cell: request.cell });
      // Пример мог использовать пакет, который не распознали заранее: ставим его и повторяем один раз.
      let missing: string | null = null;
      this.intercept = (message) => {
        const m = message as { type: string; missing_module?: string | null };
        if (m.type === 'done' && m.missing_module) missing = this.packageFor(m.missing_module);
        return !missing;
      };
      try {
        this.driver!.run_example(payload);
      } finally {
        this.intercept = null;
      }
      if (!missing) return;
      try {
        await this.ensurePackages([missing]);
      } catch (error) {
        post({ type: 'package-error', runId: request.runId, message: errorText(error) });
        return;
      }
      post({ type: 'retried', runId: request.runId, name: missing });
      post({ type: 'started', runId: request.runId });
      this.driver!.run_example(payload);
    } catch (error) {
      // Ошибка вне Python-кода: переполнение стека WebAssembly, аварийная остановка Pyodide.
      post({ type: 'fatal', runId: request.runId, message: errorText(error) });
    }
  }
}

function errorText(error: unknown): string {
  const text = error instanceof Error ? error.message : String(error);
  return text.length > 500 ? `${text.slice(0, 500)}…` : text;
}
