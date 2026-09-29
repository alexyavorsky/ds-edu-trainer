# Примеры к статье numpy/einsum.

# %% setup
A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])
v = np.array([1, 10])

# %% sums
print(np.einsum("ij->", A))        # сумма всех элементов
print(np.einsum("ij->j", A))       # сумма по строкам: для каждого столбца
np.einsum("ij->i", A)              # для каждой строки
# ─── вывод ───
# 10
# [4 6]
# array([3, 7])

# %% transpose-trace
print(np.einsum("ij->ji", A))      # транспонирование
np.einsum("ii->", A)               # след: сумма диагонали
# ─── вывод ───
# [[1 3]
#  [2 4]]
# np.int64(5)

# %% products
print(np.einsum("ij,jk->ik", A, B))   # матричное произведение, как A @ B
print(np.einsum("ij,j->i", A, v))     # матрица на вектор
np.einsum("i,i->", v, v)              # скалярное произведение
# ─── вывод ───
# [[19 22]
#  [43 50]]
# [21 43]
# np.int64(101)

# %% elementwise
print(np.einsum("ij,ij->ij", A, B))   # поэлементно, как A * B
np.einsum("ij,ij->i", A, B)           # построчное скалярное произведение
# ─── вывод ───
# [[ 5 12]
#  [21 32]]
# array([17, 53])

# %% batch
batch_a = np.ones((5, 2, 3))
batch_b = np.ones((5, 3, 4))
np.einsum("bij,bjk->bik", batch_a, batch_b).shape   # пачка матриц
# ─── вывод ───
# (5, 2, 4)

# %% outer
np.einsum("i,j->ij", v, v)            # внешнее произведение
# ─── вывод ───
# array([[  1,  10],
#        [ 10, 100]])

# %% mismatch [raises=ValueError]
np.einsum("ij,jk->ik", A, np.ones((3, 2)))   # j = 2 и j = 3 не совпадают
# ─── вывод ───
# ValueError: operands could not be broadcast together with remapped shapes [original->remapped]: (2,2)->(2,newaxis,2) (3,2)->(2,3)
