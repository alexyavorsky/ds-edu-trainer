# Примеры к статье numpy/views-copies.

# %% setup
prices = np.array([100, 200, 300, 400, 500])

# %% view
part = prices[1:4]          # срез — представление
part[0] = 0
prices                      # исходный массив изменился
# ─── вывод ───
# array([100,   0, 300, 400, 500])

# %% copy
part = prices[1:4].copy()   # независимая копия
part[0] = 0
prices
# ─── вывод ───
# array([100, 200, 300, 400, 500])

# %% check
view = prices[::2]
fancy = prices[[0, 2, 4]]
print(view.base is prices)             # у представления base — исходный массив
print(fancy.base is None)              # у копии собственные данные
np.shares_memory(prices, view), np.shares_memory(prices, fancy)
# ─── вывод ───
# True
# True
# (True, False)

# %% reshape-view
grid = prices.reshape(5, 1)
grid[0, 0] = -1             # reshape тоже даёт представление
prices
# ─── вывод ───
# array([ -1, 200, 300, 400, 500])

# %% function-arg
def normalize(a):
    a /= a.max()            # на месте: меняет массив вызывающего
    return a

data = np.array([2.0, 4.0, 8.0])
normalize(data)
data
# ─── вывод ───
# array([0.25, 0.5 , 1.  ])

# %% big-base
big = np.arange(1_000_000)
first = big[:3]             # держит ссылку на весь миллион элементов
print(first.base.size)
first = big[:3].copy()      # после копии большой массив можно освободить
print(first.base)
# ─── вывод ───
# 1000000
# None
