# Примеры к статье pandas/intro.

# %% setup
sales = pd.DataFrame({
    "city": ["Омск", "Тула", "Сочи"],
    "cups": [120, 85, 240],
    "price": [180.0, 165.0, 210.0],
})

# %% series
temps = pd.Series([12.5, 9.0, 21.3], index=["Омск", "Тула", "Сочи"])
temps
# ─── вывод ───
# Омск    12.5
# Тула     9.0
# Сочи    21.3
# dtype: float64

# %% dataframe
sales
# ─── вывод ───
#    city  cups  price
# 0  Омск   120  180.0
# 1  Тула    85  165.0
# 2  Сочи   240  210.0

# %% column
col = sales["cups"]
print(type(col))
col
# ─── вывод ───
# <class 'pandas.Series'>
# 0    120
# 1     85
# 2    240
# Name: cups, dtype: int64

# %% vectorized
sales["revenue"] = sales["cups"] * sales["price"]   # столбец целиком, без цикла
sales
# ─── вывод ───
#    city  cups  price  revenue
# 0  Омск   120  180.0  21600.0
# 1  Тула    85  165.0  14025.0
# 2  Сочи   240  210.0  50400.0

# %% numpy
sales["cups"].to_numpy()                             # данные столбца — массив NumPy
# ─── вывод ───
# array([120,  85, 240])

# %% version
pd.__version__
# ─── вывод ───
# '3.0.6'

# %% str-dtype
names = pd.Series(["Аня", "Борис"])
print(names.dtype)
names.dtype == object          # старая проверка «строковый ли столбец» больше не работает
# ─── вывод ───
# str
# False
