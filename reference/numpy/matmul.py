# Примеры к статье numpy/matmul.

# %% setup
# цены 3 товаров в 2 магазинах и заказы: 2 покупателя × 3 товара
prices = np.array([[120, 110],
                   [ 80,  85],
                   [ 45,  40]])      # (3 товара, 2 магазина)
orders = np.array([[1, 2, 0],
                   [3, 0, 4]])       # (2 покупателя, 3 товара)

# %% matmul
orders @ prices                      # (2, 3) @ (3, 2) → (2, 2): стоимость заказа в каждом магазине
# ─── вывод ───
# array([[280, 280],
#        [540, 490]])

# %% star
a = np.array([[1, 2], [3, 4]])
print(a * a)                         # поэлементно
a @ a                                # матричное произведение
# ─── вывод ───
# [[ 1  4]
#  [ 9 16]]
# array([[ 7, 10],
#        [15, 22]])

# %% vector
v = np.array([1, 0, 2])
print(orders @ v)                    # матрица на вектор → вектор (2,)
v @ v                                # вектор на вектор → число (скалярное произведение)
# ─── вывод ───
# [ 1 11]
# np.int64(5)

# %% dot-outer
x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
print(np.dot(x, y), np.inner(x, y))  # скалярное произведение
np.outer(x, y)                       # все попарные произведения (3, 3)
# ─── вывод ───
# 32 32
# array([[ 4,  5,  6],
#        [ 8, 10, 12],
#        [12, 15, 18]])

# %% batch
batch = np.ones((10, 2, 3))          # 10 матриц 2 × 3
(batch @ prices).shape               # каждая умножается на prices
# ─── вывод ───
# (10, 2, 2)

# %% dot-vs-matmul
a = np.ones((2, 3, 4))
b = np.ones((2, 4, 5))
print((a @ b).shape)                 # попарно по первой оси
np.dot(a, b).shape                   # np.dot для 3D делает совсем другое
# ─── вывод ───
# (2, 3, 5)
# (2, 3, 2, 5)

# %% mismatch [raises=ValueError]
orders @ orders                      # (2, 3) @ (2, 3): 3 ≠ 2
# ─── вывод ───
# ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 2 is different from 3)

# %% scalar [raises=ValueError]
2 @ orders                           # на число умножают через *
# ─── вывод ───
# ValueError: matmul: Input operand 0 does not have enough dimensions (has 0, gufunc core with signature (n?,k),(k,m?)->(n?,m?) requires 1)
