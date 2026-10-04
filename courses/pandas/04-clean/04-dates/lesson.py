# Урок pd-dates. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% text
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders["date"].head(3)

# %% convert
orders["date"] = pd.to_datetime(orders["date"])
orders["date"].head(3)

# %% parts
print(orders["date"].dt.year.head(3).tolist())
print(orders["date"].dt.month.tail(3).tolist())
print(orders["date"].dt.day.tail(3).tolist())

# %% months [exercise]
orders["month"] = orders["date"].dt.month
december = orders[orders["month"] == 12]
# ─── заготовка ───
# добавьте в orders столбец month
december = ...
# ─── проверка ───
def test_month():
    "month — номер месяца"
    assert "month" in orders.columns, "в orders нет столбца month"
    assert orders["month"].dtype != object and str(orders["month"].dtype) != "str", "в month должен быть номер месяца числом"
    assert orders["month"].min() == 1 and orders["month"].max() == 12, "в month должны быть числа от 1 до 12"
    assert (orders["month"] == 7).sum() == 127, "месяцы не те: нужен номер месяца из даты"


def test_december():
    "december — строки декабря"
    assert isinstance(december, pd.DataFrame), f"december — это {type(december).__name__}, а нужна таблица"
    assert len(december) == 329, f"в december {len(december)} строк — нужны все строки декабря"
# ─── другое решение ───
orders = orders.assign(month=orders["date"].dt.month)
december = orders[orders["date"] >= "2025-12-01"]
# ─── ошибка ───
orders["month"] = orders["date"].dt.day
december = orders[orders["month"] == 12]
# ─── ошибка ───
orders["month"] = orders["date"].dt.month
december = orders[orders["month"] == 11]

# %% weekday
orders["weekday"] = orders["date"].dt.dayofweek
orders[["date", "weekday"]].head(3)

# %% weekday-names
names = {0: "пн", 1: "вт", 2: "ср", 3: "чт", 4: "пт", 5: "сб", 6: "вс"}
orders["weekday"].map(names).value_counts()

# %% weekend [exercise]
is_weekend = orders["weekday"] >= 5
weekend_share = is_weekend.mean()
# ─── заготовка ───
is_weekend = ...
weekend_share = ...
# ─── проверка ───
def test_mask():
    "is_weekend — маска суббот и воскресений"
    assert isinstance(is_weekend, pd.Series) and is_weekend.dtype == bool, "is_weekend — маска: сравнение столбца weekday с числом"
    assert is_weekend.sum() != 425, "в маске только воскресенья (6), а суббота — это 5"
    assert is_weekend.sum() != 758, "в маске пятница и суббота: дни считаются с нуля"
    assert is_weekend.sum() == 812, f"в маске {is_weekend.sum()} строк — нужны субботы и воскресенья"


def test_share():
    "weekend_share — доля покупок в выходные"
    assert abs(weekend_share - 812 / 2448) < 1e-9, f"weekend_share = {weekend_share!r} — это не доля покупок в выходные"
# ─── другое решение ───
is_weekend = orders["date"].dt.dayofweek.isin([5, 6])
weekend_share = is_weekend.sum() / len(orders)
# ─── ошибка ───
is_weekend = orders["weekday"] == 6
weekend_share = is_weekend.mean()
# ─── ошибка ───
is_weekend = orders["weekday"] >= 4
weekend_share = is_weekend.mean()

# %% compare
print((orders["date"] >= "2025-12-25").sum())
print(orders["date"].min(), orders["date"].max())

# %% delta
span = orders["date"].max() - orders["date"].min()
print(span)
print(span.days)
print(pd.to_datetime("2025-12-31") - orders["date"].max())

# %% delta-series
since_start = orders["date"] - orders["date"].min()
print(since_start.tail(2))
print(since_start.dt.days.tail(2).tolist())

# %% parse-dates
fresh = pd.read_csv("data/shop_orders.csv", parse_dates=["date"])
fresh.dtypes.head(3)

# %% dot-format
supplier = pd.read_csv("data/supplier_prices.csv")
print(supplier["updated"].head(3).tolist())
pd.to_datetime(supplier["updated"], format="%d.%m.%Y").head(3)

# %% guess-trap
guessed = pd.to_datetime(pd.Series(["05.01.2026", "06.01.2026"]))
print(guessed.dt.month.tolist())
print(guessed.dt.day.tolist())

# %% guess-quiz [quiz]
print(pd.to_datetime(pd.Series(["03.02.2026"]), format="%d.%m.%Y").dt.month.tolist()[0])

# %% fresh-prices [exercise]
updated = pd.to_datetime(supplier["updated"], format="%d.%m.%Y")
last_update = updated.max()
age_days = (pd.to_datetime("2026-02-01") - updated).dt.days
# ─── заготовка ───
updated = ...
last_update = ...
age_days = ...
# ─── проверка ───
def test_updated():
    "updated — даты обновления"
    assert isinstance(updated, pd.Series), f"updated — это {type(updated).__name__}, а нужен Series дат"
    assert str(updated.dtype).startswith("datetime64"), f"тип updated — {updated.dtype}, а нужны даты: pd.to_datetime"
    assert updated.dt.month.tolist() == [1] * 20, "все даты должны быть январскими: в файле день стоит первым — задайте формат явно"
    assert updated.dt.day.tolist()[:3] == [15, 13, 12], "дни не те: проверьте формат"


