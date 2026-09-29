# Примеры к статье numpy/reshape.

# %% setup
hours = np.arange(12)   # показания за 12 часов

# %% basic
hours.reshape(3, 4)     # 3 строки по 4
# ─── вывод ───
# array([[ 0,  1,  2,  3],
#        [ 4,  5,  6,  7],
#        [ 8,  9, 10, 11]])

# %% minus-one
print(hours.reshape(-1, 6).shape)   # -1: вычисли сам
print(hours.reshape(2, 2, -1).shape)
hours.reshape(-1)                   # в одну строку
# ─── вывод ───
# (2, 6)
# (2, 2, 3)
# array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])

# %% order
print(hours.reshape(3, 4))              # по строкам (C)
hours.reshape(3, 4, order="F")          # по столбцам (Fortran)
# ─── вывод ───
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]
# array([[ 0,  3,  6,  9],
#        [ 1,  4,  7, 10],
#        [ 2,  5,  8, 11]])

# %% ravel-flatten
grid = hours.reshape(3, 4)
flat_view = grid.ravel()                # представление, если можно
flat_copy = grid.flatten()              # всегда копия
flat_view[0] = 100
print(grid[0, 0])
flat_copy[1] = 200
grid[0, 1]
# ─── вывод ───
# 100
# np.int64(1)

# %% bad-size [raises=ValueError]
hours.reshape(5, 2)                     # 12 элементов не делятся на 5 × 2
# ─── вывод ───
# ValueError: cannot reshape array of size 12 into shape (5,2)

# %% resize-function
np.resize(np.array([1, 2, 3]), 7)       # повторяет данные до нужного размера
# ─── вывод ───
# array([1, 2, 3, 1, 2, 3, 1])

# %% set-shape [deprecated]
grid = np.arange(6)
grid.shape = (2, 3)
# ─── вывод ───
# DeprecationWarning: Setting the shape on a NumPy array has been deprecated in NumPy 2.5.
# As an alternative, you can create a new view using np.reshape (with copy=False if needed).
