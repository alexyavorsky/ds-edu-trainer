# Урок np-comparisons. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import numpy as np

weather = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1)
tmin = weather[:, 1]
tmax = weather[:, 2]
precip = weather[:, 3]
print(tmax[:8])

# %% mask
warm = tmax > 0
print(warm[:8])
print(warm.shape, warm.dtype)

# %% two-arrays
print((tmax > tmin)[:5])
print((tmax > tmin).all())

# %% count
print((tmax > 0).sum())    # сколько дней с плюсом
print((tmax > 0).mean())   # какая это доля года

# %% hot-days [exercise]
hot = tmax > 25
n_hot = hot.sum()
# ─── заготовка ───
hot = ...
n_hot = ...
# ─── проверка ───
def test_mask():
    "hot — маска из 365 значений True/False"
    assert isinstance(hot, np.ndarray), f"hot — это {type(hot).__name__}, а нужна маска: tmax > 25"
    assert hot.dtype == bool, f"тип hot — {hot.dtype}, а маска — логический массив: сравнение tmax > 25"
    assert hot.shape == (365,), f"у hot форма {hot.shape}, а нужно значение на каждый день"


def test_count():
    "n_hot — число жарких дней"
    assert n_hot != 356, "356 — число дней не выше 25: нужны дни, когда tmax > 25"
    assert n_hot == 9, f"n_hot = {n_hot}, а жарких дней (выше 25 °C) — 9"
# ─── другое решение ───
hot = 25 < tmax
n_hot = np.sum(hot)
# ─── ошибка ───
hot = tmax > 25
n_hot = len(hot)
# ─── ошибка ───
hot = tmax < 25
n_hot = hot.sum()

# %% frost [exercise]
frost_share = (tmin < -10).mean()
# ─── заготовка ───
frost_share = ...
# ─── проверка ───
def test_share():
    "frost_share — доля дней с минимумом ниже −10 °C"
    assert frost_share != 32, "32 — это число таких дней; нужна доля — среднее маски"
    assert abs(frost_share - 32 / 365) < 1e-9, f"frost_share = {frost_share}, а доля морозных ночей — 32 / 365 ≈ 0.088"
# ─── другое решение ───
frost_share = (tmin < -10).sum() / len(tmin)
# ─── ошибка ───
frost_share = (tmin < -10).sum()
# ─── ошибка ───
frost_share = (tmax < -10).mean()

# %% compare [quiz]
np.array([3, 7, 1, 9]) > 5

# %% any-all
print((tmax > 20).any())    # был ли день теплее 20
print((tmax > 20).all())    # все ли дни теплее 20

# %% records [exercise]
over_30 = (tmax > 30).any()
always_above = (tmin > -20).all()
# ─── заготовка ───
over_30 = ...
always_above = ...
# ─── проверка ───
def test_over_30():
    "over_30 — был ли день выше 30 °C"
    assert not isinstance(over_30, np.ndarray), "over_30 — массив, а нужен один ответ True или False: (tmax > 30).any()"
    assert over_30 == False, f"over_30 = {over_30}, а дней выше 30 °C не было — проверьте условие и any()"
    assert isinstance(over_30, (bool, np.bool_)), "over_30 должно быть True или False"


def test_always():
    "always_above — все ли минимумы выше −20 °C"
    assert not isinstance(always_above, np.ndarray), "always_above — массив, а нужен один ответ: (tmin > -20).all()"
    assert always_above == True, f"always_above = {always_above}, а минимум каждый день был выше −20 °C (самый холодный — −14.9)"
# ─── другое решение ───
over_30 = tmax.max() > 30
always_above = tmin.min() > -20
# ─── ошибка ───
over_30 = tmax > 30
always_above = tmin > -20

# %% if-mask [raises=ValueError]
if tmax > 25:
    print("жарко")

# %% dry [exercise]
rainy = (precip > 0).sum()
dry = (precip == 0).sum()
# ─── заготовка ───
rainy = ...
dry = ...
# ─── проверка ───
def test_rainy():
    "rainy — число дней с осадками"
    assert rainy == 168, f"rainy = {rainy}, а дней с осадками (больше 0 мм) — 168"


def test_dry():
    "dry — число дней без осадков"
    assert dry == 197, f"dry = {dry}, а дней без осадков — 197"
    assert rainy + dry == 365, "вместе rainy и dry должны давать все 365 дней"
# ─── другое решение ───
rainy = (precip > 0).sum()
dry = 365 - rainy
# ─── ошибка ───
rainy = (precip >= 0).sum()
dry = (precip == 0).sum()
