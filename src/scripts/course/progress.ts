/**
 * Прогресс курсов в localStorage этого браузера (после входа — ещё и в Supabase, см. scripts/sync/):
 *   edu:course:v1 = { ex: {«урок/упражнение»: {t, hash}}, done: {урок: {v, t}}, last: {курс: {lesson, t}} }
 *   edu:code:v1:«урок/упражнение» = { code, starter, t } — код упражнения (scripts/code-store.ts, как у задач)
 * t — время изменения (мс): по нему синхронизация выбирает более свежую версию.
 * Урок пройден, если его отметили вручную или решены все упражнения (явная отметка важнее).
 */
import * as codeStore from '../code-store';
import { noteChange } from '../sync/pending';

export const STORE_KEY = 'edu:course:v1';
const KEY = STORE_KEY;
export const COURSE_EVENT = 'edu:course-change';

export interface Store {
  ex: Record<string, { t: number; hash: string }>;
  done: Record<string, { v: boolean; t: number }>;
  last: Record<string, { lesson: string; t: number }>;
}

export function read(): Store {
  try {
    const raw = localStorage.getItem(KEY);
    const data = raw ? (JSON.parse(raw) as Partial<Store>) : {};
    return { ex: data.ex ?? {}, done: data.done ?? {}, last: data.last ?? {} };
  } catch {
    return { ex: {}, done: {}, last: {} };
  }
}

export function write(store: Store): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(store));
  } catch {
    /* приватный режим или переполненное хранилище — прогресс просто не сохранится */
  }
  document.dispatchEvent(new CustomEvent(COURSE_EVENT));
}

export const exerciseKey = (lesson: string, exercise: string) => `${lesson}/${exercise}`;

export function isSolved(lesson: string, exercise: string): boolean {
  return exerciseKey(lesson, exercise) in read().ex;
}

function update(part: 'ex' | 'done' | 'last', id: string, entry: Store[typeof part][string]): void {
  const store = read();
  (store[part] as Record<string, unknown>)[id] = entry;
  write(store);
  noteChange(`course.${part}`, id, entry.t);
}

export function setSolved(lesson: string, exercise: string, hash: string): void {
  update('ex', exerciseKey(lesson, exercise), { t: Date.now(), hash });
}

/** Пройден ли урок: явная отметка, иначе — решены все упражнения. */
export function isDone(lesson: string, exercises: string[], store = read()): boolean {
  const mark = store.done[lesson];
  if (mark) return mark.v;
  return exercises.length > 0 && exercises.every((e) => exerciseKey(lesson, e) in store.ex);
}

export function setDone(lesson: string, done: boolean): void {
  update('done', lesson, { v: done, t: Date.now() });
}

export function setLast(course: string, lesson: string): void {
  update('last', course, { lesson, t: Date.now() });
}

export function getLast(course: string): string | null {
  return read().last[course]?.lesson ?? null;
}

// ─── Код упражнений ─────────────────────────────────────────────────────────

export type { SavedCode } from '../code-store';

export const loadCode = (lesson: string, exercise: string) => codeStore.loadCode(exerciseKey(lesson, exercise));

export function saveCode(lesson: string, exercise: string, saved: { code: string; starter: string } | null): void {
  codeStore.saveCode(exerciseKey(lesson, exercise), saved);
}

// ─── Отметки на страницах ───────────────────────────────────────────────────

/**
 * [data-lesson-mark="урок"] + data-exercises="a,b" — класс is-done у пройденного урока;
 * [data-course-progress] + data-lessons="урок:a,b;урок2:c" — счётчик и полоска.
 */
export function renderCourseProgress(): void {
  const store = read();
  const exercisesOf = (el: HTMLElement) => (el.dataset.exercises ?? '').split(',').filter(Boolean);
  document.querySelectorAll<HTMLElement>('[data-lesson-mark]').forEach((el) => {
    el.classList.toggle('is-done', isDone(el.dataset.lessonMark!, exercisesOf(el), store));
  });
  document.querySelectorAll<HTMLElement>('[data-course-progress]').forEach((el) => {
    const lessons = (el.dataset.lessons ?? '').split(';').filter(Boolean).map((part) => {
      const [id, ex = ''] = part.split(':');
      return { id, ex: ex.split(',').filter(Boolean) };
    });
    const done = lessons.filter((l) => isDone(l.id, l.ex, store)).length;
    const count = el.querySelector<HTMLElement>('[data-progress-count]');
    const bar = el.querySelector<HTMLElement>('[data-progress-bar]');
    if (count) count.textContent = String(done);
    if (bar) bar.style.width = lessons.length ? `${(done / lessons.length) * 100}%` : '0%';
    el.classList.toggle('is-complete', lessons.length > 0 && done === lessons.length);
  });
}

export function watchCourseProgress(): void {
  renderCourseProgress();
  document.addEventListener(COURSE_EVENT, renderCourseProgress);
  window.addEventListener('storage', (e) => {
    if (e.key === KEY) renderCourseProgress();
  });
}
