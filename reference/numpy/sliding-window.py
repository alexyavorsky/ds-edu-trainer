# Примеры к статье numpy/sliding-window.

# %% setup
from numpy.lib.stride_tricks import sliding_window_view

visits = np.array([120.0, 135, 128, 150, 162, 158, 170])   # посетители по дням

# %% windows
sliding_window_view(visits, 3)          # все окна длины 3
# ─── вывод ───
# array([[120., 135., 128.],
#        [135., 128., 150.],
#        [128., 150., 162.],
#        [150., 162., 158.],
#        [162., 158., 170.]])

# %% moving-average
sliding_window_view(visits, 3).mean(axis=1).round(2)   # скользящее среднее
# ─── вывод ───
# array([127.67, 137.67, 146.67, 156.67, 163.33])

# %% moving-max
sliding_window_view(visits, 3).max(axis=1)             # максимум за 3 дня
# ─── вывод ───
# array([135., 150., 162., 162., 170.])

# %% step
sliding_window_view(visits, 3)[::2]                    # окна с шагом 2
# ─── вывод ───
# array([[120., 135., 128.],
#        [128., 150., 162.],
#        [162., 158., 170.]])

# %% two-dims
img = np.arange(16).reshape(4, 4)
patches = sliding_window_view(img, (2, 2))
print(patches.shape)                    # 3 × 3 окна размера 2 × 2
patches.max(axis=(-2, -1))              # максимум в каждом окне
# ─── вывод ───
# (3, 3, 2, 2)
# array([[ 5,  6,  7],
#        [ 9, 10, 11],
#        [13, 14, 15]])

# %% readonly [raises=ValueError]
w = sliding_window_view(visits, 3)
w[0, 0] = 0                             # окна пересекаются — запись запрещена
# ─── вывод ───
# ValueError: assignment destination is read-only

# %% cumsum-average
c = np.cumsum(np.insert(visits, 0, 0))
((c[3:] - c[:-3]) / 3).round(2)         # то же скользящее среднее за O(n)
# ─── вывод ───
# array([127.67, 137.67, 146.67, 156.67, 163.33])
