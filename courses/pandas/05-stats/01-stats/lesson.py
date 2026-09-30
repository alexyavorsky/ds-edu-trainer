# Урок pd-stats. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
moscow = weather[weather["city"] == "Москва"]
moscow.head(3)

# %% mean-median
rain = moscow["precip_mm"]
print(rain.mean())
print(rain.median())
print((rain == 0).mean())

# %% outlier
salaries = pd.Series([60, 65, 70, 75, 80])
with_boss = pd.Series([60, 65, 70, 75, 80, 900])
print(salaries.mean(), salaries.median())
print(with_boss.mean(), with_boss.median())

# %% median-quiz [quiz]
print(pd.Series([1, 2, 100]).median())

# %% typical [exercise]
orders = pd.read_csv("data/shop_orders.csv")
revenue = orders["price"] * orders["quantity"]
mean_revenue = revenue.mean()
median_revenue = revenue.median()
above_mean = (revenue > mean_revenue).mean()
# ─── заготовка ───
orders = pd.read_csv("data/shop_orders.csv")
revenue = orders["price"] * orders["quantity"]
mean_revenue = ...
median_revenue = ...
above_mean = ...
# ─── проверка ───
def test_typical():
    "mean_revenue и median_revenue — среднее и медиана выручки строки"
    assert abs(mean_revenue - 1348.61928) < 1e-4, f"mean_revenue = {mean_revenue!r}, а среднее ≈ 1348.62: revenue.mean()"
    assert abs(median_revenue - 1348.61928) > 1e-4, "в median_revenue — среднее; медиану считает метод median()"
    assert median_revenue == 1080, f"median_revenue = {median_revenue!r}, а медиана — 1080"


def test_above():
    "above_mean — доля строк с выручкой выше средней"
    assert abs(above_mean - 963) > 1e-9, "963 — число таких строк, а нужна доля: среднее маски"
    assert abs(above_mean - 963 / 2448) < 1e-9, f"above_mean = {above_mean!r}, а доля ≈ 0.393: среднее маски revenue > mean_revenue"
# ─── другое решение ───
orders = pd.read_csv("data/shop_orders.csv")
revenue = orders["price"] * orders["quantity"]
mean_revenue = revenue.sum() / len(revenue)
median_revenue = revenue.quantile(0.5)
above_mean = (revenue > mean_revenue).sum() / len(revenue)
# ─── ошибка ───
orders = pd.read_csv("data/shop_orders.csv")
revenue = orders["price"] * orders["quantity"]
mean_revenue = revenue.mean()
median_revenue = revenue.mean()
above_mean = (revenue > mean_revenue).mean()
# ─── ошибка ───
orders = pd.read_csv("data/shop_orders.csv")
revenue = orders["price"] * orders["quantity"]
mean_revenue = revenue.mean()
median_revenue = revenue.median()
above_mean = (revenue > mean_revenue).sum()

# %% std
sochi = weather[weather["city"] == "Сочи"]
print(moscow["temp_max"].mean(), moscow["temp_max"].std())
print(sochi["temp_max"].mean(), sochi["temp_max"].std())

# %% std-toy
print(pd.Series([10, 10, 10, 10]).std())
print(pd.Series([9, 10, 10, 11]).std())
print(pd.Series([0, 5, 15, 20]).std())

# %% spread [exercise]
novosibirsk = weather[weather["city"] == "Новосибирск"]
mean_nsk = novosibirsk["temp_max"].mean()
std_nsk = novosibirsk["temp_max"].std()
range_nsk = novosibirsk["temp_max"].max() - novosibirsk["temp_max"].min()
# ─── заготовка ───
novosibirsk = ...
mean_nsk = ...
std_nsk = ...
range_nsk = ...
# ─── проверка ───
def test_city():
    "novosibirsk — погода в Новосибирске"
    assert isinstance(novosibirsk, pd.DataFrame), f"novosibirsk — это {type(novosibirsk).__name__}, а нужна таблица: weather[маска]"
    assert len(novosibirsk) == 365 and (novosibirsk["city"] == "Новосибирск").all(), "в novosibirsk должны быть 365 строк одного города: weather[weather[\"city\"] == \"Новосибирск\"]"


def test_numbers():
    "среднее, стандартное отклонение и размах temp_max"
    assert abs(mean_nsk - 4.359178) < 1e-5, f"mean_nsk = {mean_nsk!r}, а средний дневной максимум ≈ 4.36"
    assert abs(std_nsk - 13.959101) < 1e-5, f"std_nsk = {std_nsk!r}, а стандартное отклонение ≈ 13.96: метод std()"
    assert abs(range_nsk - 30.7) > 1e-9, "в range_nsk — максимум, а размах — это максимум минус минимум"
    assert abs(range_nsk - 51.4) < 1e-9, f"range_nsk = {range_nsk!r}, а размах — 51.4 градуса: max() − min()"
