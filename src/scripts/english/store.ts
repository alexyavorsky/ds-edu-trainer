/**
 * Прогресс упражнений по английскому в localStorage (docs/ENGLISH_PLAN.md, 0.3 «Где хранится прогресс»):
 *   edu:drill:v1:«урок/упражнение» = { hash, items: { "<n>": { ok, tries, shown, input } }, t } — состояние пунктов;
 *   edu:test:v1:«урок» = { best, last, t } — баллы контрольной и входной проверки в процентах.
 * Решённые упражнения и пройденные уроки — в общем edu:course:v1 (src/scripts/course/progress.ts).
 * t — время изменения (мс): по нему синхронизация выбирает более свежую версию.
 */
import type { Input } from '../../lib/english/check';

export interface ItemState {
  ok: boolean; // хоть раз введён верно
  tries: number; // неверные попытки
  shown: boolean; // открывали «Показать ответ»
  input: Input | null; // что вписано сейчас
}

export interface DrillState {
  hash: string; // версия упражнения: изменилась — состояние пунктов сбрасывается
  items: Record<string, ItemState>;
  t: number;
}

export interface TestResult {
  best: number; // лучший результат, %
  last: number; // последний, %
  t: number;
}

const drillKey = (lesson: string, exercise: string) => `edu:drill:v1:${lesson}/${exercise}`;
const testKey = (lesson: string) => `edu:test:v1:${lesson}`;

function read<T>(key: string): T | null {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : null;
  } catch {
    return null;
  }
}

function write(key: string, value: unknown): void {
  try {
    if (value === null) localStorage.removeItem(key);
    else localStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* приватный режим или переполненное хранилище — состояние просто не сохранится */
  }
}

export const loadDrill = (lesson: string, exercise: string) => read<DrillState>(drillKey(lesson, exercise));

export function saveDrill(lesson: string, exercise: string, state: Omit<DrillState, 't'> | null): void {
  write(drillKey(lesson, exercise), state && { ...state, t: Date.now() });
}

export const loadTest = (lesson: string) => read<TestResult>(testKey(lesson));

/** Записывает попытку; возвращает обновлённый результат (лучший хранится). */
export function saveTest(lesson: string, percent: number): TestResult {
  const prev = loadTest(lesson);
  const result = { best: Math.max(prev?.best ?? 0, percent), last: percent, t: Date.now() };
  write(testKey(lesson), result);
  return result;
}
