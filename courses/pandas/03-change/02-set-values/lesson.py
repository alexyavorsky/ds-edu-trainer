# Урок pd-set-values. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% cell
import pandas as pd

products = pd.read_csv("data/products.csv")
products.loc[9, "price"] = 190
products.loc[9]

# %% by-mask
is_tea = products["category"] == "Чай"
products.loc[is_tea, "price"] = 400
products[is_tea]

# %% by-mask-calc
is_sweet = products["category"] == "Сладости"
products.loc[is_sweet, "price"] = products.loc[is_sweet, "price"] + 20
products[is_sweet]

# %% fix [exercise]
fixed = pd.read_csv("data/products.csv")
fixed.loc[12, "price"] = 250
fixed.loc[12, "cost"] = 120
# ─── заготовка ───
fixed = pd.read_csv("data/products.csv")
# исправьте цену и себестоимость в строке с меткой 12
# ─── проверка ───
def test_fixed():
    "в строке 12 цена 250 и себестоимость 120"
    assert isinstance(fixed, pd.DataFrame) and fixed.shape == (20, 5), "fixed должна остаться таблицей товаров: 20 строк, 5 столбцов"
    assert fixed.loc[12, "price"] != 210 or fixed.loc[12, "cost"] != 100, "строка 12 не изменилась"
    assert fixed.loc[12, "price"] == 250, f"цена в строке 12 — {fixed.loc[12, 'price']}, а нужна 250"
    assert fixed.loc[12, "cost"] == 120, f"себестоимость в строке 12 — {fixed.loc[12, 'cost']}, а нужна 120"


def test_rest():
    "остальные строки не изменились"
    assert fixed["price"].sum() == 18160 + 40, "изменились цены в других строках: менять нужно только строку с меткой 12"
    assert fixed["cost"].sum() == 9670 + 20, "изменилась себестоимость в других строках: менять нужно только строку с меткой 12"
# ─── другое решение ───
fixed = pd.read_csv("data/products.csv")
fixed.loc[12, ["price", "cost"]] = [250, 120]
# ─── ошибка ───
fixed = pd.read_csv("data/products.csv")
fixed.loc[12, "price"] = 250
# ─── ошибка ───
fixed = pd.read_csv("data/products.csv")
fixed["price"] = 250
fixed["cost"] = 120

# %% text
products.loc[products["price"] > 2000, "category"] = "Премиум"
products["category"].value_counts()

# %% chained [warns]
fresh = pd.read_csv("data/products.csv")
fresh[fresh["category"] == "Чай"]["price"] = 0

# %% chained-result
fresh[fresh["category"] == "Чай"]

# %% tea-up [exercise]
sale = pd.read_csv("data/products.csv")
sale.loc[sale["category"] == "Чай", "price"] = sale.loc[sale["category"] == "Чай", "price"] + 30
# ─── заготовка ───
sale = pd.read_csv("data/products.csv")
# поднимите цену всего чая на 30 ₽
# ─── проверка ───
def test_tea():
    "чай подорожал на 30 ₽"
    assert isinstance(sale, pd.DataFrame) and sale.shape == (20, 5), "sale должна остаться таблицей товаров: 20 строк, 5 столбцов"
    tea = sale.loc[sale["category"] == "Чай", "price"].tolist()
    assert tea != [350, 390, 540, 260], "цены чая не изменились. Если вы писали sale[...][\"price\"] = ..., это запись в два шага: она меняет временную копию. Нужна запись в один шаг — через loc"
    assert tea != [30, 30, 30, 30], "цены чая стали равны 30, а нужно прибавить 30 к прежним ценам"
    assert tea == [380, 420, 570, 290], f"цены чая сейчас {tea}, а нужно прибавить 30 к прежним ценам чая"


def test_rest():
    "остальные цены не изменились"
    rest = sale.loc[sale["category"] != "Чай", "price"].sum()
    assert rest == 18160 - 1540, "изменились цены не только чая: слева должна стоять маска категории «Чай»"
# ─── другое решение ───
sale = pd.read_csv("data/products.csv")
sale.loc[sale["category"] == "Чай", "price"] += 30
# ─── ошибка ───
sale = pd.read_csv("data/products.csv")
sale[sale["category"] == "Чай"]["price"] += 30
# ─── ошибка ───
sale = pd.read_csv("data/products.csv")
sale.loc[sale["category"] == "Чай", "price"] = 30
# ─── ошибка ───
sale = pd.read_csv("data/products.csv")
sale["price"] = sale["price"] + 30

