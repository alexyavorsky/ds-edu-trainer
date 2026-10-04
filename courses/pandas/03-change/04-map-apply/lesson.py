# Урок pd-map-apply. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% map
import pandas as pd

products = pd.read_csv("data/products.csv")
shelf = {"Кофе": "A", "Чай": "A", "Сладости": "B", "Посуда": "C", "Аксессуары": "C"}
products["shelf"] = products["category"].map(shelf)
products[["name", "category", "shelf"]].head(7)

# %% map-missing
partial = products["category"].map({"Кофе": "A", "Чай": "A"})
print(partial.tail(3))
print(partial.notna().all())
print(products["shelf"].notna().all())

# %% discount [exercise]
goods = pd.read_csv("data/products.csv")
rates = {"Кофе": 0.04, "Чай": 0.06, "Сладости": 0.12, "Посуда": 0.18, "Аксессуары": 0.18}
goods["discount"] = goods["category"].map(rates)
goods["sale_price"] = (goods["price"] * (1 - goods["discount"])).round()
# ─── заготовка ───
goods = pd.read_csv("data/products.csv")
rates = {"Кофе": 0.04, "Чай": 0.06, "Сладости": 0.12, "Посуда": 0.18, "Аксессуары": 0.18}
# добавьте в goods столбцы discount и sale_price
# ─── проверка ───
def test_discount():
    "discount — скидка категории"
    assert "discount" in goods.columns, "в goods нет столбца discount"
    assert goods["discount"].notna().all(), "в discount есть пропуски: словарь должен содержать все пять категорий"
    assert goods["discount"].tolist()[:6] == [0.04, 0.04, 0.04, 0.04, 0.04, 0.06], "скидки не те: применять словарь нужно к столбцу category"
    assert abs(goods["discount"].sum() - 2.18) < 1e-9, "скидки не те: применять словарь нужно к столбцу category"


def test_price():
    "sale_price — цена со скидкой, округлённая до рублей"
    assert "sale_price" in goods.columns, "в goods нет столбца sale_price"
    assert abs(goods.loc[0, "sale_price"] - 58) > 1e-6, "в sale_price — размер скидки, а нужна цена со скидкой"
    assert abs(goods.loc[1, "sale_price"] - 662.4) > 1e-6, "значения не округлены до рублей"
    assert goods.loc[0, "sale_price"] == 1392, f"sale_price в первой строке — {goods.loc[0, 'sale_price']}, а должна быть 1392"
    assert goods["sale_price"].sum() == 15819, "не все цены верны: проверьте формулу и округление"
# ─── другое решение ───
goods = pd.read_csv("data/products.csv")
rates = {"Кофе": 0.04, "Чай": 0.06, "Сладости": 0.12, "Посуда": 0.18, "Аксессуары": 0.18}
goods = goods.assign(discount=goods["category"].map(rates))
goods["sale_price"] = (goods["price"] - goods["price"] * goods["discount"]).round()
# ─── ошибка ───
goods = pd.read_csv("data/products.csv")
rates = {"Кофе": 0.04, "Чай": 0.06, "Сладости": 0.12, "Посуда": 0.18, "Аксессуары": 0.18}
goods["discount"] = goods["category"].map(rates)
goods["sale_price"] = (goods["price"] * goods["discount"]).round()
# ─── ошибка ───
goods = pd.read_csv("data/products.csv")
rates = {"Кофе": 0.04, "Чай": 0.06, "Сладости": 0.12, "Посуда": 0.18, "Аксессуары": 0.18}
goods["discount"] = goods["category"].map(rates)
goods["sale_price"] = goods["price"] * (1 - goods["discount"])

# %% replace
products["category"].replace({"Посуда": "Для дома", "Аксессуары": "Для дома"}).value_counts()

# %% map-quiz [quiz]
print(pd.Series(["да", "нет", "да"]).map({"да": 1}).notna().sum())

# %% groups [exercise]
goods["group"] = goods["category"].replace({"Кофе": "Напитки", "Чай": "Напитки"})
n_drinks = (goods["group"] == "Напитки").sum()
# ─── заготовка ───
# добавьте в goods столбец group
n_drinks = ...
# ─── проверка ───
def test_group():
    "group — кофе и чай объединены в «Напитки»"
    assert "group" in goods.columns, "в goods нет столбца group"
    assert goods["group"].notna().all(), "в group есть пропуски: похоже, использован map — он превращает в пропуск всё, чего нет в словаре. Нужен replace"
    assert "Кофе" not in goods["group"].tolist() and "Чай" not in goods["group"].tolist(), "в group остались «Кофе» или «Чай»: оба нужно заменить на «Напитки»"
    assert sorted(goods["group"].unique()) == ["Аксессуары", "Напитки", "Посуда", "Сладости"], f"в group сейчас значения {sorted(goods['group'].unique())}"
    assert goods["category"].tolist()[0] == "Кофе", "столбец category менять не нужно: результат replace запишите в новый столбец group"


