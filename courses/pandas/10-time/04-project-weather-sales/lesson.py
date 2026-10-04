# Урок pd-project-weather-sales. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv", parse_dates=["date"])
orders["revenue"] = orders["price"] * orders["quantity"]
msk = orders[orders["city"] == "Москва"]
weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
moscow = weather[weather["city"] == "Москва"].set_index("date")
print(len(msk), len(moscow))
moscow.head(3)

# %% daily [exercise]
calendar = pd.date_range("2025-01-01", "2025-12-31")
total = msk.groupby("date")["revenue"].sum().reindex(calendar, fill_value=0)
tea = msk[msk["category"] == "Чай"].groupby("date")["revenue"].sum().reindex(calendar, fill_value=0)
# ─── заготовка ───
calendar = pd.date_range("2025-01-01", "2025-12-31")
total = ...
tea = ...
# ─── проверка ───
def test_total():
    "total — выручка Москвы за каждый день года"
    assert isinstance(total, pd.Series), f"total — это {type(total).__name__}, а нужен Series"
    assert len(total) == 365, f"в total {len(total)} значений, а нужно 365 — по одному на каждый день"
    assert total.isna().sum() == 0, "в total пропуски: в дни без продаж выручка — ноль"
    assert total.sum() == 1310110, "сумма total не равна выручке Москвы за год"


def test_tea():
    "tea — выручка от чая в Москве за каждый день года"
    assert isinstance(tea, pd.Series) and len(tea) == 365, "tea — 365 значений"
    assert tea.isna().sum() == 0, "в tea пропуски: в дни без продаж выручка — ноль"
    assert tea.sum() != 1310110, "в tea вся выручка, а нужен только чай"
    assert tea.sum() == 230690, "сумма tea не равна выручке от чая в Москве"
# ─── другое решение ───
calendar = pd.date_range("2025-01-01", "2025-12-31")
total = msk.set_index("date")["revenue"].resample("D").sum().reindex(calendar, fill_value=0)
tea = msk.query("category == 'Чай'").groupby("date")["revenue"].sum().reindex(calendar).fillna(0)
# ─── ошибка ───
calendar = pd.date_range("2025-01-01", "2025-12-31")
total = msk.groupby("date")["revenue"].sum()
tea = msk[msk["category"] == "Чай"].groupby("date")["revenue"].sum()
# ─── ошибка ───
calendar = pd.date_range("2025-01-01", "2025-12-31")
total = msk.groupby("date")["revenue"].sum().reindex(calendar, fill_value=0)
tea = msk.groupby("date")["revenue"].sum().reindex(calendar, fill_value=0)

# %% table [exercise]
data = pd.DataFrame({"temp": moscow["temp_max"], "rain": moscow["precip_mm"], "tea": tea, "total": total})
gaps = data.isna().sum()
# ─── заготовка ───
data = ...
gaps = ...
# ─── проверка ───
def test_data():
    "data — температура, осадки и продажи рядом"
    assert isinstance(data, pd.DataFrame), f"data — это {type(data).__name__}, а нужна таблица"
    assert list(data.columns) == ["temp", "rain", "tea", "total"], f"столбцы сейчас {list(data.columns)}, а нужны temp, rain, tea, total"
    assert len(data) == 365, f"в data {len(data)} строк, а должно быть 365 — по дню"
    assert abs(data["temp"].iloc[0] - (-3.2)) < 1e-9, "temp — столбец temp_max таблицы moscow"
    assert data["tea"].sum() == 230690 and data["total"].sum() == 1310110, "tea и total не те: нужны ряды из прошлого шага"


def test_gaps():
    "gaps — пропуски по столбцам"
    assert isinstance(gaps, pd.Series) and list(gaps.index) == ["temp", "rain", "tea", "total"], "gaps — это должно быть число пропусков в каждом столбце data"
    assert gaps["rain"] == 1 and gaps.sum() == 1, "числа не те: нужно число пропусков в каждом столбце data"
# ─── другое решение ───
data = pd.concat([moscow["temp_max"].rename("temp"), moscow["precip_mm"].rename("rain"), tea.rename("tea"), total.rename("total")], axis=1)
gaps = len(data) - data.count()
# ─── ошибка ───
data = pd.DataFrame({"temp": moscow["temp_min"], "rain": moscow["precip_mm"], "tea": tea, "total": total})
gaps = data.isna().sum()

# %% corr-toy
height = pd.Series([150, 160, 170, 180, 190])
print(round(height.corr(pd.Series([50, 58, 66, 75, 84])), 3))
print(round(height.corr(pd.Series([9, 8, 6, 5, 3])), 3))
print(round(height.corr(pd.Series([4, 9, 2, 8, 5])), 3))

# %% corr-day [exercise]
r_day = data["temp"].corr(data["tea"])
r_rain = data["rain"].corr(data["total"])
# ─── заготовка ───
r_day = ...
r_rain = ...
# ─── проверка ───
def test_r_day():
    "r_day — корреляция температуры и продаж чая по дням"
    assert not isinstance(r_day, (pd.Series, pd.DataFrame)), "r_day — таблица или Series, а нужно одно число"
    assert abs(r_day - (-0.1715)) < 1e-3, f"r_day = {r_day!r} — это не корреляция temp и tea"


def test_r_rain():
    "r_rain — корреляция осадков и общей выручки"
    assert abs(r_rain - 0.0625) < 1e-3, f"r_rain = {r_rain!r} — это не корреляция rain и total"
# ─── другое решение ───
r_day = data[["temp", "tea"]].corr().loc["temp", "tea"]
r_rain = data["total"].corr(data["rain"])
# ─── ошибка ───
r_day = data["temp"].corr(data["total"])
r_rain = data["rain"].corr(data["total"])

