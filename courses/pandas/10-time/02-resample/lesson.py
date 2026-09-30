# Урок pd-resample. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% daily
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv", parse_dates=["date"])
orders["revenue"] = orders["price"] * orders["quantity"]
daily = orders.groupby("date")["revenue"].sum()
calendar = pd.date_range("2025-01-01", "2025-12-31")
sales = daily.reindex(calendar, fill_value=0)
order_count = orders.groupby("date")["order_id"].nunique().reindex(calendar, fill_value=0).rename("orders")
print(sales.head(3))
order_count.head(3)

# %% month-end
order_count.resample("ME").sum().head(4)

# %% month-start
order_count.resample("MS").sum().head(4)

# %% old-m [raises=ValueError]
order_count.resample("M").sum()

# %% stamp
week = order_count.resample("W").sum().index[20]
print(week)
print(week.month, week.quarter)

# %% months [exercise]
monthly = sales.resample("ME").sum()
best_month = monthly.idxmax().month
worst_month = monthly.idxmin().month
# ─── заготовка ───
monthly = ...
best_month = ...
worst_month = ...
# ─── проверка ───
def test_monthly():
    "monthly — выручка по месяцам"
    assert isinstance(monthly, pd.Series), f"monthly — это {type(monthly).__name__}, а нужен Series: sales.resample(\"ME\").sum()"
    assert len(monthly) == 12, f"в monthly {len(monthly)} значений, а месяцев 12: частота \"ME\""
    assert monthly.iloc[0] != 10288 and abs(monthly.iloc[0] - 10288.387) > 1, "в monthly средние за день, а нужны суммы за месяц: .sum()"
    assert monthly.iloc[0] == 318940 and monthly.sum() == 3301420, "суммы не те: январь — 318940, весь год — 3301420"


def test_best():
    "best_month и worst_month — номера лучшего и худшего месяца"
    assert not isinstance(best_month, pd.Timestamp), "best_month — дата, а нужен номер месяца: у даты есть атрибут .month"
    assert best_month == 12, f"best_month = {best_month!r}, а лучший месяц — декабрь (12): monthly.idxmax().month"
    assert worst_month == 7, f"worst_month = {worst_month!r}, а худший месяц — июль (7): monthly.idxmin().month"
# ─── другое решение ───
monthly = sales.resample("MS").sum()
best_month = monthly.sort_values().index[-1].month
worst_month = monthly.sort_values().index[0].month
# ─── ошибка ───
monthly = sales.resample("ME").mean()
best_month = monthly.idxmax().month
worst_month = monthly.idxmin().month
# ─── ошибка ───
monthly = sales.resample("ME").sum()
best_month = monthly.idxmax()
worst_month = monthly.idxmin()

# %% weekly
weekly_orders = order_count.resample("W").sum()
print(len(weekly_orders))
weekly_orders.head(3)

# %% weekly-edges
print(order_count.resample("W").count().iloc[[0, 1, -1]])

# %% weeks-quiz [quiz]
two_weeks = pd.Series(1, index=pd.date_range("2025-03-03", "2025-03-16"))
print(two_weeks.resample("W").sum().tolist())

# %% weeks [exercise]
weekly = sales.resample("W").sum()
full_weeks = weekly.iloc[1:-1]
best_week_end = full_weeks.idxmax()
week_mean = full_weeks.mean()
# ─── заготовка ───
weekly = ...
full_weeks = ...
best_week_end = ...
week_mean = ...
# ─── проверка ───
def test_weekly():
    "weekly — выручка по неделям, full_weeks — без неполных первой и последней"
    assert isinstance(weekly, pd.Series) and len(weekly) == 53, "weekly — 53 значения: sales.resample(\"W\").sum()"
    assert weekly.sum() == 3301420, "сумма по неделям должна остаться выручкой года"
    assert isinstance(full_weeks, pd.Series), f"full_weeks — это {type(full_weeks).__name__}, а нужен Series: weekly.iloc[1:-1]"
    assert len(full_weeks) == 51, f"в full_weeks {len(full_weeks)} недель, а полных недель 51: отбросьте первую и последнюю — iloc[1:-1]"


def test_best():
    "best_week_end — дата окончания лучшей недели, week_mean — средняя недельная выручка"
    assert best_week_end == pd.to_datetime("2025-11-16"), f"best_week_end = {best_week_end}, а лучшая неделя закончилась 16 ноября: full_weeks.idxmax()"
    assert abs(week_mean - 62290.943) > 1, "среднее посчитано по всем 53 неделям, включая две неполные: считайте по full_weeks"
    assert abs(week_mean - 62962.941) < 1e-2, f"week_mean = {week_mean!r}, а средняя выручка полной недели ≈ 62963"
