# Примеры к статье pandas/alignment.

# %% setup
plan = pd.Series({"Омск": 100, "Тула": 80, "Сочи": 60})
fact = pd.Series({"Тула": 90, "Омск": 110, "Пермь": 40})

# %% arithmetic
fact - plan                          # по меткам, а не по позициям; порядок не важен
# ─── вывод ───
# Омск     10.0
# Пермь     NaN
# Сочи      NaN
# Тула     10.0
# dtype: float64

# %% fill-value
fact.sub(plan, fill_value=0)         # отсутствующая метка считается нулём
# ─── вывод ───
# Омск     10.0
# Пермь    40.0
# Сочи    -60.0
# Тула     10.0
# dtype: float64

# %% reindex
plan.reindex(["Омск", "Тула", "Пермь"])            # новый набор меток; новых нет — NaN
# ─── вывод ───
# Омск     100.0
# Тула      80.0
# Пермь      NaN
# dtype: float64

# %% reindex-fill
plan.reindex(["Омск", "Тула", "Пермь"], fill_value=0)
# ─── вывод ───
# Омск     100
# Тула      80
# Пермь      0
# dtype: int64

# %% align
a, b = plan.align(fact, join="inner")              # только общие метки
a, b
# ─── вывод ───
# (Омск    100
# Тула     80
# dtype: int64, Омск    110
# Тула     90
# dtype: int64)

# %% assign-column
df = pd.DataFrame({"plan": plan})
df["fact"] = fact                                   # новый столбец тоже выравнивается по индексу
df
# ─── вывод ───
#       plan   fact
# Омск   100  110.0
# Тула    80   90.0
# Сочи    60    NaN

# %% values
df = pd.DataFrame({"plan": plan})
df["fact"] = fact.to_numpy()[:3]                    # массив без индекса — по порядку позиций
df
# ─── вывод ───
#       plan  fact
# Омск   100    90
# Тула    80   110
# Сочи    60    40