# %% weekly [exercise]
weekly = data.resample("W").agg(temp=("temp", "mean"), tea=("tea", "sum")).iloc[1:-1]
r_week = weekly["temp"].corr(weekly["tea"])
# ─── заготовка ───
weekly = ...
r_week = ...
# ─── проверка ───
def test_weekly():
    "weekly — средняя температура и выручка от чая по полным неделям"
    assert isinstance(weekly, pd.DataFrame), f"weekly — это {type(weekly).__name__}, а нужна таблица"
    assert list(weekly.columns) == ["temp", "tea"], f"столбцы сейчас {list(weekly.columns)}, а нужны temp и tea"
    assert len(weekly) != 53, "в weekly 53 недели вместе с неполными: отбросьте первую и последнюю"
    assert len(weekly) == 51, f"в weekly {len(weekly)} строк, а полных недель 51"
    assert weekly["tea"].iloc[0] > 3000, "tea — сумма за неделю, а не среднее"
    assert weekly["temp"].iloc[0] > -20, "temp — средняя за неделю, а не сумма"


def test_r_week():
    "r_week — корреляция по неделям"
    assert abs(r_week - (-0.4110)) < 1e-3, f"r_week = {r_week!r} — это не корреляция temp и tea по неделям"
# ─── другое решение ───
weekly = pd.DataFrame({"temp": data["temp"].resample("W").mean(), "tea": data["tea"].resample("W").sum()}).iloc[1:-1]
r_week = weekly.corr().loc["temp", "tea"]
# ─── ошибка ───
weekly = data.resample("W").agg(temp=("temp", "mean"), tea=("tea", "sum"))
r_week = weekly["temp"].corr(weekly["tea"])

# %% monthly [exercise]
monthly = data.resample("ME").agg(temp=("temp", "mean"), tea=("tea", "sum")).round(1)
r_month = monthly["temp"].corr(monthly["tea"])
tea_peak = monthly["tea"].idxmax().month
# ─── заготовка ───
monthly = ...
r_month = ...
tea_peak = ...
# ─── проверка ───
def test_monthly():
    "monthly — средняя температура и выручка от чая по месяцам"
    assert isinstance(monthly, pd.DataFrame) and list(monthly.columns) == ["temp", "tea"], "monthly — таблица со столбцами temp и tea"
    assert len(monthly) == 12, f"в monthly {len(monthly)} строк, а месяцев 12"
    assert monthly["temp"].iloc[0] == -3.8 and monthly["tea"].iloc[0] == 27400, "значения не те: средняя температура и сумма чая за месяц, один знак"


def test_answers():
    "r_month — корреляция по месяцам, tea_peak — лучший месяц чая"
    assert abs(r_month - (-0.7041)) < 2e-3, f"r_month = {r_month!r} — это не корреляция temp и tea по месяцам"
    assert tea_peak == 12, f"tea_peak = {tea_peak!r} — это не номер лучшего месяца чая"
# ─── другое решение ───
monthly = pd.DataFrame({"temp": data["temp"].resample("ME").mean(), "tea": data["tea"].resample("ME").sum()}).round(1)
r_month = monthly.corr().loc["tea", "temp"]
tea_peak = monthly.sort_values("tea").index[-1].month
# ─── ошибка ───
monthly = data.resample("ME").agg(temp=("temp", "sum"), tea=("tea", "sum")).round(1)
r_month = monthly["temp"].corr(monthly["tea"])
tea_peak = monthly["tea"].idxmax().month

# %% monthly-view
monthly

# %% bands [exercise]
data["band"] = pd.cut(data["temp"], bins=[-50, 0, 15, 50], labels=["мороз", "прохладно", "тепло"])
tea_by_band = data.groupby("band")["tea"].mean().round(1)
# ─── заготовка ───
# добавьте в data столбец band
tea_by_band = ...
# ─── проверка ───
def test_band():
    "band — температурная группа дня"
    assert "band" in data.columns, "в data нет столбца band"
    counts = data["band"].value_counts()
    assert counts["мороз"] == 106 and counts["прохладно"] == 129 and counts["тепло"] == 130, "группы не те: сверьте границы и подписи с условием"


def test_tea():
    "tea_by_band — средняя дневная выручка от чая в каждой группе"
    assert isinstance(tea_by_band, pd.Series) and len(tea_by_band) == 3, "tea_by_band — Series по трём группам"
    assert tea_by_band["мороз"] != 96850, "в tea_by_band суммы, а нужна средняя выручка в день"
    assert tea_by_band.tolist() == [913.7, 544.3, 489.4], f"значения сейчас {tea_by_band.tolist()}: нужна средняя дневная выручка чая в группе, один знак"
# ─── другое решение ───
data["band"] = pd.cut(data["temp"], [-50, 0, 15, 50], labels=["мороз", "прохладно", "тепло"])
tea_by_band = data.pivot_table(values="tea", index="band", aggfunc="mean")["tea"].round(1)
# ─── ошибка ───
data["band"] = pd.cut(data["temp"], bins=[-50, 0, 15, 50], labels=["мороз", "прохладно", "тепло"])
tea_by_band = data.groupby("band")["tea"].sum().round(1)

# %% within
data["month"] = data.index.month
temp_dev = data["temp"] - data.groupby("month")["temp"].transform("mean")
tea_dev = data["tea"] - data.groupby("month")["tea"].transform("mean")
print(round(temp_dev.corr(tea_dev), 2))

# %% summary
print("Корреляция температуры и продаж чая:")
print("  по дням   ", round(r_day, 2))
print("  по неделям", round(r_week, 2))
print("  по месяцам", round(r_month, 2))
print("Осадки и выручка:", round(r_rain, 2))
print(tea_by_band)
