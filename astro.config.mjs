// @ts-check
import { cpSync, existsSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import mdx from '@astrojs/mdx';
import { defineConfig } from 'astro/config';
import { loadEnv } from 'vite';

/**
 * Service role key Supabase обходит RLS — ему не место ни в браузере, ни в сборке. Ключ с ролью
 * service_role (JWT) или секретный ключ (sb_secret_…) в PUBLIC_-переменной останавливает сборку,
 * а готовые файлы dist/ проверяются на такие ключи (README, «Аккаунты и Supabase»).
 */
/** @param {string | undefined} value */
function isSecretKey(value) {
  if (!value) return false;
  if (value.startsWith('sb_secret_')) return true;
  const payload = value.split('.')[1];
  if (!payload) return false;
  try {
    return JSON.parse(Buffer.from(payload, 'base64url').toString()).role === 'service_role';
  } catch {
    return false;
  }
}

function noSupabaseSecrets() {
  const env = { ...loadEnv(process.env.NODE_ENV ?? 'production', process.cwd(), 'PUBLIC_'), ...process.env };
  const leaked = Object.keys(env).filter((name) => name.startsWith('PUBLIC_') && isSecretKey(env[name]));
  if (leaked.length) {
    throw new Error(`${leaked.join(', ')}: это секретный ключ Supabase (service role). Сайту нужен только anon / publishable key.`);
  }
  return {
    name: 'no-supabase-secrets',
    hooks: {
      /** @param {{ dir: URL }} options */
      'astro:build:done': ({ dir }) => {
        const root = fileURLToPath(dir);
        const jwt = /eyJ[\w-]+\.(eyJ[\w-]+)\.[\w-]+/g;
        /** @type {string[]} */
        const found = [];
        for (const file of readdirSync(root, { recursive: true, encoding: 'utf8' })) {
          if (!/\.(js|mjs|html|json)$/.test(file)) continue;
          const text = readFileSync(join(root, file), 'utf8');
          if (/sb_secret_[\w-]{20,}/.test(text) || [...text.matchAll(jwt)].some((m) => isSecretKey(`x.${m[1]}.x`))) found.push(file);
        }
        if (found.length) throw new Error(`В сборке найден секретный ключ Supabase: ${found.join(', ')}`);
      },
    },
  };
}

/**
 * Задачи жили в корне сайта (/<книга>/<глава>/<задача>), теперь — в /tasks/…. Старые ссылки и закладки
 * перенаправляются двумя способами:
 * - на Vercel — сервером (301, до поиска файлов, #якорь браузер сохраняет): на каждый раздел задач — папку
 *   challenges/<раздел>/ с book.toml — правило «/<раздел>/… → /tasks/<раздел>/…». Список разделов берётся из
 *   папок при сборке. vercel.json для этого не подходит: Vercel читает его до сборки. Поэтому на Vercel
 *   (переменная VERCEL) сборка выкладывается через Build Output API: dist/ копируется в .vercel/output/static,
 *   правила пишутся в .vercel/output/config.json. Локально ничего не пишется (проверить: VERCEL=1 npm run build);
 * - везде — страницами с <meta http-equiv="refresh"> (`redirects` ниже): запасной вариант для другого хостинга,
 *   astro dev и astro preview. На Vercel их закрывают правила 301.
 * Раздел задач с именем страницы или папки сайта (tasks, courses…) останавливает сборку: перенаправление закрыло бы её.
 */
function taskSections() {
  const root = fileURLToPath(new URL('./challenges/', import.meta.url));
  return readdirSync(root)
    .filter((name) => !/^[._]/.test(name) && statSync(join(root, name)).isDirectory() && existsSync(join(root, name, 'book.toml')))
    .sort();
}

function vercelTaskRedirects() {
  return {
    name: 'vercel-task-redirects',
    hooks: {
      'astro:config:setup': () => {
        const taken = new Set(
          ['./src/pages/', './public/'].flatMap((d) => readdirSync(new URL(d, import.meta.url)).map((n) => n.replace(/\.[^.]+$/, ''))),
        );
        const clash = taskSections().filter((s) => taken.has(s));
        if (clash.length) throw new Error(`Раздел задач совпадает с адресом страницы сайта: /${clash.join(', /')} — перенаправление его закроет`);
      },
      /** @param {{ dir: URL }} options */
      'astro:build:done': ({ dir }) => {
        if (!process.env.VERCEL) return;
        const dist = fileURLToPath(dir);
        const sections = taskSections();
        const output = fileURLToPath(new URL('./.vercel/output/', import.meta.url));
        rmSync(output, { recursive: true, force: true });
        mkdirSync(output, { recursive: true });
        cpSync(dist, join(output, 'static'), { recursive: true });
        const escape = (/** @type {string} */ s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const config = {
          version: 3,
          routes: [
            ...sections.map((s) => ({ src: `^/${escape(s)}(/.*)?$`, headers: { Location: `/tasks/${s}$1` }, status: 301 })),
            { src: '^/_astro/(.*)$', headers: { 'cache-control': 'public, max-age=31536000, immutable' }, continue: true },
            { handle: 'filesystem' },
            { src: '/.*', dest: '/404.html', status: 404 },
          ],
        };
        writeFileSync(join(output, 'config.json'), `${JSON.stringify(config, null, 2)}\n`);
      },
    },
  };
}

export default defineConfig({
  integrations: [mdx(), noSupabaseSecrets(), vercelTaskRedirects()],
  trailingSlash: 'ignore',
  // запасной вариант к правилам 301 на Vercel (vercelTaskRedirects выше)
  redirects: {
    '/[book]': '/tasks/[book]',
    '/[book]/[chapter]': '/tasks/[book]/[chapter]',
    '/[book]/[chapter]/[task]': '/tasks/[book]/[chapter]/[task]',
  },
  markdown: {
    shikiConfig: { theme: 'vitesse-dark', wrap: false },
  },
});
