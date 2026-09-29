# Примеры к статье pandas/apply.

# %% setup
import timeit

orders = pd.DataFrame({
    "size": ["S", "M", "L", "M"],
    "price": [150, 180, 210, 180],
    "qty": [2, 1, 3, 4],
})

# %% vectorized
orders["price"] * orders["qty"]                   # сначала — операции над столбцами
# ─── вывод ───
# 0    300
# 1    180
# 2    630
# 3    720
# dtype: int64

# %% map-dict
orders["size"].map({"S": "маленький", "M": "средний", "L": "большой"})
# ─── вывод ───
# 0    маленький
# 1      средний
# 2      большой
# 3      средний
# Name: size, dtype: str

# %% map-func
orders["price"].map(lambda p: f"{p} ₽")
# ─── вывод ───
# 0    150 ₽
# 1    180 ₽
# 2    210 ₽
# 3    180 ₽
# Name: price, dtype: str

# %% frame-map
orders[["price", "qty"]].map(lambda x: x * 10)    # поэлементно по всей таблице
# ─── вывод ───
#    price  qty
# 0   1500   20
# 1   1800   10
# 2   2100   30
# 3   1800   40

# %% apply-columns
orders[["price", "qty"]].apply(lambda col: col.max() - col.min())   # функция получает столбец
# ─── вывод ───
# price    60
# qty       3
# dtype: int64

# %% apply-rows
def label(row):
    return f"{row['size']}×{row['qty']}"

orders.apply(label, axis=1)                       # функция получает строку
# ─── вывод ───
# 0    S×2
# 1    M×1
# 2    L×3
# 3    M×4
# dtype: str

# %% pipe
def add_total(df):
    return df.assign(total=df["price"] * df["qty"])

def only_big(df, limit):
    return df[df["total"] > limit]

orders.pipe(add_total).pipe(only_big, limit=400)
# ─── вывод ───
#   size  price  qty  total
# 2    L    210    3    630
# 3    M    180    4    720

# %% slow [timing=2026-09-29, machine=Apple M4 · macOS · Python 3.14]
big = pd.concat([orders] * 5000, ignore_index=True)       # 20 000 строк
t_apply = min(timeit.repeat(lambda: big.apply(lambda r: r["price"] * r["qty"], axis=1), number=1, repeat=3))
t_vector = min(timeit.repeat(lambda: big["price"] * big["qty"], number=1, repeat=3))
print(f"apply: {t_apply * 1000:.1f} мс, столбцы: {t_vector * 1000:.2f} мс")
print(f"ускорение: ×{t_apply / t_vector:.0f}")           # apply по строкам — цикл Python
# ─── вывод ───
# apply: 33.3 мс, столбцы: 0.04 мс
# ускорение: ×811

# %% applymap [raises=AttributeError]
orders.applymap(str)
# ─── вывод ───
# AttributeError: 'DataFrame' object has no attribute 'applymap'
