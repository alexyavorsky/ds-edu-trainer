/**
 * Запуск примеров справочника в браузере — данные для сборки страниц.
 * reference/browser.json пишет scripts/validate_pyodide.ts: какие примеры в Pyodide дают другой вывод
 * (пометка у кнопки) и какие не работают (кнопка неактивна). Версии пакетов — из pyodide-lock.json
 * npm-пакета pyodide той же версии, что грузит сайт.
 */
import { existsSync, readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { join } from 'node:path';
import { REFERENCE_DIR } from './challenges';

export interface BrowserStatus {
  status: 'differs' | 'unavailable';
  reason?: string;
}

const STATUS_PATH = join(REFERENCE_DIR, 'browser.json');

export function browserStatus(articleId: string, cellId: string): BrowserStatus | undefined {
  if (!existsSync(STATUS_PATH)) return undefined;
  const data = JSON.parse(readFileSync(STATUS_PATH, 'utf-8')) as { examples: Record<string, BrowserStatus> };
  return data.examples[`${articleId}#${cellId}`];
}

let versions: Record<string, string> | null = null;

/** Версии Python и пакетов в Pyodide: { python: '3.14.2', numpy: '2.4.6', … }. */
export function pyodideVersions(): Record<string, string> {
  if (versions) return versions;
  const require = createRequire(import.meta.url);
  const lock = JSON.parse(readFileSync(require.resolve('pyodide/pyodide-lock.json'), 'utf-8')) as {
    info: { python: string };
    packages: Record<string, { version: string }>;
  };
  versions = { python: lock.info.python };
  for (const name of ['numpy', 'pandas', 'matplotlib', 'pyarrow']) if (lock.packages[name]) versions[name] = lock.packages[name].version;
  return versions;
}
