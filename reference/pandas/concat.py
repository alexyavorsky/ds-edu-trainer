# Примеры к статье pandas/concat.

# %% setup
jan = pd.DataFrame({"city": ["Омск", "Тула"], "cups": [120, 95]})
feb = pd.DataFrame({"city": ["Омск", "Сочи"], "cups": [130, 60]})

# %% rows
pd.concat([jan, feb])                          # индекс повторяется
# ─── вывод ───
#    city  cups
# 0  Омск   120
# 1  Тула    95
# 0  Омск   130
# 1  Сочи    60

# %% ignore-index
pd.concat([jan, feb], ignore_index=True)
# ─── вывод ───
#    city  cups
# 0  Омск   120
# 1  Тула    95
# 2  Омск   130
# 3  Сочи    60

# %% keys
pd.concat([jan, feb], keys=["янв", "фев"])     # откуда строка — во внешнем уровне индекса
# ─── вывод ───
#        city  cups
# янв 0  Омск   120
#     1  Тула    95
# фев 0  Омск   130
#     1  Сочи    60

# %% columns-differ
extra = pd.DataFrame({"city": ["Пермь"], "rating": [4.7]})
pd.concat([jan, extra], ignore_index=True)     # недостающие столбцы — NaN
# ─── вывод ───
#     city   cups  rating
# 0   Омск  120.0     NaN
# 1   Тула   95.0     NaN
# 2  Пермь    NaN     4.7

# %% join-inner
extra = pd.DataFrame({"city": ["Пермь"], "rating": [4.7]})
pd.concat([jan, extra], join="inner", ignore_index=True)   # только общие столбцы
# ─── вывод ───
#     city
# 0   Омск
# 1   Тула
# 2  Пермь

# %% axis1
prices = pd.DataFrame({"price": [180, 165]})
pd.concat([jan, prices], axis=1)               # рядом; строки сопоставляются по индексу
# ─── вывод ───
#    city  cups  price
# 0  Омск   120    180
# 1  Тула    95    165

# %% loop
parts = []
for month, cups in [("янв", 120), ("фев", 130), ("мар", 110)]:
    parts.append(pd.DataFrame({"month": [month], "cups": [cups]}))
pd.concat(parts, ignore_index=True)            # собрать части в список и склеить один раз
# ─── вывод ───
#   month  cups
# 0   янв   120
# 1   фев   130
# 2   мар   110

# %% append-removed [raises=AttributeError]
jan.append(feb)
# ─── вывод ───
# AttributeError: 'DataFrame' object has no attribute 'append'