# ─── другое решение ───
weekly = sales.resample("W-SUN").sum()
full_weeks = weekly.loc["2025-01-12":"2025-12-28"]
best_week_end = full_weeks.sort_values().index[-1]
week_mean = full_weeks.sum() / len(full_weeks)
# ─── ошибка ───
weekly = sales.resample("W").sum()
full_weeks = weekly
best_week_end = full_weeks.idxmax()
week_mean = full_weeks.mean()

# %% table
weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
moscow = weather[weather["city"] == "Москва"].set_index("date")
moscow.resample("ME")["temp_max"].mean().round(1).head(3)

# %% climate [exercise]
climate = moscow.resample("ME").agg(temp=("temp_max", "mean"), rain=("precip_mm", "sum")).round(1)
rainiest = climate["rain"].idxmax().month
# ─── заготовка ───
climate = ...
rainiest = ...
# ─── проверка ───
def test_climate():
    "climate — средний дневной максимум и сумма осадков по месяцам"
    assert isinstance(climate, pd.DataFrame), f"climate — это {type(climate).__name__}, а нужна таблица: moscow.resample(\"ME\").agg(...)"
    assert list(climate.columns) == ["temp", "rain"], f"столбцы сейчас {list(climate.columns)}, а нужны temp и rain"
    assert len(climate) == 12, f"в climate {len(climate)} строк, а месяцев 12"
    assert climate["temp"].iloc[6] == 21.7, "temp — средний temp_max за месяц, один знак: в июле 21.7"
    assert climate["rain"].iloc[6] != 1.5, "rain — не среднее, а сумма осадков за месяц: (\"precip_mm\", \"sum\")"
    assert climate["rain"].iloc[6] == 48.0, "rain — сумма precip_mm за месяц: в июле 48.0"


def test_rainiest():
    "rainiest — номер самого дождливого месяца"
    assert rainiest == 6, f"rainiest = {rainiest!r}, а больше всего осадков выпало в июне (6): climate[\"rain\"].idxmax().month"
# ─── другое решение ───
r = moscow.resample("ME")
climate = pd.DataFrame({"temp": r["temp_max"].mean(), "rain": r["precip_mm"].sum()}).round(1)
rainiest = climate.sort_values("rain").index[-1].month
# ─── ошибка ───
climate = moscow.resample("ME").agg(temp=("temp_max", "mean"), rain=("precip_mm", "mean")).round(1)
rainiest = climate["rain"].idxmax().month

# %% quarters
order_count.resample("QE").sum()

# %% empty-periods
print(daily.resample("D").sum().loc["2025-07-01":"2025-07-03"])
print(daily.resample("D").mean().loc["2025-07-01":"2025-07-03"])

# %% quarter [exercise]
quarterly = sales.resample("QE").sum()
quarter_share = (quarterly / quarterly.sum()).round(3)
weak_quarter = quarter_share.idxmin().quarter
# ─── заготовка ───
quarterly = ...
quarter_share = ...
weak_quarter = ...
# ─── проверка ───
def test_quarterly():
    "quarterly — выручка по кварталам, quarter_share — доли кварталов"
    assert isinstance(quarterly, pd.Series) and len(quarterly) == 4, "quarterly — четыре значения: sales.resample(\"QE\").sum()"
    assert quarterly.tolist() == [867150, 864320, 652000, 917950], f"значения сейчас {quarterly.tolist()}, а должны быть [867150, 864320, 652000, 917950]"
    assert isinstance(quarter_share, pd.Series) and quarter_share.tolist() == [0.263, 0.262, 0.197, 0.278], "quarter_share — quarterly, делённый на свою сумму, с округлением до трёх знаков: [0.263, 0.262, 0.197, 0.278]"


def test_weak():
    "weak_quarter — номер самого слабого квартала"
    assert weak_quarter == 3, f"weak_quarter = {weak_quarter!r}, а самый слабый квартал — третий: quarter_share.idxmin().quarter"
# ─── другое решение ───
quarterly = sales.resample("QE").sum()
quarter_share = round(quarterly / sales.sum(), 3)
weak_quarter = quarterly.sort_values().index[0].quarter
# ─── ошибка ───
quarterly = sales.resample("QE").sum()
quarter_share = (quarterly / quarterly.sum()).round(3)
weak_quarter = quarter_share.idxmax().quarter
