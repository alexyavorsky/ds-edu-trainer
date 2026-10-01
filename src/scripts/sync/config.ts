/**
 * Настройки Supabase из переменных окружения сборки (README, «Аккаунты и Supabase»).
 * Без PUBLIC_SUPABASE_URL и PUBLIC_SUPABASE_ANON_KEY вход не показывается и клиент Supabase не грузится.
 * Сюда — только публичный ключ (anon / publishable): он и так виден в браузере, доступ ограничивает RLS.
 * Service role key сайту не нужен; astro.config.mjs останавливает сборку, если его подставили сюда.
 */
export const SUPABASE_URL: string = import.meta.env.PUBLIC_SUPABASE_URL ?? '';
export const SUPABASE_ANON_KEY: string = import.meta.env.PUBLIC_SUPABASE_ANON_KEY ?? '';
export const ACCOUNTS_ENABLED = Boolean(SUPABASE_URL && SUPABASE_ANON_KEY);

/**
 * Supabase Auth требует почту, а вход у нас по логину: логин превращается в служебный адрес
 * «логин@LOGIN_DOMAIN». Писем на него не отправляется (подтверждение почты выключено). Менять домен
 * после появления пользователей нельзя — их адреса перестанут совпадать.
 */
export const LOGIN_DOMAIN = 'ds-edu-trainer.vercel.app';

/** 3–32 символа: латиница, цифры, «_» и «-», начинается с буквы или цифры. Регистр не важен. */
export const LOGIN_PATTERN = /^[a-z0-9][a-z0-9_-]{2,31}$/;
export const PASSWORD_MIN = 8;

export const normalizeLogin = (login: string) => login.trim().toLowerCase();
export const loginToEmail = (login: string) => `${normalizeLogin(login)}@${LOGIN_DOMAIN}`;
export const emailToLogin = (email: string | undefined) => (email ?? '').split('@')[0];
