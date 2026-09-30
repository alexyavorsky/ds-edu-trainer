# Урок np-dtypes. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% kinds [platform]
import numpy as np

counts = np.array([1, 2, 3])
temps = np.array([18.5, 21.0])
flags = np.array([True, False])
print(counts.dtype, temps.dtype, flags.dtype)

# %% mixed
np.array([1, 2.5, 3])

# %% astype
prices = np.array([99.9, 149.5, 20.99])
print(prices.astype(int))
print(prices)   # исходный массив не изменился

# %% rubles [exercise]
prices = np.array([199.9, 49.5, 1250.75])
rubles = prices.astype(int)
# ─── заготовка ───
prices = np.array([199.9, 49.5, 1250.75])
rubles = ...
# ─── проверка ───
def test_int():
    "rubles — массив целых чисел"
    assert isinstance(rubles, np.ndarray), f"rubles — это {type(rubles).__name__}, а нужен массив: prices.astype(int)"
    assert rubles.dtype.kind == "i", f"тип rubles — {rubles.dtype}, а нужны целые: astype(int)"


def test_values():
    "копейки отброшены"
    assert isinstance(rubles, np.ndarray), "rubles пока не массив — сначала исправьте то, о чём говорит проверка выше"
    assert rubles.tolist() == [199, 49, 1250], f"в rubles {rubles.tolist()}, а без копеек цены — 199, 49, 1250"
# ─── другое решение ───
prices = np.array([199.9, 49.5, 1250.75])
rubles = np.array(prices, dtype=int)
# ─── ошибка ───
prices = np.array([199.9, 49.5, 1250.75])
rubles = prices // 1

# %% truncate [quiz]
np.array([1.9, 2.1]).astype(int)

# %% dtype-arg
print(np.zeros(3, dtype=int))
print(np.array([1, 2, 3], dtype=float))

# %% counters [exercise]
visits = np.zeros(7, dtype=int)
# ─── заготовка ───
visits = ...
# ─── проверка ───
def test_visits():
    "visits — семь целых нулей"
    assert isinstance(visits, np.ndarray), f"visits — это {type(visits).__name__}, а нужен массив: np.zeros(...)"
    assert len(visits) == 7, f"в visits {len(visits)} счётчиков, а дней недели 7"
    assert visits.dtype.kind == "i", f"тип visits — {visits.dtype}, а нужны целые: добавьте dtype=int"
    assert visits.sum() == 0, "все счётчики должны быть нулями"
# ─── другое решение ───
visits = np.full(7, 0)
# ─── ошибка ───
visits = np.zeros(7)

# %% ratings [exercise]
ratings = np.array([4, 5, 3, 5], dtype=float)
# ─── заготовка ───
ratings = ...
# ─── проверка ───
def test_ratings():
    "ratings — оценки 4, 5, 3, 5 дробного типа"
    assert isinstance(ratings, np.ndarray), f"ratings — это {type(ratings).__name__}, а нужен массив"
    assert ratings.dtype == np.float64, f"тип ratings — {ratings.dtype}, а нужен дробный: dtype=float"
    assert ratings.tolist() == [4, 5, 3, 5], f"в ratings {ratings.tolist()}"
# ─── другое решение ───
ratings = np.array([4, 5, 3, 5]).astype(float)
# ─── ошибка ───
ratings = np.array([4, 5, 3, 5])

# %% bools
answers = np.array([True, False, True, True, False])
print(answers.sum())
print(answers.mean())

# %% attendance [exercise]
came = np.array([True, True, False, True, True, True, False, True])
present = came.sum()
share = came.mean()
# ─── заготовка ───
came = np.array([True, True, False, True, True, True, False, True])
present = ...
share = ...
# ─── проверка ───
def test_present():
    "present — сколько пришло"
    assert present == 6, f"present = {present}, а пришли 6 учеников из 8"


def test_share():
    "share — доля пришедших"
    assert share != 75, "получились проценты, а нужна доля от 0 до 1"
    assert abs(share - 0.75) < 1e-9, f"share = {share}, а пришла доля 6 / 8 = 0.75"
# ─── другое решение ───
came = np.array([True, True, False, True, True, True, False, True])
present = np.sum(came)
share = present / len(came)
# ─── ошибка ───
came = np.array([True, True, False, True, True, True, False, True])
present = len(came)
share = came.mean()

# %% overflow
small = np.array([100, 120], dtype=np.int8)
small + 50
