# Примеры к статье numpy/histogram.

# %% setup
ages = np.array([23, 35, 41, 29, 52, 38, 61, 27, 45, 33, 30, 58])

# %% histogram
counts, edges = np.histogram(ages, bins=4)   # 4 интервала одинаковой ширины
print(counts)
edges
# ─── вывод ───
# [4 4 1 3]
# array([23. , 32.5, 42. , 51.5, 61. ])

# %% bins-list
counts, edges = np.histogram(ages, bins=[20, 30, 40, 50, 70])   # свои границы
counts
# ─── вывод ───
# array([3, 4, 2, 3])

# %% last-closed
np.histogram(np.array([10, 20, 30]), bins=[10, 20, 30])   # 30 попало в последний интервал
# ─── вывод ───
# (array([1, 2]), array([10, 20, 30]))

# %% density
counts, edges = np.histogram(ages, bins=[20, 40, 70], density=True)
counts * np.diff(edges)                                    # доли; в сумме 1
# ─── вывод ───
# array([0.58333333, 0.41666667])

# %% bincount
rolls = np.array([3, 1, 3, 6, 2, 3, 6])
print(np.bincount(rolls))                  # сколько раз каждое число 0, 1, 2, …
np.bincount(rolls, minlength=8)
# ─── вывод ───
# [0 1 1 3 0 0 2]
# array([0, 1, 1, 3, 0, 0, 2, 0])

# %% bincount-weights
store = np.array([0, 1, 0, 2, 1])          # номер магазина каждой продажи
amount = np.array([100, 250, 80, 40, 60])
np.bincount(store, weights=amount)         # сумма продаж по магазинам
# ─── вывод ───
# array([180., 310.,  40.])

# %% digitize
np.digitize(ages, bins=[30, 45, 60])       # номер группы: 0 — до 30, 1 — 30–44, …
# ─── вывод ───
# array([0, 1, 1, 0, 2, 1, 3, 0, 2, 1, 1, 2])

# %% bincount-float [raises=TypeError]
np.bincount(np.array([1.0, 2.0]))
# ─── вывод ───
# TypeError: Cannot cast array data from dtype('float64') to dtype('int64') according to the rule 'safe'
