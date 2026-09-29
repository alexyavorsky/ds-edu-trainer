# Тренажёр задач по книгам

Личный сайт для повторения материала: задачи строго по главам книги. Решать можно прямо на сайте — Python
выполняется в браузере (Pyodide), — или в своём редакторе: файл с тестами копируется одной кнопкой.
Сейчас есть «Грокаем алгоритмы» (1-е издание): 10 глав, 80 задач, и справочник по NumPy 2.5 и pandas 3.0:
99 статей, 744 проверенных примера. Задачи по NumPy и pandas — «скоро».

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
| `npm run check` | типы TypeScript / Astro |

## Деплой

Vercel: импортировать репозиторий — Astro определяется автоматически. PDF книги в `.gitignore` и не публикуется.
