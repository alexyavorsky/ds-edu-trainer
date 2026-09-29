# План справочников NumPy и pandas

Версии: **NumPy 2.5.3**, **pandas 3.0.6** — последние стабильные на PyPI и в документации на 29.09.2026.
Порядок статей — порядок изучения. Машиночитаемое оглавление: `reference/<тема>/topic.toml`.

Уровни: **Б** — базовый, **С** — средний, **П** — продвинутый.

## NumPy — 48 статей (Б 11 · С 24 · П 11 · итоговые 2)

### 1. Основы
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `intro` Что такое NumPy | Б | ndarray против list, векторные операции вместо циклов, `import numpy as np`, версия |
| `display` Настройки отображения | Б | print и repr, `np.set_printoptions` (precision, suppress, threshold, linewidth), контекст `np.printoptions`, скаляры `np.float64(1.5)` в NumPy 2; какие настройки заданы в справочнике |
| `creation` Создание массивов | Б | array/asarray, zeros, ones, full, empty, arange, linspace, eye/identity, `*_like` |
| `attributes` Атрибуты массива | Б | shape, ndim, size, dtype, itemsize, nbytes, len |
| `dtypes` Типы данных и astype | Б | int/float/bool/complex/str, astype, переполнение целых, iinfo/finfo; правила приведения NEP 50 (было/стало 1.x → 2.x) |

### 2. Индексация
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `indexing` Индексация и срезы | Б | `a[i]`, отрицательные индексы, `start:stop:step`, присваивание в срез |
| `indexing-nd` Многомерная индексация | Б | `a[i, j]`, строка и столбец, срезы по нескольким осям, `...` |
| `boolean` Булевы маски | С | сравнение → маска, `a[mask]`, `&`, `|`, `~` и скобки, присваивание по маске, count_nonzero, any/all |
| `fancy` Fancy-индексация | С | массив индексов, порядок и повторы, `np.ix_`, присваивание; результат — копия |
| `where` where, nonzero, select | С | `np.where` с 1 и 3 аргументами, nonzero, argwhere, select для нескольких условий |

### 3. Вычисления
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `arithmetic` Арифметика с массивами | Б | поэлементные `+ - * / // % **`, операции с числом, деление на ноль → inf/nan и предупреждение |
| `comparing` Сравнение массивов | Б | `==` поэлементно; почему `if a == b:` падает; array_equal, allclose, isclose; сравнение float |
| `aggregations` Базовые агрегации | Б | sum, min, max, mean, prod, ptp, any, all; функция или метод; пустой массив |
| `rounding` Округление и clip | Б | round (банковское округление), floor, ceil, trunc, rint, clip; np.fix устарел |
| `axis` Оси: axis и keepdims | С | **схема axis=0 / axis=1**, агрегации по осям, keepdims, argmin/argmax, cumsum/cumprod |
| `ufunc` Универсальные функции | С | sqrt, exp, log, abs, maximum против max; методы reduce, accumulate, outer, at; параметр where= |
| `broadcasting` Транслирование | С | **образец**: правила, таблица форм, **схема**, newaxis, типичные ошибки |
| `diff` Разности: diff и gradient | С | diff (n, axis, prepend/append), связь с cumsum, gradient |

### 4. Форма массива
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `views-copies` Представления и копии | С | что даёт view, а что копию; .base, shares_memory, copy() |
| `reshape` reshape и ravel | С | reshape, `-1`, порядок C/F, ravel против flatten, np.resize |
| `transpose` T, newaxis, squeeze | С | T/transpose/swapaxes/moveaxis, newaxis/expand_dims, squeeze |
| `join-split` Объединение и разделение | С | concatenate, stack, vstack/hstack/column_stack, split/array_split; row_stack удалён в 2.5 |
| `repeat-tile` repeat и tile | С | повтор элементов против повтора целого массива, по осям |
| `flip-roll` flip, roll, rot90 | С | разворот по осям, циклический сдвиг, поворот |
| `pad` Дополнение: pad | С | pad_width, режимы constant/edge/reflect/wrap |

### 5. Сортировка и множества
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `sorting` Сортировка | С | sort (axis, kind, `descending=` — новое в 2.5), argsort, lexsort, строки по столбцу |
| `searching` searchsorted и partition | С | бинарный поиск, side=, partition/argpartition для top-k |
| `unique-sets` Уникальные и множества | С | unique (return_counts/index/inverse, axis), unique_values/unique_counts, isin, intersect1d, union1d, setdiff1d, setxor1d |

