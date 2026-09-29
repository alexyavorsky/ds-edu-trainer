# Примеры к статье numpy/boolean.

# %% setup
# дневная температура за две недели
temps = np.array([3, -2, 5, 8, -1, 0, 12, 15, 9, -4, 6, 11, 14, 2])

# %% mask
warm = temps > 5
print(warm)
temps[warm]              # только элементы, где маска True
# ─── вывод ───
# [False False False  True False False  True  True  True False  True  True
#   True False]
# array([ 8, 12, 15,  9,  6, 11, 14])

# %% combine
print(temps[(temps > 0) & (temps < 10)])   # и
print(temps[(temps < 0) | (temps > 12)])   # или
temps[~(temps > 5)]                        # не
# ─── вывод ───
# [3 5 8 9 6 2]
# [-2 -1 15 -4 14]
# array([ 3, -2,  5, -1,  0, -4,  2])

# %% assign
fixed = temps.copy()
fixed[fixed < 0] = 0     # отрицательные — в ноль
fixed
# ─── вывод ───
# array([ 3,  0,  5,  8,  0,  0, 12, 15,  9,  0,  6, 11, 14,  2])

# %% count
print((temps < 0).sum())          # True считается как 1
print(np.count_nonzero(temps > 10))
print((temps > 10).mean())        # доля дней
print((temps > 20).any(), (temps > -10).all())
# ─── вывод ───
# 3
# 4
# 0.2857142857142857
# False True

# %% two-dims
grid = np.array([[1, -2, 3],
                 [-4, 5, -6]])
grid[grid > 0]           # результат всегда одномерный
# ─── вывод ───
# array([1, 3, 5])

# %% python-and [raises=ValueError]
temps[(temps > 0) and (temps < 10)]
# ─── вывод ───
# ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

# %% precedence [raises=ValueError]
temps[temps > 0 & temps < 10]     # & выполняется раньше сравнений
# ─── вывод ───
# ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
