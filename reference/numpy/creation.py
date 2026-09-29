# Примеры к статье numpy/creation.

# %% from-list
np.array([[1, 2, 3],
          [4, 5, 6]], dtype=float)
# ─── вывод ───
# array([[1., 2., 3.],
#        [4., 5., 6.]])

# %% filled
print(np.zeros(3))
print(np.ones((2, 3), dtype=int))
np.full((2, 2), 7)
# ─── вывод ───
# [0. 0. 0.]
# [[1 1 1]
#  [1 1 1]]
# array([[7, 7],
#        [7, 7]])

# %% arange
print(np.arange(5))
print(np.arange(2, 10, 3))       # stop не входит
np.arange(0, 1, 0.25)
# ─── вывод ───
# [0 1 2 3 4]
# [2 5 8]
# array([0.  , 0.25, 0.5 , 0.75])

# %% linspace
print(np.linspace(0, 1, 5))                   # 5 точек, конец входит
np.linspace(0, 1, 5, endpoint=False)
# ─── вывод ───
# [0.   0.25 0.5  0.75 1.  ]
# array([0. , 0.2, 0.4, 0.6, 0.8])

# %% eye
np.eye(3, dtype=int)
# ─── вывод ───
# array([[1, 0, 0],
#        [0, 1, 0],
#        [0, 0, 1]])

# %% like
temps = np.array([[12.5, 14.0], [9.0, 11.5]])
print(np.zeros_like(temps))
np.full_like(temps, np.nan)
# ─── вывод ───
# [[0. 0.]
#  [0. 0.]]
# array([[nan, nan],
#        [nan, nan]])

# %% arange-float
np.arange(1, 1.3, 0.1)           # ожидали 3 числа, а получили 4
# ─── вывод ───
# array([1. , 1.1, 1.2, 1.3])

# %% shape-tuple [raises=TypeError]
np.zeros(2, 3)                   # второй аргумент — это dtype
# ─── вывод ───
# TypeError: Cannot interpret '3' as a data type