### 6. Данные
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `nan-inf` NaN и бесконечности | С | `nan != nan`, isnan/isinf/isfinite, nan-функции, nan_to_num, предупреждения |
| `random` Случайные числа | С | default_rng(seed), integers, random, uniform, normal, choice, shuffle/permutation; было: np.random.seed/rand |
| `statistics` Статистика | С | mean, average(weights), median, std/var (ddof), percentile/quantile (method), corrcoef, cov |
| `histogram` Гистограммы и подсчёт | С | histogram (bins, range), bincount, digitize |
| `meshgrid` Сетки: meshgrid | С | meshgrid (indexing xy/ij), mgrid/ogrid, значения функции на сетке |
| `datetime64` Даты: datetime64 | С | datetime64/timedelta64, единицы, арифметика, arange по датам, busday |
| `io` Сохранение и загрузка | С | save/load, savez/savez_compressed, savetxt/loadtxt, genfromtxt с пропусками |

### 7. Продвинутое
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `matmul` Матричное умножение | П | `@`, dot, matmul, vdot, inner, outer — чем отличаются |
| `linalg` Линейная алгебра | П | solve, inv, det, eig/eigh (eig с 2.5 всегда комплексный), norm, lstsq, matrix_rank |
| `vectorization` Векторизация вместо циклов | П | как переписать цикл; почему np.vectorize не ускоряет |
| `inplace-out` Операции на месте и out= | П | `+=`, out=, where=, ошибка приведения типов при `+=` |
| `memory-layout` Порядок памяти и strides | П | C/F, strides, flags, ascontiguousarray; почему транспонирование бесплатно |
| `sliding-window` Скользящие окна | П | sliding_window_view, скользящее среднее, чем опасен as_strided |
| `einsum` einsum | П | нотация; след, транспонирование, матричное произведение, батчи |
| `structured` Структурированные массивы | П | dtype с полями, доступ по имени, сортировка по полю, когда лучше pandas |
| `masked` Маскированные массивы | П | np.ma: masked_array, masked_where, агрегации, filled |
| `apply-along-axis` apply_along_axis | П | как работает и чем его заменить |
| `strings` Строки: np.strings | П | модуль np.strings и StringDType (NumPy 2); было: np.char |

### 8. Итоги
| Статья | Содержание |
| --- | --- |
| `mistakes` Частые ошибки | «неправильно → правильно» с проверенными примерами |
| `cheatsheet` Шпаргалка | таблицы «задача → код» по темам, со ссылками на статьи |

## pandas — 51 статья (Б 13 · С 28 · П 8 · итоговые 2)

### 1. Основы
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `intro` Что такое pandas | Б | Series, DataFrame, индекс, связь с NumPy, `import pandas as pd`; главное о pandas 3 |
| `display` Настройки отображения | Б | set_option/option_context, max_rows/max_columns/width/precision/float_format; какие настройки заданы в справочнике |
| `series` Series | Б | создание из списка, словаря, скаляра; index, name, dtype |
| `dataframe` DataFrame | Б | из словаря списков, списка словарей, массива; index и columns |
| `read-csv` Чтение CSV | Б | sep, header, names, index_col, usecols, dtype, parse_dates, na_values, nrows, decimal, encoding; to_csv |
| `io-formats` Excel, JSON, Parquet | Б | read_excel/to_excel (sheet_name), read_json/to_json (orient, lines), read_parquet/to_parquet |
| `inspect` Первичный осмотр | Б | head/tail, shape, info, dtypes, describe, value_counts, nunique |

### 2. Выбор данных
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `select-columns` Выбор столбцов | Б | `df["a"]`, `df[["a", "b"]]`, доступ через точку и его ловушки, select_dtypes, filter |
| `loc-iloc` loc, iloc, at, iat | Б | по меткам и позициям; срез с концом и без; строки и столбцы вместе; скаляры |
| `filtering` Фильтрация строк | Б | условия, `&`, `|`, `~`, скобки, isin, between, query |

