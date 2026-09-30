# Урок np-final-dynamics. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% base
import numpy as np

path = "data/shop_orders.csv"
nums = np.loadtxt(path, delimiter=",", skiprows=1, usecols=(7, 8))
revenue = nums[:, 0] * nums[:, 1]
total = revenue.sum()
print(revenue.shape, total)

# %% month
dates = np.loadtxt(path, delimiter=",", skiprows=1, usecols=1, dtype=str)
month = np.array([int(d[5:7]) for d in dates])
print(dates[:3], dates[-3:])
print(month[:3], month[-3:])

# %% months [exercise]
monthly = np.bincount(month, weights=revenue)[1:]
best_month = monthly.argmax() + 1
worst_month = monthly.argmin() + 1
# ─── заготовка ───
monthly = ...
best_month = ...
worst_month = ...
# ─── проверка ───
def test_monthly():
    "monthly — выручка двенадцати месяцев"
    assert isinstance(monthly, np.ndarray), f"monthly — это {type(monthly).__name__}, а нужен массив из np.bincount"
    assert len(monthly) != 13, "в monthly 13 чисел: нулевой элемент — несуществующий месяц 0, уберите его срезом [1:]"
    assert len(monthly) == 12, f"в monthly {len(monthly)} чисел, а месяцев 12"
    assert monthly[0] == 318940, f"выручка января — {monthly[0]}, а должна быть 318 940: веса — revenue"
    assert monthly.sum() == 3301420, "сумма monthly не равна выручке года"


def test_best():
    "best_month и worst_month — номера месяцев"
    assert best_month != 11 and worst_month != 6, "это индексы; номер месяца на единицу больше"
    assert best_month == 12, f"best_month = {best_month}, а лучший месяц — декабрь (12)"
    assert worst_month == 7, f"worst_month = {worst_month}, а худший месяц — июль (7)"
# ─── другое решение ───
monthly = np.bincount(month - 1, weights=revenue)
best_month = np.argmax(monthly) + 1
worst_month = np.argmin(monthly) + 1
# ─── ошибка ───
monthly = np.bincount(month, weights=revenue)
best_month = monthly.argmax()
worst_month = monthly.argmin()
# ─── ошибка ───
monthly = np.bincount(month, weights=revenue)[1:]
best_month = monthly.argmax()
worst_month = monthly.argmin()

# %% changes [exercise]
change = monthly[1:] - monthly[:-1]
rise_month = change.argmax() + 2
# ─── заготовка ───
change = ...
rise_month = ...
# ─── проверка ───
def test_change():
    "change — изменения к прошлому месяцу"
    assert isinstance(change, np.ndarray) and change.shape == (11,), "change — 11 разностей соседних месяцев"
    assert change[0] != 68510, "знак перепутан: из следующего месяца вычитайте предыдущий — monthly[1:] - monthly[:-1]"
    assert change[0] == -68510, f"change[0] = {change[0]}, а февраль к январю — −68 510"


def test_rise():
    "rise_month — месяц самого большого роста"
    assert rise_month != 10 and rise_month != 11, "change[0] — это февраль: номер месяца — индекс плюс 2"
    assert rise_month == 12, f"rise_month = {rise_month}, а сильнее всего выручка выросла в декабре"
# ─── другое решение ───
change = monthly[1:] - monthly[:11]
rise_month = np.argmax(change) + 2
# ─── ошибка ───
change = monthly[1:] - monthly[:-1]
rise_month = change.argmax() + 1

# %% cumulative [exercise]
running = monthly.cumsum()
half_month = (running >= running[-1] / 2).argmax() + 1
# ─── заготовка ───
running = ...
half_month = ...
# ─── проверка ───
def test_running():
    "running — накопленная выручка"
    assert isinstance(running, np.ndarray) and running.shape == (12,), "running — 12 накопленных сумм: monthly.cumsum()"
    assert running[-1] == 3301420, f"последний элемент running — {running[-1]}, а должен быть выручкой года"
    assert running[1] == 569370, "running[1] должен быть январь + февраль = 569 370"


def test_half():
    "half_month — месяц, когда набрана половина"
    assert half_month != 5, "это индекс; номер месяца на единицу больше"
    assert half_month == 6, f"half_month = {half_month}, а половина годовой выручки набрана к концу июня"
# ─── другое решение ───
running = np.cumsum(monthly)
half_month = np.argmax(running >= total / 2) + 1
# ─── ошибка ───
running = monthly.cumsum()
half_month = (running >= running[-1] / 2).argmax()

