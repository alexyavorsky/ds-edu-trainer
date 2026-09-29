# Примеры к статье pandas/set-index.

# %% setup
stock = pd.DataFrame({
    "sku": ["A-1", "B-7", "C-3"],
    "item": ["латте", "чай", "раф"],
    "qty": [12, 40, 7],
})

# %% set-index
by_sku = stock.set_index("sku")
print(by_sku)
by_sku.loc["B-7", "qty"]                 # теперь доступ по артикулу
# ─── вывод ───
#       item  qty
# sku
# A-1  латте   12
# B-7    чай   40
# C-3    раф    7
# np.int64(40)

# %% reset-index
stock.set_index("sku").reset_index()     # индекс снова обычный столбец
# ─── вывод ───
#    sku   item  qty
# 0  A-1  латте   12
# 1  B-7    чай   40
# 2  C-3    раф    7

# %% reset-drop
filtered = stock[stock["qty"] > 10]
print(filtered)                          # индекс 0, 1 с пропуском
filtered.reset_index(drop=True)          # новый 0, 1, 2… без старого индекса
# ─── вывод ───
#    sku   item  qty
# 0  A-1  латте   12
# 1  B-7    чай   40
#    sku   item  qty
# 0  A-1  латте   12
# 1  B-7    чай   40

# %% keep-column
stock.set_index("sku", drop=False)       # столбец остаётся и в данных
# ─── вывод ───
#      sku   item  qty
# sku
# A-1  A-1  латте   12
# B-7  B-7    чай   40
# C-3  C-3    раф    7

# %% rename-axis
stock.set_index("sku").rename_axis("артикул")
# ─── вывод ───
#           item  qty
# артикул
# A-1      латте   12
# B-7        чай   40
# C-3        раф    7

# %% unique
dup = pd.DataFrame({"qty": [12, 40, 5]}, index=["латте", "чай", "чай"])
print(dup.index.is_unique)
dup.loc["чай"]                           # повтор метки — несколько строк вместо одной
# ─── вывод ───
# False
#      qty
# чай   40
# чай    5

# %% missing-label [raises=KeyError]
stock.set_index("sku").loc["Z-9"]
# ─── вывод ───
# KeyError: 'Z-9'
