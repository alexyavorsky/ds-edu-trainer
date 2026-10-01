# Поток 0.1 «Закрыть курс pandas» — отчёт

Ветка `pandas-finish` (от origin/main). PR не открывался.

## Что сделано

1. **Скрытие сохранённого вывода ниже нерешённого упражнения** (платформа курсов, оба курса).
2. **Мини-проект очистки — два урока:** `pd-project-clean` (часть 1, прежний id) и `pd-project-clean-2` (часть 2).
3. **COURSES_PLAN.md / README.md:** программа pandas — 51 урок, модуль 4 с двумя уроками проекта, описание
   `project-climate` сверено с уроком.
4. **Лимит 5 минут на урок в `validate_browsers.ts`** с понятной ошибкой; остальные уроки проверяются дальше.

## Как устроено скрытие

- `<Demo>` на сборке помечает `data-gated` ячейку с сохранённым выводом, если перед ней в lesson.mdx есть
  хотя бы одно упражнение, и выводит плашку «Вывод появится, когда решите упражнения выше — чтобы он не
  подсказал ответ» с кнопками «Показать всё равно» (эта ячейка) и «Весь вывод урока» (все ячейки урока).
- Встроенный скрипт страницы урока (`<script is:inline>` перед `<article>`) ставит `html.gate-on` до
  разметки ячеек; CSS прячет помеченный вывод и показывает плашку. Поэтому ответ не мелькает, пока грузится
  модуль страницы.
- `lesson.ts` (`renderGate`): идёт по ячейкам урока; ячейка получает `is-unlocked`, если все упражнения выше
  решены (`progress.isSolved`, localStorage `edu:course:v1`). Пересчёт — при событии прогресса (решено
  упражнение в этой вкладке) и при `storage` (другая вкладка, будущая синхронизация).
- Живой вывод виден всегда: `showLive` ставит `has-live` (плашка скрыта), выполненная ячейка получает
  `is-open` — после «Вернуть» или «Перезапустить» её сохранённый вывод уже не прячется.
- Вторая кнопка «Весь вывод урока» нужна: тому, кто повторяет урок или читает его без решения, нажимать
  «Показать» у каждой ячейки неудобно. Действует до перезагрузки страницы (не сохраняется: решённые упражнения
  и так снимают скрытие навсегда).
- **Без JS вывод виден.** Без JS упражнение не решить — скрытый вывод остался бы скрытым навсегда; страница
  без JS — учебник для чтения, где сохранённый вывод и есть результат. Ноутбук .ipynb не затронут.
- Вопросы (`<Quiz>`) не скрывают вывод: у них нет отметки «решено» в прогрессе, а ответ на вопрос вывод
  демонстрации не раскрывает.

Проверено в Chromium через Playwright на `/courses/pandas/project-clean-2` (production-сборка, `astro preview`):
без JS — все 5 выводов видны; с JS и пустым прогрессом — открыт только `prepare` (выше нет упражнений),
4 скрыты с плашкой; «Показать всё равно» открывает одну ячейку; отметки `signup` и `points` в localStorage →
открыты `bonus-before` и `dups`, `check` и `summary` скрыты; «Весь вывод урока» открывает всё; живой запуск
`dups` (с автозапуском ячеек выше) показывает живой вывод; настоящее решение `signup` в редакторе → `bonus-before`
открылся сразу, без перезагрузки. На 375 px плашка переносится, горизонтальной прокрутки нет.

## Мини-проект очистки

- Часть 1 `pd-project-clean` (15 мин, 3 упражнения: `ids`, `city`, `email`): осмотр выгрузки, коды и имена,
  города и сегменты, почта; новая демонстрация `text-done` «Что изменила очистка текста» — 240 кодов, 5 городов,
  3 сегмента, полных повторов 12; текст объясняет, почему дубли удаляются только во второй части.
