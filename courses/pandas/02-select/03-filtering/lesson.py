# Урок pd-filtering. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% mask
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders["price"] > 3000

# %% apply
orders[orders["price"] > 3000].head()

# %% named
is_tea = orders["category"] == "Чай"
tea = orders[is_tea]
print(len(tea))
print(tea["price"].mean())

# %% expensive [exercise]
expensive = orders[orders["price"] > 2000]
n_expensive = len(expensive)
# ─── заготовка ───
expensive = ...
n_expensive = ...
# ─── проверка ───
def test_expensive():
    "expensive — строки с ценой выше 2000"
    assert not (isinstance(expensive, pd.Series) and expensive.dtype == bool), "expensive — это маска из True и False, а нужны сами строки: подставьте маску в orders[...]"
    assert isinstance(expensive, pd.DataFrame), f"expensive — это {type(expensive).__name__}, а нужна таблица: orders[условие]"
    assert expensive.shape[1] == 9, "в expensive должны остаться все 9 столбцов"
    assert len(expensive) != 2448, "в expensive все строки таблицы: условие не применено"
    assert expensive["price"].min() > 2000, f"в expensive есть цена {expensive['price'].min()}, а нужны строго больше 2000"
    assert len(expensive) == 66, f"в expensive {len(expensive)} строк, а строк с ценой выше 2000 — 66"


def test_count():
    "n_expensive — сколько таких строк"
    assert n_expensive == 66, f"n_expensive = {n_expensive!r}, а строк с ценой выше 2000 — 66"
# ─── другое решение ───
mask = orders["price"] > 2000
expensive = orders.loc[mask]
n_expensive = mask.sum()
# ─── ошибка ───
expensive = orders["price"] > 2000
n_expensive = len(expensive)
# ─── ошибка ───
expensive = orders[orders["price"] >= 1000]
n_expensive = len(expensive)

# %% count
many = orders["quantity"] >= 5
print(many.sum())
print(many.mean())

# %% share [exercise]
is_moscow = orders["city"] == "Москва"
n_moscow = is_moscow.sum()
share_moscow = is_moscow.mean()
# ─── заготовка ───
is_moscow = ...
n_moscow = ...
share_moscow = ...
# ─── проверка ───
def test_mask():
    "is_moscow — маска: True у строк из Москвы"
    assert not isinstance(is_moscow, pd.DataFrame), "is_moscow — отфильтрованная таблица, а нужна сама маска: orders[\"city\"] == \"Москва\""
    assert isinstance(is_moscow, pd.Series) and is_moscow.dtype == bool, "is_moscow должна быть Series из True и False: сравнение столбца city с \"Москва\" через =="
    assert len(is_moscow) == 2448, f"в маске {len(is_moscow)} значений, а строк 2448"
    assert is_moscow.sum() == 948, "маска отмечает не те строки: сравните столбец city со строкой \"Москва\""


def test_numbers():
    "n_moscow и share_moscow — число и доля строк"
    assert n_moscow == 948, f"n_moscow = {n_moscow!r}, а строк из Москвы 948: сумма маски"
    assert abs(share_moscow - 948 / 2448) < 1e-9, f"share_moscow = {share_moscow!r}, а доля ≈ 0.387: среднее маски"
# ─── другое решение ───
is_moscow = orders["city"] == "Москва"
n_moscow = len(orders[is_moscow])
share_moscow = n_moscow / len(orders)
# ─── ошибка ───
is_moscow = orders[orders["city"] == "Москва"]
n_moscow = 948
share_moscow = 948 / 2448
# ─── ошибка ───
is_moscow = orders["city"] == "Москва"
n_moscow = is_moscow.sum()
share_moscow = is_moscow.sum()

# %% and
orders[(orders["city"] == "Новосибирск") & (orders["price"] > 3000)]

# %% or-not
site_or_app = (orders["channel"] == "сайт") | (orders["channel"] == "приложение")
print(site_or_app.sum())
print((~site_or_app).sum())

# %% word-and [raises=ValueError]
orders[(orders["city"] == "Казань") and (orders["quantity"] >= 5)]

# %% no-parens [raises=TypeError]
orders[orders["city"] == "Казань" & orders["quantity"] >= 5]

