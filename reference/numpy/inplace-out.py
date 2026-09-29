# Примеры к статье numpy/inplace-out.

# %% setup
prices = np.array([100.0, 250.0, 80.0])

# %% inplace-vs-new
alias = prices                 # вторая ссылка на тот же массив
prices = prices * 1.1          # новый массив; alias по-прежнему старый
print(alias)
alias *= 1.1                   # на месте: меняется сам массив
alias
# ─── вывод ───
# [100. 250.  80.]
# array([110., 275.,  88.])

# %% out
result = np.empty(3)
np.multiply(prices, 0.9, out=result)   # результат записан в готовый массив
result
# ─── вывод ───
# array([ 90., 225.,  72.])

# %% out-self
np.sqrt(prices, out=prices)            # на месте для любой ufunc
prices.round(4)
# ─── вывод ───
# array([10.    , 15.8114,  8.9443])

# %% where-out
values = np.array([4.0, -9.0, 16.0])
np.sqrt(values, out=values, where=values > 0)   # отрицательные остались как есть
values
# ─── вывод ───
# array([ 2., -9.,  4.])

# %% int-inplace [raises=UFuncTypeError]
counts = np.array([1, 2, 3])
counts += 0.5                  # результат float не помещается в int-массив
# ─── вывод ───
# UFuncTypeError: Cannot cast ufunc 'add' output from dtype('float64') to dtype('int64') with casting rule 'same_kind'

# %% int-new
counts = np.array([1, 2, 3])
counts = counts + 0.5          # обычное присваивание создаёт float-массив
counts
# ─── вывод ───
# array([1.5, 2.5, 3.5])
