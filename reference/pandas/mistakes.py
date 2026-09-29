# Примеры к статье pandas/mistakes: для каждой ошибки — «неправильно» и «правильно».

# %% setup
sales = pd.DataFrame({
    "city": ["Омск", "Тула", None, "Омск"],
    "cups": [30, 12, 18, 25],
    "price": [180.0, None, 165.0, 190.0],
    "manager": ["Аня", "Борис", "Вика", "Аня"],
})

# %% chained-wrong [warns]
sales["cups"][0] = 100
sales["cups"].tolist()
# ─── вывод ───
# ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment.
# Such chained assignment never works to update the original DataFrame or Series, because the intermediate object on which we are setting values always behaves as a copy (due to Copy-on-Write).
#
# Try using '.loc[row_indexer, col_indexer] = value' instead, to perform the assignment in a single step.
#
# See the documentation for a more detailed explanation: https://pandas.pydata.org/pandas-docs/stable/user_guide/copy_on_write.html#chained-assignment
# [30, 12, 18, 25]

# %% chained-right
sales.loc[0, "cups"] = 100
sales["cups"].tolist()
# ─── вывод ───
# [100, 12, 18, 25]

# %% and-wrong [raises=ValueError]
sales[(sales["cups"] > 15) and (sales["city"] == "Омск")]
# ─── вывод ───
# ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().

# %% and-right
sales[(sales["cups"] > 15) & (sales["city"] == "Омск")]
# ─── вывод ───
#    city  cups  price manager
# 0  Омск    30  180.0     Аня
# 3  Омск    25  190.0     Аня

# %% assign-wrong
sales.drop(columns=["price"])
sales.columns.tolist()                 # столбец на месте: результат drop потерян
# ─── вывод ───
# ['city', 'cups', 'price', 'manager']

# %% assign-right
sales = sales.drop(columns=["price"])
sales.columns.tolist()
# ─── вывод ───
# ['city', 'cups', 'manager']

# %% position-wrong [raises=KeyError]
by_city = sales.set_index("cups")["city"]
by_city[0]                             # 0 — метка, а не позиция
# ─── вывод ───
# KeyError: 0

# %% position-right
by_city = sales.set_index("cups")["city"]
by_city.iloc[0]
# ─── вывод ───
# 'Омск'

# %% nan-wrong
sales[sales["price"] == np.nan]        # пусто
# ─── вывод ───
# Empty DataFrame
# Columns: [city, cups, price, manager]
# Index: []

# %% nan-right
sales[sales["price"].isna()]
# ─── вывод ───
#    city  cups  price manager
# 1  Тула    12    NaN   Борис

# %% dropna-wrong
sales.groupby("city")["cups"].sum().sum(), sales["cups"].sum()   # суммы не сходятся
# ─── вывод ───
# (np.int64(67), np.int64(85))

# %% dropna-right
sales.groupby("city", dropna=False)["cups"].sum()
# ─── вывод ───
# city
# Омск    55
# Тула    12
# NaN     18
# Name: cups, dtype: int64

# %% mean-wrong [raises=TypeError]
sales.groupby("city", dropna=False).mean()
# ─── вывод ───
# TypeError: dtype 'str' does not support operation 'mean'

# %% mean-right
sales.groupby("city", dropna=False)[["cups", "price"]].mean()
# ─── вывод ───
#       cups  price
# city
# Омск  27.5  185.0
# Тула  12.0    NaN
# NaN   18.0  165.0

# %% merge-wrong
cities = pd.DataFrame({"city": ["Омск", "Омск", "Тула"], "region": ["Сибирь", "Сибирь", "Центр"]})
len(sales), len(sales.merge(cities, on="city", how="left"))   # строк стало больше
# ─── вывод ───
# (4, 6)

# %% merge-right
cities = pd.DataFrame({"city": ["Омск", "Омск", "Тула"], "region": ["Сибирь", "Сибирь", "Центр"]})
sales.merge(cities.drop_duplicates("city"), on="city", how="left", validate="many_to_one")
# ─── вывод ───
#    city  cups  price manager  region
# 0  Омск    30  180.0     Аня  Сибирь
# 1  Тула    12    NaN   Борис   Центр
# 2   NaN    18  165.0    Вика     NaN
# 3  Омск    25  190.0     Аня  Сибирь

# %% dates-wrong
from pathlib import Path
Path("log.csv").write_text("day,visits\n2024-03-01,10\n2024-03-02,12\n")
pd.read_csv("log.csv").dtypes          # даты остались строками
# ─── вывод ───
# day         str
# visits    int64
# dtype: object

# %% dates-right
from pathlib import Path
Path("log.csv").write_text("day,visits\n2024-03-01,10\n2024-03-02,12\n")
pd.read_csv("log.csv", parse_dates=["day"]).dtypes
# ─── вывод ───
# day       datetime64[us]
# visits             int64
# dtype: object

# %% index-wrong
sales.to_csv("out.csv")
pd.read_csv("out.csv").columns.tolist()   # лишний столбец Unnamed: 0
# ─── вывод ───
# ['Unnamed: 0', 'city', 'cups', 'price', 'manager']

# %% index-right
sales.to_csv("out.csv", index=False)
pd.read_csv("out.csv").columns.tolist()
# ─── вывод ───
# ['city', 'cups', 'price', 'manager']
