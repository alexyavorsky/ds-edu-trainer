# Примеры к статье numpy/attributes.

# %% basic
sales = np.array([[120, 80, 45, 60],
                  [100, 95, 50, 70],
                  [130, 85, 40, 65]])   # 3 магазина × 4 товара
print("shape:", sales.shape)
print("ndim:", sales.ndim)
print("size:", sales.size)
print("dtype:", sales.dtype)
print("len:", len(sales))
# ─── вывод ───
# shape: (3, 4)
# ndim: 2
# size: 12
# dtype: int64
# len: 3

# %% bytes
prices64 = np.zeros(1000)
prices32 = np.zeros(1000, dtype=np.float32)
print(prices64.itemsize, prices64.nbytes)
print(prices32.itemsize, prices32.nbytes)
# ─── вывод ───
# 8 8000
# 4 4000

# %% three-dims
week = np.zeros((7, 24, 3))   # дни × часы × датчики
week.shape, week.ndim, week.size
# ─── вывод ───
# ((7, 24, 3), 3, 504)

# %% shapes-differ
v = np.array([1, 2, 3])
print(v.shape, v.reshape(3, 1).shape, v.reshape(1, 3).shape)
# ─── вывод ───
# (3,) (3, 1) (1, 3)

# %% zero-dim [raises=TypeError]
x = np.array(5)
print(x.shape, x.ndim)
len(x)
# ─── вывод ───
# () 0
# TypeError: len() of unsized object
