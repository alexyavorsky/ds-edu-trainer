# Урок np-array-math. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% pairs
import numpy as np

prices = np.array([120, 80, 45, 300])
qty = np.array([3, 5, 10, 1])
prices * qty

# %% plan-fact
plan = np.array([50, 40, 60])
fact = np.array([46, 44, 60])
print(fact - plan)   # на сколько отличается от плана
print(fact / plan)   # какая доля плана выполнена

# %% totals [exercise]
morning = np.array([34, 41, 38, 45, 52, 60, 58])
evening = np.array([21, 25, 19, 30, 44, 51, 40])
total = morning + evening
# ─── заготовка ───
morning = np.array([34, 41, 38, 45, 52, 60, 58])
evening = np.array([21, 25, 19, 30, 44, 51, 40])
total = ...
# ─── проверка ───
def test_array():
    "total — массив из семи чисел"
    assert isinstance(total, np.ndarray), f"total — это {type(total).__name__}, а нужен массив: арифметика с массивами даёт массив"
    assert len(total) == 7, f"в total {len(total)} чисел, а дней 7"


def test_values():
    "total — продажи за каждый день"
    assert isinstance(total, np.ndarray), "total пока не массив — сначала исправьте то, о чём говорит проверка выше"
    got = total.tolist()
    assert got == [55, 66, 57, 75, 96, 111, 98], f"получилось {got}, а в понедельник продано 55 чашек"
# ─── другое решение ───
morning = np.array([34, 41, 38, 45, 52, 60, 58])
evening = np.array([21, 25, 19, 30, 44, 51, 40])
total = evening + morning
# ─── ошибка ───
morning = np.array([34, 41, 38, 45, 52, 60, 58])
evening = np.array([21, 25, 19, 30, 44, 51, 40])
total = [34, 41, 38, 45, 52, 60, 58] + [21, 25, 19, 30, 44, 51, 40]

# %% div-mod
minutes = np.array([75, 130, 45, 200])
print(minutes // 60)   # целые часы
print(minutes % 60)    # оставшиеся минуты

# %% clock [exercise]
calls = np.array([130, 59, 360, 245, 61])
mins = calls // 60
secs = calls % 60
# ─── заготовка ───
calls = np.array([130, 59, 360, 245, 61])
mins = ...
secs = ...
# ─── проверка ───
def test_mins():
    "mins — целые минуты каждого звонка"
    assert isinstance(mins, np.ndarray), f"mins — это {type(mins).__name__}, а нужен массив"
    got = np.asarray(mins).tolist()
    assert got != [130 / 60, 59 / 60, 6.0, 245 / 60, 61 / 60], "обычное деление / дало дробные минуты, а нужны целые — вспомните целочисленное деление"
    assert got == [2, 0, 6, 4, 1], f"в mins {got}, а 130 секунд — это 2 целые минуты"


def test_secs():
    "secs — оставшиеся секунды"
    assert isinstance(secs, np.ndarray), f"secs — это {type(secs).__name__}, а нужен массив"
    assert np.asarray(secs).tolist() == [10, 59, 0, 5, 1], f"в secs {np.asarray(secs).tolist()}, а у 130 секунд остаётся 10"
# ─── другое решение ───
calls = np.array([130, 59, 360, 245, 61])
mins = calls // 60
secs = calls - mins * 60
# ─── ошибка ───
calls = np.array([130, 59, 360, 245, 61])
mins = calls / 60
secs = calls % 60
# ─── ошибка ───
calls = np.array([130, 59, 360, 245, 61])
mins = calls % 60
secs = calls // 60

# %% times-pairs [quiz]
np.array([1, 2, 3]) * np.array([2, 2, 2])

# %% lengths
print(len(prices), len(qty))
print(len(np.array([1, 2, 3])))

# %% length-error [raises=ValueError]
np.array([1, 2, 3]) + np.array([10, 20])

# %% avg-check [exercise]
revenue = np.array([18400, 21150, 16800, 25300, 30600])
checks = np.array([92, 105, 80, 110, 136])
avg_check = revenue / checks
# ─── заготовка ───
revenue = np.array([18400, 21150, 16800, 25300, 30600])
checks = np.array([92, 105, 80, 110, 136])
avg_check = ...
# ─── проверка ───
def test_array():
    "avg_check — массив из пяти чисел"
    assert isinstance(avg_check, np.ndarray), f"avg_check — это {type(avg_check).__name__}, а нужен массив: арифметика с массивами даёт массив"
    assert len(avg_check) == 5, f"в avg_check {len(avg_check)} чисел, а дней 5"


def test_values():
    "средний чек = выручка / число покупок"
    assert isinstance(avg_check, np.ndarray), "avg_check пока не массив — сначала исправьте то, о чём говорит проверка выше"
    got = np.asarray(avg_check, dtype=float)
    assert not np.allclose(got, [92 / 18400, 105 / 21150, 80 / 16800, 110 / 25300, 136 / 30600]), "деление перевёрнуто: выручку делят на число покупок, а не наоборот"
    assert np.allclose(got, [200, 201.43, 210, 230, 225], atol=0.01), f"получилось {np.round(got, 2).tolist()}, а в первый день чек 200 ₽"
# ─── другое решение ───
revenue = np.array([18400, 21150, 16800, 25300, 30600])
checks = np.array([92, 105, 80, 110, 136])
avg_check = revenue * (1 / checks)
# ─── ошибка ───
revenue = np.array([18400, 21150, 16800, 25300, 30600])
checks = np.array([92, 105, 80, 110, 136])
avg_check = checks / revenue

# %% plan-percent [exercise]
goal = np.array([500, 320, 280, 150, 200])
done = np.array([540, 288, 280, 90, 230])
percent = done / goal * 100
# ─── заготовка ───
goal = np.array([500, 320, 280, 150, 200])
done = np.array([540, 288, 280, 90, 230])
percent = ...
# ─── проверка ───
def test_array():
    "percent — массив из пяти процентов"
    assert isinstance(percent, np.ndarray), f"percent — это {type(percent).__name__}, а нужен массив"
    assert len(percent) == 5, f"в percent {len(percent)} чисел, а городов 5"


def test_values():
    "процент выполнения плана по каждому городу"
    assert isinstance(percent, np.ndarray), "percent пока не массив — сначала исправьте то, о чём говорит проверка выше"
    got = np.asarray(percent, dtype=float)
    assert not np.allclose(got, [1.08, 0.9, 1.0, 0.6, 1.15]), "получилась доля, а нужны проценты: доля 1 — это 100 %"
    assert np.allclose(got, [108, 90, 100, 60, 115]), f"получилось {np.round(got, 1).tolist()}, а первый город выполнил план на 108 %"
# ─── другое решение ───
goal = np.array([500, 320, 280, 150, 200])
done = np.array([540, 288, 280, 90, 230])
percent = 100 * done / goal
# ─── ошибка ───
goal = np.array([500, 320, 280, 150, 200])
done = np.array([540, 288, 280, 90, 230])
percent = done / goal
