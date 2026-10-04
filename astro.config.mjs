// @ts-check
import { readdirSync, readFileSync } from 'node:fs';
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

export default defineConfig({
  integrations: [mdx(), noSupabaseSecrets()],
  trailingSlash: 'ignore',
  // Задачи жили в корне сайта (/<книга>/<глава>/<задача>) — старые ссылки и закладки ведут на /tasks/…
  redirects: {
    '/[book]': '/tasks/[book]',
    '/[book]/[chapter]': '/tasks/[book]/[chapter]',
    '/[book]/[chapter]/[task]': '/tasks/[book]/[chapter]/[task]',
  },
  markdown: {
    shikiConfig: { theme: 'vitesse-dark', wrap: false },
  },
});
