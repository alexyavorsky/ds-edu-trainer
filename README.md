# Тренажёр задач по книгам

Личный сайт для повторения материала: задачи строго по главам книги. Решать можно прямо на сайте — Python
выполняется в браузере (Pyodide), — или в своём редакторе: файл с тестами копируется одной кнопкой.
Сейчас есть «Грокаем алгоритмы» (1-е издание): 10 глав, 80 задач, справочник по NumPy 2.5 и pandas 3.0:
99 статей, 744 проверенных примера, и курсы с нуля — уроки-ноутбуки с упражнениями: NumPy (10 модулей,
43 урока) и pandas (12 модулей, 51 урок); программа — [docs/COURSES_PLAN.md](docs/COURSES_PLAN.md). Задачи по NumPy и pandas — «скоро».

## Быстрый старт

```bash
npm install
npm run dev          # http://localhost:4321
npm run validate     # проверка всех задач (Python 3.11+)
npm run build        # статическая сборка в dist/
```

Справочник (нужны NumPy и pandas зафиксированных версий — только для разработки):

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_reference.py            # выполнить все примеры и сверить вывод
.venv/bin/python scripts/validate_reference.py --update   # перезаписать вывод после правки примеров
.venv/bin/python scripts/validate_reference.py --retime   # заново снять замеры времени на этой машине
```

## Как добавить статью справочника

1. Добавьте slug в нужный раздел `reference/<тема>/topic.toml`.
2. Создайте `<slug>.mdx` по образцу `reference/numpy/broadcasting.mdx` и `<slug>.py` с ячейками `# %% id`.
3. Запустите `validate_reference.py <тема>/<slug> --update` — вывод впишется в `.py`, на сайте он появится сам.

## Как добавить урок курса

1. Создайте папку `courses/<курс>/<NN-модуль>/<NN-урок>/` с `lesson.mdx` (текст и места ячеек) и `lesson.py`
   (код ячеек) по образцу `courses/numpy/01-start/02-first-array/`. Формат — [docs/COURSES_PLAN.md](docs/COURSES_PLAN.md).
2. Запустите `node scripts/validate_courses.ts <id урока> --update` — урок выполнится в Pyodide и CPython,
   сохранённый вывод запишется в `output.json`.
3. Всё — урок появится в программе курса. Удалили папку — урок исчез.

## Как добавить задачу

1. Создайте папку `challenges/<книга>/<NN-глава>/<slug>/` с файлами:
   `meta.toml`, `task.md`, `starter.py`, `solution.py`, `tests.py`
   (для `type = "complexity"` — `meta.toml`, `task.md`, `code.py`).
   По желанию — `alt_solutions/` (другие корректные решения) и `mutants.toml` (типичные ошибки, которые тесты должны ловить).
2. Запустите `python3 scripts/validate.py --chapter <NN-глава>`. Задача, не прошедшая валидацию, считается несделанной.
3. Всё — задача появится на сайте. Удалили папку — задача исчезла.

Новая книга или тема — новая папка в `challenges/` с `book.toml`. Формат полей и приёмы в тестах — в
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Образец главы — `challenges/grokking-algorithms/03-recursion/`.

## Проверки

| Команда | Что проверяет |
| --- | --- |
| `python3 scripts/validate.py` | meta, файлы, решение проходит тесты, заготовка — нет, каждая ошибка fix-bug ловится отдельно |
| `python3 scripts/validate.py --bundle <папка> [--solution]` | печатает собранный файл, который копируется с сайта |
| `python3 scripts/validate.py --export bundles` и `python scripts/run_bundles.py bundles` | запуск всех эталонов и альтернатив как обычных скриптов (так делает CI на Windows/macOS/Linux × Python 3.10–3.14) |
| `npm run check:bundles` | сборка на сайте совпадает с проверенной сборкой байт в байт |
| `.venv/bin/python scripts/validate_reference.py --strict` | справочник: структура, ссылки, все примеры выполняются и дают показанный вывод и графики; замеры времени выполняются, но числа не сравниваются |
| `node scripts/validate_pyodide.ts` | то же в Python для браузера (Pyodide в Node.js): эталоны проходят, заготовки — нет; примеры справочника сверяются с `reference/browser.json` (`--update` — обновить) |
| `node scripts/validate_browsers.ts` | эталоны в Chromium, Firefox и WebKit (Playwright, после `npm run build`) и пробы глубины рекурсии: в Safari стек меньше всего |
| `node scripts/validate_courses.ts` | курсы: структура, понятия по порядку, каждый урок целиком с эталонами, заготовками, другими решениями и ошибками — в Pyodide и CPython; сохранённый вывод совпадает (`--update` — записать); ноутбук .ipynb выполняется |
| `npm run check` | типы TypeScript / Astro |
| `npm run test:supabase` | миграция Supabase в PGlite (Postgres в WebAssembly): каждый пользователь видит и меняет только свои строки, аноним — ничего, слияние записей по времени |

## Деплой

Vercel: импортировать репозиторий — Astro определяется автоматически. PDF книги в `.gitignore` и не публикуется.

## Аккаунты и Supabase

Без настройки сайт работает только с localStorage: кнопки «Войти» нет, код Supabase не загружается. После
настройки появляется необязательный вход по **логину и паролю** (без почты): прогресс, отметки «Решено» и код
задач и упражнений сохраняются в Supabase и доступны на других устройствах. Без входа всё по-прежнему хранится
только в браузере.

**Как устроено.**

