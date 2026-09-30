# Урок np-project-expenses. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% data
import numpy as np

days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
week1 = np.array([1450, 980, 2300, 1200, 3100, 4200, 1800])
week2 = np.array([1320, 1150, 1980, 2450, 2900, 5100, 2100])
print(week1)
print(week2)

# %% averages [exercise]
avg1 = week1.mean()
avg2 = week2.mean()
# ─── заготовка ───
avg1 = ...
avg2 = ...
# ─── проверка ───
def test_avg1():
    "avg1 — средние траты в день первой недели"
    assert not isinstance(avg1, np.ndarray), "avg1 — массив, а нужно одно число: week1.mean()"
    assert abs(avg1 - 2147.142857) < 0.001, f"avg1 = {avg1}, а в первую неделю в среднем тратилось ≈ 2147.14 ₽"


def test_avg2():
    "avg2 — средние траты в день второй недели"
    assert not isinstance(avg2, np.ndarray), "avg2 — массив, а нужно одно число: week2.mean()"
    assert abs(avg2 - 2147.142857) > 0.001, "avg2 совпадает со средним первой недели — посчитайте его по week2"
    assert abs(avg2 - 2428.571428) < 0.001, f"avg2 = {avg2}, а во вторую неделю в среднем тратилось ≈ 2428.57 ₽"
# ─── другое решение ───
avg1 = week1.sum() / 7
avg2 = np.mean(week2)
# ─── ошибка ───
avg1 = week1.mean()
avg2 = week1.mean()

# %% change [exercise]
change = week2 - week1
# ─── заготовка ───
change = ...
# ─── проверка ───
def test_array():
    "change — массив из семи разниц"
    assert isinstance(change, np.ndarray), f"change — это {type(change).__name__}, а нужен массив: week2 - week1"
    assert len(change) == 7, f"в change {len(change)} чисел, а дней 7"


def test_values():
    "change = вторая неделя − первая"
    assert isinstance(change, np.ndarray), "change пока не массив — сначала исправьте то, о чём говорит проверка выше"
    got = change.tolist()
    assert got != [130, -170, 320, -1250, 200, -900, -300], "знаки перевёрнуты: из второй недели вычитайте первую"
    assert got == [-130, 170, -320, 1250, -200, 900, 300], f"получилось {got}, а в понедельник траты изменились на 1320 − 1450 = −130 ₽"
# ─── другое решение ───
change = -week1 + week2
# ─── ошибка ───
change = week1 - week2

# %% change-print
print(change)
print("больше всего траты выросли в", days[change.argmax()])

# %% usd [exercise]
week2_usd = week2 / 92
# ─── заготовка ───
week2_usd = ...
# ─── проверка ───
def test_usd():
    "траты второй недели в долларах"
    assert isinstance(week2_usd, np.ndarray), f"week2_usd — это {type(week2_usd).__name__}, а нужен массив: разделите week2 на курс"
    got = np.asarray(week2_usd, dtype=float)
    assert not np.allclose(got[:1], [1320 * 92]), "вы умножили на курс, а рубли в доллары переводят делением"
    assert np.allclose(got, [14.35, 12.5, 21.52, 26.63, 31.52, 55.43, 22.83], atol=0.01), f"получилось {np.round(got, 2).tolist()}, а 1320 ₽ — это ≈ 14.35 $"
# ─── другое решение ───
rate = 92
week2_usd = week2 / rate
# ─── ошибка ───
week2_usd = week2 * 92

# %% max-day [exercise]
max_day = days[week2.argmax()]
max_sum = week2.max()
# ─── заготовка ───
max_day = ...
max_sum = ...
# ─── проверка ───
def test_day():
    "max_day — название самого дорогого дня"
    assert not isinstance(max_day, (int, np.integer)), f"max_day = {max_day} — это число; нужно название дня из списка days"
    assert max_day == "сб", f"max_day = {max_day!r}, а больше всего во второй неделе потратили в субботу"


def test_sum():
    "max_sum — сколько потратили в этот день"
    assert max_sum != 5, "5 — это индекс дня; сама сумма — week2.max()"
    assert max_sum == 5100, f"max_sum = {max_sum}, а в субботу потратили 5100 ₽"
# ─── другое решение ───
i = week2.argmax()
max_day = days[i]
max_sum = week2[i]
# ─── ошибка ───
max_day = days[week1.argmax()]
max_sum = week1.max()

# %% budget [exercise]
left = 2000 - week2
left_total = left.sum()
# ─── заготовка ───
left = ...
left_total = ...
# ─── проверка ───
def test_left():
    "left — остаток бюджета по дням"
    assert isinstance(left, np.ndarray), f"left — это {type(left).__name__}, а нужен массив: 2000 - week2"
    got = left.tolist()
    assert got != [-680, -850, -20, 450, 900, 3100, 100], "знаки перевёрнуты: остаток — это бюджет минус траты"
    assert got == [680, 850, 20, -450, -900, -3100, -100], f"получилось {got}, а в понедельник осталось 2000 − 1320 = 680 ₽"


def test_total():
    "left_total — остаток за неделю"
    assert left_total == -3000, f"left_total = {left_total}, а за неделю бюджет превышен на 3000 ₽ (остаток −3000)"
# ─── другое решение ───
left = 2000 - week2
left_total = 2000 * 7 - week2.sum()
# ─── ошибка ───
left = week2 - 2000
left_total = left.sum()

# %% shares [exercise]
shares = week2 / week2.sum() * 100
# ─── заготовка ───
shares = ...
# ─── проверка ───
def test_shares():
    "доля каждого дня в тратах недели, в процентах"
    assert isinstance(shares, np.ndarray), f"shares — это {type(shares).__name__}, а нужен массив"
    got = np.asarray(shares, dtype=float)
    assert not np.isclose(got.sum(), 1), "сумма долей — 1: это доли, а нужны проценты — умножьте на 100"
    assert np.isclose(got.sum(), 100), f"сумма процентов — {got.sum():.1f}, а должна быть 100: делите на сумму за неделю"
    assert np.allclose(got, [7.76, 6.76, 11.65, 14.41, 17.06, 30.0, 12.35], atol=0.01), f"получилось {np.round(got, 1).tolist()}"
# ─── другое решение ───
shares = 100 * week2 / np.sum(week2)
# ─── ошибка ───
shares = week2 / week2.sum()
# ─── ошибка ───
shares = week2 / week2.max() * 100

# %% summary
print("в среднем в день:", round(avg1), "→", round(avg2), "₽")
print("рост:", round((week2.sum() / week1.sum() - 1) * 100, 1), "%")
print("самый дорогой день:", max_day, max_sum, "₽")
print("остаток бюджета за неделю:", left_total, "₽")
