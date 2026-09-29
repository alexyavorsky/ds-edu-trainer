# Примеры к статье numpy/meshgrid.

# %% setup
x = np.array([0, 1, 2, 3])   # 4 точки по горизонтали
y = np.array([10, 20, 30])   # 3 точки по вертикали

# %% basic
X, Y = np.meshgrid(x, y)
print(X)
Y
# ─── вывод ───
# [[0 1 2 3]
#  [0 1 2 3]
#  [0 1 2 3]]
# array([[10, 10, 10, 10],
#        [20, 20, 20, 20],
#        [30, 30, 30, 30]])

# %% function
X, Y = np.meshgrid(x, y)
X + Y                        # значение функции в каждой точке сетки
# ─── вывод ───
# array([[10, 11, 12, 13],
#        [20, 21, 22, 23],
#        [30, 31, 32, 33]])

# %% ij
X, Y = np.meshgrid(x, y, indexing="ij")
X.shape, Y.shape             # (len(x), len(y)) вместо (len(y), len(x))
# ─── вывод ───
# ((4, 3), (4, 3))

# %% sparse
X, Y = np.meshgrid(x, y, sparse=True)
print(X.shape, Y.shape)      # без повторов: транслирование сделает остальное
X + Y
# ─── вывод ───
# (1, 4) (3, 1)
# array([[10, 11, 12, 13],
#        [20, 21, 22, 23],
#        [30, 31, 32, 33]])

# %% broadcasting
x[np.newaxis, :] + y[:, np.newaxis]   # тот же результат без meshgrid
# ─── вывод ───
# array([[10, 11, 12, 13],
#        [20, 21, 22, 23],
#        [30, 31, 32, 33]])

# %% mgrid
rows, cols = np.mgrid[0:2, 0:3]       # сетка индексов по срезам
print(rows)
cols
# ─── вывод ───
# [[0 0 0]
#  [1 1 1]]
# array([[0, 1, 2],
#        [0, 1, 2]])

# %% distance
X, Y = np.meshgrid(np.linspace(-1, 1, 5), np.linspace(-1, 1, 5))
(np.sqrt(X**2 + Y**2) <= 1).astype(int)   # точки внутри круга радиуса 1
# ─── вывод ───
# array([[0, 0, 1, 0, 0],
#        [0, 1, 1, 1, 0],
#        [1, 1, 1, 1, 1],
#        [0, 1, 1, 1, 0],
#        [0, 0, 1, 0, 0]])
