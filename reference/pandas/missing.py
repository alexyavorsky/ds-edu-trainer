# Примеры к статье pandas/missing.

# %% setup
temps = pd.DataFrame({
    "city": ["Омск", "Тула", "Сочи", None],
    "mon": [12.0, None, 21.0, 8.0],
    "tue": [None, None, 22.5, 9.5],
})

# %% isna
print(temps.isna())
temps.isna().sum()                       # пропуски по столбцам
# ─── вывод ───
#     city    mon    tue
# 0  False  False   True
# 1  False   True   True
# 2  False  False  False
# 3   True  False  False
# city    1
# mon     1
# tue     2
# dtype: int64

# %% fillna
print(temps.fillna({"city": "?", "mon": 0}))   # по столбцам
temps["mon"].fillna(temps["mon"].mean())       # средним
# ─── вывод ───
#    city   mon   tue
# 0  Омск  12.0   NaN
# 1  Тула   0.0   NaN
# 2  Сочи  21.0  22.5
# 3     ?   8.0   9.5
# 0    12.000000
# 1    13.666667
# 2    21.000000
# 3     8.000000
# Name: mon, dtype: float64

# %% ffill
temps[["mon", "tue"]].ffill(axis=1)       # предыдущим значением в строке
# ─── вывод ───
#     mon   tue
# 0  12.0  12.0
# 1   NaN   NaN
# 2  21.0  22.5
# 3   8.0   9.5

# %% dropna
print(temps.dropna())                    # строки без единого пропуска
print(temps.dropna(subset=["city"]))     # пропуск только в city
temps.dropna(thresh=2)                   # хотя бы 2 непустых значения
# ─── вывод ───
#    city   mon   tue
# 2  Сочи  21.0  22.5
#    city   mon   tue
# 0  Омск  12.0   NaN
# 1  Тула   NaN   NaN
# 2  Сочи  21.0  22.5
#    city   mon   tue
# 0  Омск  12.0   NaN
# 2  Сочи  21.0  22.5
# 3   NaN   8.0   9.5

# %% interpolate
s = pd.Series([10.0, None, None, 16.0, None, 20.0])
s.interpolate()                          # линейно между соседями
# ─── вывод ───
# 0    10.0
# 1    12.0
# 2    14.0
# 3    16.0
# 4    18.0
# 5    20.0
# dtype: float64

# %% none-nan
print(pd.Series([1, None]).dtype)        # число + None → float64 с NaN
print(pd.Series(["a", None]).dtype)      # строка + None → str с NaN
pd.Series([1, None], dtype="Int64")      # целые с пропуском — pd.NA
# ─── вывод ───
# float64
# str
# 0       1
# 1    <NA>
# dtype: Int64

# %% nan-eq
temps["mon"] == np.nan                   # так пропуски не найти
# ─── вывод ───
# 0    False
# 1    False
# 2    False
# 3    False
# Name: mon, dtype: bool

# %% method-removed [raises=TypeError]
temps["mon"].fillna(method="ffill")
# ─── вывод ───
# TypeError: NDFrame.fillna() got an unexpected keyword argument 'method'
