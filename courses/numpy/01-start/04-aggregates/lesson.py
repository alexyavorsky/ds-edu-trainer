# Урок np-aggregates. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% sum-mean
import numpy as np

temps = np.array([18.5, 21.0, 19.2, 25.4, 23.1, 17.8, 20.3])
print(temps.sum())
temps.mean()

# %% print-scalar
avg = temps.mean()
print(avg)
print(round(avg, 1))

# %% min-max
print(temps.min(), temps.max())

# %% steps [exercise]
steps = np.array([8200, 10450, 6100, 9800, 12300, 15400, 4300])
total_steps = steps.sum()
avg_steps = steps.mean()
# ─── заготовка ───
steps = np.array([8200, 10450, 6100, 9800, 12300, 15400, 4300])
total_steps = ...
avg_steps = ...
# ─── проверка ───
def test_total():
    "total_steps — сумма за неделю"
    assert not isinstance(total_steps, np.ndarray), "total_steps — массив, а нужно одно число: вызовите steps.sum()"
    assert total_steps == 66550, f"total_steps = {total_steps}, а за неделю пройдено 66550 шагов"


def test_avg():
    "avg_steps — среднее в день"
    assert not isinstance(avg_steps, np.ndarray), "avg_steps — массив, а нужно одно число: вызовите steps.mean()"
    assert abs(avg_steps - 9507.142857) < 0.001, f"avg_steps = {avg_steps}, а в среднем в день — 66550 / 7 ≈ 9507.14"
# ─── другое решение ───
steps = np.array([8200, 10450, 6100, 9800, 12300, 15400, 4300])
total_steps = np.sum(steps)
avg_steps = total_steps / len(steps)
# ─── ошибка ───
steps = np.array([8200, 10450, 6100, 9800, 12300, 15400, 4300])
total_steps = steps.sum()
avg_steps = steps.sum() / 6

# %% argmax
days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
i = temps.argmax()
print(i, days[i])
print(days[temps.argmin()])

# %% best-day [exercise]
sales = np.array([41200, 38900, 45100, 39800, 52300, 61700, 48800])
best_day = days[sales.argmax()]
# ─── заготовка ───
sales = np.array([41200, 38900, 45100, 39800, 52300, 61700, 48800])
best_day = ...
# ─── проверка ───
def test_day():
    "best_day — название дня с наибольшей выручкой"
    assert best_day != 61700, "61700 — сама выручка, а нужно название дня: используйте argmax и список days"
    assert not isinstance(best_day, (int, np.integer)), f"best_day = {best_day} — это индекс; по нему возьмите название из списка days"
    assert best_day == "сб", f"best_day = {best_day!r}, а больше всего выручки в субботу"
# ─── другое решение ───
sales = np.array([41200, 38900, 45100, 39800, 52300, 61700, 48800])
best_day = days[np.argmax(sales)]
# ─── ошибка ───
sales = np.array([41200, 38900, 45100, 39800, 52300, 61700, 48800])
best_day = sales.argmax()
# ─── ошибка ───
sales = np.array([41200, 38900, 45100, 39800, 52300, 61700, 48800])
best_day = sales.max()

# %% argmax-value [quiz]
print(np.array([3, 9, 4]).argmax())

# %% functions
print(np.sum(temps), np.mean(temps))
print(np.mean([2, 4, 9]))

# %% deviation [exercise]
diff = temps - temps.mean()
# ─── заготовка ───
diff = ...
# ─── проверка ───
def test_array():
    "diff — массив отклонений для каждого дня"
    assert isinstance(diff, np.ndarray), f"diff — это {type(diff).__name__}, а нужен массив: temps минус среднее"
    assert len(diff) == 7, f"в diff {len(diff)} чисел, а дней 7"


def test_values():
    "diff = температура − средняя"
    assert isinstance(diff, np.ndarray), "diff пока не массив — сначала исправьте то, о чём говорит проверка выше"
    got = np.asarray(diff, dtype=float)
    assert not np.allclose(got, -np.array([-2.257143, 0.242857, -1.557143, 4.642857, 2.342857, -2.957143, -0.457143]), atol=1e-4), (
        "знаки перевёрнуты: вычитайте среднее из температуры, а не температуру из среднего"
    )
    assert np.allclose(got, [-2.257143, 0.242857, -1.557143, 4.642857, 2.342857, -2.957143, -0.457143], atol=1e-4), (
        f"получилось {np.round(got, 2).tolist()}, а первый день холоднее среднего на 2.26 °C"
    )
# ─── другое решение ───
avg = np.mean(temps)
diff = temps - avg
# ─── ошибка ───
diff = temps.mean() - temps

# %% spread [exercise]
spread = temps.max() - temps.min()
# ─── заготовка ───
spread = ...
# ─── проверка ───
def test_spread():
    "spread — максимум минус минимум"
    assert not isinstance(spread, np.ndarray), "spread — массив, а нужно одно число: temps.max() - temps.min()"
    assert abs(spread - 7.6) < 1e-9, f"spread = {spread}, а размах — 25.4 − 17.8 = 7.6"
# ─── другое решение ───
spread = np.max(temps) - np.min(temps)
# ─── ошибка ───
spread = temps.max() - temps.mean()
