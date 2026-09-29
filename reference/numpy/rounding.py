# Примеры к статье numpy/rounding.

# %% setup
prices = np.array([19.49, 5.5, -12.71, 104.5, 7.25])

# %% round
print(np.round(prices))          # до целых
print(np.round(prices, 1))       # до десятых
np.round(prices, -1)             # до десятков
# ─── вывод ───
# [ 19.   6. -13. 104.   7.]
# [ 19.5   5.5 -12.7 104.5   7.2]
# array([ 20.,  10., -10., 100.,  10.])

# %% floor-ceil-trunc
print(np.floor(prices))          # вниз
print(np.ceil(prices))           # вверх
np.trunc(prices)                 # к нулю — отбросить дробную часть
# ─── вывод ───
# [ 19.   5. -13. 104.   7.]
# [ 20.   6. -12. 105.   8.]
# array([ 19.,   5., -12., 104.,   7.])

# %% to-int
print(np.round(prices).astype(int))
prices.astype(int)               # без round — дробная часть просто отброшена
# ─── вывод ───
# [ 19   6 -13 104   7]
# array([ 19,   5, -12, 104,   7])

# %% clip
scores = np.array([-5, 40, 87, 120])
print(np.clip(scores, 0, 100))   # загнать в диапазон [0, 100]
np.clip(scores, 0, None)         # только нижняя граница
# ─── вывод ───
# [  0  40  87 100]
# array([  0,  40,  87, 120])

# %% bankers
np.round(np.array([0.5, 1.5, 2.5, 3.5]))
# ─── вывод ───
# array([0., 2., 2., 4.])

# %% fix [deprecated]
np.fix(np.array([1.7, -1.7]))
# ─── вывод ───
# DeprecationWarning: numpy.fix is deprecated. Use numpy.trunc instead, which is faster and follows the Array API standard.
# array([ 1., -1.])
