# Примеры к статье pandas/columns.

# %% setup
menu = pd.DataFrame({
    "item": ["латте", "чай", "раф"],
    "price": [180, 90, 220],
    "cost": [60, 15, 80],
})

# %% add
menu["margin"] = menu["price"] - menu["cost"]    # новый столбец из вычисления
menu["currency"] = "RUB"                          # одно значение на все строки
menu
# ─── вывод ───
#     item  price  cost  margin currency
# 0  латте    180    60     120      RUB
# 1    чай     90    15      75      RUB
# 2    раф    220    80     140      RUB

# %% assign
menu.assign(
    margin=lambda d: d["price"] - d["cost"],
    margin_pct=lambda d: (d["margin"] / d["price"] * 100).round(1),
)
# ─── вывод ───
#     item  price  cost  margin  margin_pct
# 0  латте    180    60     120        66.7
# 1    чай     90    15      75        83.3
# 2    раф    220    80     140        63.6

# %% pd-col
menu.assign(price_usd=pd.col("price") / 90)       # pd.col — ссылка на столбец (pandas 3.0)
# ─── вывод ───
#     item  price  cost  price_usd
# 0  латте    180    60   2.000000
# 1    чай     90    15   1.000000
# 2    раф    220    80   2.444444

# %% insert
menu.insert(1, "size", ["M", "L", "M"])           # вставить на позицию 1
menu
# ─── вывод ───
#     item size  price  cost
# 0  латте    M    180    60
# 1    чай    L     90    15
# 2    раф    M    220    80

# %% rename
menu.rename(columns={"item": "позиция", "price": "цена"})
# ─── вывод ───
#   позиция  цена  cost
# 0   латте   180    60
# 1     чай    90    15
# 2     раф   220    80

# %% drop
menu.drop(columns=["cost"])
# ─── вывод ───
#     item  price
# 0  латте    180
# 1    чай     90
# 2    раф    220

# %% change
menu["price"] = (menu["price"] * 1.1).round()     # заменить значения столбца
menu
# ─── вывод ───
#     item  price  cost
# 0  латте  198.0    60
# 1    чай   99.0    15
# 2    раф  242.0    80

# %% drop-missing [raises=KeyError]
menu.drop(columns=["discount"])
# ─── вывод ───
# KeyError: "['discount'] not found in axis"
