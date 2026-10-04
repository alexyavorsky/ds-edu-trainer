# Урок np-project-hot-days. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import numpy as np

weather = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1)
tmin = weather[:, 1]
tmax = weather[:, 2]
precip = weather[:, 3]
print(weather.shape)

# %% days [exercise]
days = np.arange(1, 366)
hot_days = days[tmax > 25]
# ─── заготовка ───
days = ...
hot_days = ...
# ─── проверка ───
def test_days():
    "days — номера от 1 до 365"
    assert isinstance(days, np.ndarray), f"days — это {type(days).__name__}, а нужен массив"
    assert len(days) == 365 and days[0] == 1 and days[-1] == 365, f"days должен идти от 1 до 365, а сейчас от {days[0]} до {days[-1]}, всего {len(days)}"


def test_hot():
    "hot_days — номера жарких дней"
    assert isinstance(hot_days, np.ndarray), f"hot_days — это {type(hot_days).__name__}, а нужен массив номеров"
    got = hot_days.tolist()
    assert got != [26.0, 25.3, 26.3, 27.2, 26.3, 25.6, 26.0, 26.0, 25.4], "это температуры, а нужны номера дней: маску можно применить и к другому массиву той же длины"
    assert got == [173, 195, 196, 197, 198, 199, 200, 218, 223], f"hot_days = {got}"
# ─── другое решение ───
days = np.arange(365) + 1
hot_days = days[25 < tmax]
# ─── ошибка ───
days = np.arange(1, 366)
hot_days = tmax[tmax > 25]
# ─── ошибка ───
days = np.arange(365)
hot_days = days[tmax > 25]

# %% hot-print
print(hot_days)
print(tmax[tmax > 25])

# %% july [exercise]
july = tmax[181:212]
july_avg = july.mean()
july_warm = (july > 20).sum()
# ─── заготовка ───
july = ...
july_avg = ...
july_warm = ...
# ─── проверка ───
def test_july():
    "july — 31 день июля"
    assert isinstance(july, np.ndarray) and len(july) == 31, "july — это должен быть срез tmax из 31 дня"
    assert july[0] == tmax[181], "срез должен начинаться с 1 июля — 182-го дня года; индексы считают с нуля"


def test_avg():
    "july_avg — средний максимум июля"
    assert abs(july_avg - 21.674194) < 1e-5, f"july_avg = {july_avg} — это не средний максимум июля"


def test_warm():
    "july_warm — июльские дни теплее 20 °C"
    assert july_warm != 11, "11 — это дни не теплее 20; нужны дни теплее 20 °C"
    assert july_warm == 20, f"july_warm = {july_warm} — это не число июльских дней теплее 20 °C"
# ─── другое решение ───
july = tmax[181:181 + 31]
july_avg = np.mean(july)
july_warm = np.sum(july > 20)
# ─── ошибка ───
july = tmax[182:213]
july_avg = july.mean()
july_warm = (july > 20).sum()

# %% heavy [exercise]
rain_share = (precip > 0).mean()
heavy_days = days[precip > 10]
# ─── заготовка ───
rain_share = ...
heavy_days = ...
# ─── проверка ───
def test_share():
    "rain_share — доля дней с осадками"
    assert rain_share != 168, "168 — число дней; нужна доля — среднее маски"
    assert abs(rain_share - 168 / 365) < 1e-9, f"rain_share = {rain_share} — это не доля дней с осадками"


def test_heavy():
    "heavy_days — номера дней с осадками больше 10 мм"
    assert isinstance(heavy_days, np.ndarray), f"heavy_days — это {type(heavy_days).__name__}, а нужен массив номеров"
    assert heavy_days.tolist() == [18, 49, 122, 129, 175, 223, 238, 261, 274, 311, 333], f"heavy_days = {heavy_days.tolist()}"
# ─── другое решение ───
rain_share = (precip > 0).sum() / 365
heavy_days = days[~(precip <= 10)]
# ─── ошибка ───
rain_share = (precip > 0).sum()
heavy_days = days[precip > 10]
# ─── ошибка ───
rain_share = (precip > 0).mean()
heavy_days = precip[precip > 10]

# %% seasons [exercise]
winter = (days <= 59) | (days >= 335)
summer = (days >= 152) & (days <= 243)
gap = tmax[summer].mean() - tmax[winter].mean()
# ─── заготовка ───
winter = ...
summer = ...
gap = ...
# ─── проверка ───
def test_masks():
    "winter — 90 дней, summer — 92 дня"
    for name, mask, n in [("winter", winter, 90), ("summer", summer, 92)]:
        assert isinstance(mask, np.ndarray) and mask.dtype == bool, f"{name} — это должна быть маска из сравнений номеров дней"
        assert mask.sum() != 0, f"в {name} нет ни одного дня: проверьте & и | — зима это «или», лето «и»"
        assert mask.sum() == n, f"в {name} {mask.sum()} дней, а должно быть {n}"


def test_gap():
    "gap — на сколько лето теплее зимы"
    assert gap > 0, f"gap = {gap}: из летнего среднего вычитайте зимнее"
    assert abs(gap - 24.827150) < 1e-4, f"gap = {gap} — это не разница средних максимумов лета и зимы"
# ─── другое решение ───
winter = ~((days > 59) & (days < 335))
summer = (days > 151) & (days < 244)
gap = tmax[summer].mean() - tmax[winter].mean()
# ─── ошибка ───
winter = (days <= 59) & (days >= 335)
summer = (days >= 152) & (days <= 243)
gap = tmax[summer].mean() - tmax[winter].mean()
# ─── ошибка ───
winter = (days <= 59) | (days >= 335)
summer = (days >= 152) & (days <= 243)
gap = tmax[winter].mean() - tmax[summer].mean()

# %% cap [exercise]
precip_fixed = np.clip(precip, 0, 20)
rain_total_fixed = precip_fixed.sum()
# ─── заготовка ───
precip_fixed = ...
rain_total_fixed = ...
# ─── проверка ───
def test_fixed():
    "precip_fixed — осадки не больше 20 мм"
    assert isinstance(precip_fixed, np.ndarray) and precip_fixed.shape == (365,), "precip_fixed — это массив на все 365 дней"
    assert precip_fixed.max() == 20, f"максимум precip_fixed — {precip_fixed.max()}, а значения выше 20 должны стать 20"


def test_total():
    "rain_total_fixed — осадки за год после поправки"
    assert abs(rain_total_fixed - 711.3) > 1e-6, "сумма не изменилась: поправьте значения выше 20 мм"
    assert abs(rain_total_fixed - 705.7) < 1e-6, f"rain_total_fixed = {rain_total_fixed} — это не сумма поправленных осадков за год"
# ─── другое решение ───
precip_fixed = precip.copy()
precip_fixed[precip_fixed > 20] = 20
rain_total_fixed = np.sum(precip_fixed)
# ─── ошибка ───
precip_fixed = precip[precip <= 20]
rain_total_fixed = precip_fixed.sum()

# %% summary
print("жарких дней:", len(hot_days), "— больше всего подряд в июле:", hot_days[1:7])
print("доля дней с осадками:", round(rain_share, 2), "| ливней:", len(heavy_days))
print("лето теплее зимы на", round(gap, 1), "°C")
print("осадков за год после поправки:", round(rain_total_fixed, 1), "мм")
