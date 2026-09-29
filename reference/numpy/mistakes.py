# Примеры к статье numpy/mistakes: для каждой ошибки — «неправильно» и «правильно».

# %% setup
a = np.array([1, 2, 3])
b = np.array([1, 2, 3])
temps = np.array([3.0, -2.0, np.nan, 8.0])

# %% eq-wrong [raises=ValueError]
if a == b:
    print("равны")
# ─── вывод ───
# ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

# %% eq-right
if np.array_equal(a, b):
    print("равны")
# ─── вывод ───
# равны

# %% and-wrong [raises=ValueError]
temps[(temps > 0) and (temps < 5)]
# ─── вывод ───
# ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()

# %% and-right
temps[(temps > 0) & (temps < 5)]
# ─── вывод ───
# array([3.])

# %% view-wrong
first_two = a[:2]
first_two[0] = 100           # хотели изменить только копию
a
# ─── вывод ───
# array([100,   2,   3])

# %% view-right
first_two = a[:2].copy()
first_two[0] = 100
a
# ─── вывод ───
# array([1, 2, 3])

# %% sort-wrong
result = a.sort()
print(result)
# ─── вывод ───
# None

# %% sort-right
result = np.sort(np.array([3, 1, 2]))
result
# ─── вывод ───
# array([1, 2, 3])

# %% nan-wrong
temps[temps == np.nan]       # пусто: NaN не равен ничему
# ─── вывод ───
# array([], dtype=float64)

# %% nan-right
temps[np.isnan(temps)]
# ─── вывод ───
# array([nan])

# %% overflow-wrong
pixels = np.array([200, 100], dtype=np.uint8)
pixels + 100                 # 300 не помещается в uint8
# ─── вывод ───
# array([ 44, 200], dtype=uint8)

# %% overflow-right
pixels = np.array([200, 100], dtype=np.uint8)
pixels.astype(np.int64) + 100
# ─── вывод ───
# array([300, 200])

# %% keepdims-wrong
m = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0],
              [7.0, 8.0, 9.0]])
m - m.mean(axis=1)           # ошибки нет, но вычтено по столбцам
# ─── вывод ───
# array([[-1., -3., -5.],
#        [ 2.,  0., -2.],
#        [ 5.,  3.,  1.]])

# %% keepdims-right
m = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0],
              [7.0, 8.0, 9.0]])
m - m.mean(axis=1, keepdims=True)
# ─── вывод ───
# array([[-1.,  0.,  1.],
#        [-1.,  0.,  1.],
#        [-1.,  0.,  1.]])

# %% int-wrong
counts = np.array([1, 2, 3])
counts[0] = 2.7              # дробная часть молча отброшена
counts
# ─── вывод ───
# array([2, 2, 3])

# %% int-right
counts = np.array([1, 2, 3], dtype=float)
counts[0] = 2.7
counts
# ─── вывод ───
# array([2.7, 2. , 3. ])

# %% shape-wrong [raises=TypeError]
np.zeros(2, 3)
# ─── вывод ───
# TypeError: Cannot interpret '3' as a data type

# %% shape-right
np.zeros((2, 3))
# ─── вывод ───
# array([[0., 0., 0.],
#        [0., 0., 0.]])

# %% math-wrong [raises=TypeError]
import math
math.sqrt(np.array([4.0, 9.0]))
# ─── вывод ───
# TypeError: only 0-dimensional arrays can be converted to Python scalars

# %% math-right
np.sqrt(np.array([4.0, 9.0]))
# ─── вывод ───
# array([2., 3.])

# %% std-wrong
np.std(np.array([2.0, 4.0, 6.0]))            # ddof=0, а pandas даст другое число
# ─── вывод ───
# np.float64(1.632993161855452)

# %% std-right
np.std(np.array([2.0, 4.0, 6.0]), ddof=1)    # как Series.std() в pandas
# ─── вывод ───
# np.float64(2.0)
