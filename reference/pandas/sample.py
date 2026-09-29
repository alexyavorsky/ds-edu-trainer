# Примеры к статье pandas/sample.

# %% setup
customers = pd.DataFrame({
    "name": ["Аня", "Борис", "Вика", "Глеб", "Дина", "Егор", "Женя", "Зоя"],
    "orders": [12, 3, 7, 1, 20, 5, 9, 2],
})

# %% n
customers.sample(n=3, random_state=42)            # 3 случайные строки
# ─── вывод ───
#     name  orders
# 1  Борис       3
# 5   Егор       5
# 0    Аня      12

# %% frac
customers.sample(frac=0.5, random_state=1)        # половина строк
# ─── вывод ───
#     name  orders
# 7    Зоя       2
# 2   Вика       7
# 1  Борис       3
# 6   Женя       9

# %% shuffle
customers.sample(frac=1, random_state=7, ignore_index=True)   # перемешать все строки
# ─── вывод ───
#     name  orders
# 0   Вика       7
# 1   Егор       5
# 2    Аня      12
# 3   Женя       9
# 4   Глеб       1
# 5  Борис       3
# 6   Дина      20
# 7    Зоя       2

# %% replace
customers.sample(n=10, replace=True, random_state=3)["name"].value_counts()   # с повторами
# ─── вывод ───
# name
# Аня      4
# Глеб     2
# Егор     2
# Вика     1
# Борис    1
# Name: count, dtype: int64

# %% weights
customers.sample(n=200, weights="orders", replace=True, random_state=5)["name"].value_counts().head(3)   # чаще всех — у кого больше заказов
# ─── вывод ───
# name
# Дина    64
# Аня     37
# Женя    30
# Name: count, dtype: int64

# %% same-seed
a = customers.sample(n=2, random_state=10)["name"].tolist()
b = customers.sample(n=2, random_state=10)["name"].tolist()
a, b
# ─── вывод ───
# (['Вика', 'Глеб'], ['Вика', 'Глеб'])

# %% too-many [raises=ValueError]
customers.sample(n=20)                            # без replace больше строк, чем есть, не взять
# ─── вывод ───
# ValueError: Cannot take a larger sample than population when 'replace=False'