### 3. Изменение данных
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `columns` Добавить, изменить, удалить столбцы | Б | `df["new"] =`, assign, insert, rename, drop, `pd.col` (новое в 3.0) |
| `sorting` Сортировка | Б | sort_values (by, ascending, na_position, key), sort_index, nlargest/nsmallest |
| `replace` Замена значений | С | replace: скаляры, словари, по столбцам, regex; replace против map |
| `where-mask` where, mask, clip | С | условная замена, отличие от np.where, clip с границами-Series |
| `duplicates` Дубликаты | С | duplicated, drop_duplicates (subset, keep) |
| `apply` map, apply, pipe | С | сначала векторные операции; Series.map, DataFrame.map (бывший applymap), apply по осям, pipe; почему apply медленный |
| `iteration` Почему iterrows медленный | С | потеря типов и скорость; itertuples, zip по столбцам, векторизация |
| `to-dict-numpy` to_dict и to_numpy | С | to_dict (orient), to_numpy, tolist; почему не .values |

### 4. Типы и очистка
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `missing` Пропуски | С | NaN/None/NA, isna, fillna, ffill/bfill (method= удалён), dropna (how, subset, thresh), interpolate |
| `dtypes` Типы данных | С | astype, to_numeric(errors="coerce"), nullable Int64/Float64/boolean, convert_dtypes |
| `strings` Строки: .str и тип str | С | тип str по умолчанию в 3.0 (было object); lower, strip, contains, replace, split, extract, len, slice, cat |
| `category` Категориальный тип | С | categories, ordered, codes, экономия памяти, observed в groupby |
| `datetime` Даты: to_datetime и .dt | С | format, errors, dayfirst, unit; компоненты .dt; Timedelta; разрешение us по умолчанию в 3.0 (было ns) |
| `date-range` date_range и временной индекс | С | date_range, частоты (ME вместо M), DatetimeIndex, выбор по строке даты |

### 5. Анализ
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `stats` Описательная статистика | Б | sum/mean/median/std/min/max/quantile, axis, skipna, numeric_only, idxmax/idxmin, cumsum |
| `corr` Корреляция | С | corr (pearson/spearman/kendall), corrwith, cov |
| `rank` Ранги | С | rank: method average/min/max/first/dense, ascending, pct, в группах |
| `cut-qcut` Интервалы: cut и qcut | С | bins, labels, right, include_lowest; qcut по квантилям |
| `sample` Случайная выборка | С | sample: n, frac, replace, weights, random_state; перемешать строки |

### 6. Группировка и сводные таблицы
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `groupby` Группировка: groupby | С | **образец**: **схема разделение → применение → объединение**, ключи, as_index, sort, dropna, observed, size против count |
| `groupby-agg` agg и именованная агрегация | С | agg со списком и словарём, именованная агрегация, свои функции |
| `groupby-transform` transform и filter | С | transform сохраняет форму, доля внутри группы, filter, cumcount/shift в группах, apply |
| `pivot-table` pivot_table и crosstab | С | values/index/columns/aggfunc/fill_value/margins; crosstab с normalize |

### 7. Форма и объединение
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `melt-pivot` melt и pivot | С | **схема** широкий ↔ длинный формат; id_vars/value_vars; pivot и ошибка на дублях |
| `stack-unstack` stack и unstack | С | **схема** переноса уровня между строками и столбцами; level, fill_value |
| `explode` explode | С | списки в ячейках → строки; в паре с str.split |
| `concat` concat | С | по строкам и столбцам, ignore_index, keys, join; не добавлять строки в цикле |
| `merge` merge: виды соединений | С | **схема** inner/left/right/outer/cross, on, размножение строк при дублях ключа |
| `merge-keys` merge: ключи и проверки | С | left_on/right_on, left_index, suffixes, indicator, validate, join |

### 8. Индексы
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `alignment` Выравнивание по индексу | С | арифметика по меткам, NaN при несовпадении, fill_value, reindex |
| `set-index` set_index и reset_index | С | set_index/reset_index (drop), reindex, rename_axis, уникальность индекса |
| `multiindex` MultiIndex | П | создание, loc с кортежами, xs, pd.IndexSlice, swaplevel, sort_index, droplevel |

### 9. Временные ряды
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `shift-diff` shift, diff, pct_change | П | сдвиги по строкам и по времени (freq), изменения, в группах |
| `rolling` rolling, expanding, ewm | П | window, min_periods, center, окна по времени "7D", expanding, ewm |
| `resample` resample и asfreq | П | понижение частоты с агрегацией, повышение с ffill/interpolate, label/closed |

