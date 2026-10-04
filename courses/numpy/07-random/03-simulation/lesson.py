# Урок np-simulation. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% two-dice
import numpy as np

rng = np.random.default_rng(1)
throws = rng.integers(1, 7, size=(100000, 2))   # строка — один бросок двух кубиков
print(throws[:3])
sums = throws.sum(axis=1)
print((sums == 7).mean())

# %% doubles [exercise]
rng = np.random.default_rng(12)
pairs = rng.integers(1, 7, size=(100000, 2))
doubles = (pairs[:, 0] == pairs[:, 1]).mean()
# ─── заготовка ───
rng = ...
doubles = ...
# ─── проверка ───
def test_doubles():
    "doubles — доля дублей"
    assert not isinstance(doubles, np.ndarray), "doubles — массив, а нужна одна доля: среднее маски"
    assert 0 < doubles < 1, f"doubles = {doubles}: доля должна быть между 0 и 1"
    assert abs(doubles - 1 / 6) < 0.01, f"doubles = {doubles:.4f}, а должно быть около 1/6 ≈ 0.167: дубль — когда числа в двух столбцах равны"
    assert abs(doubles - 0.16459) < 1e-9, f"doubles = {doubles}: создайте генератор с seed 12 и бросьте кубики 100000 × 2"
# ─── другое решение ───
rng = np.random.default_rng(12)
pairs = rng.integers(1, 7, size=(100000, 2))
doubles = np.mean(pairs[:, 0] - pairs[:, 1] == 0)
# ─── ошибка ───
rng = np.random.default_rng(12)
pairs = rng.integers(1, 7, size=(100000, 2))
doubles = (pairs[:, 0] == pairs[:, 1]).sum()

# %% heads [exercise]
rng = np.random.default_rng(5)
flips = rng.random((50000, 5)) < 0.5
at_least_3 = (flips.sum(axis=1) >= 3).mean()
# ─── заготовка ───
rng = ...
at_least_3 = ...
# ─── проверка ───
def test_share():
    "at_least_3 — доля серий с тремя и больше орлами"
    assert not isinstance(at_least_3, np.ndarray), "at_least_3 — массив, а нужна одна доля"
    assert abs(at_least_3 - 0.5) < 0.02, f"at_least_3 = {at_least_3:.4f}, а должно быть около 0.5: орлов в серии — сумма по строке, условие — три и больше"
    assert abs(at_least_3 - 0.50136) < 1e-9, f"at_least_3 = {at_least_3}: seed 5, таблица 50000 × 5"
# ─── другое решение ───
rng = np.random.default_rng(5)
heads_count = (rng.random(size=(50000, 5)) < 0.5).sum(axis=1)
at_least_3 = np.mean(heads_count > 2)
# ─── ошибка ───
rng = np.random.default_rng(5)
flips = rng.random((50000, 5)) < 0.5
at_least_3 = (flips.sum(axis=1) > 3).mean()
# ─── ошибка ───
rng = np.random.default_rng(5)
flips = rng.random((50000, 5)) < 0.5
at_least_3 = (flips.sum(axis=0) >= 3).mean()

# %% pi
rng = np.random.default_rng(1)
points = rng.random((100000, 2))
inside = (points[:, 0] ** 2 + points[:, 1] ** 2) <= 1
print(inside.mean() * 4)

# %% pi-est [exercise]
rng = np.random.default_rng(3)
pts = rng.random((100000, 2))
pi_est = ((pts[:, 0] ** 2 + pts[:, 1] ** 2) <= 1).mean() * 4
# ─── заготовка ───
rng = ...
pi_est = ...
# ─── проверка ───
def test_pi():
    "pi_est — оценка числа π"
    assert not isinstance(pi_est, np.ndarray), "pi_est — массив, а нужно одно число"
    assert abs(pi_est - 0.78378) > 0.1, "это доля точек внутри круга, а она равна π/4"
    assert abs(pi_est - 3.14159) < 0.05, f"pi_est = {pi_est:.4f}, а должно быть близко к 3.14"
    assert abs(pi_est - 3.13512) < 1e-9, f"pi_est = {pi_est}: seed 3, 100000 точек, таблица 100000 × 2"
# ─── другое решение ───
rng = np.random.default_rng(3)
xy = rng.random((100000, 2))
pi_est = 4 * np.mean((xy ** 2).sum(axis=1) <= 1)
# ─── ошибка ───
rng = np.random.default_rng(3)
pts = rng.random((100000, 2))
pi_est = ((pts[:, 0] ** 2 + pts[:, 1] ** 2) <= 1).mean()

# %% birthday-idea
group = np.sort(np.random.default_rng(6).integers(1, 366, size=23))
print(group)
print(group[1:] == group[:-1])
print((group[1:] == group[:-1]).any())

# %% birthday [exercise]
rng = np.random.default_rng(23)
days = np.sort(rng.integers(1, 366, size=(10000, 23)), axis=1)
same_bday = (days[:, 1:] == days[:, :-1]).any(axis=1).mean()
# ─── заготовка ───
rng = ...
same_bday = ...
# ─── проверка ───
def test_bday():
    "same_bday — доля групп с совпавшим днём рождения"
    assert not isinstance(same_bday, np.ndarray), "same_bday — массив, а нужна одна доля"
    assert abs(same_bday - 0.507) < 0.03, (
        f"same_bday = {same_bday:.4f}, а должно быть около 0.5. Не забыли отсортировать каждую строку и искать совпадения соседей внутри строки?"
    )
    assert abs(same_bday - 0.4995) < 1e-9, f"same_bday = {same_bday}: seed 23, таблица 10000 × 23"
# ─── другое решение ───
rng = np.random.default_rng(23)
groups = np.sort(rng.integers(1, 366, size=(10000, 23)), axis=1)
same_bday = np.mean((groups[:, 1:] - groups[:, :-1] == 0).sum(axis=1) > 0)
# ─── ошибка ───
rng = np.random.default_rng(23)
days = rng.integers(1, 366, size=(10000, 23))
same_bday = (days[:, 1:] == days[:, :-1]).any(axis=1).mean()

# %% speed
rng = np.random.default_rng(0)
big = rng.integers(1, 7, size=(1000000, 2)).sum(axis=1)
print(len(big), (big == 7).mean())
