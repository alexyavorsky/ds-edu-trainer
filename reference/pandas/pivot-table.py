# Примеры к статье pandas/pivot-table.

# %% setup
sales = pd.DataFrame({
    "city":  ["Омск", "Омск", "Тула", "Тула", "Омск", "Пермь", "Тула"],
    "drink": ["латте", "чай", "латте", "латте", "латте", "чай", "чай"],
    "month": ["янв", "янв", "янв", "фев", "фев", "фев", "фев"],
    "cups":  [30, 12, 18, 25, 20, 16, 9],
})

# %% basic
sales.pivot_table(values="cups", index="city", columns="drink", aggfunc="sum")
# ─── вывод ───
# drink  латте   чай
# city
# Омск    50.0  12.0
# Пермь    NaN  16.0
# Тула    43.0   9.0

# %% fill-margins
sales.pivot_table(values="cups", index="city", columns="drink",
                  aggfunc="sum", fill_value=0, margins=True, margins_name="Итого")
# ─── вывод ───
# drink  латте  чай  Итого
# city
# Омск      50   12     62
# Пермь      0   16     16
# Тула      43    9     52
# Итого     93   37    130

# %% two-index
sales.pivot_table(values="cups", index=["city", "month"], columns="drink", aggfunc="sum", fill_value=0)
# ─── вывод ───
# drink        латте  чай
# city  month
# Омск  фев       20    0
#       янв       30   12
# Пермь фев        0   16
# Тула  фев       25    9
#       янв       18    0

# %% several-funcs
sales.pivot_table(values="cups", index="city", aggfunc=["sum", "count"])
# ─── вывод ───
#        sum count
#       cups  cups
# city
# Омск    62     3
# Пермь   16     1
# Тула    52     3

# %% crosstab
pd.crosstab(sales["city"], sales["drink"])                       # сколько строк в каждой паре
# ─── вывод ───
# drink  латте  чай
# city
# Омск       2    1
# Пермь      0    1
# Тула       2    1

# %% crosstab-normalize
pd.crosstab(sales["city"], sales["drink"], normalize="index").round(2)   # доли по строкам
# ─── вывод ───
# drink  латте   чай
# city
# Омск    0.67  0.33
# Пермь   0.00  1.00
# Тула    0.67  0.33

# %% default-mean
sales.pivot_table(values="cups", index="city", columns="drink")  # без aggfunc — среднее!
# ─── вывод ───
# drink  латте   чай
# city
# Омск    25.0  12.0
# Пермь    NaN  16.0
# Тула    21.5   9.0
