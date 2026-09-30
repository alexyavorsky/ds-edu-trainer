# Урок np-statistics. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import numpy as np

subjects = ["математика", "физика", "программирование", "история", "английский"]
scores = np.loadtxt("data/scores.csv", delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5))
print(scores.shape)
print(scores[:3])

# %% median-vs-mean
salaries = np.array([42, 45, 48, 50, 51, 53, 55, 58, 60, 400])   # тыс. ₽, последний — директор
print(salaries.mean())
print(np.median(salaries))

# %% medians [exercise]
subject_median = np.median(scores, axis=0)
# ─── заготовка ───
subject_median = ...
# ─── проверка ───
def test_median():
    "subject_median — медиана каждого предмета"
    assert isinstance(subject_median, np.ndarray), f"subject_median — это {type(subject_median).__name__}, а нужен массив: np.median(scores, axis=0)"
    assert subject_median.shape != (30,), "получилось 30 чисел — по студенту; для предметов сворачивайте строки — axis=0"
    assert subject_median.shape == (5,), f"у subject_median форма {subject_median.shape}, а нужно 5 чисел"
    assert subject_median[0] == 68.0, f"медиана по математике — {subject_median[0]}, а должна быть 68: это медиана, а не среднее?"
# ─── другое решение ───
subject_median = np.percentile(scores, 50, axis=0)
# ─── ошибка ───
subject_median = scores.mean(axis=0)
# ─── ошибка ───
subject_median = np.median(scores, axis=1)

# %% std
math = scores[:, 0]
print(math.mean(), math.std())
print(np.round(scores.std(axis=0), 1))

# %% spread [exercise]
subject_std = scores.std(axis=0)
most_spread = subject_std.argmax()
# ─── заготовка ───
subject_std = ...
most_spread = ...
# ─── проверка ───
def test_std():
    "subject_std — разброс по каждому предмету"
    assert isinstance(subject_std, np.ndarray) and subject_std.shape == (5,), "subject_std — 5 чисел, по предмету: scores.std(axis=0)"
    assert np.allclose(subject_std, [11.712, 12.606, 12.189, 12.573, 12.131], atol=1e-3), f"subject_std = {np.round(subject_std, 2).tolist()}"


def test_most():
    "most_spread — индекс предмета с наибольшим разбросом"
    assert most_spread == 1, f"most_spread = {most_spread}, а сильнее всего разброс по физике — индекс 1"
# ─── другое решение ───
subject_std = np.std(scores, axis=0)
most_spread = np.argmax(subject_std)
# ─── ошибка ───
subject_std = scores.std(axis=0)
most_spread = subject_std.argmin()

# %% percentile
print(np.percentile(math, 50), np.median(math))
print(np.percentile(math, 90))
print(np.percentile(scores, 90))    # по всей таблице

# %% top10 [exercise]
top_line = np.percentile(scores[:, 0], 90)
top_count = (scores[:, 0] >= top_line).sum()
# ─── заготовка ───
top_line = ...
top_count = ...
# ─── проверка ───
def test_line():
    "top_line — 90-й процентиль по математике"
    assert abs(top_line - 10) > 1e-9, "10 — это не процентиль; np.percentile(баллы, 90)"
    assert abs(top_line - np.percentile(scores[:, 0], 10)) > 1e-9, "это 10-й процентиль; для лучших 10 % нужен 90-й"
    assert abs(top_line - 83.3) < 1e-6, f"top_line = {top_line}, а 90-й процентиль по математике — 83.3"


def test_count():
    "top_count — сколько студентов не ниже порога"
    assert top_count == 3, f"top_count = {top_count}, а не ниже порога — 3 студента из 30"
# ─── другое решение ───
math_scores = scores[:, 0]
top_line = np.percentile(math_scores, 90)
top_count = np.sum(math_scores >= top_line)
# ─── ошибка ───
top_line = np.percentile(scores, 90)
top_count = (scores[:, 0] >= top_line).sum()

# %% round
print(np.round(np.array([1.234, 5.678]), 1))
print(np.round(2.5), np.round(3.5))

# %% round-quiz [quiz]
print(np.round(np.array([0.5, 1.5, 2.5])))

# %% report [exercise]
report = np.round(scores.mean(axis=0), 1)
# ─── заготовка ───
report = ...
# ─── проверка ───
def test_report():
    "report — средние по предметам с одним знаком"
    assert isinstance(report, np.ndarray) and report.shape == (5,), "report — 5 чисел, по предмету: np.round(scores.mean(axis=0), 1)"
    assert report.tolist() != [68.0, 67.0, 69.0, 70.0, 66.0], "округлено до целых; нужен один знак после точки — второй аргумент 1"
    assert report.tolist() == [67.8, 66.8, 69.0, 69.7, 66.0], f"report = {report.tolist()}"
# ─── другое решение ───
report = scores.mean(axis=0).round(1)
# ─── ошибка ───
report = np.round(scores.mean(axis=0))
