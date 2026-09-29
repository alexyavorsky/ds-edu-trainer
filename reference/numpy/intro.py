# Примеры к статье numpy/intro.

# %% list-vs-array
print([1, 2, 3] * 2)             # список: повторение
np.array([1, 2, 3]) * 2          # массив: умножение каждого элемента
# ─── вывод ───
# [1, 2, 3, 1, 2, 3]
# array([2, 4, 6])

# %% vectorized
celsius = np.array([-5.0, 0.0, 12.5, 30.0])
celsius * 9 / 5 + 32             # формула сразу для всех значений, без цикла
# ─── вывод ───
# array([23. , 32. , 54.5, 86. ])

# %% two-dims
table = np.array([[1, 2, 3],
                  [4, 5, 6]])
print(table.shape)
table + 10
# ─── вывод ───
# (2, 3)
# array([[11, 12, 13],
#        [14, 15, 16]])

# %% one-type
print(np.array([1, 2.5, 3]))     # целые стали float
np.array([1, "два", 3])          # всё превратилось в строки
# ─── вывод ───
# [1.  2.5 3. ]
# array(['1', 'два', '3'], dtype='<U21')

# %% version
np.__version__
# ─── вывод ───
# '2.5.3'

# %% append-copies
scores = np.array([4, 5])
more = np.append(scores, 3)      # новый массив, исходный не меняется
print(scores)
more
# ─── вывод ───
# [4 5]
# array([4, 5, 3])
