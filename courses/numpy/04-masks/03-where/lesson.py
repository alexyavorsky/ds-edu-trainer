# Урок np-where. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% assign
import numpy as np

readings = np.array([21.5, -999.0, 22.1, 22.4, -999.0, 23.0])
readings[readings == -999] = 0
print(readings)

# %% clean [exercise]
sold = np.array([48, 52, -3, 61, 0, -7, 58])
fixed = sold.copy()
fixed[fixed < 0] = 0
# ─── заготовка ───
sold = np.array([48, 52, -3, 61, 0, -7, 58])
fixed = ...
# ─── проверка ───
def test_fixed():
    "в fixed отрицательные заменены нулём"
    assert isinstance(fixed, np.ndarray), f"fixed — это {type(fixed).__name__}, а нужна копия массива sold"
    assert fixed.tolist() != [48, 52, 61, 0, 58], "из fixed выкинуты элементы, а нужно заменить их нулём, сохранив все дни"
    assert fixed.tolist() == [48, 52, 0, 61, 0, 0, 58], f"fixed = {fixed.tolist()}, а должно быть [48, 52, 0, 61, 0, 0, 58]"


def test_sold():
    "sold не изменился"
    assert sold.tolist() == [48, 52, -3, 61, 0, -7, 58], "sold изменился: сделайте копию sold.copy() и меняйте её"
# ─── другое решение ───
sold = np.array([48, 52, -3, 61, 0, -7, 58])
fixed = np.where(sold < 0, 0, sold)
# ─── ошибка ───
sold = np.array([48, 52, -3, 61, 0, -7, 58])
fixed = sold
fixed[fixed < 0] = 0
# ─── ошибка ───
sold = np.array([48, 52, -3, 61, 0, -7, 58])
fixed = sold[sold >= 0]

# %% where
nums = np.array([5, -3, 8, -1])
print(np.where(nums > 0, nums, 0))       # отрицательные → 0
print(np.where(nums > 0, "да", "нет"))

# %% labels
weather = np.loadtxt("data/moscow_2025.csv", delimiter=",", skiprows=1)
tmax = weather[:, 2]
signs = np.where(tmax > 0, "плюс", "минус")
signs[:5]

# %% bonus [exercise]
sales = np.array([120000, 95000, 150000, 80000, 110000])
bonus = np.where(sales > 100000, (sales - 100000) * 0.1, 0)
# ─── заготовка ───
sales = np.array([120000, 95000, 150000, 80000, 110000])
bonus = ...
# ─── проверка ───
def test_bonus():
    "премия 10 % от перевыполнения, остальным 0"
    assert isinstance(bonus, np.ndarray), f"bonus — это {type(bonus).__name__}, а нужен массив из np.where"
    got = np.asarray(bonus, dtype=float).tolist()
    assert got != [12000, 0, 15000, 0, 11000], "премия посчитана от всех продаж, а нужно от превышения плана: (sales - 100000) * 0.1"
    assert got != [2000, -500, 5000, -2000, 1000], "у невыполнивших план премия отрицательная, а должна быть 0 — используйте np.where"
    assert got == [2000, 0, 5000, 0, 1000], f"bonus = {got}, а премии — [2000, 0, 5000, 0, 1000]"
# ─── другое решение ───
sales = np.array([120000, 95000, 150000, 80000, 110000])
extra = sales - 100000
bonus = np.clip(extra, 0, None) * 0.1
# ─── ошибка ───
sales = np.array([120000, 95000, 150000, 80000, 110000])
bonus = (sales - 100000) * 0.1
# ─── ошибка ───
sales = np.array([120000, 95000, 150000, 80000, 110000])
bonus = np.where(sales > 100000, sales * 0.1, 0)

# %% where-quiz [quiz]
np.where(np.array([1, -2, 3]) > 0, 1, 0)

# %% clip
points = np.array([105, 98, -3, 76, 110, 64])
np.clip(points, 0, 100)

# %% scores [exercise]
raw = np.array([88, 104, -5, 67, 100, 0, 121])
scores = np.clip(raw, 0, 100)
# ─── заготовка ───
raw = np.array([88, 104, -5, 67, 100, 0, 121])
scores = ...
# ─── проверка ───
def test_scores():
    "баллы прижаты к границам 0 и 100"
    assert isinstance(scores, np.ndarray), f"scores — это {type(scores).__name__}, а нужен массив: np.clip(raw, 0, 100)"
    got = scores.tolist()
    assert got != [88, 67, 100, 0], "выброшены элементы, а нужно прижать их к границам и сохранить все баллы"
    assert got == [88, 100, 0, 67, 100, 0, 100], f"scores = {got}, а должно быть [88, 100, 0, 67, 100, 0, 100]"
# ─── другое решение ───
raw = np.array([88, 104, -5, 67, 100, 0, 121])
scores = np.where(raw > 100, 100, np.where(raw < 0, 0, raw))
# ─── ошибка ───
raw = np.array([88, 104, -5, 67, 100, 0, 121])
scores = raw[(raw >= 0) & (raw <= 100)]
# ─── ошибка ───
raw = np.array([88, 104, -5, 67, 100, 0, 121])
scores = np.clip(raw, 100, 0)

# %% season [exercise]
season = np.where(tmax >= 15, "тепло", "холодно")
warm_days = (season == "тепло").sum()
# ─── заготовка ───
season = ...
warm_days = ...
# ─── проверка ───
def test_season():
    "season — подпись для каждого дня"
    assert isinstance(season, np.ndarray), f"season — это {type(season).__name__}, а нужен массив подписей из np.where"
    assert season.shape == (365,), f"у season форма {season.shape}, а нужна подпись на каждый из 365 дней"
    assert set(season.tolist()) == {"тепло", "холодно"}, f"в season должны быть только подписи \"тепло\" и \"холодно\", а есть {sorted(set(season.tolist()))[:4]}"


def test_count():
    "warm_days — число тёплых дней"
    assert warm_days != 235, "235 — это «холодные» дни: проверьте порядок подписей — сначала для «да», потом для «нет»"
    assert warm_days == 130, f"warm_days = {warm_days}, а дней с максимумом 15 °C и выше — 130"
# ─── другое решение ───
season = np.where(tmax < 15, "холодно", "тепло")
warm_days = (tmax >= 15).sum()
# ─── ошибка ───
season = np.where(tmax >= 15, "холодно", "тепло")
warm_days = (season == "тепло").sum()
