# Примеры к статье pandas/merge.

# %% setup
left = pd.DataFrame({"id": [1, 2, 3], "name": ["Аня", "Борис", "Вика"]})
right = pd.DataFrame({"id": [2, 3, 4], "city": ["Тула", "Сочи", "Омск"]})

# %% inner
left.merge(right, on="id")                     # how="inner" по умолчанию
# ─── вывод ───
#    id   name  city
# 0   2  Борис  Тула
# 1   3   Вика  Сочи

# %% left
left.merge(right, on="id", how="left")
# ─── вывод ───
#    id   name  city
# 0   1    Аня   NaN
# 1   2  Борис  Тула
# 2   3   Вика  Сочи

# %% right
left.merge(right, on="id", how="right")
# ─── вывод ───
#    id   name  city
# 0   2  Борис  Тула
# 1   3   Вика  Сочи
# 2   4    NaN  Омск

# %% outer
left.merge(right, on="id", how="outer")
# ─── вывод ───
#    id   name  city
# 0   1    Аня   NaN
# 1   2  Борис  Тула
# 2   3   Вика  Сочи
# 3   4    NaN  Омск

# %% cross
sizes = pd.DataFrame({"size": ["S", "L"]})
drinks = pd.DataFrame({"drink": ["латте", "чай"]})
drinks.merge(sizes, how="cross")               # все сочетания
# ─── вывод ───
#    drink size
# 0  латте    S
# 1  латте    L
# 2    чай    S
# 3    чай    L

# %% lookup
orders = pd.DataFrame({"order": [10, 11, 12, 13], "id": [2, 2, 3, 5]})
orders.merge(left, on="id", how="left")        # подставить имя клиента в заказы
# ─── вывод ───
#    order  id   name
# 0     10   2  Борис
# 1     11   2  Борис
# 2     12   3   Вика
# 3     13   5    NaN

# %% many-to-many
a = pd.DataFrame({"key": ["x", "x"], "a": [1, 2]})
b = pd.DataFrame({"key": ["x", "x", "x"], "b": [10, 20, 30]})
a.merge(b, on="key")                           # 2 × 3 = 6 строк
# ─── вывод ───
#   key  a   b
# 0   x  1  10
# 1   x  1  20
# 2   x  1  30
# 3   x  2  10
# 4   x  2  20
# 5   x  2  30

# %% dtype-mismatch [raises=ValueError]
right_str = right.astype({"id": str})
left.merge(right_str, on="id")                 # 2 и "2" — разные значения
# ─── вывод ───
# ValueError: You are trying to merge on int64 and str columns for key 'id'. If you wish to proceed you should use pd.concat
