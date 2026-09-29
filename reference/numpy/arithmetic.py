# Примеры к статье numpy/arithmetic.

# %% setup
price = np.array([120.0, 80.0, 45.0])   # цена за штуку
qty = np.array([3, 10, 4])              # количество

# %% elementwise
print(price * qty)       # стоимость каждой позиции
print(price + 5)         # с числом — к каждому элементу
qty ** 2
# ─── вывод ───
# [360. 800. 180.]
# [125.  85.  50.]
# array([  9, 100,  16])

# %% division
a = np.array([7, -7, 8])
print(a / 2)             # всегда float
print(a // 2)            # деление с округлением вниз, как в Python
a % 3                    # остаток того же знака, что делитель
# ─── вывод ───
# [ 3.5 -3.5  4. ]
# [ 3 -4  4]
# array([1, 2, 2])

# %% new-array
total = price * qty
total[0] = 0
price                    # операция создала новый массив, price не изменился
# ─── вывод ───
# array([120.,  80.,  45.])

# %% zero-division [warns]
np.array([1.0, -1.0, 0.0]) / 0
# ─── вывод ───
# RuntimeWarning: divide by zero encountered in divide
# RuntimeWarning: invalid value encountered in divide
# array([ inf, -inf,  nan])

# %% int-zero [warns]
np.array([5, 7]) // 0    # у целых нет inf — получается 0 и предупреждение
# ─── вывод ───
# RuntimeWarning: divide by zero encountered in floor_divide
# array([0, 0])

# %% negative-power [raises=ValueError]
np.array([2, 4]) ** -1   # целое в отрицательной степени
# ─── вывод ───
# ValueError: Integers to negative integer powers are not allowed.

# %% shapes [raises=ValueError]
price + np.array([1, 2])
# ─── вывод ───
# ValueError: operands could not be broadcast together with shapes (3,) (2,)