# %% subset
tea = fresh[fresh["category"] == "Чай"]
tea["price"] = 0
print(tea["price"].tolist())
print(fresh.loc[fresh["category"] == "Чай", "price"].tolist())

# %% column-copy
prices = fresh["price"]
prices.loc[0] = 1
print(prices.loc[0])
print(fresh.loc[0, "price"])

# %% cow-quiz [quiz]
t = pd.DataFrame({"x": [1, 2, 3]})
part = t[t["x"] > 1]
part["x"] = 100
print(t["x"].sum())

# %% alias
same = fresh
same.loc[0, "price"] = 1
print(fresh.loc[0, "price"])

# %% copy
backup = fresh.copy()
backup.loc[0, "price"] = 5000
print(backup.loc[0, "price"])
print(fresh.loc[0, "price"])

# %% draft [exercise]
original = pd.read_csv("data/products.csv")
draft = original.copy()
draft["price"] = 0
# ─── заготовка ───
original = pd.read_csv("data/products.csv")
draft = ...
# обнулите столбец price в draft
# ─── проверка ───
def test_draft():
    "draft — копия с нулевыми ценами"
    assert isinstance(draft, pd.DataFrame), f"draft — это {type(draft).__name__}, а нужна таблица: копия original"
    assert draft.shape == (20, 5), f"у draft размер {draft.shape}, а должен быть (20, 5) — как у original"
    assert draft["price"].sum() == 0, "цены в draft не обнулены"
    assert draft["cost"].sum() == 9670, "в draft изменилась себестоимость, а обнулить нужно только price"


def test_original():
    "original не изменилась"
    assert draft is not original, "draft и original — одна и та же таблица под двумя именами: draft = original не создаёт копию. Нужна копия"
    assert original["price"].sum() == 18160, "цены в original изменились, а она должна остаться исходной"
# ─── другое решение ───
original = pd.read_csv("data/products.csv")
draft = original.assign(price=0)
# ─── ошибка ───
original = pd.read_csv("data/products.csv")
draft = original
draft["price"] = 0
# ─── ошибка ───
original = pd.read_csv("data/products.csv")
draft = original.copy()

# %% float-error [raises=TypeError]
fresh.loc[1, "price"] = 699.9

# %% astype
fresh["price"] = fresh["price"].astype(float)
fresh.loc[1, "price"] = 699.9
fresh.head(3)

# %% coffee [exercise]
raised = pd.read_csv("data/products.csv")
raised["price"] = raised["price"].astype(float)
is_coffee = raised["category"] == "Кофе"
raised.loc[is_coffee, "price"] = raised.loc[is_coffee, "price"] * 1.075
# ─── заготовка ───
raised = pd.read_csv("data/products.csv")
# поднимите цену кофе на 7.5 %
# ─── проверка ───
def test_coffee():
    "кофе подорожал на 7.5 %"
    assert isinstance(raised, pd.DataFrame) and raised.shape == (20, 5), "raised должна остаться таблицей товаров: 20 строк, 5 столбцов"
    coffee = raised.loc[raised["category"] == "Кофе", "price"].tolist()
    assert coffee != [1450, 690, 790, 1290, 720], "цены кофе не изменились: записывайте через loc с маской"
    expected = [1558.75, 741.75, 849.25, 1386.75, 774.0]
    assert all(abs(a - b) < 1e-6 for a, b in zip(coffee, expected)), f"цены кофе сейчас {coffee}: прежние цены кофе нужно поднять на 7.5 %"


def test_rest():
    "остальные цены не изменились"
    rest = raised.loc[raised["category"] != "Кофе", "price"].sum()
    assert abs(rest - (18160 - 4940)) < 1e-6, "изменились цены не только кофе: слева должна стоять маска категории «Кофе»"
# ─── другое решение ───
raised = pd.read_csv("data/products.csv")
raised["price"] = raised["price"] * 1.0
raised.loc[raised["category"] == "Кофе", "price"] *= 1.075
# ─── ошибка ───
raised = pd.read_csv("data/products.csv")
raised["price"] = raised["price"] * 1.075
