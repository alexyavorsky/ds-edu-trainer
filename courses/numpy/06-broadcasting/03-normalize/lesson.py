# Урок np-normalize. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import numpy as np

scores = np.loadtxt("data/scores.csv", delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5))
print(np.round(scores.mean(axis=0), 1))
print(np.round(scores.std(axis=0), 1))

# %% z-one
math = scores[:, 0]
z_math = (math - math.mean()) / math.std()
print(np.round(z_math[:5], 2))
print(round(z_math.mean(), 6) == 0, round(z_math.std(), 6))

# %% z-physics [exercise]
phys = scores[:, 1]
z_phys = (phys - phys.mean()) / phys.std()
best_phys = z_phys.argmax()
# ─── заготовка ───
z_phys = ...
best_phys = ...
# ─── проверка ───
def test_z():
    "z_phys — z-оценки по физике"
    assert isinstance(z_phys, np.ndarray) and z_phys.shape == (30,), "z_phys — 30 чисел, по студенту"
    assert abs(z_phys.mean()) < 1e-9, "среднее z-оценок должно быть 0: проверьте скобки — (x - x.mean()) / x.std()"
    assert abs(z_phys.std() - 1) < 1e-9, "std z-оценок должно быть 1: делите на x.std()"
    assert abs(z_phys[0] - (-1.409)) < 1e-3, f"у первого студента z = {z_phys[0]:.3f}, а должно быть −1.409: это физика, столбец 1?"


def test_best():
    "best_phys — лучший по физике"
    assert best_phys == 28, f"best_phys = {best_phys}, а лучшая z-оценка по физике — у студента с индексом 28"
# ─── другое решение ───
x = scores[:, 1]
z_phys = (x - np.mean(x)) / np.std(x)
best_phys = np.argmax(z_phys)
# ─── ошибка ───
x = scores[:, 1]
z_phys = x - x.mean() / x.std()
best_phys = z_phys.argmax()
# ─── ошибка ───
x = scores[:, 0]
z_phys = (x - x.mean()) / x.std()
best_phys = z_phys.argmax()

# %% z-table
z_demo = (scores - scores.mean(axis=0)) / scores.std(axis=0)
print(z_demo.shape)
print(np.round(z_demo[:2], 1))
print(np.allclose(z_demo.mean(axis=0), 0), np.allclose(z_demo.std(axis=0), 1))

# %% z-all [exercise]
z = (scores - scores.mean(axis=0)) / scores.std(axis=0)
# ─── заготовка ───
z = ...
# ─── проверка ───
def test_shape():
    "z — таблица 30 × 5"
    assert isinstance(z, np.ndarray) and z.shape == (30, 5), f"z должна быть таблицей 30 × 5"


def test_standard():
    "в каждом столбце среднее 0 и std 1"
    assert isinstance(z, np.ndarray) and z.shape == (30, 5), "сначала исправьте то, о чём говорит проверка выше"
    assert np.allclose(z.mean(axis=0), 0), "средние столбцов должны быть 0: вычитайте scores.mean(axis=0) и не забудьте скобки"
    assert not np.allclose(z.std(axis=1), 1), "стандартизованы строки, а нужно — столбцы: axis=0"
    assert np.allclose(z.std(axis=0), 1), "std столбцов должны быть 1: делите на scores.std(axis=0), а не на общий std таблицы"
# ─── другое решение ───
mu = scores.mean(axis=0)
sigma = scores.std(axis=0)
z = (scores - mu) / sigma
# ─── ошибка ───
z = (scores - scores.mean(axis=0)) / scores.std()
# ─── ошибка ───
z = (scores - scores.mean()) / scores.std()

# %% minmax [exercise]
lo = scores.min(axis=0)
hi = scores.max(axis=0)
scaled = (scores - lo) / (hi - lo)
# ─── заготовка ───
scaled = ...
# ─── проверка ───
def test_scaled():
    "в каждом столбце минимум 0 и максимум 1"
    assert isinstance(scaled, np.ndarray) and scaled.shape == (30, 5), "scaled — таблица 30 × 5"
    assert np.allclose(scaled.min(axis=0), 0), "минимум каждого столбца должен стать 0: вычитайте min(axis=0)"
    assert np.allclose(scaled.max(axis=0), 1), "максимум каждого столбца должен стать 1: делите на (max − min) по столбцам, в скобках"
    assert np.allclose(scaled[0], [0.452, 0.038, 0.463, 0.769, 0.667], atol=1e-3), f"первая строка — {np.round(scaled[0], 3).tolist()}"
# ─── другое решение ───
scaled = (scores - np.min(scores, axis=0)) / np.ptp(scores, axis=0)
# ─── ошибка ───
scaled = (scores - scores.min(axis=0)) / scores.max(axis=0)
# ─── ошибка ───
scaled = (scores - scores.min()) / (scores.max() - scores.min())

# %% overall [exercise]
overall = z.mean(axis=1)
top_student = overall.argmax()
# ─── заготовка ───
overall = ...
top_student = ...
# ─── проверка ───
def test_overall():
    "overall — средняя z-оценка студента"
    assert isinstance(overall, np.ndarray), f"overall — это {type(overall).__name__}, а нужен массив"
    assert overall.shape != (5,), "получилось 5 чисел — по предмету; средняя студента — axis=1"
    assert overall.shape == (30,), f"у overall форма {overall.shape}, а нужно 30 чисел"


def test_top():
    "top_student — лучший по средней z-оценке"
    assert top_student == 11, f"top_student = {top_student}, а лучшая средняя z-оценка — у студента с индексом 11"
# ─── другое решение ───
overall = z.sum(axis=1) / 5
top_student = np.argmax(overall)
# ─── ошибка ───
overall = z.mean(axis=0)
top_student = overall.argmax()
