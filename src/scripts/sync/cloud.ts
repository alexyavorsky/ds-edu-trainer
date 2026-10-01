/**
 * Клиент Supabase: вход, регистрация и синхронизация. Отдельный чанк — грузится, только если Supabase
 * настроен и человек вошёл или нажал «Войти» (scripts/sync/account.ts).
 *
 * Синхронизация (sync):
 *   1. забрать из облака строки, изменённые после прошлого раза (при входе — все), и применить записи,
 *      которые новее локальных;
 *   2. отправить очередь изменений (sync/pending.ts) в merge_user_data — сервер сливает по записям.
 * При входе в очередь попадает всё локальное: накопленный без входа прогресс не теряется.
 * Повтор безопасен: и слияние на сервере, и применение здесь идемпотентны.
 */
import { createClient, type SupabaseClient } from '@supabase/supabase-js';
import {
  emailToLogin,
  LOGIN_PATTERN,
  loginToEmail,
  normalizeLogin,
  PASSWORD_MIN,
  SUPABASE_ANON_KEY,
  SUPABASE_URL,
} from './config';
import { allLocalKeys, applyRemote, KEY_PATTERN, localEntries, type Entries } from './local';
import { ACCOUNT_KEY, readAccount, readPending, writePending, type Account, type Pending } from './pending';

const CURSOR_KEY = 'edu:sync:cursor:v1';
/** Перекрытие окна чтения: строки, записанные чуть раньше прошлого чтения, но позже видимые. */
const OVERLAP_MS = 5 * 60_000;
/** Предел одного запроса записи (байт JSON) и одной записи кода. */
const BATCH_BYTES = 400_000;
const ENTRY_BYTES = 200_000;
/** Строк за запрос чтения (у PostgREST в Supabase по умолчанию не больше 1000). */
const PAGE = 500;

let client: SupabaseClient | null = null;
const supabase = () =>
  (client ??= createClient(SUPABASE_URL, SUPABASE_ANON_KEY, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: false },
  }));

export type Result = { ok: true } | { ok: false; error: string };
export type SyncState = 'ok' | 'offline' | 'signed-out' | 'error';

// ─── Вход ───────────────────────────────────────────────────────────────────

function validate(login: string, password: string): string | null {
  if (!LOGIN_PATTERN.test(normalizeLogin(login)))
    return 'Логин: 3–32 символа — латинские буквы, цифры, «_» и «-», начинается с буквы или цифры.';
  if (password.length < PASSWORD_MIN) return `Пароль — не короче ${PASSWORD_MIN} символов.`;
  return null;
}

function authMessage(error: { code?: string; status?: number; message?: string; name?: string }): string {
  const code = error.code ?? '';
  if (code === 'invalid_credentials') return 'Неверный логин или пароль.';
  if (code === 'user_already_exists' || code === 'email_exists') return 'Такой логин уже занят.';
  if (code === 'weak_password') return 'Пароль слишком простой — возьмите длиннее или сложнее.';
  if (code.includes('rate_limit') || error.status === 429) return 'Слишком много попыток. Подождите несколько минут.';
  if (code === 'signup_disabled') return 'Регистрация сейчас выключена.';
  if (code === 'email_not_confirmed' || code === 'email_address_invalid')
    return 'Вход не настроен до конца: в Supabase включено подтверждение почты (см. README).';
  if (error.name === 'AuthRetryableFetchError' || !error.status) return 'Сервер недоступен. Проверьте сеть или попробуйте позже.';
  return 'Не получилось. Попробуйте ещё раз.';
}

function remember(user: { id: string; email?: string }): Account {
  const account = { id: user.id, login: emailToLogin(user.email) };
  localStorage.setItem(ACCOUNT_KEY, JSON.stringify(account));
  localStorage.removeItem(CURSOR_KEY); // первый проход после входа — полный
  return account;
}

