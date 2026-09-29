# Примеры к статье numpy/diff.

# %% setup
meter = np.array([1200, 1215, 1233, 1240, 1262])   # показания счётчика по дням

# %% basic
np.diff(meter)                    # расход за каждый день: на 1 элемент короче
# ─── вывод ───
# array([15, 18,  7, 22])

# %% prepend
np.diff(meter, prepend=meter[0])  # та же длина: первый день — 0
# ─── вывод ───
# array([ 0, 15, 18,  7, 22])

# %% inverse
usage = np.diff(meter)
meter[0] + np.concatenate([[0], np.cumsum(usage)])   # cumsum восстанавливает показания
# ─── вывод ───
# array([1200, 1215, 1233, 1240, 1262])

# %% second
np.diff(meter, n=2)               # изменение расхода
# ─── вывод ───
# array([  3, -11,  15])

# %% two-dims
table = np.array([[1, 4, 9],
                  [2, 3, 7]])
print(np.diff(table))             # по умолчанию — вдоль последней оси (строк)
np.diff(table, axis=0)            # между строками
# ─── вывод ───
# [[3 5]
#  [1 4]]
# array([[ 1, -1, -2]])

# %% gradient
np.gradient(np.array([1.0, 4.0, 9.0, 16.0]))   # центральные разности, длина та же
# ─── вывод ───
# array([3., 4., 6., 7.])

# %% unsigned
level = np.array([5, 3, 8], dtype=np.uint8)
np.diff(level)                    # 3 − 5 в беззнаковом типе даёт 254
# ─── вывод ───
# array([254,   5], dtype=uint8)
