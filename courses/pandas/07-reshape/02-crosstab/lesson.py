# Урок pd-crosstab. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% counts
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
pd.crosstab(orders["city"], orders["channel"])

# %% margins
pd.crosstab(orders["city"], orders["channel"], margins=True, margins_name="Всего")

# %% goods [exercise]
cat_channel = pd.crosstab(orders["category"], orders["channel"])
tea_app = cat_channel.loc["Чай", "приложение"]
# ─── заготовка ───
cat_channel = ...
tea_app = ...
# ─── проверка ───
def test_table():
    "cat_channel — число строк: категории × каналы"
    assert isinstance(cat_channel, pd.DataFrame), f"cat_channel — это {type(cat_channel).__name__}, а нужна таблица: pd.crosstab(столбец для строк, столбец для столбцов)"
    assert "Чай" in cat_channel.index and "сайт" in cat_channel.columns, "в строках — категории, в столбцах — каналы: сначала orders[\"category\"], потом orders[\"channel\"]"
    assert cat_channel.shape == (5, 3), f"у cat_channel размер {cat_channel.shape}, а нужно 5 × 3 — без итогов"
    assert cat_channel.loc["Кофе", "сайт"] == 469 and cat_channel.sum().sum() == 2448, "в ячейках должно быть число строк таблицы orders"


def test_cell():
    "tea_app — строк с чаем в приложении"
    assert tea_app == 185, f"tea_app = {tea_app!r}, а строк с чаем, купленным в приложении, — 185: cat_channel.loc[\"Чай\", \"приложение\"]"
# ─── другое решение ───
cat_channel = orders.pivot_table(values="order_id", index="category", columns="channel", aggfunc="count")
tea_app = len(orders[(orders["category"] == "Чай") & (orders["channel"] == "приложение")])
# ─── ошибка ───
cat_channel = pd.crosstab(orders["channel"], orders["category"])
tea_app = cat_channel.loc["приложение", "Чай"]
# ─── ошибка ───
cat_channel = pd.crosstab(orders["category"], orders["channel"], margins=True)
tea_app = cat_channel.loc["Чай", "приложение"]

# %% by-row
pd.crosstab(orders["city"], orders["channel"], normalize="index").round(3)

# %% by-column
pd.crosstab(orders["city"], orders["channel"], normalize="columns").round(3)

# %% by-all
pd.crosstab(orders["city"], orders["channel"], normalize="all").round(3)

# %% norm-quiz [quiz]
t = pd.DataFrame({"a": ["x", "x", "y", "y"], "b": ["p", "q", "p", "p"]})
print(pd.crosstab(t["a"], t["b"], normalize="index").loc["x", "p"])

# %% rows [exercise]
city_mix = pd.crosstab(orders["city"], orders["category"], normalize="index").round(3)
tea_city = city_mix["Чай"].idxmax()
# ─── заготовка ───
city_mix = ...
tea_city = ...
# ─── проверка ───
def test_mix():
    "city_mix — доли категорий в покупках каждого города"
    assert isinstance(city_mix, pd.DataFrame), f"city_mix — это {type(city_mix).__name__}, а нужна таблица: pd.crosstab(...)"
    assert "Казань" in city_mix.index and "Чай" in city_mix.columns, "в строках — города, в столбцах — категории"
    assert city_mix.loc["Москва", "Кофе"] != 379, "в ячейках числа строк, а нужны доли: normalize=\"index\""
    assert abs(city_mix.loc["Москва", "Кофе"] - 0.155) > 0.01, "доли посчитаны от всей таблицы, а нужны внутри города: normalize=\"index\""
    assert abs(city_mix.loc["Москва", "Кофе"] - 0.389) > 0.005, "доли посчитаны по столбцам (какая доля кофе приходится на Москву), а нужны по строкам: normalize=\"index\""
    assert city_mix.loc["Москва", "Кофе"] == 0.4 and city_mix.loc["Новосибирск", "Чай"] == 0.329, "доли должны быть округлены до трёх знаков: у кофе в Москве — 0.4, у чая в Новосибирске — 0.329"


