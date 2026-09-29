# Примеры к статье pandas/select-columns.

# %% setup
menu = pd.DataFrame({
    "item": ["латте", "чай", "раф"],
    "price": [180, 90, 220],
    "price_old": [170, 90, 200],
    "size": ["M", "L", "M"],
    "vegan": [False, True, False],
})

# %% one
menu["price"]                   # один столбец — Series
# ─── вывод ───
# 0    180
# 1     90
# 2    220
# Name: price, dtype: int64

# %% many
menu[["item", "price"]]         # список столбцов — DataFrame
# ─── вывод ───
#     item  price
# 0  латте    180
# 1    чай     90
# 2    раф    220

# %% one-as-frame
menu[["price"]]                 # двойные скобки — DataFrame из одного столбца
# ─── вывод ───
#    price
# 0    180
# 1     90
# 2    220

# %% attribute
print(menu.price.max())         # доступ через точку — только для чтения и простых имён
menu.size                       # size — это атрибут DataFrame, а не столбец!
# ─── вывод ───
# 220
# 15

# %% select-dtypes
print(menu.select_dtypes(include="number").columns)
menu.select_dtypes(include=["str", "bool"]).columns
# ─── вывод ───
# Index(['price', 'price_old'], dtype='str')
# Index(['item', 'size', 'vegan'], dtype='str')

# %% filter
menu.filter(like="price")       # столбцы, в имени которых есть «price»
# ─── вывод ───
#    price  price_old
# 0    180        170
# 1     90         90
# 2    220        200

# %% missing [raises=KeyError]
menu["cost"]
# ─── вывод ───
# KeyError: 'cost'
