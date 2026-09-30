# Урок pd-time-index. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
moscow = weather[weather["city"] == "Москва"].set_index("date").drop(columns=["city"])
moscow.head(3)

# %% index-type
print(type(moscow.index))
print(moscow.index.min(), moscow.index.max())

# %% one-day
moscow.loc["2025-05-09"]

# %% one-month
moscow.loc["2025-05"].head(3)

# %% month-len
print(len(moscow.loc["2025-05"]))
print(moscow.loc["2025-05", "temp_max"].mean())

# %% feb-quiz [quiz]
print(len(moscow.loc["2025-02"]))

# %% march [exercise]
march = moscow.loc["2025-03"]
march_max = march["temp_max"].max()
march_warmest = march["temp_max"].idxmax()
# ─── заготовка ───
march = ...
march_max = ...
march_warmest = ...
# ─── проверка ───
def test_march():
    "march — мартовские дни"
    assert isinstance(march, pd.DataFrame), f"march — это {type(march).__name__}, а нужна таблица: moscow.loc[\"2025-03\"]"
    assert len(march) == 31, f"в march {len(march)} строк, а в марте 31 день: moscow.loc[\"2025-03\"]"
    assert set(march.index.month) == {3}, "в march должны быть только мартовские дни"


def test_warmest():
    "march_max — наибольшая температура марта, march_warmest — её дата"
    assert abs(march_max - 8.3) < 1e-9, f"march_max = {march_max!r}, а наибольший temp_max в марте — 8.3"
    assert march_warmest == pd.to_datetime("2025-03-19"), f"march_warmest = {march_warmest}, а самый тёплый день марта — 19-е: march[\"temp_max\"].idxmax()"
# ─── другое решение ───
march = moscow[moscow.index.month == 3]
march_max = max(march["temp_max"])
march_warmest = march.sort_values("temp_max").index[-1]
# ─── ошибка ───
march = moscow.loc["2025-03-01"]
march_max = 8.3
march_warmest = pd.to_datetime("2025-03-19")
# ─── ошибка ───
march = moscow.loc["2025-03"]
march_max = march["temp_max"].max()
march_warmest = march["temp_max"].max()

# %% slice
moscow.loc["2025-12-29":"2025-12-31"]

# %% slice-months
spring = moscow.loc["2025-03":"2025-05"]
print(len(spring))
print(spring.index.min(), spring.index.max())

# %% seasons [exercise]
summer = moscow.loc["2025-06":"2025-08"]
summer_mean = summer["temp_max"].mean()
holidays = moscow.loc["2025-05-01":"2025-05-11", "temp_max"]
holidays_mean = holidays.mean()
# ─── заготовка ───
summer = ...
summer_mean = ...
holidays = ...
holidays_mean = ...
# ─── проверка ───
def test_summer():
    "summer — три летних месяца, summer_mean — средний дневной максимум"
    assert isinstance(summer, pd.DataFrame) and len(summer) == 92, "summer — 92 дня с июня по август: moscow.loc[\"2025-06\":\"2025-08\"]"
    assert abs(summer_mean - 21.128261) < 1e-5, f"summer_mean = {summer_mean!r}, а средний дневной максимум лета ≈ 21.13"


def test_holidays():
    "holidays — temp_max с 1 по 11 мая включительно"
    assert isinstance(holidays, pd.Series), f"holidays — это {type(holidays).__name__}, а нужен Series: moscow.loc[срез дат, \"temp_max\"]"
    assert len(holidays) != 10, "в holidays 10 дней: срез по меткам включает обе границы — 11 мая тоже должно войти"
    assert len(holidays) == 11 and holidays.index[0] == pd.to_datetime("2025-05-01") and holidays.index[-1] == pd.to_datetime("2025-05-11"), "holidays — 11 дней с 1 по 11 мая"
    assert abs(holidays_mean - 13.490909) < 1e-5, f"holidays_mean = {holidays_mean!r}, а средняя за эти дни ≈ 13.49: holidays.mean()"
# ─── другое решение ───
summer = moscow[moscow.index.month.isin([6, 7, 8])]
summer_mean = summer["temp_max"].sum() / summer["temp_max"].count()
holidays = moscow["temp_max"].loc["2025-05-01":"2025-05-11"]
holidays_mean = holidays.sum() / len(holidays)
# ─── ошибка ───
summer = moscow.loc["2025-06":"2025-08"]
summer_mean = summer["temp_max"].mean()
holidays = moscow.loc["2025-05-01":"2025-05-10", "temp_max"]
holidays_mean = holidays.mean()

# %% index-parts
print(moscow.index.month[:3].tolist())
print(moscow.index.dayofweek[:3].tolist())
print((moscow.index.dayofweek >= 5).sum())

# %% daily
orders = pd.read_csv("data/shop_orders.csv", parse_dates=["date"])
orders["revenue"] = orders["price"] * orders["quantity"]
daily = orders.groupby("date")["revenue"].sum()
print(len(daily))
daily.head(3)

# %% missing-day [raises=KeyError]
daily.loc["2025-07-02"]

# %% date-range
pd.date_range("2025-01-01", "2025-01-05")

# %% calendar [exercise]
calendar = pd.date_range("2025-01-01", "2025-12-31")
sales = daily.reindex(calendar, fill_value=0)
empty_days = (sales == 0).sum()
december = sales.loc["2025-12"].sum()
# ─── заготовка ───
calendar = ...
sales = ...
empty_days = ...
december = ...
# ─── проверка ───
def test_calendar():
    "calendar — все дни 2025 года"
    assert isinstance(calendar, pd.DatetimeIndex), f"calendar — это {type(calendar).__name__}, а нужен набор дат: pd.date_range(\"2025-01-01\", \"2025-12-31\")"
    assert len(calendar) == 365, f"в calendar {len(calendar)} дней, а в 2025 году их 365"


def test_sales():
    "sales — выручка за каждый день года, без пропущенных дат"
    assert isinstance(sales, pd.Series), f"sales — это {type(sales).__name__}, а нужен Series: daily.reindex(calendar, fill_value=0)"
    assert len(sales) == 365, f"в sales {len(sales)} значений, а должно быть 365 — по одному на каждый день года"
    assert sales.isna().sum() == 0, "в sales пропуски: в дни без продаж выручка — ноль, fill_value=0"
    assert sales.sum() == 3301420, "сумма sales должна остаться выручкой года — 3 301 420"


def test_numbers():
    "empty_days — дней без продаж, december — выручка декабря"
    assert empty_days == 7, f"empty_days = {empty_days!r}, а дней без продаж — 7: сумма маски sales == 0"
    assert december == 371310, f"december = {december!r}, а выручка декабря — 371310: sales.loc[\"2025-12\"].sum()"
# ─── другое решение ───
calendar = pd.date_range("2025-01-01", periods=365)
sales = daily.reindex(calendar).fillna(0)
empty_days = len(calendar) - len(daily)
december = sales[sales.index.month == 12].sum()
# ─── ошибка ───
calendar = pd.date_range("2025-01-01", "2025-12-31")
sales = daily.reindex(calendar)
empty_days = (sales == 0).sum()
december = sales.loc["2025-12"].sum()
# ─── ошибка ───
calendar = pd.date_range("2025-01-01", "2025-12-31")
sales = daily
empty_days = (sales == 0).sum()
december = sales.loc["2025-12"].sum()

# %% unsorted [raises=KeyError]
shuffled = moscow.sort_values("temp_max")
shuffled.loc["2025-03-01":"2025-03-05"]
