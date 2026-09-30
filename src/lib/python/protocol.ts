/** Сообщения между страницей и воркером с Python. Результаты тестов — как в runtime/runner.py. */

export type TestStatus = 'passed' | 'failed' | 'error' | 'not_written' | 'timeout' | 'not_run';

export interface TestResult {
  title: string;
  status: TestStatus;
  message: string;
  error_type: string | null;
  line: number | null; // строка в коде решения (как в редакторе), если ошибка в нём
}

export interface TestInfo {
  title: string;
  timeout: number; // локальный лимит, секунд
  timeout_message: string;
}

export interface CodeError {
  type: string;
  message: string;
  line: number | null;
}

interface RunBase {
  runId: number;
  packages: string[];
}

export interface TaskRun extends RunBase {
  kind: 'task';
  code: string;
  footer: string; // то, что в копируемом файле идёт после кода решения: tests.py, _TESTS, раннер
}

export interface ExampleRun extends RunBase {
  kind: 'example';
  setup: string;
  code: string;
  filename: string; // «reference/numpy/broadcasting.py»
  cell: string;
}

/** Файл данных урока: пишется в data/ рабочей папки сеанса. */
export interface LessonFile {
  name: string; // «shop_orders.csv»
  url: string; // откуда взять: «/courses/data/shop_orders.csv»
}

/**
 * Урок курса: ячейки выполняются в одном пространстве имён (сеанс). session задаёт страница — новый id
 * значит новый сеанс («Перезапустить»). prepare только загружает пакеты и данные.
 */
export interface LessonRun extends RunBase {
  kind: 'lesson';
  op: 'prepare' | 'cell' | 'check' | 'quiz';
  lesson: string;
  session: string;
  files: LessonFile[];
  cell: string;
  code: string;
  tests?: string; // check: функции test_*
  targets?: string[]; // check: переменные, которые заготовка задаёт как `...`
}

export type RunRequest = TaskRun | ExampleRun | LessonRun;

/** Запрос без runId — его проставляет тот, кто управляет воркером. */
export type RunInput = Omit<TaskRun, 'runId'> | Omit<ExampleRun, 'runId'> | Omit<LessonRun, 'runId'>;

export interface TaskDone {
  type: 'done';
  runId: number;
  phase: 'syntax' | 'load' | 'tests';
  error?: CodeError;
  results?: TestResult[];
  truncated: boolean;
  memory?: boolean;
}

export interface ExampleDone {
  type: 'done';
  runId: number;
  lines: string[];
  error: { type: string; mro: string[]; line: number | null } | null;
  missing_module: string | null;
  plots: string[];
  warnings: string[];
  truncated: boolean;
  elapsed: number;
  memory: boolean;
}

export interface LessonError {
  type: string;
  mro: string[];
  text: string; // «Тип: сообщение»
  line: number | null; // строка ячейки
}

export interface LessonDone {
  type: 'done';
  runId: number;
  op: LessonRun['op'];
  lines: string[]; // stdout, stderr, предупреждения
  result: string[] | null; // repr последнего выражения
  html: string | null; // таблица DataFrame
  error: LessonError | null;
  plots: string[];
  warnings: string[];
  truncated: boolean;
  elapsed: number;
  memory: boolean;
  phase?: 'run' | 'missing' | 'tests'; // check: где остановились
  results?: TestResult[];
}

export type FromWorker =
  | { type: 'status'; stage: 'python' }
  | { type: 'status'; stage: 'package'; name: string; runId: number }
  | { type: 'ready' }
  | { type: 'load-error'; message: string }
  | { type: 'package-error'; runId: number; message: string }
  | { type: 'started'; runId: number }
  | { type: 'retried'; runId: number; name: string }
  | { type: 'restart'; runId: number; reason: string }
  | { type: 'output'; runId: number; chunks: [string, string][]; truncated: boolean }
  | { type: 'tests'; runId: number; tests: TestInfo[] }
  | { type: 'test-start'; runId: number; index: number }
  | { type: 'test'; runId: number; index: number; result: TestResult; elapsed: number }
  | { type: 'fatal'; runId: number; message: string }
  | TaskDone
  | ExampleDone
  | LessonDone;
