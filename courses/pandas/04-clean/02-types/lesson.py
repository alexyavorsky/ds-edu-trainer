# Урок pd-types. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

supplier = pd.read_csv("data/supplier_prices.csv")
supplier.head(6)

# %% dtypes
supplier.dtypes

# %% text-sum
print(supplier["cost"].head(3).sum())
print((supplier["cost"].head(3) * 2).tolist())

# %% text-mean [raises=TypeError]
supplier["cost"].mean()

# %% astype-fail [raises=ValueError]
supplier["cost"].astype(int)

# %% coerce
cost = pd.to_numeric(supplier["cost"], errors="coerce")
cost.head(6)

# %% coerce-rows
supplier.loc[cost.isna(), ["product_id", "name", "cost"]]

# %% write-back
supplier["cost"] = cost
print(supplier["cost"].dtype)
print(supplier["cost"].mean())

# %% fix [exercise]
raw = pd.read_csv("data/supplier_prices.csv")
cost_num = pd.to_numeric(raw["cost"], errors="coerce")
n_bad = cost_num.isna().sum()
cost_total = cost_num.sum()
# ─── заготовка ───
raw = pd.read_csv("data/supplier_prices.csv")
cost_num = ...
n_bad = ...
cost_total = ...
# ─── проверка ───
def test_cost():
    "cost_num — себестоимость числами"
    assert isinstance(cost_num, pd.Series), f"cost_num — это {type(cost_num).__name__}, а нужен Series: pd.to_numeric(raw[\"cost\"], errors=\"coerce\")"
    assert cost_num.dtype == float, f"тип cost_num — {cost_num.dtype}, а должен быть float64: текст в числа переводит pd.to_numeric"
    assert len(cost_num) == 20, f"в cost_num {len(cost_num)} значений, а товаров 20: строки удалять не нужно"
    assert cost_num[0] == 920, "значения не те: переводить нужно столбец cost"


def test_numbers():
    "n_bad и cost_total — сколько значений не распозналось и сумма остальных"
    assert n_bad == 3, f"n_bad = {n_bad!r}, а нераспознанных значений 3: cost_num.isna().sum()"
    assert not isinstance(cost_total, str), "cost_total — склеенная строка: сумму нужно считать по cost_num, а не по текстовому столбцу"
    assert abs(cost_total - 9150) < 1e-6, f"cost_total = {cost_total!r}, а сумма распознанных значений — 9150"
# ─── другое решение ───
raw = pd.read_csv("data/supplier_prices.csv")
cost_num = pd.to_numeric(raw["cost"].replace({"нет данных": None, "—": None}))
n_bad = len(cost_num) - cost_num.count()
cost_total = cost_num.dropna().sum()
# ─── ошибка ───
raw = pd.read_csv("data/supplier_prices.csv")
cost_num = pd.to_numeric(raw["cost"], errors="coerce")
n_bad = cost_num.notna().sum()
cost_total = cost_num.sum()
# ─── ошибка ───
raw = pd.read_csv("data/supplier_prices.csv")
cost_num = pd.to_numeric(raw["cost"], errors="coerce").dropna()
n_bad = 3
cost_total = cost_num.sum()

# %% coerce-trap
price = pd.to_numeric(supplier["price"], errors="coerce")
print(price.isna().sum(), "из", len(price))

# %% stock
supplier["stock"].head(4)

# %% stock-int [raises=IntCastingNaNError]
supplier["stock"].astype(int)

# %% nullable
stock = supplier["stock"].astype("Int64")
stock.head(4)

# %% nullable-use
print(stock.isna().sum())
print(stock.sum())
print(stock.max())

# %% ratings [exercise]
delivery = pd.read_csv("data/delivery_h1.csv")
delivery["rating"] = delivery["rating"].astype("Int64")
delivery["days"] = delivery["days"].astype("Int64")
fives = (delivery["rating"] == 5).sum()
# ─── заготовка ───
delivery = pd.read_csv("data/delivery_h1.csv")
# переведите столбцы rating и days в целый тип с пропусками
fives = ...
# ─── проверка ───
def test_types():
    "rating и days — целые с пропусками"
    assert str(delivery["rating"].dtype) != "float64", "тип rating по-прежнему float64: результат astype нужно записать обратно в столбец"
    assert str(delivery["rating"].dtype) == "Int64", f"тип rating — {delivery['rating'].dtype}, а нужен Int64 (с заглавной буквы, в кавычках)"
    assert str(delivery["days"].dtype) == "Int64", f"тип days — {delivery['days'].dtype}, а нужен Int64"
    assert delivery["rating"].isna().sum() == 287 and delivery["days"].isna().sum() == 36, "пропуски должны остаться пропусками: заполнять их не нужно"
    assert len(delivery) == 816, "строки удалять не нужно"


def test_fives():
    "fives — сколько пятёрок"
    assert fives == 102, f"fives = {fives!r}, а оценок «5» — 102: сумма маски delivery[\"rating\"] == 5"
# ─── другое решение ───
delivery = pd.read_csv("data/delivery_h1.csv")
delivery = delivery.astype({"rating": "Int64", "days": "Int64"})
fives = delivery["rating"].value_counts()[5]
# ─── ошибка ───
delivery = pd.read_csv("data/delivery_h1.csv")
delivery["rating"].astype("Int64")
delivery["days"].astype("Int64")
fives = (delivery["rating"] == 5).sum()
# ─── ошибка ───
delivery = pd.read_csv("data/delivery_h1.csv")
delivery["rating"] = delivery["rating"].fillna(0).astype(int)
delivery["days"] = delivery["days"].fillna(0).astype(int)
fives = (delivery["rating"] == 5).sum()

# %% truncate
weights = pd.Series([0.25, 0.9, 1.5, 2.99])
print(weights.astype(int).tolist())
print(weights.round().astype(int).tolist())

# %% trunc-quiz [quiz]
print(pd.Series([1.7, 2.2]).astype(int).tolist())

# %% to-str
codes = pd.Series([7, 42, 105])
print(codes.astype(str).tolist())
print(pd.Series([True, False, True]).astype(int).tolist())

# %% zero-stock [exercise]
stock_int = supplier["stock"].fillna(0).astype(int)
total_stock = stock_int.sum()
# ─── заготовка ───
stock_int = ...
total_stock = ...
# ─── проверка ───
def test_stock():
    "stock_int — остатки обычными целыми, пропуски — нули"
    assert isinstance(stock_int, pd.Series), f"stock_int — это {type(stock_int).__name__}, а нужен Series"
    assert stock_int.isna().sum() == 0, "в stock_int остались пропуски: сначала fillna(0), потом astype(int)"
    assert str(stock_int.dtype) != "float64", "тип stock_int — float64: после fillna(0) добавьте astype(int)"
    assert str(stock_int.dtype) in ("int64", "int32"), f"тип stock_int — {stock_int.dtype}, а нужен обычный целый: astype(int)"
    assert stock_int.tolist()[:4] == [120, 64, 0, 64], f"первые значения — {stock_int.tolist()[:4]}, а должны быть [120, 64, 0, 64]"


def test_total():
    "total_stock — всего единиц на складе"
    assert total_stock == 1253, f"total_stock = {total_stock!r}, а всего на складе 1253"
# ─── другое решение ───
stock_int = supplier["stock"].astype("Int64").fillna(0).astype("int64")
total_stock = int(supplier["stock"].sum())
# ─── ошибка ───
stock_int = supplier["stock"].fillna(0)
total_stock = stock_int.sum()
# ─── ошибка ───
stock_int = supplier["stock"].astype("Int64")
total_stock = stock_int.sum()
