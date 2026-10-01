/**
 * Статус «Решено» хранится в localStorage этого браузера (после входа — ещё и в Supabase, см. sync/).
 * Любой элемент с data-progress / data-solved-marker обновляется автоматически.
 *
 *   edu:solved:v2 = {задача: {v: решено ли, t: время изменения, мс}}
 * t нужен синхронизации: снятая отметка побеждает, только если она новее. Старый формат
 * edu:solved:v1 (массив id) читается, пока v2 нет, — его отметки получают t = 0.
 */
import { noteChange } from './sync/pending';

export const SOLVED_KEY = 'edu:solved:v2';
const OLD_KEY = 'edu:solved:v1';
export const SOLVED_EVENT = 'edu:solved-change';

export type SolvedMarks = Record<string, { v: boolean; t: number }>;

export function readSolvedMarks(): SolvedMarks {
  try {
    const raw = localStorage.getItem(SOLVED_KEY);
    if (raw) return JSON.parse(raw) as SolvedMarks;
    const old = localStorage.getItem(OLD_KEY);
    return old ? Object.fromEntries((JSON.parse(old) as string[]).map((id) => [id, { v: true, t: 0 }])) : {};
  } catch {
    return {};
  }
}

export function writeSolvedMarks(marks: SolvedMarks): void {
  try {
    localStorage.setItem(SOLVED_KEY, JSON.stringify(marks));
  } catch {
    /* приватный режим или отключённое хранилище — статус просто не сохранится */
  }
  document.dispatchEvent(new CustomEvent(SOLVED_EVENT));
}

export function getSolved(): Set<string> {
  return new Set(Object.entries(readSolvedMarks()).filter(([, m]) => m.v).map(([id]) => id));
}

export function setSolved(id: string, solved: boolean): void {
  const marks = readSolvedMarks();
  if ((marks[id]?.v ?? false) === solved) return;
  marks[id] = { v: solved, t: Date.now() };
  writeSolvedMarks(marks);
  noteChange('solved', id, marks[id].t);
}

export function renderProgress(): void {
  const solved = getSolved();
  document.querySelectorAll<HTMLElement>('[data-progress]').forEach((el) => {
    const ids = (el.dataset.ids ?? '').split(',').filter(Boolean);
    const done = ids.filter((id) => solved.has(id)).length;
    const count = el.querySelector<HTMLElement>('[data-progress-count]');
    const bar = el.querySelector<HTMLElement>('[data-progress-bar]');
    if (count) count.textContent = String(done);
    if (bar) bar.style.width = ids.length ? `${(done / ids.length) * 100}%` : '0%';
    el.classList.toggle('is-complete', ids.length > 0 && done === ids.length);
  });
  document.querySelectorAll<HTMLElement>('[data-solved-marker]').forEach((el) => {
    el.classList.toggle('is-solved', solved.has(el.dataset.solvedMarker ?? ''));
  });
  document.querySelectorAll<HTMLInputElement>('[data-solved-toggle] input[data-id]').forEach((input) => {
    input.checked = solved.has(input.dataset.id ?? ''); // «Решено» могли отметить тесты на странице
  });
}

renderProgress();
document.addEventListener(SOLVED_EVENT, renderProgress);
window.addEventListener('storage', (e) => {
  if (e.key === SOLVED_KEY) document.dispatchEvent(new CustomEvent(SOLVED_EVENT));
});
