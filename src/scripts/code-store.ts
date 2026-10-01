/**
 * Код задач и упражнений в localStorage: edu:code:v1:«id» = {code, starter, t}.
 *   id — задача («ga-find-term») или упражнение урока («np-first-array/add»);
 *   starter — хеш заготовки, от которой начат код; t — время изменения, мс (у старых записей задач его нет).
 * Код, совпадающий с заготовкой, не хранится. Сохранение без изменений ничего не пишет — иначе
 * открытая на втором устройстве страница перезаписала бы более новый код при уходе со страницы.
 */
import { noteChange } from './sync/pending';

const PREFIX = 'edu:code:v1:';
export const CODE_REMOTE_EVENT = 'edu:code-remote';

export interface SavedCode {
  code: string;
  starter: string;
  t?: number;
}

/** Событие CODE_REMOTE_EVENT: код пришёл с другого устройства (null — там вернули заготовку). */
export interface CodeRemoteDetail {
  id: string;
  saved: SavedCode | null;
}

export function loadCode(id: string): SavedCode | null {
  try {
    const raw = localStorage.getItem(PREFIX + id);
    return raw ? (JSON.parse(raw) as SavedCode) : null;
  } catch {
    return null;
  }
}

export function saveCode(id: string, saved: { code: string; starter: string } | null): void {
  const current = loadCode(id);
  const t = Date.now();
  try {
    if (saved) {
      if (current && current.code === saved.code && current.starter === saved.starter) return;
      localStorage.setItem(PREFIX + id, JSON.stringify({ code: saved.code, starter: saved.starter, t }));
    } else {
      if (!current) return;
      localStorage.removeItem(PREFIX + id);
    }
  } catch {
    return; /* приватный режим или переполненное хранилище — код просто не сохранится */
  }
  noteChange(`code:${id}`, id, t);
}

/** Записать код как есть (с его t) — для синхронизации, без постановки в очередь. */
export function putCode(id: string, saved: SavedCode | null): void {
  try {
    if (saved) localStorage.setItem(PREFIX + id, JSON.stringify(saved));
    else localStorage.removeItem(PREFIX + id);
  } catch {
    return;
  }
  document.dispatchEvent(new CustomEvent<CodeRemoteDetail>(CODE_REMOTE_EVENT, { detail: { id, saved } }));
}

export function listCodeIds(): string[] {
  const ids: string[] = [];
  try {
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith(PREFIX)) ids.push(key.slice(PREFIX.length));
    }
  } catch {
    /* хранилище недоступно */
  }
  return ids;
}

/**
 * Следить за кодом с другого устройства: onRemote вызывается, только если человек ещё не менял код
 * на этой странице (текущий код совпадает с тем, что был при открытии), — иначе его правки важнее,
 * а более свежая версия уйдёт в облако при следующем сохранении.
 */
export function watchRemoteCode(id: string, untouched: () => boolean, onRemote: (saved: SavedCode | null) => void): void {
  document.addEventListener(CODE_REMOTE_EVENT, (e) => {
    const { detail } = e as CustomEvent<CodeRemoteDetail>;
    if (detail.id === id && untouched()) onRemote(detail.saved);
  });
}
