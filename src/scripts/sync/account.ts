/**
 * Кнопка аккаунта в шапке и окно входа (components/Account.astro). Сам по себе лёгкий: клиент Supabase
 * (sync/cloud.ts) грузится, только когда человек вошёл или открыл окно входа.
 *
 * Когда синхронизировать: при открытии страницы, через пару секунд после изменения, при появлении сети,
 * при возвращении на вкладку (если прошло больше минуты) и при уходе с неё.
 */
import { PASSWORD_MIN } from './config';
import { PENDING_EVENT, readAccount, readPending } from './pending';
import type * as Cloud from './cloud';

type State = Cloud.SyncState | 'syncing';

const root = document.querySelector<HTMLElement>('[data-account]');
const dialog = document.querySelector<HTMLDialogElement>('[data-account-dialog]');
if (root && dialog) init(root, dialog);

function init(root: HTMLElement, dialog: HTMLDialogElement): void {
  let cloud: Promise<typeof Cloud> | null = null;
  const loadCloud = () => (cloud ??= import('./cloud'));
  const q = <T extends HTMLElement = HTMLElement>(s: string) => dialog.querySelector<T>(s)!;

  const label = root.querySelector<HTMLElement>('[data-account-label]')!;
  const authForm = q<HTMLFormElement>('[data-view="auth"]');
  const accountView = q('[data-view="account"]');
  const statusLine = q('[data-sync-status]');
  let mode: 'signin' | 'signup' = 'signin';
  let state: State = 'ok';
  let lastSync = 0;

  // ─── Отображение ──────────────────────────────────────────────────────────
  const STATUS: Record<State, string> = {
    ok: 'Прогресс и код сохраняются в облаке.',
    syncing: 'Синхронизация…',
    offline: 'Синхронизация недоступна — всё сохраняется в этом браузере и уйдёт в облако позже.',
    error: 'Синхронизация не удалась — всё сохраняется в этом браузере, повторим позже.',
    'signed-out': 'Сессия закончилась — войдите снова.',
  };

  function render(): void {
    const account = readAccount();
    root.hidden = false;
    label.textContent = account ? account.login : 'Войти';
    root.dataset.state = account ? (state === 'ok' && Object.keys(readPending()).length ? 'syncing' : state) : '';
    root.querySelector('button')!.setAttribute('aria-label', account ? `Аккаунт ${account.login}` : 'Войти или зарегистрироваться');
    authForm.hidden = Boolean(account);
    accountView.hidden = !account;
    if (account) {
      q('[data-account-login]').textContent = account.login;
      statusLine.textContent = STATUS[state];
      statusLine.classList.toggle('is-warn', state !== 'ok' && state !== 'syncing');
    }
  }

  // ─── Синхронизация ────────────────────────────────────────────────────────
  let timer: ReturnType<typeof setTimeout> | undefined;
  async function sync(): Promise<void> {
    clearTimeout(timer);
    if (!readAccount()) return;
    state = 'syncing';
    render();
    const api = await loadCloud();
    state = await api.sync();
    lastSync = Date.now();
    if (state === 'signed-out') showMessage('Сессия закончилась. Войдите снова — прогресс в этом браузере сохранён.');
    render();
  }
  const later = (ms: number) => {
    clearTimeout(timer);
    timer = setTimeout(() => void sync(), ms);
  };

  document.addEventListener(PENDING_EVENT, () => {
    render();
    later(2000);
  });
  window.addEventListener('online', () => void sync());
  document.addEventListener('visibilitychange', () => {
    if (!readAccount()) return;
    if (document.visibilityState === 'hidden' && Object.keys(readPending()).length) void sync();
    if (document.visibilityState === 'visible' && Date.now() - lastSync > 60_000) void sync();
  });
  window.addEventListener('storage', (e) => {
    if (e.key === 'edu:account:v1') render(); // вошли или вышли в другой вкладке
  });

  // ─── Окно ─────────────────────────────────────────────────────────────────
  const errorBox = q('[data-error]');
  const messageBox = q('[data-message]');
  function showMessage(text: string): void {
    messageBox.textContent = text;
    messageBox.hidden = !text;
  }
  function showError(box: HTMLElement, text: string): void {
    box.textContent = text;
    box.hidden = !text;
  }

  root.querySelector('button')!.addEventListener('click', () => {
    showError(errorBox, '');
    render();
    dialog.showModal();
    if (!readAccount()) {
      void loadCloud(); // заранее, пока человек вводит логин
      q<HTMLInputElement>('input[name="login"]').focus();
    }
  });
  dialog.querySelectorAll('[data-close]').forEach((b) => b.addEventListener('click', () => dialog.close()));
  dialog.addEventListener('click', (e) => {
    if (e.target === dialog) dialog.close(); // клик по фону
  });
  dialog.addEventListener('close', () => {
    showMessage('');
    dialog.querySelectorAll<HTMLDetailsElement>('details').forEach((d) => (d.open = false));
    dialog.querySelectorAll<HTMLInputElement>('input[type="password"]').forEach((i) => (i.value = ''));
  });

  // вход / регистрация
  const tabs = [...dialog.querySelectorAll<HTMLButtonElement>('[data-mode]')];
  const setMode = (next: typeof mode) => {
    mode = next;
    tabs.forEach((t) => t.setAttribute('aria-selected', String(t.dataset.mode === mode)));
    dialog.querySelectorAll<HTMLElement>('[data-signup-only]').forEach((el) => (el.hidden = mode !== 'signup'));
    q<HTMLInputElement>('input[name="password2"]').required = mode === 'signup';
    q<HTMLInputElement>('input[name="password"]').autocomplete = mode === 'signup' ? 'new-password' : 'current-password';
    q('[data-auth-title]').textContent = mode === 'signup' ? 'Регистрация' : 'Вход';
    q('[data-submit]').textContent = mode === 'signup' ? 'Зарегистрироваться' : 'Войти';
    showError(errorBox, '');
  };
  tabs.forEach((t) => t.addEventListener('click', () => setMode(t.dataset.mode as typeof mode)));
  setMode('signin');

  authForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = new FormData(authForm);
    const login = String(form.get('login') ?? '');
    const password = String(form.get('password') ?? '');
    if (mode === 'signup' && password !== String(form.get('password2') ?? '')) {
      showError(errorBox, 'Пароли не совпадают.');
      return;
    }
    const submit = q<HTMLButtonElement>('[data-submit]');
    submit.disabled = true;
    showError(errorBox, '');
    try {
      const api = await loadCloud();
      const result = mode === 'signup' ? await api.signUp(login, password) : await api.signIn(login, password);
      if (!result.ok) {
        showError(errorBox, result.error);
        return;
      }
      authForm.reset();
      showMessage(
        mode === 'signup'
          ? 'Аккаунт создан. Прогресс из этого браузера переносится в облако.'
          : 'Вы вошли. Прогресс из этого браузера и из облака объединяется.',
      );
      await sync();
    } catch {
      showError(errorBox, 'Сервер недоступен. Проверьте сеть или попробуйте позже.');
    } finally {
      submit.disabled = false;
    }
  });

  // аккаунт
  q('[data-sync-now]').addEventListener('click', () => void sync());
  q('[data-sign-out]').addEventListener('click', async () => {
    const api = await loadCloud();
    await api.signOut().catch(() => {});
    state = 'ok';
    setMode('signin');
    render();
  });

  const passwordForm = q<HTMLFormElement>('[data-password-form]');
  const passwordError = q('[data-password-error]');
  passwordForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = new FormData(passwordForm);
    const password = String(form.get('new') ?? '');
    if (password !== String(form.get('new2') ?? '')) return showError(passwordError, 'Пароли не совпадают.');
    if (password.length < PASSWORD_MIN) return showError(passwordError, `Пароль — не короче ${PASSWORD_MIN} символов.`);
    const button = passwordForm.querySelector<HTMLButtonElement>('button')!;
    button.disabled = true;
    try {
      const result = await (await loadCloud()).changePassword(password);
      if (!result.ok) return showError(passwordError, result.error);
      passwordForm.reset();
      showError(passwordError, '');
      passwordForm.closest('details')!.open = false;
      showMessage('Пароль изменён.');
    } finally {
      button.disabled = false;
    }
  });

  const deleteError = q('[data-delete-error]');
  q('[data-delete-account]').addEventListener('click', async (e) => {
    const button = e.currentTarget as HTMLButtonElement;
    button.disabled = true;
    try {
      const result = await (await loadCloud()).deleteAccount();
      if (!result.ok) return showError(deleteError, result.error);
      state = 'ok';
      setMode('signin');
      render();
      showMessage('Аккаунт и данные в облаке удалены. В этом браузере всё осталось.');
    } finally {
      button.disabled = false;
    }
  });

  render();
  if (readAccount()) {
    // не мешать загрузке страницы: синхронизация, когда браузер освободится
    const idle = window.requestIdleCallback ?? ((fn: () => void) => setTimeout(fn, 300));
    idle(() => void sync());
  }
}