- Часть 2 `pd-project-clean-2` (20 мин, 4 упражнения: `signup`, `points`, `dedupe`, `report`): ячейка
  «Подготовка» (`prepare`) — шаги части 1 одним блоком; даты, баллы (с «Типичной ошибкой» про `coerce`), дубли,
  сверка с эталоном, ответ, выводы. Шаги перенумерованы, ссылка на `info` из части 1 поправлена.
- Почта перенесена в часть 1: это тоже очистка текста (план «текст → даты → числа → дубли» сохранён).
- Прогресс: у `pd-project-clean` остаются упражнения `ids`, `city`, `email`; отметки `signup`/`points`/`dedupe`/
  `report` старого урока остаются в localStorage под старым ключом и в новом уроке не засчитываются (другой id
  урока) — ученикам, прошедшим проект, придётся решить их заново во второй части. Отметка «урок пройден» первой
  части сохраняется.
- output.json обоих уроков — только `validate_courses.ts <id> --update`.

## Лимит урока в проверке браузеров

- `browser-check.html`: каждый урок (вместе с запуском Python и пакетов) гоняется наперегонки с таймером
  `lessonTimeout`; при превышении воркер завершается, в результат идёт запись `lesson-timeout` с последней
  начатой ячейкой, её видом и прошедшим временем; проверка переходит к следующему уроку.
- `validate_browsers.ts`: `LESSON_TIMEOUT = 5 * 60`, `--lesson-timeout <с>` для проверки механизма; сообщение
  `chromium: урок pd-first-table не уложился в 4 с — остановлен на ячейке «load» (последняя начатая), прошло 4 с`;
  в итоге «остановлено по времени: N», код выхода 1. Дополнительно: ошибка JS на странице проверки теперь
  обрывает ожидание сразу (раньше — 30 минут тишины), а при превышении общего лимита (30 мин) в ошибке
  последние строки журнала страницы.
- Решение «продолжать»: один зависший урок не должен прятать ошибки в остальных; итог всё равно красный.

## Проверки

| Команда | Итог |
| --- | --- |
| `node scripts/validate_courses.ts pandas --python …/edu-platform/.venv/bin/python` | ✓ 51 урок, 874 прогона (60 с); предупреждения только о `minutes: 25` у итоговых уроков (было и раньше) |
| `npm run check` | 0 ошибок, 0 предупреждений |
| `npm run build` | 294 страницы |
| `node scripts/validate_browsers.ts chromium --only <51 id pandas>` | ✓ уроки 51 из 51 (ячеек 679), 224 с |
| `… chromium --only pd-project-clean,pd-project-clean-2,pd-first-table --lesson-timeout 4` | ожидаемо ✗: первый урок остановлен по времени с сообщением выше, два следующих прошли |
| Playwright-сценарий скрытия вывода (см. выше) | все состояния как задумано |

Firefox/WebKit локально не запускались (известно). .venv — основного checkout.

## Изменённые места (для ревью)

- `courses/pandas/04-clean/06-project-clean/{lesson.mdx, lesson.py, output.json}` — часть 1.
- `courses/pandas/04-clean/07-project-clean-2/{lesson.mdx, lesson.py, output.json}` — новый урок, часть 2.
- `src/components/course/Demo.astro` — `data-gated`, плашка с двумя кнопками.
- `src/scripts/course/lesson.ts` — `initGate`/`renderGate` в `Lesson`, классы `has-live`/`is-open` в `DemoView`.
- `src/scripts/course/progress.ts` — экспорт `STORE_KEY` (для события `storage`).
- `src/pages/courses/[course]/[lesson].astro` — встроенный скрипт `gate-on` перед `<article>` (вне списка
  разрешённых каталогов, но это страница урока платформы курсов; без него вывод мелькал бы до загрузки модуля).
