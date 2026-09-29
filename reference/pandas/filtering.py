# Примеры к статье pandas/filtering.

# %% setup
orders = pd.DataFrame({
    "city": ["Омск", "Тула", "Сочи", "Омск", "Тула", "Пермь"],
    "amount": [1200, 450, 3100, 800, 2500, 950],
    "status": ["доставлен", "отменён", "доставлен", "в пути", "доставлен", "отменён"],
})

# %% condition
orders[orders["amount"] > 1000]
# ─── вывод ───
#    city  amount     status
# 0  Омск    1200  доставлен
# 2  Сочи    3100  доставлен
# 4  Тула    2500  доставлен

# %% and-or
print(orders[(orders["city"] == "Омск") & (orders["amount"] > 1000)])
orders[(orders["city"] == "Сочи") | (orders["status"] == "отменён")]
# ─── вывод ───
#    city  amount     status
# 0  Омск    1200  доставлен
#     city  amount     status
# 1   Тула     450    отменён
# 2   Сочи    3100  доставлен
# 5  Пермь     950    отменён

# %% not
orders[~(orders["status"] == "отменён")]
# ─── вывод ───
#    city  amount     status
# 0  Омск    1200  доставлен
# 2  Сочи    3100  доставлен
# 3  Омск     800     в пути
# 4  Тула    2500  доставлен

# %% isin
orders[orders["city"].isin(["Омск", "Тула"])]
# ─── вывод ───
#    city  amount     status
# 0  Омск    1200  доставлен
# 1  Тула     450    отменён
# 3  Омск     800     в пути
# 4  Тула    2500  доставлен

# %% between
orders[orders["amount"].between(800, 1200)]          # границы включены
# ─── вывод ───
#     city  amount     status
# 0   Омск    1200  доставлен
# 3   Омск     800     в пути
# 5  Пермь     950    отменён

# %% query
limit = 1000
orders.query("amount > @limit and status == 'доставлен'")
# ─── вывод ───
#    city  amount     status
# 0  Омск    1200  доставлен
# 2  Сочи    3100  доставлен
# 4  Тула    2500  доставлен

# %% loc-column
orders.loc[orders["amount"] > 2000, ["city", "amount"]]
# ─── вывод ───
#    city  amount
# 2  Сочи    3100
# 4  Тула    2500

# %% python-and [raises=ValueError]
orders[(orders["amount"] > 500) and (orders["city"] == "Омск")]
# ─── вывод ───
# ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
