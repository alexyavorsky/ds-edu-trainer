# Примеры к статье pandas/cut-qcut.

# %% setup
ages = pd.Series([17, 23, 35, 41, 18, 52, 67, 29, 30, 45], name="age")

# %% cut
pd.cut(ages, bins=[0, 18, 30, 50, 100])          # интервалы (a, b]: правая граница входит
# ─── вывод ───
# 0      (0, 18]
# 1     (18, 30]
# 2     (30, 50]
# 3     (30, 50]
# 4      (0, 18]
# 5    (50, 100]
# 6    (50, 100]
# 7     (18, 30]
# 8     (18, 30]
# 9     (30, 50]
# Name: age, dtype: category
# Categories (4, interval[int64, right]): [(0, 18] < (18, 30] < (30, 50] < (50, 100]]

# %% labels
groups = pd.cut(ages, bins=[0, 18, 30, 50, 100], labels=["до 18", "18–30", "30–50", "50+"])
groups.value_counts(sort=False)
# ─── вывод ───
# age
# до 18    2
# 18–30    3
# 30–50    3
# 50+      2
# Name: count, dtype: int64

# %% right
pd.cut(ages, bins=[0, 18, 30, 50, 100], right=False).value_counts(sort=False)   # [a, b)
# ─── вывод ───
# age
# [0, 18)      1
# [18, 30)     3
# [30, 50)     4
# [50, 100)    2
# Name: count, dtype: int64

# %% equal-width
pd.cut(ages, bins=3)                              # 3 интервала одинаковой ширины
# ─── вывод ───
# 0     (16.95, 33.667]
# 1     (16.95, 33.667]
# 2    (33.667, 50.333]
# 3    (33.667, 50.333]
# 4     (16.95, 33.667]
# 5      (50.333, 67.0]
# 6      (50.333, 67.0]
# 7     (16.95, 33.667]
# 8     (16.95, 33.667]
# 9    (33.667, 50.333]
# Name: age, dtype: category
# Categories (3, interval[float64, right]): [(16.95, 33.667] < (33.667, 50.333] < (50.333, 67.0]]

# %% qcut
pd.qcut(ages, q=4, labels=["Q1", "Q2", "Q3", "Q4"]).value_counts(sort=False)   # примерно поровну в каждой
# ─── вывод ───
# age
# Q1    3
# Q2    2
# Q3    2
# Q4    3
# Name: count, dtype: int64

# %% bins-out
edges = pd.qcut(ages, q=4, retbins=True)[1]
edges                                             # границы квартилей
# ─── вывод ───
# array([17. , 24.5, 32.5, 44. , 67. ])

# %% outside
pd.cut(pd.Series([5, 150]), bins=[0, 18, 100])    # значение вне интервалов → NaN
# ─── вывод ───
# 0    (0.0, 18.0]
# 1            NaN
# dtype: category
# Categories (2, interval[int64, right]): [(0, 18] < (18, 100]]

# %% qcut-duplicates [raises=ValueError]
pd.qcut(pd.Series([1, 1, 1, 1, 2, 3]), q=4)       # границы квантилей совпадают
# ─── вывод ───
# ValueError: Bin edges must be unique: Index([1.0, 1.0, 1.0, 1.75, 3.0], dtype='float64').
# You can drop duplicate edges by setting the 'duplicates' kwarg
