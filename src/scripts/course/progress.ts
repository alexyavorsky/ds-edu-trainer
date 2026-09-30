/**
 * Прогресс курсов в localStorage этого браузера (позже — синхронизация, docs/COURSES_PLAN.md):
 *   edu:course:v1 = { ex: {«урок/упражнение»: {t, hash}}, done: {урок: {v, t}}, last: {курс: {lesson, t}} }
 *   edu:code:v1:«урок/упражнение» = { code, starter, t } — код упражнения (как у задач)
 * t — время изменения (мс): по нему синхронизация выбирает более свежую версию.
 * Урок пройден, если его отметили вручную или решены все упражнения (явная отметка важнее).
 */
const KEY = 'edu:course:v1';
export const COURSE_EVENT = 'edu:course-change';

interface Store {
  ex: Record<string, { t: number; hash: string }>;
  done: Record<string, { v: boolean; t: number }>;
  last: Record<string, { lesson: string; t: number }>;
}

function read(): Store {
  try {
    const raw = localStorage.getItem(KEY);
    const data = raw ? (JSON.parse(raw) as Partial<Store>) : {};
    return { ex: data.ex ?? {}, done: data.done ?? {}, last: data.last ?? {} };
  } catch {
    return { ex: {}, done: {}, last: {} };
  }
}

function update(change: (store: Store) => void): void {
  const store = read();
  change(store);
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

export function setSolved(lesson: string, exercise: string, hash: string): void {
  update((s) => (s.ex[exerciseKey(lesson, exercise)] = { t: Date.now(), hash }));
}

/** Пройден ли урок: явная отметка, иначе — решены все упражнения. */
export function isDone(lesson: string, exercises: string[], store = read()): boolean {
  const mark = store.done[lesson];
  if (mark) return mark.v;
  return exercises.length > 0 && exercises.every((e) => exerciseKey(lesson, e) in store.ex);
}

export function setDone(lesson: string, done: boolean): void {
  update((s) => (s.done[lesson] = { v: done, t: Date.now() }));
}

export function setLast(course: string, lesson: string): void {
  update((s) => (s.last[course] = { lesson, t: Date.now() }));
}

export function getLast(course: string): string | null {
  return read().last[course]?.lesson ?? null;
}

// ─── Код упражнений ─────────────────────────────────────────────────────────

export interface SavedCode {
  code: string;
  starter: string; // хеш заготовки, от которой начат код
  t: number;
}

const codeKey = (lesson: string, exercise: string) => `edu:code:v1:${exerciseKey(lesson, exercise)}`;

export function loadCode(lesson: string, exercise: string): SavedCode | null {
  try {
    const raw = localStorage.getItem(codeKey(lesson, exercise));
    return raw ? (JSON.parse(raw) as SavedCode) : null;
  } catch {
    return null;
  }
}

export function saveCode(lesson: string, exercise: string, saved: Omit<SavedCode, 't'> | null): void {
  try {
    if (saved) localStorage.setItem(codeKey(lesson, exercise), JSON.stringify({ ...saved, t: Date.now() }));
    else localStorage.removeItem(codeKey(lesson, exercise));
  } catch {
    /* код просто не сохранится */
  }
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