# ─── другое решение ───
novosibirsk = weather.query("city == 'Новосибирск'")
stats = novosibirsk["temp_max"].describe()
mean_nsk = stats["mean"]
std_nsk = stats["std"]
range_nsk = stats["max"] - stats["min"]
# ─── ошибка ───
novosibirsk = weather[weather["city"] == "Новосибирск"]
mean_nsk = novosibirsk["temp_max"].mean()
std_nsk = novosibirsk["temp_max"].std()
range_nsk = novosibirsk["temp_max"].max()

# %% quantile
print(moscow["temp_max"].quantile(0.5))
print(moscow["temp_max"].quantile(0.9))

# %% quantiles
moscow["temp_max"].quantile([0.25, 0.5, 0.75])

# %% hot [exercise]
q90 = moscow["temp_max"].quantile(0.9)
hot_days = moscow[moscow["temp_max"] > q90]
n_hot = len(hot_days)
# ─── заготовка ───
q90 = ...
hot_days = ...
n_hot = ...
# ─── проверка ───
def test_q90():
    "q90 — 90-й процентиль дневного максимума"
    assert abs(q90 - 18.5) > 1e-9, "18.5 — это квантиль 0.75; нужен 0.9"
    assert abs(q90 - 22.0) < 1e-9, f"q90 = {q90!r}, а 90-й процентиль — 22.0: moscow[\"temp_max\"].quantile(0.9)"


def test_hot():
    "hot_days — дни теплее q90"
    assert isinstance(hot_days, pd.DataFrame), f"hot_days — это {type(hot_days).__name__}, а нужна таблица: moscow[маска]"
    assert len(hot_days) != 38, "в hot_days попали дни с температурой ровно 22.0: условие — строго больше q90"
    assert len(hot_days) == 36 and n_hot == 36, f"в hot_days {len(hot_days)} строк, n_hot = {n_hot!r}, а дней теплее q90 — 36"
    assert hot_days["temp_max"].min() > 22.0, "в hot_days есть дни не теплее 22.0"
# ─── другое решение ───
q90 = moscow["temp_max"].quantile([0.9]).iloc[0]
hot_days = moscow.query("temp_max > @q90")
n_hot = (moscow["temp_max"] > q90).sum()
# ─── ошибка ───
q90 = moscow["temp_max"].quantile(0.9)
hot_days = moscow[moscow["temp_max"] >= q90]
n_hot = len(hot_days)
# ─── ошибка ───
q90 = moscow["temp_max"].quantile(0.75)
hot_days = moscow[moscow["temp_max"] > q90]
n_hot = len(hot_days)

# %% idxmax
label = moscow["temp_max"].idxmax()
print(label)
moscow.loc[label]

# %% frame-stats
moscow[["temp_min", "temp_max", "precip_mm", "wind_ms"]].mean()

# %% frame-error [raises=TypeError]
moscow.mean()

# %% extremes [exercise]
coldest_label = moscow["temp_min"].idxmin()
coldest_date = moscow.loc[coldest_label, "date"]
windiest = moscow.loc[moscow["wind_ms"].idxmax()]
# ─── заготовка ───
coldest_label = ...
coldest_date = ...
windiest = ...
# ─── проверка ───
def test_coldest():
    "самая холодная ночь: метка строки и дата"
    assert coldest_label != 196, "196 — метка самого тёплого дня; самую низкую температуру ищет idxmin по столбцу temp_min"
    assert coldest_label == 44, f"coldest_label = {coldest_label!r}, а метка строки с наименьшим temp_min — 44: moscow[\"temp_min\"].idxmin()"
    assert not isinstance(coldest_date, pd.Series), "coldest_date — целая строка, а нужна одна дата: moscow.loc[coldest_label, \"date\"]"
    assert coldest_date == pd.to_datetime("2025-02-14"), f"coldest_date = {coldest_date}, а самая холодная ночь — 14 февраля"


def test_windiest():
    "windiest — строка самого ветреного дня"
    assert isinstance(windiest, pd.Series), f"windiest — это {type(windiest).__name__}, а нужна строка таблицы: moscow.loc[метка]"
    assert "wind_ms" in windiest.index, "windiest должна быть целой строкой таблицы moscow со всеми столбцами"
    assert windiest["wind_ms"] == 13.6 and windiest["date"] == pd.to_datetime("2025-08-07"), "это не самый ветреный день: метка — moscow[\"wind_ms\"].idxmax()"
# ─── другое решение ───
coldest_label = moscow.sort_values("temp_min").index[0]
coldest_date = moscow["date"].loc[coldest_label]
windiest = moscow.nlargest(1, "wind_ms").iloc[0]
# ─── ошибка ───
coldest_label = moscow["temp_max"].idxmax()
coldest_date = moscow.loc[coldest_label, "date"]
windiest = moscow.loc[moscow["wind_ms"].idxmax()]
# ─── ошибка ───
coldest_label = moscow["temp_min"].idxmin()
coldest_date = moscow.loc[coldest_label]
windiest = moscow.loc[moscow["wind_ms"].idxmax()]