export async function signIn(login: string, password: string): Promise<Result> {
  const invalid = validate(login, password);
  if (invalid) return { ok: false, error: invalid };
  const { data, error } = await supabase().auth.signInWithPassword({ email: loginToEmail(login), password });
  if (error || !data.user) return { ok: false, error: authMessage(error ?? {}) };
  remember(data.user);
  return { ok: true };
}

export async function signUp(login: string, password: string): Promise<Result> {
  const invalid = validate(login, password);
  if (invalid) return { ok: false, error: invalid };
  const { data, error } = await supabase().auth.signUp({ email: loginToEmail(login), password });
  if (error) return { ok: false, error: authMessage(error) };
  // без сессии — в проекте включено подтверждение почты: письмо уйдёт в никуда, войти не выйдет
  if (!data.session || !data.user) return { ok: false, error: authMessage({ code: 'email_not_confirmed', status: 400 }) };
  remember(data.user);
  return { ok: true };
}

/** Выйти на этом устройстве. Локальные данные остаются — сайт работает как без входа. */
export async function signOut(): Promise<void> {
  try {
    await supabase().auth.signOut({ scope: 'local' });
  } finally {
    forget();
  }
}

function forget(): void {
  localStorage.removeItem(ACCOUNT_KEY);
  localStorage.removeItem(CURSOR_KEY);
  writePending({});
}

/** Есть ли действующая сессия; если нет (истекла, вышли в другой вкладке) — забыть вход. */
export async function checkSession(): Promise<boolean> {
  const { data, error } = await supabase().auth.getSession();
  // сеть или спящий проект при обновлении токена — это не выход: пусть sync сочтёт это офлайном
  if (error && (error.name === 'AuthRetryableFetchError' || !error.status || error.status >= 500)) throw error;
  const account = readAccount();
  if (data.session && account && data.session.user.id === account.id) return true;
  if (data.session && !account) remember(data.session.user);
  else if (!data.session) forget();
  return Boolean(data.session);
}

export async function changePassword(password: string): Promise<Result> {
  if (password.length < PASSWORD_MIN) return { ok: false, error: `Пароль — не короче ${PASSWORD_MIN} символов.` };
  const { error } = await supabase().auth.updateUser({ password });
  if (error) return { ok: false, error: error.code === 'same_password' ? 'Это ваш текущий пароль.' : authMessage(error) };
  return { ok: true };
}

/** Удалить аккаунт и все его данные в облаке. Данные в этом браузере остаются. */
export async function deleteAccount(): Promise<Result> {
  const { error } = await supabase().rpc('delete_own_account');
  if (error) return { ok: false, error: 'Не получилось удалить аккаунт. Попробуйте позже.' };
  await signOut();
  return { ok: true };
}

// ─── Синхронизация ──────────────────────────────────────────────────────────

let running: Promise<SyncState> | null = null;
let again = false;

/** Синхронизировать; параллельные вызовы ждут текущий проход, затем выполняется ещё один. */
export function sync(): Promise<SyncState> {
  if (running) {
    again = true;
    return running;
  }
  running = (async () => {
    let state: SyncState;
    do {
      again = false;
      state = await syncOnce();
    } while (again && state === 'ok');
    return state;
  })().finally(() => (running = null));
  return running;
}

