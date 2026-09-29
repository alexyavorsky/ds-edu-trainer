# Примеры к статье pandas/rank.

# %% setup
race = pd.DataFrame({
    "runner": ["Аня", "Борис", "Вика", "Глеб", "Дина"],
    "group": ["A", "B", "A", "B", "A"],
    "time": [52.1, 49.8, 52.1, 55.0, 50.3],      # меньше — лучше
})

# %% average
race["time"].rank()                     # у равных — средний ранг (3.5)
# ─── вывод ───
# 0    3.5
# 1    1.0
# 2    3.5
# 3    5.0
# 4    2.0
# Name: time, dtype: float64

# %% methods
pd.DataFrame({
    "time": race["time"],
    "average": race["time"].rank(),
    "min": race["time"].rank(method="min"),
    "dense": race["time"].rank(method="dense"),
    "first": race["time"].rank(method="first"),
})
# ─── вывод ───
#    time  average  min  dense  first
# 0  52.1      3.5  3.0    3.0    3.0
# 1  49.8      1.0  1.0    1.0    1.0
# 2  52.1      3.5  3.0    3.0    4.0
# 3  55.0      5.0  5.0    4.0    5.0
# 4  50.3      2.0  2.0    2.0    2.0

# %% descending
race.assign(place=race["time"].rank(method="min").astype(int)).sort_values("place")
# ─── вывод ───
#   runner group  time  place
# 1  Борис     B  49.8      1
# 4   Дина     A  50.3      2
# 0    Аня     A  52.1      3
# 2   Вика     A  52.1      3
# 3   Глеб     B  55.0      5

# %% pct
race["time"].rank(pct=True)             # доля участников не хуже
# ─── вывод ───
# 0    0.7
# 1    0.2
# 2    0.7
# 3    1.0
# 4    0.4
# Name: time, dtype: float64

# %% groups
race.assign(place_in_group=race.groupby("group")["time"].rank(method="min"))
# ─── вывод ───
#   runner group  time  place_in_group
# 0    Аня     A  52.1             2.0
# 1  Борис     B  49.8             1.0
# 2   Вика     A  52.1             2.0
# 3   Глеб     B  55.0             2.0
# 4   Дина     A  50.3             1.0

# %% float
race["time"].rank(method="min").dtype   # ранги — float, даже целые
# ─── вывод ───
# dtype('float64')
