/**
 * Очередь изменений для синхронизации с Supabase (README, «Аккаунты и Supabase»).
 *
 * Модули прогресса и кода зовут noteChange(ключ, запись) при каждом изменении. Если человек не вошёл
 * (нет edu:account:v1), ничего не происходит — сайт работает только с localStorage, как раньше.
 * Если вошёл — запись попадает в очередь edu:sync:pending:v1 и уходит в Supabase (scripts/sync/cloud.ts),
 * в том числе после перезагрузки страницы или появления сети.
 */
export const ACCOUNT_KEY = 'edu:account:v1';
const PENDING_KEY = 'edu:sync:pending:v1';
export const PENDING_EVENT = 'edu:sync-pending';

/** {ключ синхронизации: {id записи: время изменения, мс}} */
export type Pending = Record<string, Record<string, number>>;

export interface Account {
  id: string;
  login: string;
}

export function readAccount(): Account | null {
  try {
    const raw = localStorage.getItem(ACCOUNT_KEY);
    return raw ? (JSON.parse(raw) as Account) : null;
  } catch {
    return null;
  }
}

export function readPending(): Pending {
  try {
    const raw = localStorage.getItem(PENDING_KEY);
    return raw ? (JSON.parse(raw) as Pending) : {};
  } catch {
    return {};
  }
}

export function writePending(pending: Pending): void {
  try {
    if (Object.keys(pending).length) localStorage.setItem(PENDING_KEY, JSON.stringify(pending));
    else localStorage.removeItem(PENDING_KEY);
  } catch {
    /* хранилище недоступно — изменения уйдут при следующей полной синхронизации */
  }
}

export function noteChange(key: string, id: string, t = Date.now()): void {
  if (!readAccount()) return;
  const pending = readPending();
  (pending[key] ??= {})[id] = t;
  writePending(pending);
  document.dispatchEvent(new CustomEvent(PENDING_EVENT));
}