def test_count():
    "n_drinks — сколько товаров-напитков"
    assert n_drinks == 9, f"n_drinks = {n_drinks!r} — это не число товаров-напитков"
# ─── другое решение ───
goods["group"] = goods["category"].replace(["Кофе", "Чай"], "Напитки")
n_drinks = goods["group"].value_counts()["Напитки"]
# ─── ошибка ───
goods["group"] = goods["category"].map({"Кофе": "Напитки", "Чай": "Напитки"})
n_drinks = (goods["group"] == "Напитки").sum()
# ─── ошибка ───
goods["group"] = goods["category"].replace({"Кофе": "Напитки"})
n_drinks = (goods["group"] == "Напитки").sum()

# %% where
import numpy as np

np.where(products["price"] >= 1000, "дорогой", "обычный")

# %% where-column
products["segment"] = np.where(products["price"] >= 1000, "дорогой", "обычный")
products["segment"].value_counts()

# %% margin [exercise]
share = (goods["price"] - goods["cost"]) / goods["price"]
goods["margin"] = np.where(share >= 0.5, "высокая", "обычная")
n_high = (goods["margin"] == "высокая").sum()
# ─── заготовка ───
share = (goods["price"] - goods["cost"]) / goods["price"]
# добавьте в goods столбец margin
n_high = ...
# ─── проверка ───
def test_margin():
    "margin — «высокая» при доле от 0.5, иначе «обычная»"
    assert "margin" in goods.columns, "в goods нет столбца margin"
    assert sorted(goods["margin"].unique()) == ["высокая", "обычная"], f"в margin сейчас значения {sorted(map(str, goods['margin'].unique()))}, а нужны «высокая» и «обычная»"
    assert goods.loc[0, "margin"] == "обычная", "у первого товара доля 0.4 — маржа «обычная»: проверьте порядок аргументов np.where(условие, если да, если нет)"
    assert goods.loc[5, "margin"] == "высокая", "у чёрного чая доля 0.57 — маржа «высокая»"


def test_count():
    "n_high — сколько товаров с высокой маржой"
    assert n_high != 9, "9 — товары с обычной маржой, а нужны с высокой"
    assert n_high == 11, f"n_high = {n_high!r} — это не число товаров с высокой маржой"
# ─── другое решение ───
share = (goods["price"] - goods["cost"]) / goods["price"]
goods["margin"] = "обычная"
goods.loc[share >= 0.5, "margin"] = "высокая"
n_high = len(goods[goods["margin"] == "высокая"])
# ─── ошибка ───
share = (goods["price"] - goods["cost"]) / goods["price"]
goods["margin"] = np.where(share >= 0.5, "обычная", "высокая")
n_high = (goods["margin"] == "высокая").sum()

# %% apply
def level(price):
    if price < 300:
        return "до 300"
    if price < 1000:
        return "300–999"
    return "от 1000"


products["level"] = products["price"].apply(level)
products[["name", "price", "level"]].head(6)

# %% apply-slow
def plus_ten_percent(price):
    return price * 1.1


slow = products["price"].apply(plus_ten_percent)
fast = products["price"] * 1.1
print((slow == fast).all())

# %% shipping [exercise]
def shipping(price):
    if price >= 1000:
        return 0
    if price >= 500:
        return 150
    return 250


goods["shipping"] = goods["price"].apply(shipping)
free = (goods["shipping"] == 0).sum()
# ─── заготовка ───
def shipping(price):
    return ...


# добавьте в goods столбец shipping
free = ...
# ─── проверка ───
def test_function():
    "shipping(price) — стоимость доставки"
    assert shipping(1000) is not ..., "функция shipping пока возвращает ... — напишите в ней правило"
    assert shipping(1000) == 0, f"shipping(1000) = {shipping(1000)!r}, а от 1000 ₽ доставка бесплатная"
    assert shipping(999) == 150 and shipping(500) == 150, "от 500 до 999 ₽ доставка стоит 150"
    assert shipping(499) == 250 and shipping(150) == 250, "дешевле 500 ₽ доставка стоит 250"


def test_column():
    "столбец shipping и число товаров с бесплатной доставкой"
    assert "shipping" in goods.columns, "в goods нет столбца shipping"
    assert goods["shipping"].tolist()[:6] == [0, 150, 150, 0, 150, 250], f"первые значения shipping — {goods['shipping'].tolist()[:6]}: примените функцию к столбцу price"
    assert goods["shipping"].sum() == 2750, "не все значения верны: примените функцию к столбцу price"
    assert free == 7, f"free = {free!r} — это не число товаров с бесплатной доставкой"
# ─── другое решение ───
def shipping(price):
    return 0 if price >= 1000 else 150 if price >= 500 else 250


goods["shipping"] = [shipping(price) for price in goods["price"]]
free = goods["shipping"].value_counts()[0]
# ─── ошибка ───
def shipping(price):
    if price > 1000:
        return 0
    if price > 500:
        return 150
    return 250


goods["shipping"] = goods["price"].apply(shipping)
free = (goods["shipping"] == 0).sum()