### 10. Продвинутое
| Статья | Ур. | Содержание |
| --- | --- | --- |
| `copy-on-write` Copy-on-Write | П | выборки ведут себя как копии; цепочечное присваивание больше не работает; откуда было SettingWithCopyWarning (было/стало) |
| `method-chaining` Цепочки методов | П | assign, pipe, query, loc с lambda, pd.col, оформление цепочек |
| `performance` Производительность и память | П | memory_usage(deep=True), category, downcast, векторизация, eval/query, Arrow-типы |
| `plot` Обзор .plot | П | kind, x/y, основные виды графиков (нужен matplotlib) |

### 11. Итоги
| Статья | Содержание |
| --- | --- |
| `mistakes` Частые ошибки | «неправильно → правильно» с проверенными примерами |
| `cheatsheet` Шпаргалка | таблицы «задача → код» по темам, со ссылками на статьи |

## Шаблон статьи

Файлы: `reference/<тема>/<статья>.mdx` (текст) и `reference/<тема>/<статья>.py` (примеры).

Frontmatter (всё остальное шапка и подвал страницы берут отсюда):

```yaml
---
title: Транслирование (broadcasting)
level: medium                 # basic | medium | advanced
summary: Зачем это нужно — одна строка.
requires: [numpy/arithmetic, numpy/axis]   # «Нужно знать», не больше 3
related: [numpy/ufunc, numpy/meshgrid]     # «Связанные темы»
functions: [np.broadcast_to, np.broadcast_shapes]   # для поиска и шпаргалки
docs: https://numpy.org/doc/2.5/user/basics.broadcasting.html
---
```

Тело — разделы в этом порядке (валидатор проверяет):

1. `## Коротко` — 2–5 пунктов. Можно сразу схему.
2. Свои разделы по теме, если нужны (например, «Правила»).
3. `## Синтаксис` — `<Syntax>`, упрощённая сигнатура. *Необязательный* (нет у обзорных статей).
4. `## Параметры` — `<Params>`: параметр — что делает — по умолчанию. *Необязательный.*
5. `## Примеры` — `<Setup />` (общие данные, если есть) и `<Example id title />` от простого к сложному.
6. `## Подводные камни` — `<Pitfall title>`: текст, при необходимости пример и `<VersionNote>`.

Шапка: уровень, версия библиотеки, заголовок, «зачем», «Нужно знать». Подвал: «Связанные темы», «Документация», «Нашли ошибку?».

Компоненты (доступны во всех статьях без import): `Syntax`, `Params`, `Setup`, `Example`, `Pitfall`,
`VersionNote`, схемы (`BroadcastDiagram`, `GroupbyDiagram`, дальше — `AxisDiagram`, `MergeDiagram`,
`MeltPivotDiagram`, `StackUnstackDiagram`). Схемы — HTML/CSS в цветах сайта, на телефоне перестраиваются.

## Формат примеров

```python
# %% setup                      ← общие данные; выполняются перед каждым примером
sales = pd.DataFrame({...})

# %% one-key                    ← <Example id="one-key" title="..." />
sales.groupby("city")["cups"].sum()
# ─── вывод ───                  ← пишет validate_reference.py --update
# city
# Омск     60
# ...

# %% whole-frame [raises=TypeError]   ← пример обязан упасть именно так
# %% overflow [warns]                  ← допускаются предупреждения (кроме Deprecation/Future)
# %% hist [norun]                      ← только проверка синтаксиса
# %% loop-vs-vector [timing]           ← замер времени: числа не сравниваются, на сайте — «замер на <машина>, <дата>»
```

- Это формат ячеек `# %%`: файл открывается в VS Code/Jupyter и запускается по ячейкам.
- Пример выполняется как ячейка Jupyter: stdout, затем repr последнего выражения.
- Перед каждым примером: `reference/prelude.py` (импорты `np`, `pd` и настройки отображения), затем `setup`. У каждого примера своё пространство имён.
- Кнопка «Копировать» копирует самодостаточный код: импорты + setup + пример. Этот же код пойдёт в будущую кнопку «Запустить» (Pyodide) — формат менять не придётся.
- `DeprecationWarning`/`FutureWarning` в любом примере — ошибка валидатора: устаревший API не пройдёт.
- Вывод одинаков на macOS и Linux: без байтов памяти (МБ с округлением или отношения), без полной точности там, где считает BLAS, без зависимости от порядка, который библиотека не гарантирует.
- Графики matplotlib сохраняются валидатором в SVG (тёмная тема сайта) и показываются вместо объекта осей.
