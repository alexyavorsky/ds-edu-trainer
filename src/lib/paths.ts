/**
 * Где лежит контент: challenges/, reference/, courses/. По умолчанию — корень репозитория. Переменная
 * EDU_CONTENT_ROOT подменяет его на другую папку с той же структурой — так проверяются образцы платформы
 * (tests/platform/: тема без пакета, задача с data.py, курс без пакета) без их появления на сайте.
 */
import { join, resolve } from 'node:path';

export const CONTENT_ROOT = resolve(process.env.EDU_CONTENT_ROOT || '.');
export const contentPath = (...parts: string[]) => join(CONTENT_ROOT, ...parts);
export const CHALLENGES_DIR = contentPath('challenges');