def test_last():
    "last_update — самое позднее обновление"
    assert last_update == pd.to_datetime("2026-01-16"), f"last_update = {last_update} — это не самая поздняя дата обновления"


def test_age():
    "age_days — сколько дней прошло до 1 февраля 2026"
    assert isinstance(age_days, pd.Series), f"age_days — это {type(age_days).__name__}, а нужен Series"
    assert not str(age_days.dtype).startswith("timedelta"), "в age_days разности дат, а нужны числа дней"
    assert age_days.tolist()[:3] != [-17, -19, -20], "знак перепутан: из 1 февраля нужно вычесть дату обновления"
    assert age_days.tolist()[:3] == [17, 19, 20], f"первые значения age_days — {age_days.tolist()[:3]}"
# ─── другое решение ───
updated = pd.to_datetime(supplier["updated"], dayfirst=True)
last_update = updated.sort_values().iloc[-1]
age_days = (pd.Timestamp(2026, 2, 1) - updated).dt.days
# ─── ошибка ───
updated = pd.to_datetime(supplier["updated"], format="%d.%m.%Y")
last_update = updated.max()
age_days = pd.to_datetime("2026-02-01") - updated
# ─── ошибка ───
updated = pd.to_datetime(supplier["updated"], format="%d.%m.%Y")
last_update = updated.max()
age_days = (updated - pd.to_datetime("2026-02-01")).dt.days

# %% returns
returns = pd.read_csv("data/returns_raw.csv")
returns["return_date"].head(6).tolist()

# %% mixed-fail [raises=ValueError, warns]
pd.to_datetime(returns["return_date"])

# %% iso-only
iso = pd.to_datetime(returns["return_date"], format="%Y-%m-%d", errors="coerce")
print(iso.head(4))
print(iso.notna().sum(), "из", len(iso))

# %% combine [exercise]
dotted = pd.to_datetime(returns["return_date"], format="%d.%m.%Y", errors="coerce")
slashed = pd.to_datetime(returns["return_date"], format="%d/%m/%Y", errors="coerce")
returns["date"] = iso.fillna(dotted).fillna(slashed)
n_unparsed = returns["date"].isna().sum()
# ─── заготовка ───
dotted = ...
slashed = ...
# добавьте в returns столбец date
n_unparsed = ...
# ─── проверка ───
def test_parts():
    "dotted и slashed — даты двух других форматов"
    assert isinstance(dotted, pd.Series) and str(dotted.dtype).startswith("datetime64"), "dotted — даты формата ДД.ММ.ГГГГ"
    assert dotted.notna().sum() == 55, f"в dotted распознано {dotted.notna().sum()} дат: проверьте формат"
    assert isinstance(slashed, pd.Series) and str(slashed.dtype).startswith("datetime64"), "slashed — даты формата ДД/ММ/ГГГГ"
    assert slashed.notna().sum() == 17, f"в slashed распознано {slashed.notna().sum()} дат: проверьте формат"


def test_date():
    "returns[\"date\"] — все даты, без пропусков"
    assert "date" in returns.columns, "в returns нет столбца date"
    assert str(returns["date"].dtype).startswith("datetime64"), "в date должны быть даты"
    assert returns["date"].isna().sum() == 0, f"в date осталось {returns['date'].isna().sum()} пропусков: соберите все три варианта"
    assert returns["date"].max() == pd.to_datetime("2026-01-17"), "даты собраны неверно: самая поздняя должна быть 17 января 2026"
    assert n_unparsed == 0, f"n_unparsed = {n_unparsed!r}, а нераспознанных дат быть не должно"
# ─── другое решение ───
dotted = pd.to_datetime(returns["return_date"], format="%d.%m.%Y", errors="coerce")
slashed = pd.to_datetime(returns["return_date"], format="%d/%m/%Y", errors="coerce")
returns["date"] = slashed.fillna(iso).fillna(dotted)
n_unparsed = len(returns) - returns["date"].count()
# ─── ошибка ───
dotted = pd.to_datetime(returns["return_date"], format="%d.%m.%Y", errors="coerce")
slashed = pd.to_datetime(returns["return_date"], format="%d/%m/%Y", errors="coerce")
returns["date"] = iso.fillna(dotted)
n_unparsed = returns["date"].isna().sum()
# ─── ошибка ───
dotted = pd.to_datetime(returns["return_date"], format="%d.%m.%Y", errors="coerce")
slashed = pd.to_datetime(returns["return_date"], format="%d/%m/%Y", errors="coerce")
returns["date"] = pd.to_datetime(returns["return_date"], format="mixed", dayfirst=True)
n_unparsed = returns["date"].isna().sum()

# %% mixed-trap
mixed = pd.to_datetime(returns["return_date"], format="mixed", dayfirst=True)
wrong = mixed != returns["date"]
print(wrong.sum())
print(returns.loc[wrong, "return_date"].head(3).tolist())
print(mixed[wrong].head(3).tolist())
