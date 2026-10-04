# Урок pd-final-data. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load [exercise]
import pandas as pd

orders = pd.read_csv("data/orders.csv", parse_dates=["date"])
products = pd.read_csv("data/products.csv")
customers_raw = pd.read_csv("data/customers_raw.csv")
returns_raw = pd.read_csv("data/returns_raw.csv")
# ─── заготовка ───
import pandas as pd

orders = ...
products = ...
customers_raw = ...
returns_raw = ...
# ─── проверка ───
def test_orders():
    "orders — заказы, дата — настоящая дата"
    assert isinstance(orders, pd.DataFrame) and orders.shape == (2448, 6), "orders — таблица из файла data/orders.csv: 2448 строк, 6 столбцов"
    assert str(orders["date"].dtype).startswith("datetime64"), "столбец date в orders должен быть датой: вспомните параметр parse_dates"


def test_rest():
    "products, customers_raw, returns_raw — остальные три файла"
    assert isinstance(products, pd.DataFrame) and products.shape == (20, 5), "products — таблица из data/products.csv: 20 строк, 5 столбцов"
    assert isinstance(customers_raw, pd.DataFrame) and customers_raw.shape == (257, 7), "customers_raw — таблица из data/customers_raw.csv: 257 строк, 7 столбцов"
    assert isinstance(returns_raw, pd.DataFrame) and returns_raw.shape == (163, 6), "returns_raw — таблица из data/returns_raw.csv: 163 строки, 6 столбцов"
# ─── другое решение ───
import pandas as pd

orders = pd.read_csv("data/orders.csv")
orders["date"] = pd.to_datetime(orders["date"])
products = pd.read_csv("data/products.csv")
customers_raw = pd.read_csv("data/customers_raw.csv")
returns_raw = pd.read_csv("data/returns_raw.csv")
# ─── ошибка ───
import pandas as pd

orders = pd.read_csv("data/orders.csv")
products = pd.read_csv("data/products.csv")
customers_raw = pd.read_csv("data/customers_raw.csv")
returns_raw = pd.read_csv("data/returns_raw.csv")

# %% look
print(customers_raw.head(4))
print(returns_raw.head(4))

# %% customers [exercise]
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers = customers_raw.assign(
    customer_id=lambda d: d["customer_id"].str.strip().str.upper(),
    city=lambda d: d["city"].str.strip().str.title().replace(short),
    segment=lambda d: d["segment"].str.strip().str.lower(),
)
customers = customers[["customer_id", "city", "segment"]].drop_duplicates().reset_index(drop=True)
# ─── заготовка ───
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers = ...
# ─── проверка ───
def test_clean():
    "customers — три чистых столбца"
    assert isinstance(customers, pd.DataFrame), f"customers — это {type(customers).__name__}, а нужна таблица"
    assert list(customers.columns) == ["customer_id", "city", "segment"], f"столбцы сейчас {list(customers.columns)}, а нужны customer_id, city, segment"
    ids = customers["customer_id"].tolist()
    assert all(i == i.strip().upper() for i in ids), "в customer_id остались пробелы или строчные буквы"
    cities = sorted(customers["city"].unique())
    assert cities == ["Екатеринбург", "Казань", "Москва", "Новосибирск", "Санкт-Петербург"], f"в city сейчас {cities}, а должно быть пять городов: уберите пробелы, приведите регистр и замените сокращения"
    assert sorted(customers["segment"].unique()) == ["новый", "оптовый", "постоянный"], "в segment должно быть три значения: уберите пробелы и приведите к строчным"


def test_unique():
    "один клиент — одна строка"
    assert isinstance(customers, pd.DataFrame) and "customer_id" in customers.columns, "сначала исправьте то, о чём говорит проверка выше"
    assert len(customers) != 257, "в customers все 257 строк: дубликаты не удалены — удаляйте их после очистки текста"
    assert len(customers) == 240 and customers["customer_id"].is_unique, f"в customers {len(customers)} строк: коды клиентов не должны повторяться"
    assert list(customers.index) == list(range(240)), "индекс customers должен идти с нуля подряд"
# ─── другое решение ───
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers = customers_raw[["customer_id", "city", "segment"]].copy()
customers["customer_id"] = customers["customer_id"].str.upper().str.strip()
customers["city"] = customers["city"].str.strip().str.title().replace(short)
customers["segment"] = customers["segment"].str.lower().str.strip()
customers = customers.drop_duplicates(subset=["customer_id"]).reset_index(drop=True)
# ─── ошибка ───
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers = customers_raw[["customer_id", "city", "segment"]].drop_duplicates().reset_index(drop=True)
# ─── ошибка ───
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers = customers_raw.assign(
    customer_id=lambda d: d["customer_id"].str.strip().str.upper(),
    city=lambda d: d["city"].str.strip().str.title().replace(short),
    segment=lambda d: d["segment"].str.strip().str.lower(),
)
customers = customers[["customer_id", "city", "segment"]]

