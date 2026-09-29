# Примеры к статье pandas/dtypes.

# %% setup
raw = pd.DataFrame({
    "id": ["001", "002", "003"],
    "price": ["120.5", "95", "нет"],
    "qty": ["3", "10", "7"],
    "vip": ["True", "False", "True"],
})

# %% dtypes
raw.dtypes                                     # всё прочитано как строки
# ─── вывод ───
# id       str
# price    str
# qty      str
# vip      str
# dtype: object

# %% astype
typed = raw.astype({"qty": "int64"})
typed.dtypes
# ─── вывод ───
# id         str
# price      str
# qty      int64
# vip        str
# dtype: object

# %% to-numeric
pd.to_numeric(raw["price"], errors="coerce")   # «нет» → NaN вместо ошибки
# ─── вывод ───
# 0    120.5
# 1     95.0
# 2      NaN
# Name: price, dtype: float64

# %% astype-fails [raises=ValueError]
raw["price"].astype(float)
# ─── вывод ───
# ValueError: could not convert string to float: 'нет'

# %% nullable
counts = pd.Series([3, None, 5], dtype="Int64")
print(counts)
counts + 1                                     # пропуск остаётся пропуском, целые — целыми
# ─── вывод ───
# 0       3
# 1    <NA>
# 2       5
# dtype: Int64
# 0       4
# 1    <NA>
# 2       6
# dtype: Int64

# %% bool-trap
print(raw["vip"].astype(bool).tolist())        # непустая строка — всегда True
raw["vip"].map({"True": True, "False": False}).tolist()
# ─── вывод ───
# [True, True, True]
# [True, False, True]

# %% convert-dtypes
pd.DataFrame({"n": [1, None], "s": ["a", None]}).convert_dtypes().dtypes
# ─── вывод ───
# n     Int64
# s    string
# dtype: object

# %% keep-zeros
raw["id"].astype(int).tolist()                 # ведущие нули пропали — id лучше оставить строкой
# ─── вывод ───
# [1, 2, 3]

# %% str-setitem [raises=TypeError]
codes = pd.Series(["A1", "B2"])
codes[0] = 5                                   # в столбец str можно писать только строки
# ─── вывод ───
# TypeError: Invalid value '5' for dtype 'str'. Value should be a string or missing value, got 'int' instead.
