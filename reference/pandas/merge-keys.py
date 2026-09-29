# Примеры к статье pandas/merge-keys.

# %% setup
clients = pd.DataFrame({"client_id": [1, 2, 3], "name": ["Аня", "Борис", "Вика"], "city": ["Омск", "Тула", "Сочи"]})
orders = pd.DataFrame({"order": [10, 11, 12], "customer": [2, 3, 4], "city": ["Тула", "Москва", "Омск"]})

# %% left-right-on
orders.merge(clients, left_on="customer", right_on="client_id", how="left")
# ─── вывод ───
#    order  customer  city_x  client_id   name city_y
# 0     10         2    Тула        2.0  Борис   Тула
# 1     11         3  Москва        3.0   Вика   Сочи
# 2     12         4    Омск        NaN    NaN    NaN

# %% suffixes
orders.merge(clients, left_on="customer", right_on="client_id",
             suffixes=("_delivery", "_client"))
# ─── вывод ───
#    order  customer city_delivery  client_id   name city_client
# 0     10         2          Тула          2  Борис        Тула
# 1     11         3        Москва          3   Вика        Сочи

# %% indicator
res = orders.merge(clients, left_on="customer", right_on="client_id", how="outer", indicator=True)
res[["order", "name", "_merge"]]
# ─── вывод ───
#    order   name      _merge
# 0    NaN    Аня  right_only
# 1   10.0  Борис        both
# 2   11.0   Вика        both
# 3   12.0    NaN   left_only

# %% validate [raises=MergeError]
dup = pd.concat([clients, clients.head(1)])        # клиент 1 записан дважды
orders.merge(dup, left_on="customer", right_on="client_id", validate="many_to_one")
# ─── вывод ───
# MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
#
# Duplicates in right:
#   client_id
#          1 ...

# %% index
cl = clients.set_index("client_id")
orders.merge(cl[["name"]], left_on="customer", right_index=True, how="left")
# ─── вывод ───
#    order  customer    city   name
# 0     10         2    Тула  Борис
# 1     11         3  Москва   Вика
# 2     12         4    Омск    NaN

# %% join
cl = clients.set_index("client_id")
orders.set_index("customer").join(cl[["name"]], how="left")   # join — merge по индексу
# ─── вывод ───
#           order    city   name
# customer
# 2            10    Тула  Борис
# 3            11  Москва   Вика
# 4            12    Омск    NaN

# %% several-keys
plan = pd.DataFrame({"city": ["Омск", "Омск"], "month": ["янв", "фев"], "plan": [100, 120]})
fact = pd.DataFrame({"city": ["Омск", "Омск"], "month": ["фев", "янв"], "fact": [130, 95]})
plan.merge(fact, on=["city", "month"])            # пара ключей
# ─── вывод ───
#    city month  plan  fact
# 0  Омск   янв   100    95
# 1  Омск   фев   120   130
