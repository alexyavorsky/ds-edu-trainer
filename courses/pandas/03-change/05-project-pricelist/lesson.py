# Урок pd-project-pricelist. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import numpy as np
import pandas as pd

price_list = pd.read_csv("data/products.csv")
growth = {"Кофе": 1.08, "Чай": 1.05, "Сладости": 1.12, "Посуда": 1.03, "Аксессуары": 1.03}
price_list.head(3)

# %% factor [exercise]
price_list["factor"] = price_list["category"].map(growth)
# ─── заготовка ───
# добавьте в price_list столбец factor
# ─── проверка ───
def test_factor():
    "factor — множитель категории"
    assert "factor" in price_list.columns, "в price_list нет столбца factor"
    assert price_list["factor"].dtype != object, "в factor не числа: словарь growth нужно применить к столбцу category"
    assert price_list["factor"].notna().all(), "в factor есть пропуски: словарь growth нужно применить к столбцу category"
    assert price_list["factor"].tolist()[:6] == [1.08, 1.08, 1.08, 1.08, 1.08, 1.05], f"первые значения factor — {price_list['factor'].tolist()[:6]}: у каждой категории свой множитель из growth"
    assert abs(price_list["factor"].sum() - 21.29) < 1e-9, "не все множители верны"
# ─── другое решение ───
price_list["factor"] = price_list["category"].replace(growth).astype(float)
# ─── ошибка ───
price_list["factor"] = price_list["name"].map(growth)
# ─── ошибка ───
price_list["factor"] = 1.08

# %% round-tens
print(round(1566.4, -1))
print(pd.Series([1566.4, 745.2, 273.0]).round(-1).tolist())

# %% new-price [exercise]
price_list["new_price"] = (price_list["price"] * price_list["factor"]).round(-1)
# ─── заготовка ───
# добавьте в price_list столбец new_price
# ─── проверка ───
def test_new_price():
    "new_price — цена × множитель, до десятков рублей"
    assert "new_price" in price_list.columns, "в price_list нет столбца new_price"
    first = price_list.loc[0, "new_price"]
    assert abs(first - 1566.0) > 1e-6, "цены не округлены до десятков рублей"
    assert abs(first - 1566.0) > 5 or abs(first - 1570.0) < 1e-6, f"первая новая цена — {first}: проверьте округление до десятков"
    assert abs(first - 1570.0) < 1e-6, f"первая новая цена — {first}, а должна быть 1570.0"
    assert price_list["new_price"].tolist()[5:9] == [370, 410, 570, 270], f"новые цены чая — {price_list['new_price'].tolist()[5:9]}"
# ─── другое решение ───
raw = price_list["price"] * price_list["factor"]
price_list["new_price"] = raw.round(-1)
# ─── ошибка ───
price_list["new_price"] = price_list["price"] * price_list["factor"]
# ─── ошибка ───
price_list["new_price"] = (price_list["price"] * price_list["factor"]).round()
# ─── ошибка ───
price_list["new_price"] = (price_list["price"] + price_list["factor"]).round(-1)

# %% freeze [exercise]
is_costly = price_list["price"] >= 1500
price_list.loc[is_costly, "new_price"] = price_list.loc[is_costly, "price"]
# ─── заготовка ───
is_costly = ...
# верните прежнюю цену дорогим товарам
# ─── проверка ───
def test_mask():
    "is_costly — товары с ценой от 1500 ₽"
    assert isinstance(is_costly, pd.Series) and is_costly.dtype == bool, "is_costly — это должна быть маска"
    assert is_costly.sum() != 2, "в маске два товара: условие «от 1500» включает и 1500"
    assert is_costly.sum() == 3, f"в маске {is_costly.sum()} товаров — проверьте условие"


def test_frozen():
    "у дорогих товаров новая цена равна прежней"
    frozen = price_list.loc[price_list["price"] >= 1500, "new_price"].tolist()
    assert frozen != [1950, 2470, 3300], "новые цены дорогих товаров не изменились. Запись в два шага — price_list[маска][\"new_price\"] = … — не работает: нужна запись в один шаг через loc"
    assert frozen == [1890, 2400, 3200], f"новые цены дорогих товаров сейчас {frozen}, а должны быть равны прежним ценам"
    assert price_list["new_price"].sum() == 18850, "изменились цены и у остальных товаров: слева должна стоять маска is_costly"
# ─── другое решение ───
is_costly = price_list["price"] >= 1500
price_list["new_price"] = np.where(is_costly, price_list["price"], price_list["new_price"])
# ─── ошибка ───
is_costly = price_list["price"] >= 1500
price_list[is_costly]["new_price"] = price_list.loc[is_costly, "price"]
# ─── ошибка ───
is_costly = price_list["price"] >= 1500
price_list["new_price"] = price_list["price"]

# %% change [exercise]
price_list["change"] = price_list["new_price"] - price_list["price"]
price_list["status"] = np.where(price_list["change"] > 0, "подорожал", "без изменений")
n_up = (price_list["status"] == "подорожал").sum()
# ─── заготовка ───
# добавьте в price_list столбцы change и status
n_up = ...
# ─── проверка ───
def test_change():
    "change — на сколько рублей выросла цена"
    assert "change" in price_list.columns, "в price_list нет столбца change"
    assert price_list.loc[0, "change"] != -120, "знак перепутан: изменение — новая цена минус прежняя"
    assert price_list["change"].tolist()[:4] == [120, 60, 60, 100], f"первые значения change — {price_list['change'].tolist()[:4]}"
    assert price_list["change"].sum() == 690, "не все значения change верны"


