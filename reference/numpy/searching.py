# Примеры к статье numpy/searching.

# %% setup
limits = np.array([0, 1000, 5000, 20000])      # границы тарифов, по возрастанию
scores = np.array([72, 45, 90, 58, 81, 39, 66]) # баллы участников

# %% searchsorted
np.searchsorted(limits, 3000)                  # куда вставить, чтобы порядок сохранился
# ─── вывод ───
# np.int64(2)

# %% side
print(np.searchsorted(limits, 5000))                  # слева от равного
np.searchsorted(limits, 5000, side="right")           # справа от равного
# ─── вывод ───
# 2
# np.int64(3)

# %% many
spend = np.array([500, 1000, 7500, 25000])
np.searchsorted(limits, spend, side="right") - 1      # номер тарифа для каждой суммы
# ─── вывод ───
# array([0, 1, 2, 3])

# %% insert
sorted_prices = np.array([90, 120, 250, 480])
pos = np.searchsorted(sorted_prices, 200)
np.insert(sorted_prices, pos, 200)
# ─── вывод ───
# array([ 90, 120, 200, 250, 480])

# %% partition
print(np.partition(scores, 2))                 # 2 наименьших слева, порядок частей не гарантирован
np.partition(scores, -3)[-3:]                  # 3 наибольших
# ─── вывод ───
# [39 45 58 90 81 72 66]
# array([72, 81, 90])

# %% top-k
idx = np.argpartition(scores, -3)[-3:]         # индексы трёх лучших…
idx[np.argsort(scores[idx])[::-1]]             # …упорядоченные по убыванию баллов
# ─── вывод ───
# array([2, 4, 0])

# %% unsorted
np.searchsorted(np.array([5, 1, 3]), 2)        # массив не отсортирован — ответ бессмысленный
# ─── вывод ───
# np.int64(2)