# %% returns [exercise]
returns = (
    returns_raw
    .drop_duplicates()
    .drop_duplicates(subset=["order_id", "product_id"])
    [["order_id", "product_id", "quantity"]]
    .rename(columns={"quantity": "returned"})
    .reset_index(drop=True)
)
# ─── заготовка ───
returns = (
    returns_raw
    # допишите шаги цепочки
)
# ─── проверка ───
def test_returns():
    "returns — по строке на возвращённую позицию: order_id, product_id, returned"
    assert isinstance(returns, pd.DataFrame), f"returns — это {type(returns).__name__}, а нужна таблица"
    assert list(returns.columns) == ["order_id", "product_id", "returned"], f"столбцы сейчас {list(returns.columns)}, а нужны order_id, product_id, returned: выберите три столбца и переименуйте quantity"
    assert len(returns) != 163, "в returns все 163 строки: дубликаты не удалены"
    assert len(returns) != 156, "удалены только полные повторы (осталось 156): ещё шесть возвратов оформлены дважды под разными номерами — ищите повторы по паре заказ и товар"
    assert len(returns) == 150, f"в returns {len(returns)} строк — проверьте удаление повторов"
    assert returns["returned"].sum() == 214, "сумма returned не та: проверьте удаление повторов"
    assert not returns.duplicated(subset=["order_id", "product_id"]).any(), "пара order_id и product_id не должна повторяться"
# ─── другое решение ───
returns = returns_raw.drop_duplicates(subset=["order_id", "product_id"])
returns = returns[["order_id", "product_id", "quantity"]].rename(columns={"quantity": "returned"}).reset_index(drop=True)
# ─── ошибка ───
returns = (
    returns_raw
    .drop_duplicates()
    [["order_id", "product_id", "quantity"]]
    .rename(columns={"quantity": "returned"})
    .reset_index(drop=True)
)
# ─── ошибка ───
returns = returns_raw[["order_id", "product_id", "quantity"]].rename(columns={"quantity": "returned"})

# %% join [exercise]
data = (
    orders
    .merge(products, on="product_id", validate="many_to_one")
    .merge(customers, on="customer_id", validate="many_to_one")
    .merge(returns, on=["order_id", "product_id"], how="left", validate="one_to_one")
)
# ─── заготовка ───
data = (
    orders
    # допишите три соединения
)
# ─── проверка ───
def test_shape():
    "data — заказы с товарами, покупателями и возвратами"
    assert isinstance(data, pd.DataFrame), f"data — это {type(data).__name__}, а нужна таблица"
    assert len(data) != 150, "осталось 150 строк — только позиции с возвратом: нужны все строки заказов — вспомните параметр how"
    assert len(data) == 2448, f"в data {len(data)} строк, а должно остаться 2448 — столько же, сколько в orders"


def test_columns():
    "в data есть столбцы всех четырёх таблиц"
    assert isinstance(data, pd.DataFrame), "сначала исправьте то, о чём говорит проверка выше"
    for column, source in [("price", "products"), ("cost", "products"), ("city", "customers"), ("segment", "customers"), ("returned", "returns")]:
        assert column in data.columns, f"в data нет столбца {column} — не присоединена таблица {source}"
    assert data["returned"].notna().sum() == 150, "возвраты стоят не у тех позиций: соединяйте по двум ключам сразу"
# ─── другое решение ───
step1 = pd.merge(orders, products, on="product_id", how="left")
step2 = pd.merge(step1, customers, on="customer_id", how="left")
data = pd.merge(step2, returns, on=["order_id", "product_id"], how="left")
# ─── ошибка ───
data = (
    orders
    .merge(products, on="product_id", validate="many_to_one")
    .merge(customers, on="customer_id", validate="many_to_one")
    .merge(returns, on=["order_id", "product_id"], validate="one_to_one")
)
# ─── ошибка ───
data = (
    orders
    .merge(products, on="product_id", validate="many_to_one")
    .merge(customers, on="customer_id", validate="many_to_one")
)

# %% money [exercise]
data["returned"] = data["returned"].fillna(0).astype("int64")
data["revenue"] = data["price"] * data["quantity"]
data["net"] = data["price"] * (data["quantity"] - data["returned"])
data["profit"] = (data["price"] - data["cost"]) * (data["quantity"] - data["returned"])
# ─── заготовка ───
# заполните пропуски в data["returned"] и добавьте столбцы revenue, net, profit
# ─── проверка ───
def test_returned():
    "returned — целое число, без пропусков"
    assert data["returned"].isna().sum() == 0, "в returned остались пропуски: позиция без возврата — ноль возвращённых штук. Результат запишите обратно в столбец"
    assert str(data["returned"].dtype) in ("int64", "int32"), "returned должен быть целым"
    assert data["returned"].sum() == 214, "сумма returned не та: пропуски — нули, остальное не меняется"


