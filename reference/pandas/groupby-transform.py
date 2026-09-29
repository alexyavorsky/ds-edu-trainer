# Примеры к статье pandas/groupby-transform.

# %% setup
sales = pd.DataFrame({
    "city":  ["Омск", "Тула", "Омск", "Пермь", "Тула", "Омск"],
    "day":   [1, 1, 2, 2, 3, 3],
    "cups":  [30, 12, 18, 25, 20, 12],
    "rating": [4.5, 4.0, None, 4.8, 3.9, None],
})

# %% agg-vs-transform
print(sales.groupby("city")["cups"].sum())             # одна строка на группу
sales.groupby("city")["cups"].transform("sum")         # значение группы в каждой строке
# ─── вывод ───
# city
# Омск     60
# Пермь    25
# Тула     32
# Name: cups, dtype: int64
# 0    60
# 1    32
# 2    60
# 3    25
# 4    32
# 5    60
# Name: cups, dtype: int64

# %% share
sales.assign(share=sales["cups"] / sales.groupby("city")["cups"].transform("sum"))
# ─── вывод ───
#     city  day  cups  rating  share
# 0   Омск    1    30     4.5  0.500
# 1   Тула    1    12     4.0  0.375
# 2   Омск    2    18     NaN  0.300
# 3  Пермь    2    25     4.8  1.000
# 4   Тула    3    20     3.9  0.625
# 5   Омск    3    12     NaN  0.200

# %% fill
sales["rating"].fillna(sales.groupby("city")["rating"].transform("mean"))   # пропуск — средним по городу
# ─── вывод ───
# 0    4.5
# 1    4.0
# 2    4.5
# 3    4.8
# 4    3.9
# 5    4.5
# Name: rating, dtype: float64

# %% filter
sales.groupby("city").filter(lambda g: len(g) >= 2)    # только города с 2+ строками
# ─── вывод ───
#    city  day  cups  rating
# 0  Омск    1    30     4.5
# 1  Тула    1    12     4.0
# 2  Омск    2    18     NaN
# 4  Тула    3    20     3.9
# 5  Омск    3    12     NaN

# %% cumulative
sales.assign(
    n=sales.groupby("city").cumcount() + 1,            # номер строки в группе
    running=sales.groupby("city")["cups"].cumsum(),    # нарастающий итог в группе
    prev=sales.groupby("city")["cups"].shift(),        # предыдущее значение в группе
)
# ─── вывод ───
#     city  day  cups  rating  n  running  prev
# 0   Омск    1    30     4.5  1       30   NaN
# 1   Тула    1    12     4.0  1       12   NaN
# 2   Омск    2    18     NaN  2       48  30.0
# 3  Пермь    2    25     4.8  1       25   NaN
# 4   Тула    3    20     3.9  2       32  12.0
# 5   Омск    3    12     NaN  3       60  18.0

# %% apply
sales.groupby("city").apply(lambda g: g.nlargest(1, "cups"))   # лучший день каждого города
# ─── вывод ───
#          day  cups  rating
# city
# Омск  0    1    30     4.5
# Пермь 3    2    25     4.8
# Тула  4    3    20     3.9

# %% apply-columns
sales.groupby("city").apply(lambda g: list(g.columns)).iloc[0]   # в функцию не попадает ключ группировки
# ─── вывод ───
# ['day', 'cups', 'rating']
