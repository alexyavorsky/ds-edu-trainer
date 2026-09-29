# Примеры к статье pandas/dataframe.

# %% from-dict
pd.DataFrame({
    "product": ["чай", "кофе", "сок"],
    "price": [120, 180, 95],
    "in_stock": [True, False, True],
})
# ─── вывод ───
#   product  price  in_stock
# 0     чай    120      True
# 1    кофе    180     False
# 2     сок     95      True

# %% from-records
rows = [
    {"name": "Аня", "age": 21},
    {"name": "Борис", "age": 19, "city": "Тула"},   # лишний ключ
]
pd.DataFrame(rows)                                  # недостающие значения — NaN
# ─── вывод ───
#     name  age  city
# 0    Аня   21   NaN
# 1  Борис   19  Тула

# %% from-array
pd.DataFrame(np.arange(6).reshape(2, 3), columns=["a", "b", "c"], index=["x", "y"])
# ─── вывод ───
#    a  b  c
# x  0  1  2
# y  3  4  5

# %% index
pd.DataFrame({"price": [120, 180]}, index=["чай", "кофе"])
# ─── вывод ───
#       price
# чай     120
# кофе    180

# %% from-series
price = pd.Series({"чай": 120, "кофе": 180})
stock = pd.Series({"кофе": 3, "чай": 10, "сок": 5})
pd.DataFrame({"price": price, "stock": stock})      # строки выравниваются по индексу
# ─── вывод ───
#       price  stock
# кофе  180.0      3
# сок     NaN      5
# чай   120.0     10

# %% parts
df = pd.DataFrame({"price": [120, 180], "qty": [3, 1]}, index=["чай", "кофе"])
print(df.shape)
print(df.columns)
print(df.index)
df.dtypes
# ─── вывод ───
# (2, 2)
# Index(['price', 'qty'], dtype='str')
# Index(['чай', 'кофе'], dtype='str')
# price    int64
# qty      int64
# dtype: object

# %% lengths [raises=ValueError]
pd.DataFrame({"a": [1, 2, 3], "b": [1, 2]})
# ─── вывод ───
# ValueError: All arrays must be of the same length
