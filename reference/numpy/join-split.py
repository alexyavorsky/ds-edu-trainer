# Примеры к статье numpy/join-split.

# %% setup
jan = np.array([[5, 3],
                [2, 7]])       # продажи за январь: 2 магазина × 2 товара
feb = np.array([[4, 6],
                [1, 8]])

# %% concatenate
print(np.concatenate([jan, feb]))           # по строкам (axis=0)
np.concatenate([jan, feb], axis=1)          # по столбцам
# ─── вывод ───
# [[5 3]
#  [2 7]
#  [4 6]
#  [1 8]]
# array([[5, 3, 4, 6],
#        [2, 7, 1, 8]])

# %% stack
both = np.stack([jan, feb])                 # новая ось: месяцы × магазины × товары
print(both.shape)
np.stack([jan, feb], axis=-1).shape
# ─── вывод ───
# (2, 2, 2)
# (2, 2, 2)

# %% vstack-hstack
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(np.vstack([a, b]))                    # векторы как строки
print(np.hstack([a, b]))                    # подряд
np.column_stack([a, b])                     # векторы как столбцы
# ─── вывод ───
# [[1 2 3]
#  [4 5 6]]
# [1 2 3 4 5 6]
# array([[1, 4],
#        [2, 5],
#        [3, 6]])

# %% split
data = np.arange(9)
print(np.split(data, 3))                    # на 3 равные части
np.split(data, [2, 5])                      # по индексам: [:2], [2:5], [5:]
# ─── вывод ───
# [array([0, 1, 2]), array([3, 4, 5]), array([6, 7, 8])]
# [array([0, 1]), array([2, 3, 4]), array([5, 6, 7, 8])]

# %% array-split
np.array_split(np.arange(7), 3)             # части могут быть неравными
# ─── вывод ───
# [array([0, 1, 2]), array([3, 4]), array([5, 6])]

# %% split-unequal [raises=ValueError]
np.split(np.arange(7), 3)
# ─── вывод ───
# ValueError: array split does not result in an equal division

# %% mismatch [raises=ValueError]
np.concatenate([jan, np.array([[1, 2, 3]])])
# ─── вывод ───
# ValueError: all the input array dimensions except for the concatenation axis must match exactly, but along dimension 1, the array at index 0 has size 2 and the array at index 1 has size 3

# %% row-stack [raises=AttributeError]
np.row_stack([jan, feb])
# ─── вывод ───
# AttributeError: module 'numpy' has no attribute 'row_stack'
