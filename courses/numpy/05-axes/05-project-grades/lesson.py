# Урок np-project-grades. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% peek
import numpy as np

subjects = ["математика", "физика", "программирование", "история", "английский"]
with open("data/scores.csv") as f:
    print(f.read()[:110])

# %% load [exercise]
scores = np.loadtxt("data/scores.csv", delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5))
ids = np.loadtxt("data/scores.csv", delimiter=",", skiprows=1, usecols=0, dtype=str)
# ─── заготовка ───
scores = ...
ids = ...
# ─── проверка ───
def test_scores():
    "scores — таблица 30 × 5"
    assert isinstance(scores, np.ndarray), f"scores — это {type(scores).__name__}, а нужен массив из np.loadtxt"
    assert scores.shape == (30, 5), f"форма scores — {scores.shape}, а нужно (30, 5): столбцы 1–5 — usecols=(1, 2, 3, 4, 5)"
    assert scores[0].tolist() == [68, 49, 68, 82, 81], "первая строка должна быть [68, 49, 68, 82, 81] — баллы студента S01"


def test_ids():
    "ids — 30 кодов студентов"
    assert isinstance(ids, np.ndarray), f"ids — это {type(ids).__name__}, а нужен массив из np.loadtxt(..., dtype=str)"
    assert ids.shape == (30,), f"форма ids — {ids.shape}, а нужно 30 кодов: usecols=0"
    assert ids[0] == "S01" and ids[-1] == "S30", f"коды должны идти от S01 до S30, а сейчас {ids[0]} … {ids[-1]}"
# ─── другое решение ───
path = "data/scores.csv"
scores = np.loadtxt(path, delimiter=",", skiprows=1, usecols=(1, 2, 3, 4, 5))
ids = np.loadtxt(path, delimiter=",", skiprows=1, dtype=str, usecols=0)
# ─── ошибка ───
scores = np.loadtxt("data/scores.csv", delimiter=",", skiprows=1, usecols=(0, 1, 2, 3, 4))

# %% subjects-avg [exercise]
subject_avg = scores.mean(axis=0)
hardest = subjects[subject_avg.argmin()]
# ─── заготовка ───
subject_avg = ...
hardest = ...
# ─── проверка ───
def test_avg():
    "subject_avg — средний балл по каждому предмету"
    assert isinstance(subject_avg, np.ndarray), f"subject_avg — это {type(subject_avg).__name__}, а нужен массив"
    assert subject_avg.shape != (30,), "получилось 30 чисел — по студенту; для предметов нужно axis=0"
    assert np.allclose(subject_avg, [67.766667, 66.766667, 69.033333, 69.7, 65.966667]), f"subject_avg = {np.round(subject_avg, 2).tolist()}"


def test_hardest():
    "hardest — предмет с самым низким средним"
    assert hardest != 4, "4 — индекс; название возьмите из списка subjects"
    assert hardest != "история", "это предмет с самым высоким средним; нужен с самым низким — argmin"
    assert hardest == "английский", f"hardest = {hardest!r}, а самый низкий средний — по английскому"
# ─── другое решение ───
subject_avg = np.mean(scores, axis=0)
hardest = subjects[np.argmin(subject_avg)]
# ─── ошибка ───
subject_avg = scores.mean(axis=0)
hardest = subjects[subject_avg.argmax()]

# %% students [exercise]
student_avg = scores.mean(axis=1)
best_id = ids[student_avg.argmax()]
# ─── заготовка ───
student_avg = ...
best_id = ...
# ─── проверка ───
def test_avg():
    "student_avg — средний балл каждого студента"
    assert isinstance(student_avg, np.ndarray) and student_avg.shape == (30,), "student_avg — 30 чисел, по студенту: axis=1"
    assert abs(student_avg[0] - 69.6) < 1e-9, f"средний балл S01 — {student_avg[0]}, а должен быть 69.6"


def test_best():
    "best_id — код лучшего студента"
    assert best_id != 11, "11 — индекс; код возьмите из ids"
    assert best_id == "S12", f"best_id = {best_id!r}, а лучший средний балл у S12"
