# Примеры к статье pandas/performance.

# %% setup
rng = np.random.default_rng(0)
n = 100_000
orders = pd.DataFrame({
    "city": rng.choice(["Москва", "Санкт-Петербург", "Казань", "Омск"], size=n),
    "qty": rng.integers(1, 20, size=n),
    "price": rng.uniform(100, 500, size=n).round(2),
})

# %% memory
usage = orders.memory_usage(deep=True, index=False)   # байты по столбцам
(usage / 2**20).round(1)                               # в мегабайтах
# ─── вывод ───
# city     2.2
# qty      0.8
# price    0.8
# dtype: float64

# %% deep
text = orders["city"]                                  # тип str
obj = text.astype(object)                              # те же строки как объекты Python
print(text.memory_usage(index=False) == text.memory_usage(deep=True, index=False))
obj.memory_usage(index=False) < obj.memory_usage(deep=True, index=False)   # без deep — только ссылки
# ─── вывод ───
# True
# True

# %% category
before = orders["city"].memory_usage(deep=True, index=False)
after = orders["city"].astype("category").memory_usage(deep=True, index=False)
before // after                                        # во сколько раз меньше: категории хранятся один раз
# ─── вывод ───
# 23

# %% downcast
small = pd.to_numeric(orders["qty"], downcast="integer")
print(small.dtype)                                     # хватит int8: значения до 20
orders["qty"].nbytes // small.nbytes                   # 8 байт на число → 1 байт
# ─── вывод ───
# int8
# 8

# %% vectorized [timing=2026-09-29, machine=Apple M4 · macOS · Python 3.14]
import timeit
t_apply = min(timeit.repeat(lambda: orders.apply(lambda r: r["qty"] * r["price"], axis=1), number=1, repeat=3))
t_vector = min(timeit.repeat(lambda: orders["qty"] * orders["price"], number=1, repeat=3))
print(f"apply: {t_apply * 1000:.0f} мс, столбцы: {t_vector * 1000:.2f} мс")
print(f"ускорение: ×{t_apply / t_vector:.0f}")         # разница — на порядки
# ─── вывод ───
# apply: 167 мс, столбцы: 0.07 мс
# ускорение: ×2431

# %% usecols
orders.to_csv("orders.csv", index=False)
pd.read_csv("orders.csv", usecols=["city", "qty"], dtype={"city": "category"}).dtypes
# ─── вывод ───
# city    category
# qty        int64
# dtype: object

# %% arrow
orders.head(3).convert_dtypes(dtype_backend="pyarrow").dtypes   # типы на основе Apache Arrow
# ─── вывод ───
# city     string[pyarrow]
# qty       int64[pyarrow]
# price    double[pyarrow]
# dtype: object

# %% eval
orders.eval("revenue = qty * price").head(3)           # выражение строкой
# ─── вывод ───
#      city  qty   price  revenue
# 0    Омск    9  342.80  3085.20
# 1  Казань   11  185.02  2035.22
# 2  Казань    3  322.50   967.50

# %% overflow
small = pd.Series([100, 120], dtype="int8")
print(small + 100)                                     # 200 и 220 не помещаются в int8
small.astype("int64") + 100
# ─── вывод ───
# 0   -56
# 1   -36
# dtype: int8
# 0    200
# 1    220
# dtype: int64
