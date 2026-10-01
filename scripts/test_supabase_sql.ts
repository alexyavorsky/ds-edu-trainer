/**
 * Проверка миграций supabase/migrations без проекта Supabase: Postgres в WebAssembly (PGlite)
 * с минимальной заменой того, что даёт Supabase (схема auth, auth.uid(), роли anon/authenticated).
 *
 *   node scripts/test_supabase_sql.ts
 *
 * Проверяет RLS (каждый видит и удаляет только свои строки, аноним — ничего, писать в таблицу напрямую
 * нельзя) и слияние записей в merge_user_data. Те же проверки на настоящем Postgres Supabase —
 * supabase/tests/user_data.test.sql (`supabase test db`).
 */
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { PGlite } from '@electric-sql/pglite';

const root = join(import.meta.dirname, '..');
const db = new PGlite();

await db.exec(`
  create role anon nologin;
  create role authenticated nologin;
  create schema auth;
  grant usage on schema auth to anon, authenticated;
  create table auth.users (id uuid primary key);
  create function auth.uid() returns uuid language sql stable as $$
    select (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')::uuid
  $$;
  grant usage on schema public to anon, authenticated;
`);
for (const file of readdirSync(join(root, 'supabase/migrations')).sort()) {
  await db.exec(readFileSync(join(root, 'supabase/migrations', file), 'utf8'));
}

const A = '00000000-0000-0000-0000-00000000000a';
const B = '00000000-0000-0000-0000-00000000000b';
await db.exec(`insert into auth.users values ('${A}'), ('${B}')`);

let failed = 0;
const check = (name: string, ok: boolean, detail = '') => {
  console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok || !detail ? '' : ` — ${detail}`}`);
  if (!ok) failed++;
};

/** Выполнить запросы от имени пользователя (или анонима) в отдельной транзакции. */
async function as<T>(user: string | null, fn: (q: (sql: string, params?: unknown[]) => Promise<{ rows: T[] }>) => Promise<void>) {
  await db.transaction(async (tx) => {
    await tx.query(`select set_config('request.jwt.claims', $1, true)`, [user ? JSON.stringify({ sub: user, role: 'authenticated' }) : '']);
    await tx.exec(`set local role ${user ? 'authenticated' : 'anon'}`);
    await fn((sql, params) => tx.query<T>(sql, params));
  });
}

async function fails(user: string | null, sql: string, params?: unknown[]): Promise<string | null> {
  try {
    await as(user, (q) => q(sql, params).then(() => undefined));
    return null;
  } catch (e) {
    return (e as Error).message;
  }
}

const merge = (user: string, data: unknown) =>
  as(user, (q) => q('select public.merge_user_data($1::jsonb)', [JSON.stringify(data)]).then(() => undefined));

type Row = { key: string; value: Record<string, { t: number; [k: string]: unknown }> };
async function rows(user: string): Promise<Row[]> {
  let result: Row[] = [];
  await as<Row>(user, async (q) => {
    result = (await q('select key, value from public.user_data order by key')).rows;
  });
  return result;
}

// ─── Запись и чтение своих строк ─────────────────────────────────────────────
await merge(A, {
  solved: { 'ga-find-term': { v: true, t: 100 }, 'ga-tile-ways': { v: true, t: 100 } },
  'course.ex': { 'np-first-array/add': { hash: 'h1', t: 50 } },
  'code:ga-find-term': { 'ga-find-term': { code: 'print(1)', starter: 's', t: 100 } },
});
await merge(B, { solved: { 'ga-digit-sum': { v: true, t: 10 } } });

const a = await rows(A);
check('A видит свои 3 строки', a.length === 3, JSON.stringify(a.map((r) => r.key)));
const b = await rows(B);
check('B видит только свою строку', b.length === 1 && b[0].key === 'solved' && 'ga-digit-sum' in b[0].value, JSON.stringify(b));

// ─── Слияние по записям ──────────────────────────────────────────────────────
await merge(A, {
  solved: {
    'ga-find-term': { v: false, t: 50 }, // старше — не применяется
    'ga-tile-ways': { v: false, t: 200 }, // новее — снимает отметку
    'ga-new': { v: true, t: 1 }, // новая запись
    broken: { v: true }, // без t — пропускается
  },
});
const solved = (await rows(A)).find((r) => r.key === 'solved')!.value;
check('старая запись не затирает новую', solved['ga-find-term'].v === true && solved['ga-find-term'].t === 100);
check('новая запись побеждает', solved['ga-tile-ways'].v === false && solved['ga-tile-ways'].t === 200);
check('новые записи добавляются, остальные сохраняются', 'ga-new' in solved && Object.keys(solved).length === 3);
check('запись без t пропускается', !('broken' in solved));

await merge(A, { 'code:ga-find-term': { 'ga-find-term': { d: true, t: 300 } } });
const code = (await rows(A)).find((r) => r.key === 'code:ga-find-term')!.value['ga-find-term'];
check('удаление кода (d) с более новым t побеждает', code.d === true && code.t === 300);

// ─── Запреты ─────────────────────────────────────────────────────────────────
let error = await fails(A, `insert into public.user_data (user_id, key, value) values ('${A}', 'solved', '{}')`);
check('прямой insert запрещён', error !== null && /permission denied/.test(error), error ?? 'прошёл');
error = await fails(A, `update public.user_data set value = '{}'`);
check('прямой update запрещён', error !== null && /permission denied/.test(error), error ?? 'прошёл');
let seen = -1;
await as<{ n: number }>(B, async (q) => {
  seen = (await q(`select count(*)::int as n from public.user_data where user_id = '${A}'`)).rows[0].n;
});
check('B не видит строк A даже по прямому фильтру', seen === 0);
let deleted = 0;
await as<{ n: number }>(B, async (q) => {
  deleted = (await q(`with d as (delete from public.user_data where user_id = '${A}' returning 1) select count(*)::int as n from d`)).rows[0].n;
});
check('B не может удалить строки A', deleted === 0 && (await rows(A)).length === 3);
error = await fails(null, 'select * from public.user_data');
check('аноним не читает таблицу', error !== null && /permission denied/.test(error), error ?? 'прошёл');
error = await fails(null, `select public.merge_user_data('{"solved": {"x": {"v": true, "t": 1}}}')`);
check('аноним не вызывает merge_user_data', error !== null, 'прошёл');
error = await fails(A, `select public.merge_user_data('{"other": {"x": {"t": 1}}}')`);
check('неизвестный ключ отклоняется', error !== null && /check constraint/.test(error), error ?? 'прошёл');
error = await fails(A, `select public.merge_user_data('{"code:ga-x": {"ga-x": {"code": "${'x'.repeat(300_000)}", "t": 1}}}')`);
check('слишком большая строка отклоняется', error !== null && /check constraint/.test(error), error ?? 'прошёл');

// ─── Удаление своих данных и аккаунта ────────────────────────────────────────
await as(B, (q) => q('delete from public.user_data').then(() => undefined));
check('B удаляет свои строки', (await rows(B)).length === 0 && (await rows(A)).length === 3);
await as(A, (q) => q('select public.delete_own_account()').then(() => undefined));
const left = await db.query<{ n: number }>('select count(*)::int as n from public.user_data');
const users = await db.query<{ id: string }>('select id from auth.users');
check('удаление аккаунта убирает пользователя и его строки', left.rows[0].n === 0 && users.rows.length === 1 && users.rows[0].id === B);

console.log(failed ? `\n${failed} проверок не прошло` : '\nвсе проверки прошли');
process.exit(failed ? 1 : 0);
