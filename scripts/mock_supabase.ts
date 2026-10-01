/**
 * Локальная замена Supabase для проверки входа и синхронизации без настоящего проекта.
 * Auth (регистрация, вход по паролю, обновление токена, смена пароля, выход) — упрощённый, в памяти;
 * REST (user_data, merge_user_data, delete_own_account) — настоящая миграция в PGlite с RLS.
 *
 *   node scripts/mock_supabase.ts [порт=54329]
 *   PUBLIC_SUPABASE_URL=http://127.0.0.1:54329 PUBLIC_SUPABASE_ANON_KEY=mock-anon-key npm run build && npx astro preview
 *
 * Служебное: GET /__mock/rows — все строки user_data; POST /__mock/offline?on=1|0 — имитация
 * недоступного (спящего) проекта: все запросы отвечают 503.
 * Только для разработки: токены не подписаны, пароли хранятся как есть.
 */
import { createServer, type IncomingMessage, type ServerResponse } from 'node:http';
import { randomUUID } from 'node:crypto';
import { readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { PGlite } from '@electric-sql/pglite';

const port = Number(process.argv[2] ?? 54329);
const root = join(import.meta.dirname, '..');
const db = new PGlite();
await db.exec(`
  create role anon nologin;
  create role authenticated nologin;
  create schema auth;
  grant usage on schema auth to anon, authenticated;
  create table auth.users (id uuid primary key, email text);
  create function auth.uid() returns uuid language sql stable as $$
    select (nullif(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')::uuid
  $$;
  grant usage on schema public to anon, authenticated;
`);
for (const file of readdirSync(join(root, 'supabase/migrations')).sort()) {
  await db.exec(readFileSync(join(root, 'supabase/migrations', file), 'utf8'));
}

interface User {
  id: string;
  email: string;
  password: string;
}
const users = new Map<string, User>(); // email → пользователь
const refresh = new Map<string, string>(); // refresh token → id
let offline = false;

const b64 = (o: unknown) => Buffer.from(JSON.stringify(o)).toString('base64url');
function session(user: User) {
  const exp = Math.floor(Date.now() / 1000) + 3600;
  const token = `${b64({ alg: 'HS256', typ: 'JWT' })}.${b64({ sub: user.id, role: 'authenticated', aud: 'authenticated', email: user.email, exp })}.mock`;
  const rt = randomUUID();
  refresh.set(rt, user.id);
  return { access_token: token, token_type: 'bearer', expires_in: 3600, expires_at: exp, refresh_token: rt, user: publicUser(user) };
}
const publicUser = (u: User) => ({
  id: u.id,
  aud: 'authenticated',
  role: 'authenticated',
  email: u.email,
  app_metadata: { provider: 'email' },
  user_metadata: {},
  created_at: new Date().toISOString(),
});

function userFromToken(req: IncomingMessage): User | null {
  const token = (req.headers.authorization ?? '').replace(/^Bearer /, '');
  try {
    const { sub, exp } = JSON.parse(Buffer.from(token.split('.')[1], 'base64url').toString());
    if (exp * 1000 < Date.now()) return null;
    return [...users.values()].find((u) => u.id === sub) ?? null;
  } catch {
    return null;
  }
}

async function asUser<T>(user: User | null, sql: string, params: unknown[] = []): Promise<T[]> {
  return db.transaction(async (tx) => {
    await tx.query(`select set_config('request.jwt.claims', $1, true)`, [user ? JSON.stringify({ sub: user.id, role: 'authenticated' }) : '']);
    await tx.exec(`set local role ${user ? 'authenticated' : 'anon'}`);
    return (await tx.query<T>(sql, params)).rows;
  });
}

function send(res: ServerResponse, status: number, body?: unknown): void {
  res.writeHead(status, { 'content-type': 'application/json', 'x-supabase-api-version': '2024-01-01' });
  res.end(body === undefined ? '' : JSON.stringify(body));
}
const authError = (res: ServerResponse, status: number, code: string, msg: string) => send(res, status, { code: status, error_code: code, msg });

async function body(req: IncomingMessage): Promise<Record<string, unknown>> {
  const chunks: Buffer[] = [];
  for await (const c of req) chunks.push(c as Buffer);
  const text = Buffer.concat(chunks).toString();
  return text ? JSON.parse(text) : {};
}

const server = createServer(async (req, res) => {
  res.setHeader('access-control-allow-origin', '*');
  res.setHeader('access-control-allow-headers', '*');
  res.setHeader('access-control-allow-methods', 'GET,POST,PUT,PATCH,DELETE,OPTIONS');
  res.setHeader('access-control-expose-headers', 'content-range, x-supabase-api-version');
  if (req.method === 'OPTIONS') return send(res, 204);
  const url = new URL(req.url!, `http://${req.headers.host}`);
  const path = url.pathname;
  try {
    if (path === '/__mock/offline') {
      offline = url.searchParams.get('on') === '1';
      return send(res, 200, { offline });
    }
    if (path === '/__mock/rows') return send(res, 200, (await db.query('select user_id, key, value, updated_at from public.user_data order by key')).rows);
    if (offline) return send(res, 503, { message: 'project paused' });

    // ─── Auth ───
    if (path === '/auth/v1/signup' && req.method === 'POST') {
      const { email, password } = (await body(req)) as { email: string; password: string };
      if (users.has(email)) return authError(res, 422, 'user_already_exists', 'User already registered');
      if (String(password).length < 8) return authError(res, 422, 'weak_password', 'Password should be at least 8 characters.');
      const user = { id: randomUUID(), email, password };
      users.set(email, user);
      await db.query('insert into auth.users (id, email) values ($1, $2)', [user.id, email]);
      return send(res, 200, session(user));
    }
    if (path === '/auth/v1/token' && req.method === 'POST') {
      const data = await body(req);
      if (url.searchParams.get('grant_type') === 'password') {
        const user = users.get(String(data.email));
        if (!user || user.password !== data.password) return authError(res, 400, 'invalid_credentials', 'Invalid login credentials');
        return send(res, 200, session(user));
      }
      const id = refresh.get(String(data.refresh_token));
      const user = [...users.values()].find((u) => u.id === id);
      if (!user) return authError(res, 400, 'refresh_token_not_found', 'Invalid Refresh Token');
      return send(res, 200, session(user));
    }
    if (path === '/auth/v1/user') {
      const user = userFromToken(req);
      if (!user) return authError(res, 401, 'bad_jwt', 'invalid JWT');
      if (req.method === 'PUT') {
        const { password } = (await body(req)) as { password?: string };
        if (password !== undefined) {
          if (password === user.password) return authError(res, 422, 'same_password', 'New password should be different');
          user.password = password;
        }
      }
      return send(res, 200, publicUser(user));
    }
    if (path === '/auth/v1/logout') return send(res, 204);

    // ─── REST ───
    const user = userFromToken(req);
    if (path === '/rest/v1/user_data' && req.method === 'GET') {
      const params: unknown[] = [];
      let where = '';
      const gt = url.searchParams.get('updated_at');
      if (gt?.startsWith('gt.')) {
        params.push(gt.slice(3));
        where = `where updated_at > $${params.length}`;
      }
      const limit = Number(url.searchParams.get('limit') ?? 1000);
      const offset = Number(url.searchParams.get('offset') ?? 0);
      const rows = await asUser(user, `select key, value, updated_at from public.user_data ${where} order by updated_at, key limit ${limit} offset ${offset}`, params);
      return send(res, 200, rows);
    }
    if (path === '/rest/v1/user_data' && req.method === 'DELETE') {
      await asUser(user, 'delete from public.user_data');
      return send(res, 204);
    }
    if (path === '/rest/v1/rpc/merge_user_data' && req.method === 'POST') {
      const { p_data } = await body(req);
      await asUser(user, 'select public.merge_user_data($1::jsonb)', [JSON.stringify(p_data)]);
      return send(res, 204);
    }
    if (path === '/rest/v1/rpc/delete_own_account' && req.method === 'POST') {
      await asUser(user, 'select public.delete_own_account()');
      if (user) users.delete(user.email);
      return send(res, 204);
    }
    return send(res, 404, { message: `mock: ${req.method} ${path}` });
  } catch (e) {
    const err = e as { code?: string; message?: string };
    return send(res, err.code === '42501' ? 401 : 400, { code: err.code, message: err.message });
  }
});
server.listen(port, '127.0.0.1', () => console.log(`mock supabase: http://127.0.0.1:${port}`));
