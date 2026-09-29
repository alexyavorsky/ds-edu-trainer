# Примеры к статье pandas/iteration.

# %% setup
import timeit

orders = pd.DataFrame({
    "item": ["латте", "чай", "раф"],
    "qty": [2, 1, 3],
    "price": [180.0, 90.0, 220.0],
})

# %% iterrows
for idx, row in orders.iterrows():
    print(idx, row["item"], row["qty"] * row["price"])
# ─── вывод ───
# 0 латте 360.0
# 1 чай 90.0
# 2 раф 660.0

# %% types-lost
_, row = next(orders[["qty", "price"]].iterrows())
row                                            # qty стал float: строка — один Series одного типа
# ─── вывод ───
# qty        2.0
# price    180.0
# Name: 0, dtype: float64

# %% itertuples
for row in orders.itertuples(index=False):
    print(row.item, row.qty * row.price)       # быстрее и типы сохраняются
# ─── вывод ───
# латте 360.0
# чай 90.0
# раф 660.0

# %% zip
for item, qty in zip(orders["item"], orders["qty"]):
    print(item, qty)
# ─── вывод ───
# латте 2
# чай 1
# раф 3

# %% vectorized
orders["total"] = orders["qty"] * orders["price"]   # вместо цикла
orders
# ─── вывод ───
#     item  qty  price  total
# 0  латте    2  180.0  360.0
# 1    чай    1   90.0   90.0
# 2    раф    3  220.0  660.0

# %% records
orders.to_dict("records")                      # список словарей — если нужен Python-код
# ─── вывод ───
# [{'item': 'латте', 'qty': 2, 'price': 180.0}, {'item': 'чай', 'qty': 1, 'price': 90.0}, {'item': 'раф', 'qty': 3, 'price': 220.0}]

# %% modify
for _, row in orders.iterrows():
    row["qty"] = 0                             # меняется копия строки
orders["qty"].tolist()
# ─── вывод ───
# [2, 1, 3]

# %% speed [timing=2026-09-29, machine=Apple M4 · macOS · Python 3.14]
big = pd.concat([orders] * 3000, ignore_index=True)   # 9000 строк
ways = {
    "iterrows": lambda: [r["qty"] * r["price"] for _, r in big.iterrows()],
    "itertuples": lambda: [r.qty * r.price for r in big.itertuples()],
    "векторно": lambda: big["qty"] * big["price"],
}
for name, f in ways.items():
    print(f"{name}: {min(timeit.repeat(f, number=1, repeat=3)) * 1000:.2f} мс")
# ─── вывод ───
# iterrows: 67.63 мс
# itertuples: 4.58 мс
# векторно: 0.03 мс
