# Примеры к статье numpy/fancy.

# %% setup
prices = np.array([250, 120, 480, 90, 310])   # цены пяти товаров
table = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# %% pick
prices[[0, 2, 4]]
# ─── вывод ───
# array([250, 480, 310])

# %% order-repeat
print(prices[[4, 0, 0, -1]])        # любой порядок, повторы, отрицательные
order = np.argsort(prices)          # индексы по возрастанию цены
prices[order]
# ─── вывод ───
# [310 250 250 310]
# array([ 90, 120, 250, 310, 480])

# %% rows
table[[2, 0]]                       # строки 2 и 0
# ─── вывод ───
# array([[7, 8, 9],
#        [1, 2, 3]])

# %% pairs-vs-ix
print(table[[0, 2], [1, 2]])        # пары: (0, 1) и (2, 2)
table[np.ix_([0, 2], [1, 2])]       # подматрица: строки 0, 2 × столбцы 1, 2
# ─── вывод ───
# [2 9]
# array([[2, 3],
#        [8, 9]])

# %% assign
discounted = prices.copy()
discounted[[1, 3]] = 0
discounted
# ─── вывод ───
# array([250,   0, 480,   0, 310])

# %% copy
chosen = prices[[0, 1]]
chosen[0] = -1
prices                              # исходный массив не изменился
# ─── вывод ───
# array([250, 120, 480,  90, 310])

# %% repeated
counts = np.zeros(3, dtype=int)
counts[[0, 0, 2]] += 1              # индекс 0 дважды, но прибавится один раз
print(counts)
counts = np.zeros(3, dtype=int)
np.add.at(counts, [0, 0, 2], 1)     # каждое вхождение учитывается
counts
# ─── вывод ───
# [1 0 1]
# array([2, 0, 1])
