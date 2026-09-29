# Примеры к статье numpy/apply-along-axis.

# %% setup
# оценки 3 учеников по 5 работам
scores = np.array([[4, 5, 3, 5, 4],
                   [3, 3, 4, 2, 5],
                   [5, 5, 5, 4, 5]])

# %% basic
def spread(row):
    return row.max() - row.min()

np.apply_along_axis(spread, 1, scores)       # функция получает каждую строку
# ─── вывод ───
# array([2, 3, 1])

# %% vectorized
scores.max(axis=1) - scores.min(axis=1)      # то же без apply_along_axis
# ─── вывод ───
# array([2, 3, 1])

# %% returns-array
def top2(row):
    return np.sort(row)[-2:]                 # функция возвращает массив

np.apply_along_axis(top2, 1, scores)
# ─── вывод ───
# array([[5, 5],
#        [4, 5],
#        [5, 5]])

# %% no-axis-function
def mode(row):
    return np.bincount(row).argmax()         # у bincount нет параметра axis

np.apply_along_axis(mode, 1, scores)         # самая частая оценка каждого ученика
# ─── вывод ───
# array([4, 3, 5])

# %% axis0
np.apply_along_axis(np.median, 0, scores)    # по столбцам — функция получает каждый столбец
# ─── вывод ───
# array([4., 5., 4., 4., 5.])