# %% kazan [exercise]
kazan_big = orders[(orders["city"] == "Казань") & (orders["quantity"] >= 5)]
# ─── заготовка ───
kazan_big = ...
# ─── проверка ───
def test_kazan():
    "kazan_big — Казань и не меньше 5 штук"
    assert isinstance(kazan_big, pd.DataFrame), f"kazan_big — это {type(kazan_big).__name__}, а нужна таблица: orders[(условие) & (условие)]"
    assert len(kazan_big) > 0, "в kazan_big нет строк: проверьте название города и условие на quantity"
    assert (kazan_big["city"] == "Казань").all(), "в kazan_big есть другие города: оба условия должны выполняться сразу — оператор &, а не |"
    assert kazan_big["quantity"].min() >= 5, "в kazan_big есть строки, где меньше 5 штук: оба условия должны выполняться сразу — оператор &"
    assert len(kazan_big) != 9, "в kazan_big 9 строк: условие «не меньше 5» — это >=, а не >"
    assert len(kazan_big) == 14, f"в kazan_big {len(kazan_big)} строк, а подходящих 14"
# ─── другое решение ───
in_kazan = orders["city"] == "Казань"
bulk = orders["quantity"] >= 5
kazan_big = orders[in_kazan & bulk]
# ─── другое решение ───
kazan_big = orders[orders["city"] == "Казань"]
kazan_big = kazan_big[kazan_big["quantity"] >= 5]
# ─── ошибка ───
kazan_big = orders[(orders["city"] == "Казань") | (orders["quantity"] >= 5)]
# ─── ошибка ───
kazan_big = orders[(orders["city"] == "Казань") & (orders["quantity"] > 5)]

# %% not-quiz [quiz]
print((~(orders["channel"] == "сайт")).sum() == (orders["channel"] != "сайт").sum())

# %% special [exercise]
special = orders[(orders["price"] >= 2000) | (orders["quantity"] >= 8)]
ordinary = orders[~((orders["price"] >= 2000) | (orders["quantity"] >= 8))]
# ─── заготовка ───
special = ...
ordinary = ...
# ─── проверка ───
def test_special():
    "special — дорогой товар или большая партия"
    assert isinstance(special, pd.DataFrame), f"special — это {type(special).__name__}, а нужна таблица"
    assert len(special) != 0, "в special нет строк: условия соединены через &, а нужно «или» — оператор |"
    assert ((special["price"] >= 2000) | (special["quantity"] >= 8)).all(), "в special есть строки, где не выполнено ни одно из условий"
    assert len(special) == 78, f"в special {len(special)} строк, а подходящих 78: цена не ниже 2000 или количество не меньше 8"


def test_ordinary():
    "ordinary — все остальные строки"
    assert isinstance(ordinary, pd.DataFrame), f"ordinary — это {type(ordinary).__name__}, а нужна таблица"
    assert len(ordinary) == 2448 - 78, f"в ordinary {len(ordinary)} строк, а остальных строк 2370: всё условие целиком в скобках и ~ перед ним"
    assert ordinary["price"].max() < 2000 and ordinary["quantity"].max() < 8, "в ordinary попали строки из special"
# ─── другое решение ───
is_special = (orders["price"] >= 2000) | (orders["quantity"] >= 8)
special = orders[is_special]
ordinary = orders[~is_special]
# ─── другое решение ───
special = orders[(orders["price"] >= 2000) | (orders["quantity"] >= 8)]
ordinary = orders[(orders["price"] < 2000) & (orders["quantity"] < 8)]
# ─── ошибка ───
special = orders[(orders["price"] >= 2000) & (orders["quantity"] >= 8)]
ordinary = orders[~((orders["price"] >= 2000) & (orders["quantity"] >= 8))]
# ─── ошибка ───
special = orders[(orders["price"] >= 2000) | (orders["quantity"] >= 8)]
ordinary = orders[~(orders["price"] >= 2000) | (orders["quantity"] >= 8)]

# %% check-all
print((kazan_big["city"] == "Казань").all())
print((orders["price"] >= 150).all())
print((orders["quantity"] >= 2).all())