- Вход — Supabase Auth. Почта ему обязательна, поэтому логин превращается в служебный адрес
  `логин@ds-edu-trainer.vercel.app` (`LOGIN_DOMAIN` в `src/scripts/sync/config.ts`). Писем на него не уходит.
  Домен нельзя менять, когда появились пользователи: их адреса перестанут совпадать.
- Данные — одна таблица `user_data` (`supabase/migrations/`): строка = ключ (`solved`, `course.ex`,
  `course.done`, `course.last`, `code:<id>`), значение = записи `{id: {…, t}}`, где `t` — время изменения.
  RLS: пользователь читает и удаляет только свои строки. Пишет только функция `merge_user_data`: она сливает
  записи по одной, побеждает более новая. Поэтому два устройства не затирают друг друга.
- В браузере localStorage остаётся основным хранилищем. После входа изменения попадают в очередь
  (`edu:sync:pending:v1`) и через пару секунд уходят в облако. Изменения из облака подтягиваются при
  открытии страницы и при возвращении на вкладку. При входе всё локальное сливается с облачным, поэтому
  накопленный без входа прогресс не теряется.
- Нет сети или проект спит — всё сохраняется в браузере, очередь уходит позже. У кнопки аккаунта появляется
  жёлтая точка.
- «Выйти» — локальные данные остаются. «Удалить аккаунт» — удаляет пользователя и его строки в облаке, в
  браузере всё остаётся.

### Создать и настроить проект

1. [supabase.com](https://supabase.com) → **New project**. Регион — ближайший к ученикам (например, Frankfurt).
   Пароль базы сохраните в менеджере паролей: сайту он не нужен.
2. **SQL Editor** → вставить содержимое `supabase/migrations/20261001000000_user_data.sql` → **Run**.
   Или через CLI: `npx supabase link --project-ref <ref>` и `npx supabase db push`.
3. **Authentication → Sign In / Providers**:
   - **Allow new users to sign up** — включено;
   - **Email** — включён; **Confirm email** — **выключено**: иначе регистрация будет ждать письма на
     служебный адрес, и войти не получится;
   - **Secure password change** — выключено: иначе смена пароля потребует подтверждения по почте;
   - **Minimum password length** — 8 (сайт тоже требует не меньше 8);
   - **Allow anonymous sign-ins** и остальные провайдеры — выключены.
4. **Project Settings → API Keys**: скопировать **Project URL** и **publishable key** (`sb_publishable_…`) или
   старый **anon** key. Это публичный ключ, он всё равно виден в браузере: доступ ограничивают политики RLS.

### Переменные в Vercel

**Project → Settings → Environment Variables**, окружения Production и Preview:

| Переменная | Значение |
| --- | --- |
| `PUBLIC_SUPABASE_URL` | `https://<ref>.supabase.co` |
| `PUBLIC_SUPABASE_ANON_KEY` | publishable или anon key |

Переменные подставляются при сборке, поэтому после их добавления нужен **Redeploy**. Для локальной проверки —
те же строки в файле `.env` (он в `.gitignore`).

**Service role key (secret key, `sb_secret_…`) не нужен ни сайту, ни сборке.** Его нельзя класть в
переменные Vercel, в `.env` и в репозиторий: он обходит RLS. Сборка остановится с ошибкой, если в
`PUBLIC_`-переменной окажется ключ с ролью `service_role` или секретный ключ, а также если такой ключ
найдётся в файлах `dist/` (`astro.config.mjs`).

Проверка после деплоя: на сайте появилась кнопка «Войти» → зарегистрироваться → отметить задачу «Решено».
В **Table Editor → user_data** появились строки (панель Supabase видит все строки, сайт — только свои).

### Сбросить пароль пользователю

Восстановления пароля по почте нет. Если ученик забыл пароль:

1. **Authentication → Users** — найти `логин@ds-edu-trainer.vercel.app`.
2. **SQL Editor** — задать временный пароль (не короче 8 символов):

   ```sql
   update auth.users
   set encrypted_password = extensions.crypt('временный-пароль', extensions.gen_salt('bf')),
       updated_at = now()
   where email = 'логин@ds-edu-trainer.vercel.app';
   ```

3. Передать временный пароль ученику: он входит и меняет пароль в меню аккаунта («Сменить пароль»).

Чтобы заодно выйти на всех устройствах ученика, удалите его сессии:
`delete from auth.sessions where user_id = (select id from auth.users where email = '…');`.
Уже выданный токен действует до конца срока (по умолчанию час).

Удалить пользователя: **Authentication → Users → Delete user**. Его строки `user_data` удалятся каскадом.

### Спящий проект

Бесплатный проект Supabase засыпает после недели без запросов. Сайт при этом работает как без входа и
сохраняет всё в браузере. Разбудить проект: **Restore project** в панели. Очереди изменений уйдут сами, когда
ученики откроют сайт.

### Проверка без проекта

- `npm run test:supabase` — миграция в PGlite: RLS и слияние (то же на настоящем Postgres —
  `supabase/tests/user_data.test.sql`, `npx supabase test db`, нужен Docker).
- `npm run mock:supabase` — локальная замена Supabase (Auth в памяти + та же миграция в PGlite) на порту 54329.
  Сборка с ней:
  `PUBLIC_SUPABASE_URL=http://127.0.0.1:54329 PUBLIC_SUPABASE_ANON_KEY=mock npm run build && npx astro preview`.
  `POST /__mock/offline?on=1` имитирует спящий проект, `GET /__mock/rows` показывает строки.
