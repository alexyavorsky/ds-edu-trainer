/**
 * Python в браузере (Pyodide): все настройки в одном месте.
 * PYODIDE_VERSION — единственное место, где задана версия: сайт грузит Pyodide этой версии с jsDelivr,
 * а npm-пакет pyodide в package.json (им проверяет scripts/validate_pyodide.ts) обязан быть той же версии —
 * проверка падает, если они разошлись.
 */

export const PYODIDE_VERSION = '314.0.7';
export const PYODIDE_INDEX_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

export const PYTHON_CONFIG = {
  /** Во сколько раз лимит теста в браузере больше локального (Python в WebAssembly медленнее). */
  timeoutFactor: 3,
  /** Лимит теста по умолчанию, как _TIMEOUT в runtime/runner.py; им же ограничено выполнение кода решения до тестов. */
  defaultTestTimeout: 2,
  /** Лимит на один пример справочника, секунд. */
  exampleTimeout: 10,
  /** Вывод print(): дальше — «вывод обрезан». */
  maxLines: 10_000,
  maxChars: 1_000_000,
  /** Потолок памяти WebAssembly: дальше Python получает MemoryError, а не роняет вкладку. */
  memoryLimitMB: 1024,
  /** Задержка сохранения кода из редактора в localStorage, мс. */
  saveDelay: 500,
} as const;

/** Пакеты не из Pyodide: ставятся micropip с PyPI (чистый Python), версия — как в requirements-dev.txt. */
export const MICROPIP_PACKAGES: Record<string, string> = {
  openpyxl: 'openpyxl==3.1.5',
};

/** Подписи пакетов в индикаторе загрузки. */
export const PACKAGE_LABEL: Record<string, string> = {
  numpy: 'NumPy',
  pandas: 'pandas',
  matplotlib: 'matplotlib',
  pyarrow: 'pyarrow',
  openpyxl: 'openpyxl',
};
