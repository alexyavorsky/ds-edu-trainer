# Примеры к статье pandas/explode.

# %% setup
orders = pd.DataFrame({
    "order": [101, 102, 103],
    "items": ["латте, круассан", "чай", "раф, чизкейк, вода"],
})

# %% split-explode
orders.assign(items=orders["items"].str.split(", ")).explode("items")
# ─── вывод ───
#    order     items
# 0    101     латте
# 0    101  круассан
# 1    102       чай
# 2    103       раф
# 2    103   чизкейк
# 2    103      вода

# %% ignore-index
orders.assign(items=orders["items"].str.split(", ")).explode("items", ignore_index=True)
# ─── вывод ───
#    order     items
# 0    101     латте
# 1    101  круассан
# 2    102       чай
# 3    103       раф
# 4    103   чизкейк
# 5    103      вода

# %% count
orders.assign(items=orders["items"].str.split(", ")).explode("items")["items"].value_counts()
# ─── вывод ───
# items
# латте       1
# круассан    1
# чай         1
# раф         1
# чизкейк     1
# вода        1
# Name: count, dtype: int64

# %% empty
tags = pd.DataFrame({"post": [1, 2], "tags": [["python", "pandas"], []]})
tags.explode("tags")                     # пустой список → NaN
# ─── вывод ───
#    post    tags
# 0     1  python
# 0     1  pandas
# 1     2     NaN

# %% several
pairs = pd.DataFrame({"id": [1], "a": [[1, 2]], "b": [["x", "y"]]})
pairs.explode(["a", "b"])                # несколько столбцов параллельно
# ─── вывод ───
#    id  a  b
# 0   1  1  x
# 0   1  2  y

# %% string-not-list
orders.explode("items")                  # строка — не список: explode ничего не делает
# ─── вывод ───
#    order               items
# 0    101     латте, круассан
# 1    102                 чай
# 2    103  раф, чизкейк, вода
