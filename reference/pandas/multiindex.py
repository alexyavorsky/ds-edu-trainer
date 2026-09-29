# Примеры к статье pandas/multiindex.

# %% setup
sales = pd.DataFrame({
    "city":  ["Омск", "Омск", "Омск", "Тула", "Тула", "Сочи"],
    "month": ["янв", "фев", "мар", "янв", "фев", "янв"],
    "cups":  [120, 130, 110, 95, 105, 60],
    "rating": [4.5, 4.6, 4.4, 4.0, 4.1, 4.8],
}).set_index(["city", "month"])

# %% show
sales
# ─── вывод ───
#             cups  rating
# city month
# Омск янв     120     4.5
#      фев     130     4.6
#      мар     110     4.4
# Тула янв      95     4.0
#      фев     105     4.1
# Сочи янв      60     4.8

# %% outer
sales.loc["Омск"]                          # все строки внешнего уровня
# ─── вывод ───
#        cups  rating
# month
# янв     120     4.5
# фев     130     4.6
# мар     110     4.4

# %% tuple
sales.loc[("Тула", "фев"), "cups"]         # полная метка — кортеж
# ─── вывод ───
# np.int64(105)

# %% xs
sales.xs("янв", level="month")             # срез по внутреннему уровню
# ─── вывод ───
#       cups  rating
# city
# Омск   120     4.5
# Тула    95     4.0
# Сочи    60     4.8

# %% index-slice
idx = pd.IndexSlice
sales.sort_index().loc[idx[:, ["янв", "фев"]], "cups"]   # любые города, два месяца
# ─── вывод ───
# city  month
# Омск  янв      120
# Сочи  янв       60
# Тула  янв       95
# Омск  фев      130
# Тула  фев      105
# Name: cups, dtype: int64

# %% levels
print(sales.index.names)
sales.index.get_level_values("city").unique()
# ─── вывод ───
# ['city', 'month']
# Index(['Омск', 'Тула', 'Сочи'], dtype='str', name='city')

# %% swap-drop
print(sales.swaplevel().sort_index().head(3))
sales.droplevel("month").head(3)
# ─── вывод ───
#             cups  rating
# month city
# мар   Омск   110     4.4
# фев   Омск   130     4.6
#       Тула   105     4.1
#       cups  rating
# city
# Омск   120     4.5
# Омск   130     4.6
# Омск   110     4.4

# %% from-groupby
sales.groupby(level="city")["cups"].sum()  # группировка по уровню индекса
# ─── вывод ───
# city
# Омск    360
# Сочи     60
# Тула    200
# Name: cups, dtype: int64

# %% flat
sales.reset_index().head(3)                # обратно в обычные столбцы
# ─── вывод ───
#    city month  cups  rating
# 0  Омск   янв   120     4.5
# 1  Омск   фев   130     4.6
# 2  Омск   мар   110     4.4

# %% unsorted [raises=UnsortedIndexError]
sales.loc["Омск":"Тула"]                  # «Сочи» стоит после «Тулы» — индекс не отсортирован
# ─── вывод ───
# UnsortedIndexError: 'Key length (1) was greater than MultiIndex lexsort depth (0)'

# %% sorted
sales.sort_index().loc["Омск":"Тула"]
# ─── вывод ───
#             cups  rating
# city month
# Омск мар     110     4.4
#      фев     130     4.6
#      янв     120     4.5
# Сочи янв      60     4.8
# Тула фев     105     4.1
#      янв      95     4.0
