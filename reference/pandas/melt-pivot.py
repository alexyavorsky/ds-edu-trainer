# Примеры к статье pandas/melt-pivot.

# %% setup
wide = pd.DataFrame({
    "city": ["Омск", "Тула"],
    "jan": [120, 95],
    "feb": [130, 105],
})

# %% melt
long = wide.melt(id_vars="city", var_name="month", value_name="cups")
long
# ─── вывод ───
#    city month  cups
# 0  Омск   jan   120
# 1  Тула   jan    95
# 2  Омск   feb   130
# 3  Тула   feb   105

# %% pivot
long = wide.melt(id_vars="city", var_name="month", value_name="cups")
long.pivot(index="city", columns="month", values="cups")
# ─── вывод ───
# month  feb  jan
# city
# Омск   130  120
# Тула   105   95

# %% value-vars
wide.melt(id_vars="city", value_vars=["feb"])    # только часть столбцов
# ─── вывод ───
#    city variable  value
# 0  Омск      feb    130
# 1  Тула      feb    105

# %% back-to-columns
long = wide.melt(id_vars="city", var_name="month", value_name="cups")
back = long.pivot(index="city", columns="month", values="cups").reset_index()
back.columns.name = None                          # убрать имя «month» над столбцами
back
# ─── вывод ───
#    city  feb  jan
# 0  Омск  130  120
# 1  Тула  105   95

# %% why-long
long = wide.melt(id_vars="city", var_name="month", value_name="cups")
long.groupby("month")["cups"].sum()               # длинный формат удобен для groupby и графиков
# ─── вывод ───
# month
# feb    235
# jan    215
# Name: cups, dtype: int64

# %% duplicates [raises=ValueError]
dup = pd.DataFrame({"city": ["Омск", "Омск"], "month": ["jan", "jan"], "cups": [120, 80]})
dup.pivot(index="city", columns="month", values="cups")   # два значения на одну ячейку
# ─── вывод ───
# ValueError: Index contains duplicate entries, cannot reshape

# %% pivot-table
dup = pd.DataFrame({"city": ["Омск", "Омск"], "month": ["jan", "jan"], "cups": [120, 80]})
dup.pivot_table(index="city", columns="month", values="cups", aggfunc="sum")
# ─── вывод ───
# month  jan
# city
# Омск   200
