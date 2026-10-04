# Урок pd-melt-pivot. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% wide
import pandas as pd

wide = pd.DataFrame({
    "city": ["Омск", "Тула"],
    "jan": [120, 95],
    "feb": [130, 105],
})
wide

# %% melt
long = wide.melt(id_vars="city", var_name="month", value_name="cups")
long

# %% melt-default
wide.melt(id_vars="city")

# %% long-use
print(long.groupby("month")["cups"].sum())
print(long[long["cups"] > 100])

# %% scores
scores = pd.read_csv("data/scores.csv")
scores.head(3)

# %% to-long [exercise]
marks = scores.melt(id_vars="student_id", var_name="subject", value_name="score")
n_marks = len(marks)
# ─── заготовка ───
marks = ...
n_marks = ...
# ─── проверка ───
def test_marks():
    "marks — длинная таблица: студент, предмет, балл"
    assert isinstance(marks, pd.DataFrame), f"marks — это {type(marks).__name__}, а нужна таблица"
    assert list(marks.columns) != ["student_id", "variable", "value"], "столбцы называются variable и value: задайте свои названия — вспомните параметры var_name и value_name"
    assert list(marks.columns) == ["student_id", "subject", "score"], f"столбцы сейчас {list(marks.columns)}, а нужны student_id, subject, score"
    assert len(marks) == 150, f"в marks {len(marks)} строк, а должно быть 150: 30 студентов × 5 предметов"
    assert sorted(marks["subject"].unique()) == ["english", "history", "math", "physics", "programming"], "в столбце subject должны быть названия пяти предметов"
    assert marks["score"].sum() == scores[["math", "physics", "programming", "history", "english"]].sum().sum(), "баллы не те: в столбце score — все оценки широкой таблицы"


def test_n():
    "n_marks — число оценок"
    assert n_marks == 150, f"n_marks = {n_marks!r} — это не число строк marks"
# ─── другое решение ───
marks = scores.melt("student_id", ["math", "physics", "programming", "history", "english"], "subject", "score")
n_marks = marks.shape[0]
# ─── ошибка ───
marks = scores.melt(id_vars="student_id")
n_marks = len(marks)
# ─── ошибка ───
marks = scores.melt(var_name="subject", value_name="score")
n_marks = len(marks)

# %% analysis [exercise]
subject_mean = marks.groupby("subject")["score"].mean().round(1)
weak = marks[marks["score"] < 50].sort_values("score")
# ─── заготовка ───
subject_mean = ...
weak = ...
# ─── проверка ───
def test_mean():
    "subject_mean — средний балл по предметам, один знак"
    assert isinstance(subject_mean, pd.Series), f"subject_mean — это {type(subject_mean).__name__}, а нужен Series"
    assert len(subject_mean) == 5 and "math" in subject_mean.index, "в индексе должны быть пять предметов"
    assert abs(subject_mean["history"] - 69.7) < 1e-9 and abs(subject_mean["english"] - 66.0) < 1e-9, "средние не те или не округлены до одного знака"


def test_weak():
    "weak — оценки ниже 50, от низких к высоким"
    assert isinstance(weak, pd.DataFrame), f"weak — это {type(weak).__name__}, а нужна таблица"
    assert len(weak) == 10 and weak["score"].max() < 50, f"в weak {len(weak)} строк — проверьте условие"
    assert weak["score"].tolist() == sorted(weak["score"].tolist()), "отсортируйте weak по баллу по возрастанию"
# ─── другое решение ───
subject_mean = marks.pivot_table(values="score", index="subject", aggfunc="mean")["score"].round(1)
weak = marks.query("score < 50").sort_values("score")
# ─── ошибка ───
subject_mean = marks.groupby("subject")["score"].mean()
weak = marks[marks["score"] < 50].sort_values("score")
# ─── ошибка ───
subject_mean = marks.groupby("subject")["score"].mean().round(1)
weak = marks[marks["score"] <= 50]

# %% pivot
long.pivot(index="city", columns="month", values="cups")