async function syncOnce(): Promise<SyncState> {
  const account = readAccount();
  if (!account) return 'signed-out';
  try {
    if (!(await checkSession())) return 'signed-out';
    const db = supabase();

    // 1. Забрать изменения из облака
    let cursor: string | null = null;
    try {
      const saved = JSON.parse(localStorage.getItem(CURSOR_KEY) ?? 'null') as { user: string; at: string } | null;
      if (saved?.user === account.id) cursor = saved.at;
    } catch {
      /* нет курсора — полный проход */
    }
    const full = cursor === null;
    const since = cursor ? new Date(Date.parse(cursor) - OVERLAP_MS).toISOString() : null;
    let latest = cursor;
    for (let from = 0; ; from += PAGE) {
      let query = db.from('user_data').select('key, value, updated_at').order('updated_at').order('key');
      if (since) query = query.gt('updated_at', since);
      const { data: rows, error, status } = await query.range(from, from + PAGE - 1);
      if (error) return failure({ ...error, status });
      for (const row of rows as { key: string; value: Record<string, unknown>; updated_at: string }[]) {
        applyRemote(row.key, row.value);
        if (!latest || Date.parse(row.updated_at) > Date.parse(latest)) latest = row.updated_at;
      }
      if (rows.length < PAGE) break;
    }

    // 2. При первом проходе — отправить всё локальное
    if (full) {
      const pending = readPending();
      for (const key of allLocalKeys()) {
        for (const [id, entry] of Object.entries(localEntries(key))) (pending[key] ??= {})[id] ??= entry.t;
      }
      writePending(pending);
    }

    // 3. Отправить очередь
    const sent = await push();
    if (sent !== true) return sent;
    // в облаке пусто — следующий проход читает всё, но уже не отправляет всё заново
    localStorage.setItem(CURSOR_KEY, JSON.stringify({ user: account.id, at: latest ?? new Date(0).toISOString() }));
    return 'ok';
  } catch (e) {
    return failure(e);
  }
}

async function push(): Promise<true | SyncState> {
  const snapshot = readPending();
  const batches: { data: Record<string, Entries>; ids: Pending }[] = [];
  let batch = { data: {} as Record<string, Entries>, ids: {} as Pending };
  let size = 0;
  const dropped: Pending = {};

  for (const [key, ids] of Object.entries(snapshot)) {
    const local = localEntries(key);
    for (const [id, t] of Object.entries(ids)) {
      // нет локально: у кода — удалён (вернули заготовку), у остального — нечего отправлять
      const entry = local[id] ?? (key.startsWith('code:') ? { d: true, t } : null);
      const bytes = entry ? JSON.stringify(entry).length : 0;
      if (!entry || !KEY_PATTERN.test(key) || bytes > ENTRY_BYTES) {
        (dropped[key] ??= {})[id] = t;
        continue;
      }
      if (size + bytes > BATCH_BYTES && size > 0) {
        batches.push(batch);
        batch = { data: {}, ids: {} };
        size = 0;
      }
      (batch.data[key] ??= {})[id] = entry;
      (batch.ids[key] ??= {})[id] = t;
      size += bytes + key.length + id.length;
    }
  }
  if (size > 0) batches.push(batch);

  const done = (ids: Pending) => {
    const pending = readPending();
    for (const [key, entries] of Object.entries(ids)) {
      for (const [id, t] of Object.entries(entries)) if (pending[key]?.[id] === t) delete pending[key][id];
      if (pending[key] && !Object.keys(pending[key]).length) delete pending[key];
    }
    writePending(pending);
  };
  done(dropped);

  for (const b of batches) {
    const { error, status } = await supabase().rpc('merge_user_data', { p_data: b.data });
    if (error) return failure({ ...error, status });
    done(b.ids);
  }
  return true;
}

function failure(error: unknown): SyncState {
  const e = error as { message?: string; code?: string; status?: number; name?: string };
  // сеть, спящий проект Supabase, таймаут — повторим позже; очередь сохранена
  if (
    e?.name === 'TypeError' ||
    e?.name === 'AuthRetryableFetchError' ||
    e?.status === 0 ||
    (e?.status ?? 0) >= 500 ||
    /fetch|network|timeout/i.test(e?.message ?? '') ||
    !navigator.onLine
  )
    return 'offline';
  if (e?.code === 'PGRST301' || e?.status === 401) {
    forget();
    return 'signed-out';
  }
  console.warn('Синхронизация не удалась:', error);
  return 'error';
}

export function currentLogin(): string | null {
  return readAccount()?.login ?? null;
}
