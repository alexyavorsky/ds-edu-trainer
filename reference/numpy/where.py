# Примеры к статье numpy/where.

# %% setup
scores = np.array([72, 45, 90, 58, 81, 39])   # баллы за тест

# %% choose
np.where(scores >= 60, "зачёт", "незачёт")
# ─── вывод ───
# array(['зачёт', 'незачёт', 'зачёт', 'незачёт', 'зачёт', 'незачёт'],
#       dtype='<U7')

# %% keep-or-replace
np.where(scores < 50, 50, scores)             # поднять до 50, остальное оставить
# ─── вывод ───
# array([72, 50, 90, 58, 81, 50])

# %% indices
idx = np.where(scores < 60)                   # то же, что np.nonzero
print(idx)
scores[idx]
# ─── вывод ───
# (array([1, 3, 5]),)
# array([45, 58, 39])

# %% two-dims
grid = np.array([[0, 3, 0],
                 [5, 0, 7]])
print(np.nonzero(grid))                       # (номера строк, номера столбцов)
np.argwhere(grid)                             # пары (строка, столбец)
# ─── вывод ───
# (array([0, 1, 1]), array([1, 0, 2]))
# array([[0, 1],
#        [1, 0],
#        [1, 2]])

# %% select
grades = np.select(
    [scores >= 85, scores >= 70, scores >= 50],
    ["отлично", "хорошо", "удовл."],
    default="неуд.",
)
grades
# ─── вывод ───
# array(['хорошо', 'неуд.', 'отлично', 'удовл.', 'хорошо', 'неуд.'],
#       dtype='<U7')

# %% both-branches [warns]
counts = np.array([4, 0, 2])
np.where(counts > 0, 100 / counts, 0)         # 100 / 0 всё равно вычисляется
# ─── вывод ───
# RuntimeWarning: divide by zero encountered in divide
# array([25.,  0., 50.])

# %% divide-where
counts = np.array([4, 0, 2])
np.divide(100, counts, out=np.zeros(3), where=counts > 0)
# ─── вывод ───
# array([25.,  0., 50.])
