# Урок pd-project-grades. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

grades = pd.read_csv("data/grades.csv")
print(grades.shape)
grades.head(4)

# %% sheet [exercise]
sheet = grades.pivot_table(values="score", index="student", columns="subject", aggfunc="mean").round(1)
# ─── заготовка ───
sheet = ...
# ─── проверка ───
def test_sheet():
    "sheet — средний балл за год: студенты × предметы"
    assert isinstance(sheet, pd.DataFrame), f"sheet — это {type(sheet).__name__}, а нужна таблица: grades.pivot_table(...)"
    assert sheet.shape == (30, 5), f"у sheet размер {sheet.shape}, а нужно 30 студентов × 5 предметов"
    assert "Анна А." in sheet.index and "Физика" in sheet.columns, "в строках — студенты, в столбцах — предметы"
    assert sheet.loc["Анна А.", "Физика"] != 109, "в ячейках суммы двух семестров, а нужно среднее: aggfunc=\"mean\""
    assert sheet.loc["Анна А.", "Физика"] == 54.5 and sheet.loc["Алексей Я.", "Программирование"] == 98.5, "в ячейках должен быть средний балл за два семестра, округлённый до одного знака"
# ─── другое решение ───
sheet = grades.groupby(["student", "subject"])["score"].mean().unstack().round(1)
# ─── ошибка ───
sheet = grades.pivot_table(values="score", index="student", columns="subject", aggfunc="sum")
# ─── ошибка ───
sheet = grades.pivot_table(values="score", index="subject", columns="student", aggfunc="mean").round(1)

# %% sheet-view
sheet.head(5)

# %% leaders [exercise]
student_avg = grades.groupby("student")["score"].mean()
top3 = student_avg.nlargest(3).round(1)
# ─── заготовка ───
student_avg = ...
top3 = ...
# ─── проверка ───
def test_avg():
    "student_avg — средний балл каждого студента за год"
    assert isinstance(student_avg, pd.Series) and len(student_avg) == 30, "student_avg — Series по 30 студентам: grades.groupby(\"student\")[\"score\"].mean()"
    assert abs(student_avg["Алексей Я."] - 89.9) < 1e-9, "средние не те: среднее столбца score по студенту"


def test_top():
    "top3 — три лучших студента, балл до одного знака"
    assert isinstance(top3, pd.Series) and len(top3) == 3, "top3 — три наибольших значения student_avg: nlargest(3)"
    assert list(top3.index) == ["Алексей Я.", "Наталья П.", "Ольга А."], f"в top3 сейчас {list(top3.index)}, а три лучших — Алексей Я., Наталья П., Ольга А."
    assert top3.tolist() == [89.9, 81.0, 79.3], f"баллы в top3 сейчас {top3.tolist()}, а должны быть [89.9, 81.0, 79.3] — округлите до одного знака"
# ─── другое решение ───
student_avg = grades.pivot_table(values="score", index="student", aggfunc="mean")["score"]
top3 = student_avg.sort_values(ascending=False).head(3).round(1)
# ─── ошибка ───
student_avg = grades.groupby("student")["score"].mean()
top3 = student_avg.nsmallest(3).round(1)
# ─── ошибка ───
student_avg = grades.groupby("student")["score"].mean()
top3 = student_avg.head(3).round(1)

# %% groups [exercise]
group_subject = grades.pivot_table(values="score", index="group", columns="subject", aggfunc="mean", margins=True, margins_name="Все").round(1)
math_leader = group_subject["Математика"].idxmax()
# ─── заготовка ───
group_subject = ...
math_leader = ...
# ─── проверка ───
def test_table():
    "group_subject — средний балл: группы × предметы, с итогами «Все»"
    assert isinstance(group_subject, pd.DataFrame), f"group_subject — это {type(group_subject).__name__}, а нужна таблица"
    assert "Все" in group_subject.index and "Все" in group_subject.columns, "в таблице нет итогов: margins=True, margins_name=\"Все\""
    assert group_subject.shape == (4, 6), f"у group_subject размер {group_subject.shape}, а нужно 4 строки (3 группы и итог) × 6 столбцов (5 предметов и итог)"
    assert group_subject.loc["ИТ-22", "Программирование"] == 77.4 and group_subject.loc["Все", "Все"] == 68.2, "в ячейках должен быть средний балл, округлённый до одного знака: у ИТ-22 по программированию — 77.4, общий — 68.2"


