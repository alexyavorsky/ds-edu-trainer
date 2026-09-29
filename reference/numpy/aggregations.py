# Примеры к статье numpy/aggregations.

# %% setup
steps = np.array([6200, 8400, 5100, 12000, 9800, 3000, 7500])   # шаги за неделю

# %% basic
print(steps.sum(), steps.mean())
print(steps.min(), steps.max())
np.ptp(steps)                     # размах: max − min
# ─── вывод ───
# 52000 7428.571428571428
# 3000 12000
# np.int64(9000)

# %% where
print(steps.argmin(), steps.argmax())   # индексы минимума и максимума
steps.argmax() + 1                      # номер дня с максимумом
# ─── вывод ───
# 5 3
# np.int64(4)

# %% any-all
print((steps > 10000).any())
(steps > 1000).all()
# ─── вывод ───
# True
# np.True_

# %% function-or-method
print(np.sum(steps) == steps.sum())
np.sum([1, 2, 3])                 # функция работает и со списком
# ─── вывод ───
# True
# np.int64(6)

# %% ptp-removed [raises=AttributeError]
steps.ptp()
# ─── вывод ───
# AttributeError: 'numpy.ndarray' object has no attribute 'ptp'

# %% builtin-sum
table = np.array([[1, 2],
                  [3, 4]])
print(sum(table))                 # встроенный sum складывает строки
print(table.sum())                # сумма всех элементов
max(table[0])                     # для одномерного встроенный работает, но медленно
# ─── вывод ───
# [4 6]
# 10
# np.int64(2)

# %% empty-max [raises=ValueError]
empty = np.array([])
print(empty.sum())                # сумма пустого — 0
empty.max()                       # у максимума нет значения по умолчанию
# ─── вывод ───
# 0.0
# ValueError: zero-size array to reduction operation maximum which has no identity