- `src/styles/course.css` — стили `.out-gate` и правила скрытия (тоже вне списка; стили страницы урока).
- `scripts/browser-check.html` — лимит на урок (файл страницы проверки для `validate_browsers.ts`).
- `scripts/validate_browsers.ts` — `LESSON_TIMEOUT`, `--lesson-timeout`, сообщение, итог, `pageerror`, журнал.
- `docs/COURSES_PLAN.md` — программа pandas (51 урок, модуль 4, `project-climate`), «Ячейки и состояние»,
  «Интерфейс», «Проверка».
- `docs/ARCHITECTURE.md` — «Курсы»: лимит урока и скрытие вывода.
- `README.md` — 51 урок pandas.

## Открытые вопросы

- Потеря отметок упражнений второй части у тех, кто уже прошёл проект (см. выше). Можно перенести отметки
  `pd-project-clean/{signup,points,dedupe,report}` → `pd-project-clean-2/…` одноразовой миграцией в `progress.ts`
  (и в Supabase) — не делал, нужно решение.
- В README таблица «Проверки» не упоминает лимит урока — описано в COURSES_PLAN.md и ARCHITECTURE.md.

## По повторному ревью

Отчёты: `pandas-finish-review-a.md` (А) и `pandas-finish-review-b.md` (Б). Решения оркестратора — в брифе.

### Скрытие ответа — точечнее (Б: В1, В3, М1–М4)

- **Диапазон.** Скрыт сохранённый вывод демонстраций в разделе упражнения: после него до ближайшего заголовка
  `#`/`##` или следующего упражнения (`demoGates` в `src/lib/courses/format.ts`, на сборке). Не скрываются
  `[raises]` (показ ошибки) и `<Demo … gate="off" />`. Пометка `gate="off"` поставлена у 19 демонстраций pandas,
  где в разделе упражнения идёт новый материал (например, `no-parens`, `columns` в first-table, `weekday`
  в dates, `min-periods` в rolling). Итог: скрыт вывод 21 демонстрации pandas из 428 (было ~280) —
  «витрины» результата: `*-view` в проектах, `coerce-rows`, `fixed-look`, `doubles-view` и т. п.
- **Открытие** — решено «своё» упражнение или урок отмечен пройденным (в том числе вручную, М2; снятие отметки
  снова скрывает). Открытая выполнением ячейка остаётся открытой до перезагрузки — записано в COURSES_PLAN (М4).
- **Плашка называет упражнение** (М1): «Вывод появится, когда решите упражнение «Типы дней», — иначе он
  подскажет ответ. Ячейку можно и выполнить.» Общий компонент `GatePlaque.astro`.
- **Без модуля урока** (В3): встроенный скрипт страницы (`define:vars` с id урока) ставит `gate-on`, читает
  `edu:course:v1` и через `MutationObserver` ставит `is-unlocked` решённому ещё до отрисовки (М3 — без
  мелькания), и сам обрабатывает кнопки плашек (делегирование `click`). `lesson.ts` только пересчитывает при
  решении и отметке урока (`renderGate`).
- **Текст с ответом** (А1–А3, Б: В2) — новый компонент `<After id="упражнение">…</After>` (`After.astro`,
  `TEXT_COMPONENTS` в format.ts; в ноутбуке — текст с пометкой «После решения упражнения выше»; валидатор
  требует упражнение выше и текст внутри; `gate` у Demo — только `"off"`).

### Ответы в тексте под упражнениями (весь курс pandas)

Поиск скриптом: абзацы и блоки после `</Exercise>` до заголовка — с цифрами и числительными; затем по месту.
- В `<After>` (26 мест): dates `weekend`, `combine`; duplicates `clean`; stats `typical`, `spread`; shares
  `ratings`, `buyers`; cut `speed`; project-climate `prep`, `compare`, `kinds`, `rain`; groupby `category`;
  agg `channels`; transform `anomaly`; project-channels `metrics`, `mix`; crosstab `happy`; project-grades
  `groups`; merge `priced`, `segments`; merge-keys `returned`; rolling `smooth`; weather-sales `corr-day`
  (два абзаца), `monthly`; plot `temps`.
