# Примеры к статье numpy/axis.

# %% setup
# продажи: 3 магазина (строки) × 4 месяца (столбцы)
sales = np.array([[5, 3, 4, 6],
                  [2, 7, 1, 3],
                  [4, 4, 5, 2]])

# %% sum-axis
print(sales.sum(axis=0))    # по каждому месяцу (столбцу)
print(sales.sum(axis=1))    # по каждому магазину (строке)
sales.sum()                 # всё вместе
# ─── вывод ───
# [11 14 10 11]
# [18 13 15]
# np.int64(46)

# %% keepdims
row_total = sales.sum(axis=1, keepdims=True)
print(row_total.shape)
(sales / row_total).round(2)   # доля каждого месяца в продажах магазина
# ─── вывод ───
# (3, 1)
# array([[0.28, 0.17, 0.22, 0.33],
#        [0.15, 0.54, 0.08, 0.23],
#        [0.27, 0.27, 0.33, 0.13]])

# %% argmax
print(sales.argmax(axis=1))  # лучший месяц каждого магазина
sales.argmax(axis=0)         # лучший магазин каждого месяца
# ─── вывод ───
# [3 1 2]
# array([0, 1, 2, 0])

# %% cumsum
print(sales.cumsum(axis=1))  # нарастающий итог по месяцам; форма не меняется
sales.cumsum()               # без axis — массив вытягивается в строку
# ─── вывод ───
# [[ 5  8 12 18]
#  [ 2  9 10 13]
#  [ 4  8 13 15]]
# array([ 5,  8, 12, 18, 20, 27, 28, 31, 35, 39, 44, 46])

# %% negative-axis
cube = np.ones((2, 3, 4))
print(cube.sum(axis=-1).shape)       # последняя ось
cube.sum(axis=(0, 2)).shape          # сразу по двум осям
# ─── вывод ───
# (2, 3)
# (3,)

# %% out-of-range [raises=AxisError]
sales.sum(axis=2)
# ─── вывод ───
# AxisError: axis 2 is out of bounds for array of dimension 2