# ─── другое решение ───
student_avg = scores.sum(axis=1) / 5
best_id = ids[np.argmax(student_avg)]
# ─── ошибка ───
student_avg = scores.mean(axis=1)
best_id = student_avg.argmax()

# %% best-per-subject [exercise]
best_by_subject = ids[scores.argmax(axis=0)]
# ─── заготовка ───
best_by_subject = ...
# ─── проверка ───
def test_best():
    "best_by_subject — лучший студент по каждому предмету"
    assert isinstance(best_by_subject, np.ndarray), f"best_by_subject — это {type(best_by_subject).__name__}, а нужен массив кодов"
    got = best_by_subject.tolist()
    assert got != [17, 28, 11, 8, 11], "это индексы строк; подставьте их в ids[...]"
    assert len(got) == 5, f"кодов {len(got)}, а предметов 5: argmax(axis=0)"
    assert got == ["S18", "S29", "S12", "S09", "S12"], f"best_by_subject = {got}"
# ─── другое решение ───
best_rows = np.argmax(scores, axis=0)
best_by_subject = ids[best_rows]
# ─── ошибка ───
best_by_subject = scores.argmax(axis=0)

# %% passed [exercise]
all_passed = (scores >= 60).all(axis=1).sum()
# ─── заготовка ───
all_passed = ...
# ─── проверка ───
def test_passed():
    "all_passed — студенты, у которых все баллы не ниже 60"
    assert not isinstance(all_passed, np.ndarray), "all_passed — массив, а нужно одно число: сумма маски .all(axis=1)"
    assert all_passed != 5, "5 — это число предметов, по которым все сдали (axis=0); нужны студенты — axis=1"
    assert all_passed == 12, f"all_passed = {all_passed}, а все предметы сдали 12 студентов"
# ─── другое решение ───
all_passed = (scores.min(axis=1) >= 60).sum()
# ─── ошибка ───
all_passed = (scores >= 60).any(axis=1).sum()

# %% risk [exercise]
at_risk = ids[(scores < 50).any(axis=1)]
# ─── заготовка ───
at_risk = ...
# ─── проверка ───
def test_risk():
    "at_risk — коды студентов с баллом ниже 50"
    assert isinstance(at_risk, np.ndarray), f"at_risk — это {type(at_risk).__name__}, а нужен массив кодов: ids[маска]"
    assert at_risk.dtype != bool, "это маска; подставьте её в ids[...], чтобы получить коды"
    assert len(at_risk) == 9, f"в at_risk {len(at_risk)} кодов, а студентов с баллом ниже 50 — 9: нужно any(axis=1)"
# ─── другое решение ───
at_risk = ids[scores.min(axis=1) < 50]
# ─── ошибка ───
at_risk = ids[(scores < 50).all(axis=1)]
# ─── ошибка ───
at_risk = (scores < 50).any(axis=1)

# %% top5 [exercise]
top5 = ids[np.argsort(student_avg)[::-1][:5]]
# ─── заготовка ───
top5 = ...
# ─── проверка ───
def test_top5():
    "top5 — пять лучших по среднему баллу"
    assert isinstance(top5, np.ndarray), f"top5 — это {type(top5).__name__}, а нужен массив кодов"
    got = top5.tolist()
    assert len(got) == 5, f"в top5 {len(got)} кодов, а нужно 5"
    assert got != ["S24", "S27", "S21", "S29", "S12"], "порядок перевёрнут: начните с лучшего"
    assert got != ["S07", "S25", "S30", "S11", "S10"], "это пять худших: argsort упорядочивает по возрастанию — разверните [::-1], потом берите [:5]"
    assert got == ["S12", "S29", "S21", "S27", "S24"], f"top5 = {got}"
# ─── другое решение ───
top5 = ids[np.argsort(student_avg)][-5:][::-1]
# ─── ошибка ───
top5 = ids[np.argsort(student_avg)][:5]

# %% summary
for name, avg in zip(subjects, np.round(subject_avg, 1)):
    print(f"{name}: {avg}")
print("самый трудный:", hardest, "| лучший студент:", best_id, round(student_avg.max(), 1))
print("сдали всё:", all_passed, "из", len(ids), "| в зоне риска:", len(at_risk))
print("пятёрка лучших:", top5)
