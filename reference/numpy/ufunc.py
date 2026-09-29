# Примеры к статье numpy/ufunc.

# %% unary
x = np.array([1.0, 4.0, 9.0, 16.0])
print(np.sqrt(x))
print(np.log10(x))
np.abs(np.array([-3, 0, 2]))
# ─── вывод ───
# [1. 2. 3. 4.]
# [0.         0.60205999 0.95424251 1.20411998]
# array([3, 0, 2])

# %% maximum
today = np.array([12, 18, 9])
yesterday = np.array([15, 11, 9])
print(np.maximum(today, yesterday))  # поэлементно из двух массивов
print(np.max(today))                 # максимум внутри одного массива
np.maximum(today, 10)                # не меньше 10
# ─── вывод ───
# [15 18  9]
# 18
# array([12, 18, 10])

# %% reduce-accumulate
deposits = np.array([100, 250, 50, 300])
print(np.add.reduce(deposits))       # то же, что sum
print(np.add.accumulate(deposits))   # то же, что cumsum
np.maximum.accumulate(np.array([3, 1, 4, 1, 5, 2]))   # максимум «на текущий момент»
# ─── вывод ───
# 700
# [100 350 400 700]
# array([3, 3, 4, 4, 5, 5])

# %% outer
np.multiply.outer(np.arange(1, 5), np.arange(1, 6))   # таблица умножения 4 × 5
# ─── вывод ───
# array([[ 1,  2,  3,  4,  5],
#        [ 2,  4,  6,  8, 10],
#        [ 3,  6,  9, 12, 15],
#        [ 4,  8, 12, 16, 20]])

# %% where-param
x = np.array([4.0, -1.0, 9.0])
np.sqrt(x, out=np.full(3, np.nan), where=x >= 0)      # корень только из неотрицательных
# ─── вывод ───
# array([ 2., nan,  3.])

# %% invalid [warns]
np.log(np.array([1.0, 0.0, -1.0]))
# ─── вывод ───
# RuntimeWarning: divide by zero encountered in log
# RuntimeWarning: invalid value encountered in log
# array([  0., -inf,  nan])

# %% math-module [raises=TypeError]
import math
math.sqrt(np.array([4.0, 9.0]))      # math работает только с одним числом
# ─── вывод ───
# TypeError: only 0-dimensional arrays can be converted to Python scalars
