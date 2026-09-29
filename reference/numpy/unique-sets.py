# Примеры к статье numpy/unique-sets.

# %% setup
orders = np.array(["чай", "кофе", "чай", "сок", "кофе", "чай"])

# %% unique
np.unique(orders)                             # уникальные значения, отсортированные
# ─── вывод ───
# array(['кофе', 'сок', 'чай'], dtype='<U4')

# %% counts
values, counts = np.unique(orders, return_counts=True)
print(values)
print(counts)
values[counts.argmax()]                       # самое частое
# ─── вывод ───
# ['кофе' 'сок' 'чай']
# [2 1 3]
# np.str_('чай')

# %% inverse
values, codes = np.unique(orders, return_inverse=True)
print(codes)                                  # номер значения для каждого элемента
values[codes]                                 # восстановить исходный массив
# ─── вывод ───
# [2 0 2 1 0 2]
# array(['чай', 'кофе', 'чай', 'сок', 'кофе', 'чай'], dtype='<U4')

# %% array-api
print(np.unique_values(orders))
np.unique_counts(orders)
# ─── вывод ───
# ['кофе' 'сок' 'чай']
# UniqueCountsResult(values=array(['кофе', 'сок', 'чай'], dtype='<U4'), counts=array([2, 1, 3]))

# %% rows
pairs = np.array([[1, 2], [3, 4], [1, 2]])
np.unique(pairs, axis=0)                      # уникальные строки
# ─── вывод ───
# array([[1, 2],
#        [3, 4]])

# %% isin
menu = np.array(["чай", "кофе"])
print(np.isin(orders, menu))
orders[~np.isin(orders, menu)]                # заказы не из меню
# ─── вывод ───
# [ True  True  True False  True  True]
# array(['сок'], dtype='<U4')

# %% sets
a = np.array([1, 2, 3, 4])
b = np.array([3, 4, 5])
print(np.intersect1d(a, b))                   # в обоих
print(np.union1d(a, b))                       # хотя бы в одном
print(np.setdiff1d(a, b))                     # в a, но не в b
np.setxor1d(a, b)                             # ровно в одном
# ─── вывод ───
# [3 4]
# [1 2 3 4 5]
# [1 2]
# array([1, 2, 5])

# %% nan
np.unique(np.array([1.0, np.nan, 2.0, np.nan]))   # NaN схлопываются в один
# ─── вывод ───
# array([ 1.,  2., nan])

# %% in1d-removed [raises=AttributeError]
np.in1d(orders, menu)
# ─── вывод ───
# AttributeError: module 'numpy' has no attribute 'in1d'

# %% nan-separate
np.unique(np.array([1.0, np.nan, 2.0, np.nan]), equal_nan=False)
# ─── вывод ───
# array([ 1.,  2., nan, nan])