# %% quarters [exercise]
quarters = monthly.reshape(4, 3).sum(axis=1)
weak_quarter = quarters.argmin() + 1
# ─── заготовка ───
quarters = ...
weak_quarter = ...
# ─── проверка ───
def test_quarters():
    "quarters — выручка кварталов"
    assert isinstance(quarters, np.ndarray), f"quarters — это {type(quarters).__name__}, а нужен массив из четырёх сумм"
    assert quarters.shape != (3,), "в quarters три числа: строка таблицы 4 × 3 — квартал, суммируйте по axis=1"
    assert quarters.shape == (4,), f"у quarters форма {quarters.shape}, а кварталов 4"
    assert quarters.tolist() == [867150, 864320, 652000, 917950], f"quarters = {quarters.tolist()}"


def test_weak():
    "weak_quarter — самый слабый квартал"
    assert weak_quarter == 3, f"weak_quarter = {weak_quarter}, а слабее всего третий квартал — лето"
# ─── другое решение ───
quarters = np.array([monthly[0:3].sum(), monthly[3:6].sum(), monthly[6:9].sum(), monthly[9:12].sum()])
weak_quarter = np.argmin(quarters) + 1
# ─── ошибка ───
quarters = monthly.reshape(4, 3).sum(axis=0)
weak_quarter = quarters.argmin() + 1

# %% pair-codes
m_demo = np.array([1, 1, 2, 2, 2])        # месяц
c_demo = np.array([0, 2, 1, 2, 2])        # канал
amount = np.array([10, 20, 30, 40, 50])
pair = (m_demo - 1) * 3 + c_demo
print(pair)
print(np.bincount(pair, weights=amount).reshape(2, 3))

# %% channels [exercise]
channel = np.loadtxt(path, delimiter=",", skiprows=1, usecols=4, dtype=str)
ch_names, ch_codes = np.unique(channel, return_inverse=True)
by_channel = np.bincount((month - 1) * 3 + ch_codes, weights=revenue).reshape(12, 3)
shares = by_channel / by_channel.sum(axis=1, keepdims=True)
site_peak = shares[:, 2].argmax() + 1
# ─── заготовка ───
by_channel = ...
shares = ...
site_peak = ...
# ─── проверка ───
def test_by_channel():
    "by_channel — выручка: 12 месяцев × 3 канала"
    assert isinstance(by_channel, np.ndarray), f"by_channel — это {type(by_channel).__name__}, а нужна таблица"
    assert by_channel.shape == (12, 3), f"у by_channel форма {by_channel.shape}, а нужна (12, 3): bincount по парному коду и reshape(12, 3)"
    assert by_channel.sum() == 3301420, "сумма by_channel не равна выручке года: веса — revenue"
    assert by_channel[0].tolist() == [81700, 106380, 130860], f"январь — {by_channel[0].tolist()}, а должен быть [81700, 106380, 130860] (маркетплейс, приложение, сайт)"


def test_shares():
    "shares — доли каналов внутри месяца"
    assert np.shape(shares) == (12, 3), "shares — таблица той же формы, что by_channel"
    assert np.allclose(shares.sum(axis=1), 1), "строки shares в сумме не дают 1: делите на сумму своей строки — by_channel.sum(axis=1, keepdims=True)"


def test_peak():
    "site_peak — месяц наибольшей доли сайта"
    assert site_peak != 9, "это индекс; номер месяца на единицу больше"
    assert site_peak == 10, f"site_peak = {site_peak}, а доля сайта была наибольшей в октябре"
# ─── другое решение ───
channel = np.loadtxt(path, delimiter=",", skiprows=1, usecols=4, dtype=str)
names_c = np.unique(channel)
by_channel = np.stack([np.bincount(month[channel == name], weights=revenue[channel == name])[1:] for name in names_c], axis=1)
shares = by_channel / by_channel.sum(axis=1)[:, np.newaxis]
site_peak = np.argmax(shares[:, 2]) + 1
# ─── ошибка ───
channel = np.loadtxt(path, delimiter=",", skiprows=1, usecols=4, dtype=str)
ch_names, ch_codes = np.unique(channel, return_inverse=True)
by_channel = np.bincount((month - 1) * 3 + ch_codes, weights=revenue).reshape(12, 3)
shares = by_channel / by_channel.sum()
site_peak = shares[:, 2].argmax() + 1

# %% summary
print("лучший месяц:", best_month, "худший:", worst_month)
print("кварталы, тыс. ₽:", np.round(quarters / 1000))
year_share = by_channel.sum(axis=0) / total
for name, share in zip(["маркетплейс", "приложение", "сайт"], year_share * 100):
    print(f"  {name}: {share:.0f} % за год")
