# Урок pd-shares. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% counts
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders["channel"].value_counts()

# %% normalize
orders["channel"].value_counts(normalize=True)

# %% percent
(orders["channel"].value_counts(normalize=True) * 100).round(1)

# %% cats [exercise]
category_pct = (orders["category"].value_counts(normalize=True) * 100).round(1)
coffee_pct = category_pct["Кофе"]
# ─── заготовка ───
category_pct = ...
coffee_pct = ...
# ─── проверка ───
def test_pct():
    "category_pct — проценты строк по категориям, один знак после запятой"
    assert isinstance(category_pct, pd.Series), f"category_pct — это {type(category_pct).__name__}, а нужен Series: value_counts(normalize=True)"
    assert len(category_pct) == 5 and "Кофе" in category_pct.index, "в category_pct должны быть пять категорий: value_counts у столбца category"
    assert category_pct["Кофе"] != 975, "в category_pct числа строк, а нужны проценты: normalize=True и умножение на 100"
    assert abs(category_pct["Кофе"] - 0.398) > 0.01, "в category_pct доли от 0 до 1, а нужны проценты: умножьте на 100"
    assert abs(category_pct["Кофе"] - 39.8284) > 1e-3, "проценты не округлены: .round(1) — выражение перед точкой возьмите в скобки"
    assert category_pct.tolist() == [39.8, 27.9, 20.4, 7.5, 4.4], f"значения сейчас {category_pct.tolist()}, а должны быть [39.8, 27.9, 20.4, 7.5, 4.4]"


def test_coffee():
    "coffee_pct — процент кофе"
    assert coffee_pct == 39.8, f"coffee_pct = {coffee_pct!r}, а кофе — 39.8 %: category_pct[\"Кофе\"]"
# ─── другое решение ───
counts = orders["category"].value_counts()
category_pct = (counts / counts.sum() * 100).round(1)
coffee_pct = category_pct.iloc[0]
# ─── ошибка ───
category_pct = orders["category"].value_counts(normalize=True).round(1)
coffee_pct = category_pct["Кофе"]
# ─── ошибка ───
category_pct = orders["category"].value_counts(normalize=True) * 100
coffee_pct = category_pct["Кофе"]

# %% nan-shares
delivery = pd.read_csv("data/delivery_h1.csv")
delivery["rating"].value_counts(normalize=True).sort_index()

# %% nan-shares-all
delivery["rating"].value_counts(normalize=True, dropna=False).sort_index()

# %% ratings [exercise]
rating_share = delivery["rating"].value_counts(normalize=True)
high_among_rated = rating_share[4] + rating_share[5]
high_among_all = (delivery["rating"] >= 4).mean()
# ─── заготовка ───
rating_share = ...
high_among_rated = ...
high_among_all = ...
# ─── проверка ───
def test_share():
    "rating_share — доли оценок среди поставленных"
    assert isinstance(rating_share, pd.Series), f"rating_share — это {type(rating_share).__name__}, а нужен Series: value_counts(normalize=True)"
    assert len(rating_share) == 5, f"в rating_share {len(rating_share)} строк, а оценок пять — без строки пропусков"
    assert abs(rating_share.sum() - 1) < 1e-9, "сумма долей должна быть 1: normalize=True"
    assert abs(rating_share[4] - 224 / 529) < 1e-9, "доли не те: delivery[\"rating\"].value_counts(normalize=True)"


def test_high():
    "доля четвёрок и пятёрок — среди оценивших и среди всех заказов"
    assert abs(high_among_rated - 326 / 816) > 1e-9, "в high_among_rated — доля среди всех заказов; среди оценивших — сумма двух значений rating_share"
    assert abs(high_among_rated - 326 / 529) < 1e-9, f"high_among_rated = {high_among_rated!r}, а среди оценивших высоких оценок ≈ 0.616"
    assert abs(high_among_all - 326 / 529) > 1e-9, "в high_among_all — доля среди оценивших; среди всех заказов — среднее маски delivery[\"rating\"] >= 4"
    assert abs(high_among_all - 326 / 816) < 1e-9, f"high_among_all = {high_among_all!r}, а среди всех заказов высоких оценок ≈ 0.4"
# ─── другое решение ───
rating_share = delivery["rating"].dropna().value_counts(normalize=True)
high_among_rated = (delivery["rating"].dropna() >= 4).mean()
high_among_all = (delivery["rating"] >= 4).sum() / len(delivery)
# ─── ошибка ───
rating_share = delivery["rating"].value_counts(normalize=True)
high_among_rated = (delivery["rating"] >= 4).mean()
high_among_all = (delivery["rating"] >= 4).mean()