- Переписано без чисел: project-clean `ids` (А2), project-clean-2 `signup` (А1), project-cities — новый абзац
  на других масках, вторая подсказка короче, «Типичная ошибка» в общем виде `маска_А[маска_Б]` (А3),
  project-plan — заметка о январе без «19 %».
- Оставлено: числа, которые не ответ (индекс `RangeIndex`, заказ 11575, 9030/8700 в заметке о `nlargest`,
  порог 50, пример 50 + 0 в «Типичной ошибке» alignment, 31 пропуск в Mistake проекта — это контрольное число).
- Итоговые демонстрации «Итог»/«Сводка» и «Выводы» в конце проектов не скрыты: это отдельный раздел
  после всех упражнений (по брифу числа можно переносить в «Выводы»). Если нужно — `gate="lesson"`
  (до решения всех упражнений) добавляется в `demoGates` парой строк; не делал.

### Правки по отчётам

- А4 `new-columns/tidy`: проверка по фиксированному набору столбцов (нет нужных / лишние), новая «ошибка» —
  удалён лишний `markup`.
- А5 project-clean-2: пять пар различаются только записью даты (`2023-07-21` и `21.07.2023`).
- А6 `dedupe`: `len(clean) != 245` с объяснением; `drop_duplicates()` до отбора `columns` добавлен в «ошибки».
- А7–А8 project-clean-2: «Подготовка» печатает число полных повторов сырой выгрузки, `bonus-before` — число
  пустых полей; текст ссылается на них; «решения упражнений первой части».
- А9 columns: `mean` падает, `sum` склеивает текст. А10 dates: пояснение к `0 days`. А11 stats: зачем `dropna`.
  А12 set-values: «в старых версиях pandas».
- В4 plot: заметка — `Series.plot` дорисовывает, `DataFrame.plot` начинает новый график; сообщение проверки
  `cities` без «дважды»; М7 — «первая строка заготовки добавляет `month`».
- В5 project-plan: октябрь, ноябрь и декабрь с планом Сочи; без Сочи худший — сентябрь (88 %). М9: условие
  `months` предупреждает про округлённую долю, проверка ловит `months_ok == 6` (сравнение `done >= 1`) с
  объяснением 0.9997, эта ошибка добавлена в «ошибки».
- В6 project-report: подъём в апреле, пик на сглаженном графике позже — скользящее среднее ставит значение
  в конец окна; М11 — «Эспрессо-смесь» и «Колумбия» вровень.
- М5 resample: ряд заказов назван `orders` (`rename`), `daily` печатает и `sales`; М6 `stamp` — метка 21-й
  недели (25 мая: месяц 5, квартал 2), с ответами `months` не совпадает.
- М10 merge: «(зачем брать только нужные — ниже…)». М12 weather-sales: укрупнение убирает шум и оставляет
  сезон.

### Сбой «numpy не загрузился» (Б: М8)

Не воспроизвёлся: 3 полных прогона `validate_courses.ts pandas` подряд и 5 прогонов восьми уроков модулей 1–2
с холодным кэшем (колёса удалены из `node_modules/pyodide` перед каждым) — все зелёные. Версия: в Node.js
Pyodide скачивает колёса в `node_modules/pyodide` при первом запросе, а валидатор держит до 4 воркеров сразу;
два воркера могут одновременно писать и читать одно колесо, а `engine.ts` глушит `errorCallback`, поэтому
причина не видна. Нужно от платформы (`src/lib/python/engine.ts`, вне этого потока): при
`!loadedPackages[name]` повторить `loadPackage` один раз и добавить в сообщение текст из `errorCallback`.

### NumPy

