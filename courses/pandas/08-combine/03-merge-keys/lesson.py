# Урок pd-merge-keys. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

orders = pd.read_csv("data/orders.csv")
products = pd.read_csv("data/products.csv")
customers = pd.read_csv("data/customers.csv")
print(list(products.columns))
print(list(customers.columns))

# %% left-right
catalog = products.rename(columns={"product_id": "id"})
joined = orders.merge(catalog, left_on="product_id", right_on="id")
list(joined.columns)

# %% same-names
both = orders.merge(products, on="product_id").merge(customers, on="customer_id")
list(both.columns)

# %% suffixes
both = orders.merge(products, on="product_id").merge(customers, on="customer_id", suffixes=("_product", "_customer"))
both[["order_id", "name_product", "name_customer", "city"]].head(3)

# %% full [exercise]
supplier = pd.read_csv("data/supplier_prices.csv")
compare = products.merge(supplier[["product_id", "cost", "stock"]], on="product_id", suffixes=("_now", "_new"))
compare["cost_new"] = pd.to_numeric(compare["cost_new"], errors="coerce")
compare["cost_change"] = compare["cost_new"] - compare["cost_now"]
# ─── заготовка ───
supplier = pd.read_csv("data/supplier_prices.csv")
compare = ...
# переведите cost_new в числа и добавьте столбец cost_change
# ─── проверка ───
def test_compare():
    "compare — товары с текущей и новой себестоимостью"
    assert isinstance(compare, pd.DataFrame), f"compare — это {type(compare).__name__}, а нужна таблица: products.merge(...)"
    assert len(compare) == 20, f"в compare {len(compare)} строк, а товаров 20"
    assert "cost_x" not in compare.columns, "столбцы называются cost_x и cost_y: задайте свои окончания — suffixes=(\"_now\", \"_new\")"
    assert "cost_now" in compare.columns and "cost_new" in compare.columns, f"в compare нужны столбцы cost_now и cost_new, а сейчас {list(compare.columns)}"
    assert "stock" in compare.columns and "name" in compare.columns, "из прайса поставщика нужны только product_id, cost и stock — тогда остальные столбцы не задвоятся"
    assert "name_now" not in compare.columns, "задвоился столбец name: берите из supplier только нужные столбцы — supplier[[\"product_id\", \"cost\", \"stock\"]]"


def test_change():
    "cost_new — числа, cost_change — на сколько выросла себестоимость"
    assert "cost_new" in compare.columns, "в compare нет столбца cost_new — сначала исправьте то, о чём говорит проверка выше"
    assert compare["cost_new"].dtype == float, "cost_new пока текст: pd.to_numeric(compare[\"cost_new\"], errors=\"coerce\")"
    assert compare["cost_new"].isna().sum() == 3, "в cost_new должно быть три пропуска — там, где поставщик написал «нет данных» или «—»"
    assert "cost_change" in compare.columns, "в compare нет столбца cost_change"
    assert compare.loc[0, "cost_change"] == 50, f"cost_change в первой строке — {compare.loc[0, 'cost_change']}, а должно быть 50 (920 − 870): новая себестоимость минус текущая"
# ─── другое решение ───
supplier = pd.read_csv("data/supplier_prices.csv")
new_cost = supplier[["product_id", "cost", "stock"]].rename(columns={"cost": "cost_new"})
compare = products.rename(columns={"cost": "cost_now"}).merge(new_cost, on="product_id")
compare["cost_new"] = pd.to_numeric(compare["cost_new"], errors="coerce")
compare["cost_change"] = compare["cost_new"] - compare["cost_now"]
# ─── ошибка ───
supplier = pd.read_csv("data/supplier_prices.csv")
compare = products.merge(supplier[["product_id", "cost", "stock"]], on="product_id")
# ─── ошибка ───
supplier = pd.read_csv("data/supplier_prices.csv")
compare = products.merge(supplier, on="product_id", suffixes=("_now", "_new"))
compare["cost_new"] = pd.to_numeric(compare["cost_new"], errors="coerce")
compare["cost_change"] = compare["cost_new"] - compare["cost_now"]

# %% returns
returns = pd.read_csv("data/returns_raw.csv").drop_duplicates()
returns = returns.drop_duplicates(subset=["order_id", "product_id"])[["order_id", "product_id", "quantity"]]
print(len(returns))
returns.head(3)

# %% wrong-key
wrong = orders.merge(returns[["order_id", "quantity"]], on="order_id", how="left", suffixes=("", "_returned"))
print(len(orders), len(wrong))
print(wrong["quantity_returned"].sum(), returns["quantity"].sum())

# %% wrong-look
wrong[wrong["order_id"] == 10001]

# %% dup-quiz [quiz]
a = pd.DataFrame({"k": ["x", "x"], "a": [1, 2]})
b = pd.DataFrame({"k": ["x", "x"], "b": [3, 4]})
print(len(a.merge(b, on="k")))

# %% two-keys
right = orders.merge(returns, on=["order_id", "product_id"], how="left", suffixes=("", "_returned"))
print(len(right))
right[right["order_id"] == 10001]