# %% cumsum
steps = pd.Series([3, 1, 4, 2])
steps.cumsum()

# %% cumsum-quiz [quiz]
print(pd.Series([1, 2, 3]).cumsum().tolist())

# %% cum-share
quantity_share = orders["quantity"].value_counts(normalize=True).sort_index()
quantity_share.cumsum().round(3).head(5)

# %% fast [exercise]
cum_days = delivery["days"].value_counts(normalize=True).sort_index().cumsum()
within_week = cum_days[7]
later = 1 - within_week
# ─── заготовка ───
cum_days = ...
within_week = ...
later = ...
# ─── проверка ───
def test_cum():
    "cum_days — накопленная доля заказов по сроку доставки"
    assert isinstance(cum_days, pd.Series), f"cum_days — это {type(cum_days).__name__}, а нужен Series: доли, отсортированные по сроку, и cumsum()"
    assert list(cum_days.index) == sorted(cum_days.index), "сроки должны идти по возрастанию: sort_index() — до cumsum()"
    assert abs(cum_days.iloc[-1] - 1) < 1e-9, "последнее значение накопленной доли должно быть 1: нужен normalize=True"
    assert abs(cum_days.iloc[0] - 119 / 780) < 1e-9, "первое значение — доля заказов со сроком 2 дня (≈ 0.153): сначала sort_index(), потом cumsum()"


def test_week():
    "within_week и later — доставлено за 7 дней и позже"
    assert abs(within_week - 749 / 780) < 1e-9, f"within_week = {within_week!r}, а за 7 дней доставлено ≈ 0.96 заказов: cum_days[7]"
    assert abs(later - 31 / 780) < 1e-9, f"later = {later!r}, а дольше недели везли ≈ 0.04 заказов: 1 − within_week"
# ─── другое решение ───
cum_days = (delivery["days"].value_counts().sort_index() / delivery["days"].count()).cumsum()
within_week = (delivery["days"].dropna() <= 7).mean()
later = (delivery["days"].dropna() > 7).mean()
# ─── ошибка ───
cum_days = delivery["days"].value_counts(normalize=True).cumsum()
within_week = cum_days[7]
later = 1 - within_week
# ─── ошибка ───
cum_days = delivery["days"].value_counts().sort_index().cumsum()
within_week = cum_days[7]
later = 1 - within_week

# %% pareto
product_share = orders["product"].value_counts(normalize=True)
product_share.cumsum().round(3).head(7)

# %% pareto-count
print((product_share.cumsum() <= 0.5).sum(), "из", len(product_share))

# %% buyers [exercise]
buyer_share = orders["customer_id"].value_counts(normalize=True)
cum_buyers = buyer_share.cumsum()
core = (cum_buyers <= 0.5).sum()
core_share = core / len(buyer_share)
# ─── заготовка ───
buyer_share = ...
cum_buyers = ...
core = ...
core_share = ...
# ─── проверка ───
def test_shares():
    "buyer_share и cum_buyers — доля строк каждого покупателя и накопленная доля"
    assert isinstance(buyer_share, pd.Series) and len(buyer_share) == 213, "buyer_share — доли 213 покупателей: orders[\"customer_id\"].value_counts(normalize=True)"
    assert abs(buyer_share.sum() - 1) < 1e-9, "сумма долей должна быть 1: normalize=True"
    assert isinstance(cum_buyers, pd.Series) and len(cum_buyers) == 213, "cum_buyers — накопленная доля: buyer_share.cumsum()"
    assert abs(cum_buyers.iloc[-1] - 1) < 1e-9 and abs(cum_buyers.iloc[0] - 56 / 2448) < 1e-9, "cum_buyers — это buyer_share.cumsum(): от самого активного покупателя к самому редкому"


def test_core():
    "core и core_share — сколько покупателей дают половину строк"
    assert core == 43, f"core = {core!r}, а половину строк дают 43 самых активных покупателя: сумма маски cum_buyers <= 0.5"
    assert abs(core_share - 43 / 213) < 1e-9, f"core_share = {core_share!r}, а это ≈ 0.2 от всех покупателей: core / число покупателей"
# ─── другое решение ───
counts = orders["customer_id"].value_counts()
buyer_share = counts / counts.sum()
cum_buyers = buyer_share.cumsum()
core = len(cum_buyers[cum_buyers <= 0.5])
core_share = core / orders["customer_id"].nunique()
# ─── ошибка ───
buyer_share = orders["customer_id"].value_counts(normalize=True)
cum_buyers = buyer_share.cumsum()
core = (cum_buyers <= 0.5).sum()
core_share = core / len(orders)