# %% pivot-flat
back = long.pivot(index="city", columns="month", values="cups").reset_index()
back.columns.name = None
back

# %% grades
grades = pd.read_csv("data/grades.csv")
grades.head(4)

# %% pivot-dup [raises=ValueError]
grades.pivot(index="student", columns="subject", values="score")

# %% pivot-quiz [quiz]
t = pd.DataFrame({"who": ["a", "a", "b", "b"], "what": ["x", "y", "x", "y"], "n": [1, 2, 3, 4]})
print(t.pivot(index="who", columns="what", values="n").shape)

# %% to-wide [exercise]
first_term = grades[grades["term"] == 1]
sheet = first_term.pivot(index="student", columns="subject", values="score")
# ─── заготовка ───
first_term = ...
sheet = ...
# ─── проверка ───
def test_term():
    "first_term — оценки первого семестра"
    assert isinstance(first_term, pd.DataFrame) and len(first_term) == 150 and (first_term["term"] == 1).all(), "first_term — 150 строк таблицы grades, где term равен 1"


def test_sheet():
    "sheet — ведомость: студенты в строках, предметы в столбцах"
    assert isinstance(sheet, pd.DataFrame), f"sheet — это {type(sheet).__name__}, а нужна таблица"
    assert sheet.shape == (30, 5), f"у sheet размер {sheet.shape}, а нужно 30 студентов × 5 предметов"
    assert "Анна А." in sheet.index and "Физика" in sheet.columns, "в строках — студенты, в столбцах — предметы"
    assert sheet.loc["Анна А.", "Физика"] == 49 and sheet.loc["Анна А.", "Математика"] == 68, "в ячейках должны быть баллы первого семестра"
# ─── другое решение ───
first_term = grades.query("term == 1")
sheet = first_term.pivot_table(values="score", index="student", columns="subject", aggfunc="first")
# ─── ошибка ───
first_term = grades[grades["term"] == 1]
sheet = first_term.pivot(index="subject", columns="student", values="score")
# ─── ошибка ───
first_term = grades[grades["term"] == 2]
sheet = first_term.pivot(index="student", columns="subject", values="score")

# %% progress [exercise]
terms = grades.pivot_table(values="score", index="student", columns="term", aggfunc="mean")
terms["growth"] = terms[2] - terms[1]
best_growth = terms["growth"].idxmax()
# ─── заготовка ───
terms = ...
# добавьте в terms столбец growth
best_growth = ...
# ─── проверка ───
def test_terms():
    "terms — средний балл студента по семестрам"
    assert isinstance(terms, pd.DataFrame), f"terms — это {type(terms).__name__}, а нужна таблица"
    assert len(terms) == 30 and 1 in terms.columns and 2 in terms.columns, "в строках — 30 студентов, в столбцах — семестры 1 и 2"
    assert abs(terms.loc["Анна А.", 1] - 69.6) < 1e-9, "в ячейках должен быть средний балл по пяти предметам"


def test_growth():
    "growth — прирост среднего балла, best_growth — кто вырос сильнее всех"
    assert "growth" in terms.columns, "в terms нет столбца growth"
    assert abs(terms.loc["Павел Ч.", "growth"] - (-11.8)) > 1e-9, "знак перепутан: из второго семестра вычитают первый"
    assert abs(terms.loc["Павел Ч.", "growth"] - 11.8) < 1e-9, "growth — средний балл второго семестра минус средний балл первого"
    assert best_growth == "Павел Ч.", f"best_growth = {best_growth!r}, а сильнее всех вырос другой студент"
# ─── другое решение ───
terms = grades.groupby(["student", "term"])["score"].mean().unstack()
terms["growth"] = terms[2] - terms[1]
best_growth = terms.sort_values("growth").index[-1]
# ─── ошибка ───
terms = grades.pivot_table(values="score", index="student", columns="term", aggfunc="mean")
terms["growth"] = terms[1] - terms[2]
best_growth = terms["growth"].idxmax()
