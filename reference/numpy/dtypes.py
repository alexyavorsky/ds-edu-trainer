# Примеры к статье numpy/dtypes.

# %% inferred
for data in ([1, 2, 3], [1.0, 2], [True, False], ["да", "нет"]):
    print(np.array(data).dtype)
# ─── вывод ───
# int64
# float64
# bool
# <U3

# %% astype
prices = np.array([19.99, 5.5, -2.7])
print(prices.astype(int))        # дробная часть отбрасывается, к нулю
print(prices.astype(np.float32))
np.array(["1.5", "2", "-3"]).astype(float)
# ─── вывод ───
# [19  5 -2]
# [19.99  5.5  -2.7 ]
# array([ 1.5,  2. , -3. ])

# %% overflow
level = np.array([120, 127], dtype=np.int8)
level + 10                       # вышли за 127 — значения «перевернулись»
# ─── вывод ───
# array([-126, -119], dtype=int8)

# %% limits
print(np.iinfo(np.int8).min, np.iinfo(np.int8).max)
print(np.iinfo(np.int64).max)
np.finfo(np.float32).eps
# ─── вывод ───
# -128 127
# 9223372036854775807
# np.float32(1.1920929e-07)

# %% assign-truncates
counts = np.array([1, 2, 3])
counts[0] = 9.9                  # массив целый — дробь отброшена
counts
# ─── вывод ───
# array([9, 2, 3])

# %% nan-int [raises=ValueError]
counts = np.array([1, 2, 3])
counts[0] = np.nan
# ─── вывод ───
# ValueError: cannot convert float NaN to integer

# %% nep50-scalar
x = np.float32(3) + 3.0
x.dtype
# ─── вывод ───
# dtype('float32')

# %% nep50-overflow [raises=OverflowError]
np.array([100], dtype=np.int8) + 200
# ─── вывод ───
# OverflowError: Python integer 200 out of bounds for int8