def test_city():
    "tea_city — город с наибольшей долей чая"
    assert tea_city == "Новосибирск", f"tea_city = {tea_city!r}, а доля чая выше всего в другом городе: city_mix[\"Чай\"].idxmax()"
# ─── другое решение ───
counts = pd.crosstab(orders["city"], orders["category"], margins=True)
city_mix = (counts.drop(columns=["All"]).drop("All").T / counts["All"].drop("All")).T.round(3)
tea_city = city_mix["Чай"].sort_values().index[-1]
# ─── ошибка ───
city_mix = pd.crosstab(orders["city"], orders["category"], normalize="columns").round(3)
tea_city = city_mix["Чай"].idxmax()
# ─── ошибка ───
city_mix = pd.crosstab(orders["city"], orders["category"])
tea_city = city_mix["Чай"].idxmax()

# %% delivery
delivery = pd.read_csv("data/delivery_h1.csv").dropna()
delivery["speed"] = pd.cut(delivery["days"], bins=[0, 3, 5, 14], labels=["быстро", "нормально", "долго"])
delivery["rating"] = delivery["rating"].astype("int64")
pd.crosstab(delivery["speed"], delivery["rating"])

# %% delivery-share
pd.crosstab(delivery["speed"], delivery["rating"], normalize="index").round(2)

# %% happy [exercise]
delivery["happy"] = delivery["rating"] >= 4
happy_table = pd.crosstab(delivery["speed"], delivery["happy"], normalize="index")
fast_happy = happy_table.loc["быстро", True]
slow_happy = happy_table.loc["долго", True]
# ─── заготовка ───
# добавьте в delivery столбец happy
happy_table = ...
fast_happy = ...
slow_happy = ...
# ─── проверка ───
def test_happy():
    "happy — оценка 4 или 5"
    assert "happy" in delivery.columns and delivery["happy"].dtype == bool, "в delivery нужен столбец-маска happy: delivery[\"rating\"] >= 4"
    assert delivery["happy"].sum() == 307, "маска не та: оценка не меньше 4"


def test_table():
    "happy_table — доля довольных и недовольных при каждой скорости"
    assert isinstance(happy_table, pd.DataFrame), f"happy_table — это {type(happy_table).__name__}, а нужна таблица: pd.crosstab(...)"
    assert happy_table.shape == (3, 2), f"у happy_table размер {happy_table.shape}, а нужно 3 скорости × 2 значения (False и True)"
    assert abs(happy_table.loc["быстро"].sum() - 1) < 1e-9, "доли в каждой строке должны давать в сумме 1: normalize=\"index\""
    assert abs(fast_happy - 168 / 202) < 1e-9, f"fast_happy = {fast_happy!r}, а среди быстрых доставок довольных ≈ 0.83: happy_table.loc[\"быстро\", True]"
    assert abs(slow_happy - 17 / 104) < 1e-9, f"slow_happy = {slow_happy!r}, а среди долгих доставок довольных ≈ 0.16"
# ─── другое решение ───
delivery["happy"] = delivery["rating"].isin([4, 5])
happy_table = pd.crosstab(delivery["speed"], delivery["happy"], normalize="index")
fast_happy = delivery.loc[delivery["speed"] == "быстро", "happy"].mean()
slow_happy = delivery.loc[delivery["speed"] == "долго", "happy"].mean()
# ─── ошибка ───
delivery["happy"] = delivery["rating"] >= 4
happy_table = pd.crosstab(delivery["speed"], delivery["happy"], normalize="columns")
fast_happy = happy_table.loc["быстро", True]
slow_happy = happy_table.loc["долго", True]
# ─── ошибка ───
delivery["happy"] = delivery["rating"] >= 4
happy_table = pd.crosstab(delivery["speed"], delivery["happy"])
fast_happy = happy_table.loc["быстро", True]
slow_happy = happy_table.loc["долго", True]