def test_leader():
    "math_leader — лучшая группа по математике"
    assert math_leader == "ИТ-23", f"math_leader = {math_leader!r}, а лучший средний балл по математике у другой группы: group_subject[\"Математика\"].idxmax()"
# ─── другое решение ───
group_subject = grades.pivot_table(values="score", index="group", columns="subject", aggfunc="mean", margins=True, margins_name="Все").round(1)
math_leader = grades[grades["subject"] == "Математика"].groupby("group")["score"].mean().idxmax()
# ─── ошибка ───
group_subject = grades.pivot_table(values="score", index="group", columns="subject", aggfunc="mean").round(1)
math_leader = group_subject["Математика"].idxmax()
# ─── ошибка ───
group_subject = grades.pivot_table(values="score", index="group", columns="subject", aggfunc="mean", margins=True, margins_name="Все").round(1)
math_leader = group_subject["Математика"].max()

# %% groups-view
group_subject

# %% progress [exercise]
by_term = grades.pivot_table(values="score", index="subject", columns="term", aggfunc="mean")
by_term["growth"] = by_term[2] - by_term[1]
grew_most = by_term["growth"].idxmax()
fell = by_term[by_term["growth"] < 0]
# ─── заготовка ───
by_term = ...
# добавьте в by_term столбец growth
grew_most = ...
fell = ...
# ─── проверка ───
def test_by_term():
    "by_term — средний балл: предметы × семестры, и прирост"
    assert isinstance(by_term, pd.DataFrame), f"by_term — это {type(by_term).__name__}, а нужна таблица"
    assert len(by_term) == 5 and 1 in by_term.columns and 2 in by_term.columns, "в строках — пять предметов, в столбцах — семестры 1 и 2: index=\"subject\", columns=\"term\""
    assert "growth" in by_term.columns, "в by_term нет столбца growth: by_term[2] - by_term[1]"
    assert abs(by_term.loc["Физика", "growth"] - 2.1666667) < 1e-5, "growth — средний балл второго семестра минус первого: у физики ≈ 2.17"


def test_answers():
    "grew_most — где баллы выросли сильнее всего, fell — где упали"
    assert grew_most == "Физика", f"grew_most = {grew_most!r}, а сильнее всего выросли баллы по другому предмету: by_term[\"growth\"].idxmax()"
    assert isinstance(fell, pd.DataFrame), f"fell — это {type(fell).__name__}, а нужна таблица: by_term[маска]"
    assert list(fell.index) == ["История"], f"в fell сейчас {list(fell.index)}, а баллы упали только по истории: by_term[by_term[\"growth\"] < 0]"
# ─── другое решение ───
by_term = grades.groupby(["subject", "term"])["score"].mean().unstack()
by_term["growth"] = by_term[2] - by_term[1]
grew_most = by_term.sort_values("growth").index[-1]
fell = by_term.query("growth < 0")
# ─── ошибка ───
by_term = grades.pivot_table(values="score", index="subject", columns="term", aggfunc="mean")
by_term["growth"] = by_term[1] - by_term[2]
grew_most = by_term["growth"].idxmax()
fell = by_term[by_term["growth"] < 0]

# %% passed [exercise]
grades["passed"] = grades["score"] >= 50
pass_table = pd.crosstab(grades["group"], grades["passed"], normalize="index")
fail_21 = pass_table.loc["ИТ-21", False]
# ─── заготовка ───
# добавьте в grades столбец passed
pass_table = ...
fail_21 = ...
# ─── проверка ───
def test_passed():
    "passed — оценка от 50 баллов"
    assert "passed" in grades.columns and grades["passed"].dtype == bool, "в grades нужен столбец-маска passed: grades[\"score\"] >= 50"
    assert (~grades["passed"]).sum() != 17, "50 баллов — это зачёт: условие >=, а не >"
    assert (~grades["passed"]).sum() == 15, "маска не та: незачётов (меньше 50 баллов) должно быть 15"