PR #4 `numpy-review` к моменту работы в main не слит — по брифу NumPy не трогал. Новое правило скрытия уже
действует и в курсе NumPy (17 демонстраций), но пометки `gate="off"` и поиск ответов в тексте для NumPy
не делались.

### Проверки (повторно)

| Команда | Итог |
| --- | --- |
| `validate_courses.ts pandas` (CPython .venv) ×3 | ✓ 51 урок, 877 прогонов, все три раза |
| `validate_courses.ts numpy` | ✓ |
| `npm run check` / `npm run build` | 0 ошибок / сборка готова |
| `validate_browsers.ts chromium --only <51 id pandas>` | ✓ 51 из 51 (ячеек 679) |
| Playwright, `project-climate` | без JS всё видно; с JS скрыты `kinds-view` и 4 `<After>`, плашка с названием; решение в другой вкладке открывает своё; «Урок пройден» открывает всё, снятие — закрывает; модуль урока заблокирован — решённые из localStorage открыты, в кадрах до загрузки закрытых нет, обе кнопки работают; живой запуск показывает вывод; 375 px без горизонтальной прокрутки |

### Изменённые места (повторное ревью)

- Платформа: `src/lib/courses/format.ts` (`demoGates`, `gate` у Demo, `After`), `src/lib/courses/site.ts`
  (`gateOf`, `exerciseBlock`), `src/lib/courses/notebook.ts` (`After`), `src/components/course/{Demo,After,
  GatePlaque}.astro`, `index.ts`, `src/scripts/course/lesson.ts` (`renderGate`), `src/pages/courses/[course]/
  [lesson].astro` (встроенный скрипт), `src/styles/course.css`, `scripts/validate_courses.ts` (проверки `After`
  и `gate`).
- Курс: `gate="off"` — first-table, series, columns, loc-iloc, filtering, set-values, types, dates, agg, rolling,
  project-report, final-data, final-report; `<After>` и переписанный текст — см. выше; lesson.py и output.json —
  new-columns (проверка), project-clean-2, project-plan, plot, resample.
- Документы: `docs/COURSES_PLAN.md` («Формат хранения» — `After`, `gate="off"`; «Ячейки и состояние» —
  новое описание скрытия; «Интерфейс»), `docs/ARCHITECTURE.md`.

## Решения оркестратора после повторного ревью

- **`gate="lesson"` / `<After id="*">`** — скрытие до решения всех упражнений урока (или отметки «Урок пройден»;
  `data-gate="*"`, встроенный скрипт получает список упражнений через `define:vars`, `lesson.ts` — так же).
  Применено: итоговые демонстрации 12 проектов (`summary`, `report` в project-channels, `text-done` в части 1
  проекта очистки, `result` в final-data — был `gate="off"`), «Выводы»/«Что получилось»/«Итог первой части»
  с ответами — 14 проектов. Плашка: «Итог появится, когда решите все упражнения урока…» / «Выводы с ответами
  появятся…». Валидатор: `gate` — `off` или `lesson`, `<After id="*">` без проверки упражнения.
  Playwright (project-climate): без JS видно; пусто — скрыто; решено 5 из 6 — скрыто; все 6 — открыто и
  встроенным скриптом (модуль заблокирован), и `lesson.ts`; «Урок пройден» открывает, «Весь вывод урока» тоже.
- **`src/lib/python/engine.ts`** — пакет, не загрузившийся с первого раза, загружается ещё раз; ошибка
  «пакет … не загрузился за две попытки: <текст Pyodide>» (раньше `errorCallback` глушился). Описано
  в ARCHITECTURE.md («Python в браузере», «Пакеты»).
- Проверки: `validate_courses.ts` (оба курса, 94 урока, 1530 прогонов) ✓; `npm run check` 0 ошибок; build ✓;
  `validate_browsers.ts chromium` по pandas — 51 из 51 ✓.