def test_money():
    "revenue — выручка, net — выручка за вычетом возвратов, profit — прибыль с проданного"
    for column in ["revenue", "net", "profit"]:
        assert column in data.columns, f"в data нет столбца {column}"
    assert data["revenue"].sum() == 3301420, "revenue не тот: выручка — цена × количество"
    assert data["net"].sum() != 3301420, "net равна revenue: из количества нужно вычесть возвращённые штуки"
    assert data["net"].sum() == 3159140, "net не тот: проверьте формулу из условия"
    assert data["profit"].sum() != 1542150, "в profit не учтены возвраты"
    assert data["profit"].sum() == 1476130, "profit не тот: проверьте формулу из условия"
# ─── другое решение ───
data["returned"] = data["returned"].fillna(0).astype("int64")
kept = data["quantity"] - data["returned"]
data = data.assign(revenue=data["price"] * data["quantity"], net=data["price"] * kept, profit=(data["price"] - data["cost"]) * kept)
# ─── ошибка ───
data["returned"] = data["returned"].fillna(0).astype("int64")
data["revenue"] = data["price"] * data["quantity"]
data["net"] = data["revenue"]
data["profit"] = (data["price"] - data["cost"]) * data["quantity"]
# ─── ошибка ───
data["revenue"] = data["price"] * data["quantity"]
data["net"] = data["price"] * (data["quantity"] - data["returned"])
data["profit"] = (data["price"] - data["cost"]) * (data["quantity"] - data["returned"])

# %% check [exercise]
shop = pd.read_csv("data/shop_orders.csv")
shop["revenue"] = shop["price"] * shop["quantity"]
ours = data.groupby("city")["revenue"].sum()
theirs = shop.groupby("city")["revenue"].sum()
cities_match = (ours == theirs).all()
no_gaps = data.isna().sum().sum() == 0
lost = data["revenue"].sum() - data["net"].sum()
# ─── заготовка ───
shop = pd.read_csv("data/shop_orders.csv")
shop["revenue"] = shop["price"] * shop["quantity"]
ours = ...
theirs = ...
cities_match = ...
no_gaps = ...
lost = ...
# ─── проверка ───
def test_match():
    "ours и theirs — выручка по городам в нашей таблице и в готовой; cities_match — совпали ли"
    assert isinstance(ours, pd.Series) and len(ours) == 5 and ours.sum() == 3301420, "ours — выручка (revenue) по городам в таблице data"
    assert isinstance(theirs, pd.Series) and len(theirs) == 5 and theirs.sum() == 3301420, "theirs — выручка по городам в таблице shop"
    assert not isinstance(cities_match, pd.Series), "cities_match — Series из пяти значений, а нужен один ответ"
    assert cities_match == True, "cities_match — это не ответ на вопрос, совпала ли выручка по всем городам"


def test_rest():
    "no_gaps — нет ли пропусков; lost — сколько выручки ушло в возвраты"
    assert not isinstance(no_gaps, (pd.Series, pd.DataFrame)), "no_gaps — не одно значение: нужен один ответ по всей таблице"
    assert no_gaps == True, "no_gaps — это не ответ на вопрос, нет ли в data пропусков"
    assert lost == 142280, f"lost = {lost!r} — это не разница сумм revenue и net"
# ─── другое решение ───
shop = pd.read_csv("data/shop_orders.csv")
shop["revenue"] = shop["price"] * shop["quantity"]
ours = data.pivot_table(values="revenue", index="city", aggfunc="sum")["revenue"]
theirs = shop.pivot_table(values="revenue", index="city", aggfunc="sum")["revenue"]
cities_match = ours.equals(theirs)
no_gaps = not data.isna().any().any()
lost = (data["price"] * data["returned"]).sum()
# ─── ошибка ───
shop = pd.read_csv("data/shop_orders.csv")
shop["revenue"] = shop["price"] * shop["quantity"]
ours = data.groupby("city")["revenue"].sum()
theirs = shop.groupby("city")["revenue"].sum()
cities_match = ours == theirs
no_gaps = data.isna().sum().sum() == 0
lost = data["revenue"].sum() - data["net"].sum()

# %% result
print(data.shape)
print(list(data.columns))
data[["date", "name", "city", "segment", "quantity", "returned", "revenue", "net", "profit"]].head(4)
