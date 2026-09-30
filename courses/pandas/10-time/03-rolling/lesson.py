# Урок pd-rolling. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% toy
import pandas as pd

steps = pd.Series([1, 2, 3, 4, 5, 6])
print(steps.rolling(3).sum().tolist())
print(steps.rolling(3).mean().tolist())

# %% sales
orders = pd.read_csv("data/shop_orders.csv", parse_dates=["date"])
orders["revenue"] = orders["price"] * orders["quantity"]
sales = orders.groupby("date")["revenue"].sum().reindex(pd.date_range("2025-01-01", "2025-12-31"), fill_value=0)
sales.head(8).tolist()

# %% week-mean
sales.rolling(3).mean().head(8).round(1).tolist()

# %% roll-quiz [quiz]
print(pd.Series([10, 20, 30, 40]).rolling(2).mean().tolist()[-1])

# %% smooth [exercise]
smooth = sales.rolling(7).mean()
n_empty = smooth.isna().sum()
peak_day = smooth.idxmax()
peak_value = smooth.max()
# ─── заготовка ───
smooth = ...
n_empty = ...
peak_day = ...
peak_value = ...
# ─── проверка ───
def test_smooth():
    "smooth — среднее за 7 дней, включая текущий"
    assert isinstance(smooth, pd.Series), f"smooth — это {type(smooth).__name__}, а нужен Series: sales.rolling(7).mean()"
    assert len(smooth) == 365, "в smooth должно быть 365 значений — по одному на день"
    assert abs(smooth.iloc[6] - 70780) > 1, "в smooth суммы за 7 дней, а нужны средние: .mean()"
    assert abs(smooth.iloc[6] - 10111.428571) < 1e-5, "седьмое значение должно быть ≈ 10111.43: среднее первых семи дней — sales.rolling(7).mean()"
    assert n_empty == 6, f"n_empty = {n_empty!r}, а пропусков в начале — 6: пока не набралось семи дней, окно не считается"


def test_peak():
    "peak_day — последний день самой сильной недели, peak_value — её средняя дневная выручка"
    assert peak_day == pd.to_datetime("2025-04-16"), f"peak_day = {peak_day}, а наибольшее скользящее среднее приходится на 16 апреля: smooth.idxmax()"
    assert abs(peak_value - 14284.285714) < 1e-5, f"peak_value = {peak_value!r}, а наибольшее значение ≈ 14284.29: smooth.max()"
# ─── другое решение ───
smooth = sales.rolling(7).sum() / 7
n_empty = len(smooth) - smooth.count()
peak_day = smooth.sort_values().dropna().index[-1]
peak_value = smooth.dropna().sort_values().iloc[-1]
# ─── ошибка ───
smooth = sales.rolling(7).sum()
n_empty = smooth.isna().sum()
peak_day = smooth.idxmax()
peak_value = smooth.max()
# ─── ошибка ───
smooth = sales.rolling(7, min_periods=1).mean()
n_empty = smooth.isna().sum()
peak_day = smooth.idxmax()
peak_value = smooth.max()

# %% min-periods
sales.rolling(7, min_periods=1).mean().head(3).round(1).tolist()

# %% shift
print(sales.head(4).tolist())
print(sales.shift(1).head(4).tolist())
print(sales.shift(-1).head(4).tolist())

# %% diff
print(sales.diff().head(4).tolist())
print((sales - sales.shift(1)).head(4).tolist())

# %% weekago [exercise]
week_ago = sales.shift(7)
change = sales - week_ago
better = (change > 0).sum()
better_share = better / change.notna().sum()
# ─── заготовка ───
week_ago = ...
change = ...
better = ...
better_share = ...
# ─── проверка ───
def test_shift():
    "week_ago — выручка того же дня недели неделей раньше, change — изменение"
    assert isinstance(week_ago, pd.Series) and len(week_ago) == 365, "week_ago — ряд той же длины: sales.shift(7)"
    assert week_ago.isna().sum() != 1, "сдвиг на один день — это вчера; неделя назад — shift(7)"
    assert week_ago.isna().sum() == 7 and week_ago.iloc[7] == 9060, "week_ago — sales, сдвинутый на 7 дней вперёд: у 8 января стоит выручка 1 января — 9060"
    assert isinstance(change, pd.Series) and change.iloc[7] == 4010, "change — сегодня минус неделю назад: у 8 января 13070 − 9060 = 4010"


def test_better():
    "better — в скольких днях выручка выше, чем неделей раньше; better_share — доля таких дней"
    assert better == 187, f"better = {better!r}, а дней с ростом к прошлой неделе — 187: сумма маски change > 0"
    assert abs(better_share - 187 / 365) > 1e-9, "доля посчитана от 365 дней, но у первых семи дней сравнивать не с чем: делите на число непустых значений change"
    assert abs(better_share - 187 / 358) < 1e-9, f"better_share = {better_share!r}, а доля ≈ 0.522: better, делённое на change.notna().sum()"