- Изменённые места: `format.ts` (`LESSON_GATE`), `Demo.astro`, `After.astro`, `lesson.ts`, `[lesson].astro`,
  `validate_courses.ts`, `engine.ts`; lesson.mdx 14 проектов pandas; COURSES_PLAN.md, ARCHITECTURE.md.

## По ревью В

- В1: в ноутбуке пометка `<After>` — отдельным абзацем; для `id="*"` — «После решения всех упражнений урока»
  (список «Выводов» в .ipynb больше не ломается, проверено в `dist/…/project-cities.ipynb`).
- М1: числа в COURSES_PLAN: по разделу упражнения скрыто 19, `gate="off"` — 16 (после М3), итогов `gate="lesson"` — 12.
- М2 set-values: «Старые версии pandas … меняли». М5 stats: пояснение про `dropna` — отдельным предложением.
- М3: новое значение `gate="<id упражнения выше>"` — скрыть до решения указанного упражнения; `share-chart`
  (→ `channels`) и `category-chart` (→ `categories`). Валидатор проверяет, что упражнение выше.
- М4 resample `stamp`: метка квартала `"QE"` (30 июня: месяц 6, квартал 2) — `"QE"` уже в таблице выше.
- М6 project-clean-2 `total`: сообщение без правильного числа.
- Проверки: `validate_courses.ts pandas` ✓, check 0 ошибок, build ✓, chromium по pandas 51/51 ✓.

## Курс NumPy

После слияния main (PR #4 `numpy-review`) курс NumPy пройден тем же способом.
- **Итоги проектов:** `gate="lesson"` у итоговых демонстраций 11 проектов (`summary` в 10, `final` в project-pixels);
  `<After id="*">` — «Выводы» с ответами в 9 проектах (в project-prices выводы без чисел, в project-pixels их нет).
- **`gate="off"`** — новый материал в разделе упражнения: `other-array` (boolean-filter), `speed` (simulation),
  `no-header` (genfromtxt), `concat-2d` (join-split), `neighbor` (distances). По разделу упражнения скрыт вывод 7
  демонстраций: `change-print`, `count-print`, `hot-print`, `half`, `check-fill`, `recommend`, `naive-days`.
- **Текст с ответом в `<After>`** (9): project-pixels `count`, project-hot-days `days`, project-prices `rubles`,
  project-dice `fair`, genfromtxt `zero-trap`, project-knn `predict`, `naive`, final-revenue `categories`, `delivery`.
- **Переписано:** заголовок `count-print` «Почему 13, а не 14» (называл ответ) → «Крест и число закрашенных точек»;
  «Типичная ошибка» под `quality` в final-revenue — без долей 20.6/21.4 % и оценок 2.4/3.7 (это ответы).
- Оставлено: числа, которые не ответ (145.3 и точность дробных, 29 строк вместо 28 в Mistake genfromtxt, 0.4 —
  неверный ответ в Mistake vectorize, «один день из 28» в project-station, 2448 строк в Mistake final-revenue).
- Проверки: `validate_courses.ts numpy` ✓; `npm run check` 0 ошибок; build ✓; `validate_browsers.ts chromium`
  по 43 урокам NumPy ✓ (ячеек 403); Playwright на project-knn — пусто: 6 мест скрыто, все упражнения решены: всё видно.
- Изменённые места: lesson.mdx 16 уроков NumPy (`01-start/05-project-expenses`, `02-shape/05-project-moscow`,
  `03-indexing/05-project-pixels`, `04-masks/02-boolean-filter`, `04-masks/04-project-hot-days`,
  `05-axes/05-project-grades`, `06-broadcasting/04-project-prices`, `07-random/03-simulation`,
  `07-random/04-project-dice`, `08-missing/02-genfromtxt`, `08-missing/03-join-split`, `08-missing/04-project-station`,
  `09-linalg/03-distances`, `09-linalg/05-project-knn`, `10-final/01-final-revenue`, `10-final/02-final-dynamics`);
  lesson.py и output.json не менялись.
