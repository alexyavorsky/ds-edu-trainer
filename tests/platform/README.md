# Образцы платформы

Минимальный контент той же структуры, что в корне репозитория, — для проверки возможностей платформы, которых
пока нет в настоящих разделах. На сайт не попадает: сайт и валидаторы читают эту папку только с переменной
`EDU_CONTENT_ROOT=tests/platform`.

| Папка | Что проверяет |
| --- | --- |
| `reference/sample/` | тема справочника без пакета: `python = "3.10"`, свой `prelude.py`, `practice`, `[raises]`, схемы `ClassDiagram` и `MroDiagram` |
| `challenges/sample/` | раздел задач без пакетов (`packages = []`): классы со свойствами, `data.py`, `lessons`, `alt_solutions`, fix-bug |
| `challenges/sample-numpy/` | раздел задач с пакетом: строка «Нужно: numpy (проверено на …)», `data.py` с NumPy |
| `courses/sample/` | курс без пакета: `python`, `concepts = "python"`, `practice` в модуле, упражнения с классами |

Проверка: `npm run check:platform` (все валидаторы и сборка сайта во временную папку). Посмотреть в браузере:
`EDU_CONTENT_ROOT=tests/platform npx astro dev`.