def test_status():
    "status и n_up — кто подорожал"
    assert "status" in price_list.columns, "в price_list нет столбца status"
    assert sorted(price_list["status"].unique()) == ["без изменений", "подорожал"], f"в status сейчас значения {sorted(map(str, price_list['status'].unique()))}"
    assert price_list.loc[14, "status"] == "без изменений" and price_list.loc[0, "status"] == "подорожал", "значения перепутаны: np.where(условие, значение для True, значение для False)"
    assert n_up == 17, f"n_up = {n_up!r} — это не число подорожавших товаров"
# ─── другое решение ───
price_list = price_list.assign(change=price_list["new_price"] - price_list["price"])
price_list["status"] = "без изменений"
price_list.loc[price_list["change"] > 0, "status"] = "подорожал"
n_up = len(price_list.query("change > 0"))
# ─── ошибка ───
price_list["change"] = price_list["price"] - price_list["new_price"]
price_list["status"] = np.where(price_list["change"] > 0, "подорожал", "без изменений")
n_up = (price_list["status"] == "подорожал").sum()
# ─── ошибка ───
price_list["change"] = price_list["new_price"] - price_list["price"]
price_list["status"] = np.where(price_list["change"] > 0, "без изменений", "подорожал")
n_up = (price_list["status"] == "подорожал").sum()

# %% final [exercise]
final = price_list.sort_values(["category", "new_price"], ascending=[True, False])[["category", "name", "price", "new_price", "change"]]
# ─── заготовка ───
final = ...
# ─── проверка ───
def test_columns():
    "final — пять столбцов, 20 товаров"
    assert isinstance(final, pd.DataFrame), f"final — это {type(final).__name__}, а нужна таблица"
    assert list(final.columns) == ["category", "name", "price", "new_price", "change"], f"столбцы сейчас {list(final.columns)}, а нужны category, name, price, new_price, change"
    assert len(final) == 20, f"в final {len(final)} строк, а товаров 20"


def test_order():
    "категории по алфавиту, внутри — от дорогих к дешёвым"
    assert isinstance(final, pd.DataFrame) and "new_price" in final.columns and "category" in final.columns, "сначала исправьте то, о чём говорит проверка выше"
    cats = final["category"].tolist()
    assert cats == sorted(cats), "категории должны идти по алфавиту: первый ключ сортировки — category"
    coffee = final.loc[final["category"] == "Кофе", "new_price"].tolist()
    assert coffee != sorted(coffee) , "внутри категории цены идут по возрастанию, а нужно по убыванию"
    assert coffee == sorted(coffee, reverse=True), "внутри категории товары должны идти по убыванию new_price"
    assert final.iloc[0]["name"] == "Кофемолка ручная", "первой строкой должна быть ручная кофемолка — самый дорогой товар первой по алфавиту категории"
# ─── другое решение ───
final = price_list[["category", "name", "price", "new_price", "change"]].sort_values(["category", "new_price"], ascending=[True, False])
# ─── ошибка ───
final = price_list.sort_values(["category", "new_price"])[["category", "name", "price", "new_price", "change"]]
# ─── ошибка ───
final = price_list.sort_values(["category", "new_price"], ascending=[True, False])

# %% final-view
final.head(8)

# %% top [exercise]
top5 = price_list.nlargest(5, "change")[["name", "change"]]
avg_growth = price_list["new_price"].sum() / price_list["price"].sum() - 1
# ─── заготовка ───
top5 = ...
avg_growth = ...
# ─── проверка ───
def test_top():
    "top5 — пять товаров с наибольшим ростом цены"
    assert isinstance(top5, pd.DataFrame), f"top5 — это {type(top5).__name__}, а нужна таблица"
    assert list(top5.columns) == ["name", "change"], f"столбцы сейчас {list(top5.columns)}, а нужны name и change"
    assert len(top5) == 5, f"в top5 {len(top5)} строк, а нужно 5"
    assert top5["change"].tolist() == [120, 100, 60, 60, 60], f"значения change в top5 — {top5['change'].tolist()}: нужны пять наибольших значений change"
    assert top5["name"].iloc[0] == "Эспрессо-смесь 1 кг", "первым должен быть товар с ростом на 120 ₽"


def test_growth():
    "avg_growth — на сколько вырос прайс-лист в целом"
    assert abs(avg_growth - 1.03799559) > 1e-6, "получилось отношение сумм; рост — это отношение минус 1"
    assert abs(avg_growth - 690) > 1e-6, "это рост в рублях, а нужна доля"
    assert abs(avg_growth - 0.03799559) < 1e-6, f"avg_growth = {avg_growth!r} — это не рост прайс-листа в целом"
# ─── другое решение ───
top5 = price_list.sort_values("change", ascending=False).head(5)[["name", "change"]]
avg_growth = price_list["change"].sum() / price_list["price"].sum()
# ─── ошибка ───
top5 = price_list.nlargest(5, "change")[["name", "change"]]
avg_growth = price_list["new_price"].sum() / price_list["price"].sum()
# ─── ошибка ───
top5 = price_list.nsmallest(5, "change")[["name", "change"]]
avg_growth = price_list["new_price"].sum() / price_list["price"].sum() - 1

# %% summary
print("товаров:", len(price_list), "· подорожало:", n_up)
print("сумма прайс-листа:", price_list["price"].sum(), "→", int(price_list["new_price"].sum()), "₽")
print("рост в целом:", round(avg_growth * 100, 1), "%")
print(price_list["status"].value_counts())
