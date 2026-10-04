# Урок np-shape. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% table
import numpy as np

sales = np.array([
    [120, 135, 150, 170],   # магазин 1: кварталы 1–4
    [ 90, 100,  95, 130],   # магазин 2
    [200, 180, 210, 250],   # магазин 3
])
sales

# %% shape
print(sales.shape)
print(sales.ndim, sales.size, len(sales))
print(np.arange(5).shape)

# %% scores [exercise]
scores = np.array([[5, 4, 5], [3, 4, 4], [5, 5, 4]])
# ─── заготовка ───
scores = ...
# ─── проверка ───
def test_array():
    "scores — двумерный массив 3 × 3"
    assert isinstance(scores, np.ndarray), f"scores — это {type(scores).__name__}, а нужен массив — его создают из списка списков"
    assert scores.ndim == 2, f"у scores {scores.ndim} измерение, а нужна таблица: каждый ученик — в своём внутреннем списке"
    assert scores.shape == (3, 3), f"форма scores — {scores.shape}, а нужно 3 ученика × 3 предмета"


def test_values():
    "оценки стоят по ученикам в строках"
    assert isinstance(scores, np.ndarray) and scores.shape == (3, 3), "сначала исправьте то, о чём говорит проверка выше"
    got = scores.tolist()
    assert got != [[5, 3, 5], [4, 4, 5], [5, 4, 4]], "таблица перевёрнута: ученик должен быть строкой, а не столбцом"
    assert got == [[5, 4, 5], [3, 4, 4], [5, 5, 4]], f"в scores {got}"
# ─── другое решение ───
first = [5, 4, 5]
second = [3, 4, 4]
third = [5, 5, 4]
scores = np.array([first, second, third])
# ─── ошибка ───
scores = np.array([5, 4, 5, 3, 4, 4, 5, 5, 4])
# ─── ошибка ───
scores = np.array([[5, 3, 5], [4, 4, 5], [5, 4, 4]])

# %% dims [exercise]
rows, cols = sales.shape
cells = sales.size
# ─── заготовка ───
rows = ...
cols = ...
cells = ...
# ─── проверка ───
def test_rows_cols():
    "rows и cols — строки и столбцы sales"
    assert not isinstance(rows, tuple), f"rows — это весь кортеж {rows}: возьмите из него первое число"
    assert (rows, cols) != (4, 3), "строки и столбцы перепутаны: в shape сначала строки"
    assert (rows, cols) == (3, 4), f"rows = {rows}, cols = {cols} — это не число строк и столбцов sales"


def test_cells():
    "cells — число элементов"
    assert cells == 12, f"cells = {cells} — это не число элементов sales"
# ─── другое решение ───
rows = sales.shape[0]
cols = sales.shape[1]
cells = rows * cols
# ─── ошибка ───
cols, rows = sales.shape
cells = sales.size
# ─── ошибка ───
rows, cols = sales.shape
cells = len(sales)

# %% shape-of [quiz]
print(np.array([[1, 2, 3], [4, 5, 6]]).shape)

# %% ragged [raises=ValueError]
np.array([[1, 2, 3], [4, 5]])

# %% zeros-2d
np.zeros((2, 3))

# %% board [exercise]
board = np.zeros((8, 8))
# ─── заготовка ───
board = ...
# ─── проверка ───
def test_board():
    "board — таблица 8 × 8 из нулей"
    assert isinstance(board, np.ndarray), f"board — это {type(board).__name__}, а нужен массив"
    assert board.shape != (64,), "получился ряд из 64 нулей, а нужна таблица: форму таблицы передают кортежем"
    assert board.shape == (8, 8), f"форма board — {board.shape}, а нужно 8 × 8"
    assert board.sum() == 0, "в board должны быть только нули"
# ─── другое решение ───
board = np.full((8, 8), 0)
# ─── ошибка ───
board = np.zeros(64)

# %% sum-2d
print(sales.sum())
print(sales.max())

# %% avg-score [exercise]
avg_score = scores.mean()
# ─── заготовка ───
avg_score = ...
# ─── проверка ───
def test_avg():
    "средняя оценка по всей таблице"
    assert not isinstance(avg_score, np.ndarray), "avg_score — массив, а нужно одно число — среднее по всей таблице"
    assert abs(avg_score - 39 / 9) < 1e-9, f"avg_score = {avg_score} — это не средняя оценка по всей таблице"
# ─── другое решение ───
avg_score = scores.sum() / scores.size
# ─── ошибка ───
avg_score = scores.sum() / len(scores)