def test_table():
    "pass_table — доля зачётов и незачётов по группам"
    assert isinstance(pass_table, pd.DataFrame), f"pass_table — это {type(pass_table).__name__}, а нужна таблица: pd.crosstab(...)"
    assert pass_table.shape == (3, 2), f"у pass_table размер {pass_table.shape}, а нужно 3 группы × 2 значения"
    assert abs(pass_table.loc["ИТ-21"].sum() - 1) < 1e-9, "доли в каждой строке должны давать в сумме 1: normalize=\"index\""
    assert abs(fail_21 - 0.08) < 1e-9, f"fail_21 = {fail_21!r}, а доля незачётов в ИТ-21 — 0.08: pass_table.loc[\"ИТ-21\", False]"
# ─── другое решение ───
grades["passed"] = ~(grades["score"] < 50)
pass_table = pd.crosstab(grades["group"], grades["passed"], normalize="index")
fail_21 = 1 - grades.loc[grades["group"] == "ИТ-21", "passed"].mean()
# ─── ошибка ───
grades["passed"] = grades["score"] >= 50
pass_table = pd.crosstab(grades["group"], grades["passed"])
fail_21 = pass_table.loc["ИТ-21", False]
# ─── ошибка ───
grades["passed"] = grades["score"] >= 50
pass_table = pd.crosstab(grades["group"], grades["passed"], normalize="index")
fail_21 = pass_table.loc["ИТ-21", True]

# %% stars [exercise]
year_marks = sheet.reset_index().melt(id_vars="student", var_name="subject", value_name="mean_score")
stars = year_marks[year_marks["mean_score"] >= 90].sort_values("mean_score", ascending=False)
# ─── заготовка ───
year_marks = ...
stars = ...
# ─── проверка ───
def test_long():
    "year_marks — длинная таблица: студент, предмет, средний балл за год"
    assert isinstance(year_marks, pd.DataFrame), f"year_marks — это {type(year_marks).__name__}, а нужна таблица: sheet.reset_index().melt(...)"
    assert list(year_marks.columns) == ["student", "subject", "mean_score"], f"столбцы сейчас {list(year_marks.columns)}, а нужны student, subject, mean_score"
    assert len(year_marks) == 150, f"в year_marks {len(year_marks)} строк, а должно быть 150: 30 студентов × 5 предметов"


def test_stars():
    "stars — годовые баллы от 90, по убыванию"
    assert isinstance(stars, pd.DataFrame), f"stars — это {type(stars).__name__}, а нужна таблица"
    assert list(stars.columns) == ["student", "subject", "mean_score"], "stars — строки таблицы year_marks со столбцами student, subject, mean_score"
    assert len(stars) == 5 and stars["mean_score"].min() >= 90, f"в stars {len(stars)} строк, а годовых баллов от 90 — пять"
    assert stars["mean_score"].tolist() == sorted(stars["mean_score"].tolist(), reverse=True), "отсортируйте stars по убыванию mean_score"
    assert stars.iloc[0]["student"] == "Алексей Я." and stars.iloc[0]["subject"] == "Программирование", "первой должна быть строка с наибольшим баллом"
# ─── другое решение ───
year_marks = grades.groupby(["student", "subject"], as_index=False)["score"].mean().round(1).rename(columns={"score": "mean_score"})
stars = year_marks.query("mean_score >= 90").sort_values("mean_score", ascending=False)
# ─── ошибка ───
year_marks = sheet.melt(var_name="subject", value_name="mean_score")
stars = year_marks[year_marks["mean_score"] >= 90].sort_values("mean_score", ascending=False)
# ─── ошибка ───
year_marks = sheet.reset_index().melt(id_vars="student", var_name="subject", value_name="mean_score")
stars = year_marks[year_marks["mean_score"] >= 90]

# %% summary
print("Лучшие студенты:")
print(top3)
print("Лучшая группа по математике:", math_leader)
print("Сильнее всего выросли баллы:", grew_most, "· упали:", list(fell.index))
print("Доля незачётов в ИТ-21:", round(fail_21 * 100), "%")
print("Годовых баллов от 90:", len(stars))
