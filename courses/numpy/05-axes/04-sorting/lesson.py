# Урок np-sorting. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% sort
import numpy as np

prices = np.array([320, 150, 890, 45, 610, 210])
print(np.sort(prices))
print(np.sort(prices)[::-1])
print(prices)    # исходный порядок сохранился

# %% sort-method
nums = np.array([3, 1, 2])
result = nums.sort()
print(result)
print(nums)

# %% top3 [exercise]
checks = np.array([1450, 380, 2990, 760, 2210, 540, 3120, 890])
top3 = np.sort(checks)[::-1][:3]
# ─── заготовка ───
checks = np.array([1450, 380, 2990, 760, 2210, 540, 3120, 890])
top3 = ...
# ─── проверка ───
def test_top3():
    "top3 — три самые большие суммы по убыванию"
    assert top3 is not None, "top3 = None: метод sort() ничего не возвращает — используйте np.sort(checks)"
    assert isinstance(top3, np.ndarray), f"top3 — это {type(top3).__name__}, а нужен массив"
    got = top3.tolist()
    assert got != [380, 540, 760], "это три самые маленькие суммы: разверните отсортированный массив — [::-1]"
    assert got != [2210, 2990, 3120], "суммы верные, но по возрастанию; нужно от большей к меньшей"
    assert got == [3120, 2990, 2210], f"top3 = {got}, а три самые большие суммы — [3120, 2990, 2210]"


def test_checks():
    "checks не изменился"
    assert checks.tolist() == [1450, 380, 2990, 760, 2210, 540, 3120, 890], "checks изменился — вместо метода sort() используйте np.sort(checks)"
# ─── другое решение ───
checks = np.array([1450, 380, 2990, 760, 2210, 540, 3120, 890])
top3 = np.sort(checks)[-3:][::-1]
# ─── ошибка ───
checks = np.array([1450, 380, 2990, 760, 2210, 540, 3120, 890])
top3 = np.sort(checks)[:3]
# ─── ошибка ───
checks = np.array([1450, 380, 2990, 760, 2210, 540, 3120, 890])
top3 = checks.sort()

# %% argsort
points = np.array([78, 92, 85, 64, 88])
print(np.argsort(points))
print(points[np.argsort(points)])

# %% rank
names = np.array(["Анна", "Иван", "Мария", "Олег", "Елена"])
order = np.argsort(points)[::-1]    # от большего балла к меньшему
print(order)
print(names[order])

# %% leaders [exercise]
sellers = np.array(["Пётр", "Юлия", "Максим", "Светлана", "Роман"])
revenue = np.array([410000, 530000, 290000, 610000, 380000])
ranking = sellers[np.argsort(revenue)[::-1]]
# ─── заготовка ───
sellers = np.array(["Пётр", "Юлия", "Максим", "Светлана", "Роман"])
revenue = np.array([410000, 530000, 290000, 610000, 380000])
ranking = ...
# ─── проверка ───
def test_ranking():
    "ranking — имена от большей выручки к меньшей"
    assert isinstance(ranking, np.ndarray), f"ranking — это {type(ranking).__name__}, а нужен массив имён: sellers[порядок]"
    got = ranking.tolist()
    assert got != [3, 1, 0, 4, 2], "это индексы; подставьте их в sellers[...], чтобы получить имена"
    assert got != ["Максим", "Роман", "Пётр", "Юлия", "Светлана"], "порядок от меньшей выручки: разверните индексы — [::-1]"
    assert got != ["Юлия", "Светлана", "Роман", "Пётр", "Максим"], "имена отсортированы по алфавиту, а нужно по выручке: np.argsort(revenue)"
    assert got == ["Светлана", "Юлия", "Пётр", "Роман", "Максим"], f"ranking = {got}"
# ─── другое решение ───
sellers = np.array(["Пётр", "Юлия", "Максим", "Светлана", "Роман"])
revenue = np.array([410000, 530000, 290000, 610000, 380000])
order = np.argsort(-revenue)
ranking = sellers[order]
# ─── ошибка ───
sellers = np.array(["Пётр", "Юлия", "Максим", "Светлана", "Роман"])
revenue = np.array([410000, 530000, 290000, 610000, 380000])
ranking = sellers[np.argsort(revenue)]
# ─── ошибка ───
sellers = np.array(["Пётр", "Юлия", "Максим", "Светлана", "Роман"])
revenue = np.array([410000, 530000, 290000, 610000, 380000])
ranking = np.sort(sellers)[::-1]

# %% argsort-quiz [quiz]
np.argsort(np.array([30, 10, 20]))

# %% unique
marks_demo = np.array([5, 4, 4, 3, 5, 5, 2, 4, 3, 5, 4, 4])
print(np.unique(marks_demo))
values_demo, counts_demo = np.unique(marks_demo, return_counts=True)
print(values_demo)
print(counts_demo)

# %% grades [exercise]
marks = np.array([4, 3, 5, 4, 4, 2, 5, 3, 4, 3, 3, 5, 3, 4, 3, 3])
values, counts = np.unique(marks, return_counts=True)
most_common = values[counts.argmax()]
# ─── заготовка ───
marks = np.array([4, 3, 5, 4, 4, 2, 5, 3, 4, 3, 3, 5, 3, 4, 3, 3])
values = ...
counts = ...
most_common = ...
# ─── проверка ───
def test_values():
    "values — разные оценки по возрастанию"
    assert isinstance(values, np.ndarray) and values.tolist() == [2, 3, 4, 5], "values — это np.unique(marks): [2, 3, 4, 5]"


def test_counts():
    "counts — сколько раз каждая"
    assert isinstance(counts, np.ndarray) and counts.tolist() == [1, 7, 5, 3], f"counts должно быть [1, 7, 5, 3] — используйте return_counts=True"


def test_most():
    "most_common — самая частая оценка"
    assert most_common != 7, "7 — сколько раз встречается самая частая оценка, а нужна сама оценка: values[counts.argmax()]"
    assert most_common != 1, "1 — это индекс; оценку возьмите из values по этому индексу"
    assert most_common == 3, f"most_common = {most_common}, а чаще всего ставили 3"
# ─── другое решение ───
marks = np.array([4, 3, 5, 4, 4, 2, 5, 3, 4, 3, 3, 5, 3, 4, 3, 3])
result = np.unique(marks, return_counts=True)
values = result[0]
counts = result[1]
most_common = values[np.argmax(counts)]
# ─── ошибка ───
marks = np.array([4, 3, 5, 4, 4, 2, 5, 3, 4, 3, 3, 5, 3, 4, 3, 3])
values, counts = np.unique(marks, return_counts=True)
most_common = counts.max()
