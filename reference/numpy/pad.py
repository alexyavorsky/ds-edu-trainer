# Примеры к статье numpy/pad.

# %% setup
signal = np.array([3, 5, 4])

# %% constant
print(np.pad(signal, 2))                      # по 2 нуля с каждой стороны
np.pad(signal, (1, 3), constant_values=-1)    # слева 1, справа 3
# ─── вывод ───
# [0 0 3 5 4 0 0]
# array([-1,  3,  5,  4, -1, -1, -1])

# %% modes
print(np.pad(signal, 2, mode="edge"))         # повторить край
print(np.pad(signal, 2, mode="reflect"))      # зеркально, без края
np.pad(signal, 2, mode="wrap")                # по кругу
# ─── вывод ───
# [3 3 3 5 4 4 4]
# [4 5 3 5 4 5 3]
# array([5, 4, 3, 5, 4, 3, 5])

# %% two-dims
img = np.array([[1, 2],
                [3, 4]])
print(np.pad(img, 1))                         # рамка из нулей
np.pad(img, ((0, 1), (2, 0)))                 # снизу 1 строка, слева 2 столбца
# ─── вывод ───
# [[0 0 0 0]
#  [0 1 2 0]
#  [0 3 4 0]
#  [0 0 0 0]]
# array([[0, 0, 1, 2],
#        [0, 0, 3, 4],
#        [0, 0, 0, 0]])

# %% moving-average
padded = np.pad(signal, 1, mode="edge")
(padded[:-2] + padded[1:-1] + padded[2:]) / 3   # среднее по 3 точкам той же длины
# ─── вывод ───
# array([3.66666667, 4.        , 4.33333333])

# %% dtype
np.pad(np.array([1, 2]), 1, constant_values=0.5)   # 0.5 в целом массиве станет 0
# ─── вывод ───
# array([0, 1, 2, 0])
