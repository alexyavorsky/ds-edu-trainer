# Урок np-axis-more. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% data
import numpy as np

monthly = np.array([
    [40, 42, 45, 50, 48, 52, 55, 58, 50, 47, 60, 75],    # магазин 1
    [30, 28, 33, 35, 40, 38, 36, 35, 39, 58, 45, 55],    # магазин 2
    [70, 72, 68, 75, 80, 85, 90, 125, 82, 79, 95, 120],  # магазин 3
])
print(monthly.shape)

# %% argmax-axis
best = monthly.argmax(axis=1)
print(best)          # индексы
print(best + 1)      # номера месяцев

# %% worst [exercise]
worst_month = monthly.argmin(axis=1) + 1
worst_value = monthly.min(axis=1)
# ─── заготовка ───
worst_month = ...
worst_value = ...
# ─── проверка ───
def test_month():
    "worst_month — номер худшего месяца каждого магазина"
    assert isinstance(worst_month, np.ndarray), f"worst_month — это {type(worst_month).__name__}, а нужен массив из трёх номеров"
    got = worst_month.tolist()
    assert len(got) == 3, f"в worst_month {len(got)} чисел, а магазинов 3: argmin(axis=1)"
    assert got != [0, 1, 2], "это индексы; номера месяцев на единицу больше"
    assert got == [1, 2, 3], f"worst_month = {got}, а худшие месяцы — январь, февраль и март: [1, 2, 3]"


def test_value():
    "worst_value — выручка в худший месяц"
    assert isinstance(worst_value, np.ndarray) and worst_value.tolist() == [40, 28, 68], "worst_value — минимум каждой строки: min(axis=1) → [40, 28, 68]"
# ─── другое решение ───
worst_month = np.argmin(monthly, axis=1) + 1
worst_value = np.min(monthly, axis=1)
# ─── ошибка ───
worst_month = monthly.argmin(axis=1)
worst_value = monthly.min(axis=1)
# ─── ошибка ───
worst_month = monthly.argmin(axis=0) + 1
worst_value = monthly.min(axis=0)

# %% cumsum
first_store = monthly[0]
print(first_store.cumsum())
print(first_store.sum())

# %% cumsum-axis
print(monthly.cumsum(axis=1))

# %% ytd [exercise]
ytd = monthly.cumsum(axis=1)
year = ytd[:, -1]
# ─── заготовка ───
ytd = ...
year = ...
# ─── проверка ───
def test_ytd():
    "ytd — накопленная выручка, 3 × 12"
    assert isinstance(ytd, np.ndarray), f"ytd — это {type(ytd).__name__}, а нужна таблица из cumsum"
    assert ytd.shape != (36,), "cumsum без axis вытянул таблицу в ряд: укажите axis=1"
    assert ytd.shape == (3, 12), f"форма ytd — {ytd.shape}, а должна остаться (3, 12)"
    assert ytd[1].tolist() == [30, 58, 91, 126, 166, 204, 240, 275, 314, 372, 417, 472], (
        "накопление должно идти вдоль месяцев каждого магазина: axis=1"
    )


def test_year():
    "year — выручка магазинов за год"
    assert isinstance(year, np.ndarray) and year.tolist() == [622, 472, 1041], "year — последний столбец ytd: ytd[:, -1] → [622, 472, 1041]"
# ─── другое решение ───
ytd = np.cumsum(monthly, axis=1)
year = monthly.sum(axis=1)
# ─── ошибка ───
ytd = monthly.cumsum(axis=0)
year = ytd[:, -1]
# ─── ошибка ───
ytd = monthly.cumsum(axis=1)
year = ytd[-1]

# %% cumsum-quiz [quiz]
np.array([3, 1, 4, 1]).cumsum()

# %% first-true
ytd_all = monthly.cumsum(axis=1)
reached = ytd_all >= 300
print(reached[0])
print(reached.argmax(axis=1) + 1)   # номер месяца для каждого магазина

# %% half-rain [exercise]
precip = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=3)
rain_cum = precip.cumsum()
half_day = (rain_cum >= rain_cum[-1] / 2).argmax() + 1
# ─── заготовка ───
precip = ...
rain_cum = ...
half_day = ...
# ─── проверка ───
def test_cum():
    "rain_cum — накопленные осадки"
    assert isinstance(rain_cum, np.ndarray) and rain_cum.shape == (365,), "rain_cum — накопленная сумма осадков на каждый день: precip.cumsum()"
    assert abs(rain_cum[-1] - 711.3) < 1e-6, f"последний элемент rain_cum — {rain_cum[-1]:.1f}, а должен быть годовой суммой 711.3"


def test_half():
    "half_day — день, когда накопилась половина осадков"
    assert half_day != 173, "173 — индекс; номер дня на единицу больше"
    assert half_day == 174, f"half_day = {half_day}, а половина годовых осадков накопилась к 174-му дню"
# ─── другое решение ───
precip = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=3)
rain_cum = np.cumsum(precip)
half_day = (rain_cum >= precip.sum() / 2).argmax() + 1
# ─── ошибка ───
precip = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1, usecols=3)
rain_cum = precip.cumsum()
half_day = (precip >= rain_cum[-1] / 2).argmax() + 1
