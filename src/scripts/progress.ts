/**
 * Статус «Решено» хранится только в localStorage этого браузера.
 * Любой элемент с data-progress / data-solved-marker обновляется автоматически.
 */
const KEY = 'edu:solved:v1';
export const SOLVED_EVENT = 'edu:solved-change';

export function getSolved(): Set<string> {
  try {
    const raw = localStorage.getItem(KEY);
    return new Set(raw ? (JSON.parse(raw) as string[]) : []);
  } catch {
    return new Set();
  }
}

export function setSolved(id: string, solved: boolean): void {
  const all = getSolved();
  if (solved) all.add(id);
  else all.delete(id);
  try {
    localStorage.setItem(KEY, JSON.stringify([...all]));
  } catch {
    /* приватный режим или отключённое хранилище — статус просто не сохранится */
  }
  document.dispatchEvent(new CustomEvent(SOLVED_EVENT));
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
}

renderProgress();
document.addEventListener(SOLVED_EVENT, renderProgress);
window.addEventListener('storage', (e) => {
  if (e.key === KEY) renderProgress();
});
