# Урок np-boolean-filter. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import numpy as np

weather = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1)
tmin = weather[:, 1]
tmax = weather[:, 2]
precip = weather[:, 3]

# %% filter
hot = tmax > 25
print(tmax[hot])
print(len(tmax[hot]), hot.sum())

# %% warm-values [exercise]
warm_nights = tmin[tmin > 15]
warmest_night = warm_nights.max()
# ─── заготовка ───
warm_nights = ...
warmest_night = ...
# ─── проверка ───
def test_values():
    "warm_nights — минимумы выше 15 °C"
    assert isinstance(warm_nights, np.ndarray), f"warm_nights — это {type(warm_nights).__name__}, а нужен массив: tmin[tmin > 15]"
    assert warm_nights.dtype != bool, "это маска из True/False, а нужны сами температуры: подставьте маску в квадратные скобки"
    assert (warm_nights > 15).all(), "в warm_nights есть значения не выше 15 °C"
    assert len(warm_nights) == 55, f"в warm_nights {len(warm_nights)} значений, а тёплых ночей (выше 15 °C) — 55"


def test_max():
    "warmest_night — самая тёплая ночь"
    assert warmest_night == 21.8, f"warmest_night = {warmest_night}, а самая тёплая ночь — 21.8 °C"
# ─── другое решение ───
mask = tmin > 15
warm_nights = tmin[mask]
warmest_night = np.max(warm_nights)
# ─── ошибка ───
warm_nights = tmin > 15
warmest_night = tmin.max()
# ─── ошибка ───
warm_nights = tmax[tmax > 15]
warmest_night = warm_nights.max()

# %% rain-mean [exercise]
rain_only = precip[precip > 0]
rain_mean = rain_only.mean()
# ─── заготовка ───
rain_only = ...
rain_mean = ...
# ─── проверка ───
def test_rain_only():
    "rain_only — осадки дождливых дней"
    assert isinstance(rain_only, np.ndarray), f"rain_only — это {type(rain_only).__name__}, а нужен массив: precip[precip > 0]"
    assert rain_only.dtype != bool, "это маска, а нужны сами осадки: подставьте маску в скобки precip[...]"
    assert len(rain_only) == 168, f"в rain_only {len(rain_only)} значений, а дней с осадками — 168"


def test_mean():
    "rain_mean — средние осадки дождливого дня"
    assert abs(rain_mean - 1.948767) > 1e-4, "это среднее по всем дням; нужно среднее только по дням с осадками"
    assert abs(rain_mean - 4.233929) < 1e-5, f"rain_mean = {rain_mean}, а в дождливый день в среднем выпадало ≈ 4.23 мм"
# ─── другое решение ───
rain_only = precip[precip != 0]
rain_mean = rain_only.sum() / len(rain_only)
# ─── ошибка ───
rain_only = precip[precip > 0]
rain_mean = precip.mean()

# %% other-array
print(tmax[precip > 0].mean())    # средний максимум в дни с осадками
print(tmax[precip > 10])          # максимумы в дни с сильными осадками

# %% combine
thaw = (tmin < 0) & (tmax > 0)
print(thaw.sum())
print(((tmax > 25) | (tmin < -12)).sum())
print((~thaw).sum())

# %% thaw [exercise]
thaw_rain = ((tmax > 0) & (tmin < 0) & (precip > 0)).sum()
# ─── заготовка ───
thaw_rain = ...
# ─── проверка ───
def test_count():
    "thaw_rain — дни с переходом через ноль и осадками"
    assert thaw_rain != 38, "38 — дни с переходом через ноль без учёта осадков: добавьте третье условие (precip > 0)"
    assert thaw_rain == 21, f"thaw_rain = {thaw_rain}, а таких дней — 21: проверьте все три условия и знак &"
# ─── другое решение ───
cross = (tmin < 0) & (tmax > 0)
thaw_rain = (cross & (precip > 0)).sum()
# ─── ошибка ───
thaw_rain = ((tmax > 0) & (tmin < 0)).sum()
# ─── ошибка ───
thaw_rain = ((tmax > 0) | (tmin < 0) | (precip > 0)).sum()

# %% extreme [exercise]
unusual = ((tmax > 25) | (tmin < -12)).sum()
# ─── заготовка ───
unusual = ...
# ─── проверка ───
def test_unusual():
    "unusual — жаркие или очень холодные дни"
    assert unusual != 0, "0 — это «и жаркий, и холодный одновременно»; нужно «или» — знак |"
    assert unusual == 21, f"unusual = {unusual}, а необычных дней — 21"
# ─── другое решение ───
unusual = (tmax > 25).sum() + (tmin < -12).sum()
# ─── ошибка ───
unusual = ((tmax > 25) & (tmin < -12)).sum()

# %% and-or [quiz]
a = np.array([4, 8, 15, 16])
a[(a > 5) & (a < 16)]

# %% and-error [raises=ValueError]
(tmin < 0) and (tmax > 0)

# %% dry-mean [exercise]
dry_max = tmax[~(precip > 0)].mean()
# ─── заготовка ───
dry_max = ...
# ─── проверка ───
def test_dry():
    "dry_max — средний максимум дней без осадков"
    assert abs(dry_max - 9.305357) > 1e-5, "это средний максимум дождливых дней; нужны дни без осадков — ~(precip > 0)"
    assert abs(dry_max - 8.967513) < 1e-5, f"dry_max = {dry_max}, а средний максимум сухих дней ≈ 8.97 °C"
# ─── другое решение ───
dry_max = tmax[precip == 0].mean()
# ─── ошибка ───
dry_max = tmax[precip > 0].mean()