# ─── другое решение ───
week_ago = sales.shift(7)
change = sales.diff(7)
better = len(change[change > 0])
better_share = (change.dropna() > 0).mean()
# ─── ошибка ───
week_ago = sales.shift(1)
change = sales - week_ago
better = (change > 0).sum()
better_share = better / change.notna().sum()
# ─── ошибка ───
week_ago = sales.shift(7)
change = sales - week_ago
better = (change > 0).sum()
better_share = (change > 0).mean()

# %% pct
print(pd.Series([100, 120, 90]).pct_change().round(2).tolist())
monthly = sales.resample("ME").sum()
print(monthly.head(3).tolist())

# %% growth [exercise]
growth = monthly.pct_change().round(3)
best_growth = growth.idxmax().month
falls = (growth < 0).sum()
# ─── заготовка ───
growth = ...
best_growth = ...
falls = ...
# ─── проверка ───
def test_growth():
    "growth — рост выручки к прошлому месяцу, три знака"
    assert isinstance(growth, pd.Series) and len(growth) == 12, "growth — 12 значений: monthly.pct_change()"
    assert growth.isna().sum() == 1, "у января нет прошлого месяца — первое значение должно быть пропуском"
    assert abs(growth.iloc[1] - (-68510)) > 1, "в growth разности в рублях, а нужен относительный рост: pct_change(), а не diff()"
    assert growth.iloc[1] == -0.215 and growth.iloc[11] == 0.294, "значения не те или не округлены: февраль — −0.215, декабрь — 0.294"


def test_answers():
    "best_growth — месяц с наибольшим ростом, falls — сколько раз выручка падала"
    assert best_growth == 12, f"best_growth = {best_growth!r}, а сильнее всего выручка выросла в декабре (12): growth.idxmax().month"
    assert falls == 3, f"falls = {falls!r}, а месяцев с падением — 3: сумма маски growth < 0"
# ─── другое решение ───
growth = (monthly / monthly.shift(1) - 1).round(3)
best_growth = growth.sort_values().dropna().index[-1].month
falls = len(growth[growth < 0])
# ─── ошибка ───
growth = monthly.diff().round(3)
best_growth = growth.idxmax().month
falls = (growth < 0).sum()

# %% temp
weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
temp = weather[weather["city"] == "Москва"].set_index("date")["temp_max"]
temp.rolling(7).mean().round(2).iloc[6:9]

# %% waves [exercise]
month_avg = temp.rolling(30).mean()
warmest_end = month_avg.idxmax()
jump = temp.diff()
biggest_drop = jump.idxmin()
# ─── заготовка ───
month_avg = ...
warmest_end = ...
jump = ...
biggest_drop = ...
# ─── проверка ───
def test_month_avg():
    "month_avg — средняя за 30 дней, warmest_end — конец самых тёплых 30 дней"
    assert isinstance(month_avg, pd.Series) and len(month_avg) == 365, "month_avg — ряд той же длины: temp.rolling(30).mean()"
    assert month_avg.isna().sum() == 29, "в начале должно быть 29 пропусков — окно из 30 дней: rolling(30)"
    assert warmest_end == pd.to_datetime("2025-08-12"), f"warmest_end = {warmest_end}, а самые тёплые 30 дней закончились 12 августа: month_avg.idxmax()"


def test_jump():
    "jump — изменение за сутки, biggest_drop — день самого резкого похолодания"
    assert isinstance(jump, pd.Series) and jump.isna().sum() == 1, "jump — разность с предыдущим днём: temp.diff()"
    assert abs(jump.iloc[2] - (-0.5)) < 1e-9, "jump — сегодня минус вчера: 3 января −3.7 − (−3.2) = −0.5"
    assert biggest_drop != pd.to_datetime("2025-03-17"), "17 марта — самое резкое потепление; похолодание — наименьшее значение: idxmin()"
    assert biggest_drop == pd.to_datetime("2025-03-20"), f"biggest_drop = {biggest_drop}, а резче всего похолодало 20 марта: jump.idxmin()"
# ─── другое решение ───
month_avg = temp.rolling(30).sum() / 30
warmest_end = month_avg.dropna().sort_values().index[-1]
jump = temp - temp.shift(1)
biggest_drop = jump.dropna().sort_values().index[0]
# ─── ошибка ───
month_avg = temp.rolling(30).mean()
warmest_end = month_avg.idxmax()
jump = temp.diff()
biggest_drop = jump.idxmax()