# %% returned [exercise]
lines = orders.merge(returns, on=["order_id", "product_id"], how="left", suffixes=("", "_returned"))
lines["quantity_returned"] = lines["quantity_returned"].fillna(0).astype("int64")
return_rate = lines["quantity_returned"].sum() / lines["quantity"].sum()
# ─── заготовка ───
lines = ...
# замените пропуски в lines["quantity_returned"] нулями, тип — целый
return_rate = ...
# ─── проверка ───
def test_lines():
    "lines — строки заказов с числом возвращённых штук"
    assert isinstance(lines, pd.DataFrame), f"lines — это {type(lines).__name__}, а нужна таблица: orders.merge(returns, ...)"
    assert len(lines) != 2458, "строк стало 2458 — больше, чем в orders: соединять нужно по двум ключам сразу, on=[\"order_id\", \"product_id\"]"
    assert len(lines) != 150, "осталось 150 строк — только позиции с возвратом: нужны все строки заказов, how=\"left\""
    assert len(lines) == 2448, f"в lines {len(lines)} строк, а должно быть 2448 — столько же, сколько в orders"
    assert "quantity_returned" in lines.columns and "quantity" in lines.columns, f"в lines нужны столбцы quantity и quantity_returned: suffixes=(\"\", \"_returned\"). Сейчас столбцы {list(lines.columns)}"
    assert lines["quantity_returned"].isna().sum() == 0, "в quantity_returned остались пропуски: позиция без возврата — это ноль возвращённых штук, fillna(0)"
    assert str(lines["quantity_returned"].dtype) in ("int64", "int32"), "quantity_returned должен быть целым: astype(\"int64\")"
    assert lines["quantity_returned"].sum() == 214, "возвращено должно быть 214 штук"


def test_rate():
    "return_rate — доля возвращённых штук"
    assert abs(return_rate - 214 / 5210) < 1e-9, f"return_rate = {return_rate!r}, а возвращено ≈ 0.041 проданных штук: сумма quantity_returned, делённая на сумму quantity"
# ─── другое решение ───
lines = pd.merge(orders, returns.rename(columns={"quantity": "quantity_returned"}), on=["order_id", "product_id"], how="left")
lines["quantity_returned"] = lines["quantity_returned"].fillna(0).astype("int64")
return_rate = returns["quantity"].sum() / orders["quantity"].sum()
# ─── ошибка ───
lines = orders.merge(returns[["order_id", "quantity"]], on="order_id", how="left", suffixes=("", "_returned"))
lines["quantity_returned"] = lines["quantity_returned"].fillna(0).astype("int64")
return_rate = lines["quantity_returned"].sum() / lines["quantity"].sum()
# ─── ошибка ───
lines = orders.merge(returns, on=["order_id", "product_id"], suffixes=("", "_returned"))
lines["quantity_returned"] = lines["quantity_returned"].fillna(0).astype("int64")
return_rate = lines["quantity_returned"].sum() / lines["quantity"].sum()

# %% validate-ok
checked = orders.merge(products, on="product_id", validate="many_to_one")
len(checked)

# %% validate-fail [raises=MergeError]
orders.merge(returns[["order_id", "quantity"]], on="order_id", how="left", validate="many_to_one")

# %% indicator
buyers = orders[["customer_id"]].drop_duplicates()
marked = customers.merge(buyers, on="customer_id", how="left", indicator=True)
marked["_merge"].value_counts()

# %% rates [exercise]
sold = lines.groupby("product_id", as_index=False).agg(sold=("quantity", "sum"), returned=("quantity_returned", "sum"))
sold["rate"] = (sold["returned"] / sold["sold"]).round(3)
rates = sold.merge(products[["product_id", "name"]], on="product_id", validate="one_to_one").sort_values("rate", ascending=False)
worst_name = rates.iloc[0]["name"]
# ─── заготовка ───
sold = ...
# добавьте в sold столбец rate
rates = ...
worst_name = ...
# ─── проверка ───
def test_sold():
    "sold — продано и возвращено штук по товарам, доля возврата"
    assert isinstance(sold, pd.DataFrame), f"sold — это {type(sold).__name__}, а нужна таблица: lines.groupby(\"product_id\", as_index=False).agg(...)"
    assert list(sold.columns)[:3] == ["product_id", "sold", "returned"], f"столбцы сейчас {list(sold.columns)}, а первые три должны быть product_id, sold, returned"
    assert len(sold) == 20 and sold["sold"].sum() == 5210 and sold["returned"].sum() == 214, "в sold 20 товаров; продано 5210 штук, возвращено 214"
    assert "rate" in sold.columns and abs(sold["rate"].max() - 0.094) < 1e-9, "rate — returned, делённое на sold, с округлением до трёх знаков; наибольшее значение — 0.094"


def test_rates():
    "rates — с названиями, по убыванию доли возврата; worst_name — товар с наибольшей долей"
    assert isinstance(rates, pd.DataFrame) and len(rates) == 20, "rates — 20 строк: sold, соединённая с названиями товаров"
    assert "name" in rates.columns and "rate" in rates.columns, "в rates нужны столбцы name и rate: sold.merge(products[[\"product_id\", \"name\"]], on=\"product_id\")"
    assert rates["rate"].tolist() == sorted(rates["rate"].tolist(), reverse=True), "отсортируйте rates по убыванию rate"
    assert worst_name == "Кофемолка ручная", f"worst_name = {worst_name!r}, а чаще всего возвращают другой товар: rates.iloc[0][\"name\"]"
# ─── другое решение ───
g = lines.groupby("product_id")
sold = pd.DataFrame({"sold": g["quantity"].sum(), "returned": g["quantity_returned"].sum()}).reset_index()
sold["rate"] = round(sold["returned"] / sold["sold"], 3)
rates = sold.merge(products[["product_id", "name"]], on="product_id").sort_values("rate", ascending=False)
worst_name = rates["name"].iloc[0]
# ─── ошибка ───
sold = lines.groupby("product_id", as_index=False).agg(sold=("quantity", "sum"), returned=("quantity_returned", "sum"))
sold["rate"] = (sold["returned"] / sold["sold"]).round(3)
rates = sold.merge(products[["product_id", "name"]], on="product_id").sort_values("returned", ascending=False)
worst_name = rates.iloc[0]["name"]
