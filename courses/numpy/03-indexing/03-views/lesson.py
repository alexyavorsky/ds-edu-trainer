# Урок np-views. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% view
import numpy as np

prices = np.array([100.0, 250.0, 80.0, 40.0])
first = prices[:2]
first[0] = 0
print(first)
print(prices)

# %% list-copy
price_list = [100.0, 250.0, 80.0, 40.0]
part = price_list[:2]
part[0] = 0
print(part)
print(price_list)

# %% copy
prices = np.array([100.0, 250.0, 80.0, 40.0])
first = prices[:2].copy()
first[0] = 0
print(first)
print(prices)

# %% sale [exercise]
prices = np.array([100.0, 250.0, 80.0, 40.0])
sale = prices[:2].copy()
sale[:] = sale * 0.5
# ─── заготовка ───
prices = np.array([100.0, 250.0, 80.0, 40.0])
sale = prices[:2]
sale[:] = sale * 0.5
# ─── проверка ───
def test_sale():
    "sale — первые два товара за полцены"
    assert isinstance(sale, np.ndarray), f"sale — это {type(sale).__name__}, а нужен массив"
    assert sale.tolist() == [50.0, 125.0], f"в sale {sale.tolist()}, а со скидкой 50 % первые два товара стоят 50 и 125"


def test_prices_kept():
    "prices не изменился"
    assert prices.tolist() == [100.0, 250.0, 80.0, 40.0], (
        f"prices изменился: {prices.tolist()} — sale смотрит на те же данные. Сделайте копию среза: prices[:2].copy()"
    )
# ─── другое решение ───
prices = np.array([100.0, 250.0, 80.0, 40.0])
sale = prices[:2] * 0.5
# ─── ошибка ───
prices = np.array([100.0, 250.0, 80.0, 40.0])
sale = prices[:2]
sale[:] = sale * 0.5

# %% view-change [quiz]
a = np.array([1, 2, 3, 4])
b = a[1:3]
b[0] = 99
print(a)

# %% useful
week_plan = np.full(7, 100)
weekend = week_plan[5:]   # суббота и воскресенье
weekend[:] = 0
print(week_plan)

# %% bonus [exercise]
plan = np.array([100.0, 110.0, 120.0, 150.0, 160.0, 170.0, 130.0, 120.0, 140.0, 150.0, 160.0, 200.0])
q2 = plan[3:6]
q2[:] = q2 * 1.1
# ─── заготовка ───
plan = np.array([100.0, 110.0, 120.0, 150.0, 160.0, 170.0, 130.0, 120.0, 140.0, 150.0, 160.0, 200.0])
q2 = ...
# ─── проверка ───
def test_plan():
    "в plan второй квартал увеличен на 10 %"
    got = np.asarray(plan, dtype=float)
    assert not np.allclose(got[3:6], [150, 160, 170]), (
        "plan не изменился. Если вы писали q2 = q2 * 1.1, это новый массив, а не окно на plan: присвойте в срез — q2[:] = q2 * 1.1"
    )
    assert np.allclose(got[3:6], [165, 176, 187]), f"второй квартал в plan — {np.round(got[3:6], 1).tolist()}, а должен стать 165, 176, 187"


def test_rest():
    "остальные месяцы не изменились"
    got = np.asarray(plan, dtype=float)
    assert np.allclose(got[:3], [100, 110, 120]) and np.allclose(got[6:], [130, 120, 140, 150, 160, 200]), (
        f"изменились не только месяцы 3–5: {np.round(got, 1).tolist()}"
    )
# ─── другое решение ───
plan = np.array([100.0, 110.0, 120.0, 150.0, 160.0, 170.0, 130.0, 120.0, 140.0, 150.0, 160.0, 200.0])
q2 = plan[3:6]
plan[3:6] = q2 * 1.1
# ─── ошибка ───
plan = np.array([100.0, 110.0, 120.0, 150.0, 160.0, 170.0, 130.0, 120.0, 140.0, 150.0, 160.0, 200.0])
q2 = plan[3:6]
q2 = q2 * 1.1
# ─── ошибка ───
plan = np.array([100.0, 110.0, 120.0, 150.0, 160.0, 170.0, 130.0, 120.0, 140.0, 150.0, 160.0, 200.0])
q2 = plan[3:6].copy()
q2[:] = q2 * 1.1

# %% backup [exercise]
scores = np.array([12, 15, 9, 20, 17, 11])
backup = scores.copy()
scores[3:] = 0
# ─── заготовка ───
scores = np.array([12, 15, 9, 20, 17, 11])
backup = ...
# ─── проверка ───
def test_scores():
    "в scores обнулено всё начиная с индекса 3"
    assert scores.tolist() == [12, 15, 9, 0, 0, 0], f"scores = {scores.tolist()}, а должно быть [12, 15, 9, 0, 0, 0]"


def test_backup():
    "backup — прежние значения"
    assert isinstance(backup, np.ndarray), f"backup — это {type(backup).__name__}, а нужна копия массива: scores.copy()"
    assert backup.tolist() != [12, 15, 9, 0, 0, 0], "backup тоже обнулился: это не копия, а тот же массив — используйте scores.copy() до изменения"
    assert backup.tolist() == [12, 15, 9, 20, 17, 11], f"backup = {backup.tolist()}, а должен хранить исходные значения"
# ─── другое решение ───
scores = np.array([12, 15, 9, 20, 17, 11])
backup = np.array(scores)
scores[3:] = 0
# ─── ошибка ───
scores = np.array([12, 15, 9, 20, 17, 11])
backup = scores
scores[3:] = 0
# ─── ошибка ───
scores = np.array([12, 15, 9, 20, 17, 11])
backup = scores[:]
scores[3:] = 0
