# Примеры к статье pandas/groupby.
# Вывод под примерами пишет scripts/validate_reference.py --update — руками не править.

# %% setup
# продажи сети кофеен за день; у одной записи нет оценки
sales = pd.DataFrame({
    "city":   ["Омск", "Тула", "Омск", "Пермь", "Тула", "Омск"],
    "drink":  ["латте", "капучино", "капучино", "латте", "латте", "латте"],
    "cups":   [30, 12, 18, 25, 20, 12],
    "rating": [4.5, 4.0, None, 4.8, 3.9, 4.2],
})

# %% one-key
sales.groupby("city")["cups"].sum()
# ─── вывод ───
# city
# Омск     60
# Пермь    25
# Тула     32
# Name: cups, dtype: int64

# %% columns
sales.groupby("city")[["cups", "rating"]].mean()
# ─── вывод ───
#        cups  rating
# city
# Омск   20.0    4.35
# Пермь  25.0    4.80
# Тула   16.0    3.95

# %% several-aggs
sales.groupby("city")["cups"].agg(["sum", "mean", "max"])
# ─── вывод ───
#        sum  mean  max
# city
# Омск    60  20.0   30
# Пермь   25  25.0   25
# Тула    32  16.0   20

# %% two-keys
sales.groupby(["city", "drink"])["cups"].sum()
# ─── вывод ───
# city   drink
# Омск   капучино    18
#        латте       42
# Пермь  латте       25
# Тула   капучино    12
#        латте       20
# Name: cups, dtype: int64

# %% as-index
sales.groupby(["city", "drink"], as_index=False)["cups"].sum()
# ─── вывод ───
#     city     drink  cups
# 0   Омск  капучино    18
# 1   Омск     латте    42
# 2  Пермь     латте    25
# 3   Тула  капучино    12
# 4   Тула     латте    20

# %% size-count
groups = sales.groupby("city")
pd.DataFrame({
    "size": groups.size(),               # все строки группы
    "count": groups["rating"].count(),   # только непустые значения
})
# ─── вывод ───
#        size  count
# city
# Омск      3      2
# Пермь     1      1
# Тула      2      2

# %% sort
sales.groupby("city", sort=False)["cups"].sum()   # в порядке первого появления
# ─── вывод ───
# city
# Омск     60
# Тула     32
# Пермь    25
# Name: cups, dtype: int64

# %% iterate
for city, part in sales.groupby("city"):
    print(city, "→ строк:", len(part), "| чашек:", part["cups"].sum())
# ─── вывод ───
# Омск → строк: 3 | чашек: 60
# Пермь → строк: 1 | чашек: 25
# Тула → строк: 2 | чашек: 32

# %% whole-frame [raises=TypeError]
sales.groupby("city").mean()   # столбец drink — строки, среднего у них нет
# ─── вывод ───
# TypeError: dtype 'str' does not support operation 'mean'

# %% dropna
deals = pd.DataFrame({
    "manager": ["Аня", None, "Аня", "Борис"],
    "amount":  [300, 500, 200, 400],
})
print(deals.groupby("manager")["amount"].sum())
deals.groupby("manager", dropna=False)["amount"].sum()
# ─── вывод ───
# manager
# Аня      500
# Борис    400
# Name: amount, dtype: int64
# manager
# Аня      500
# Борис    400
# NaN      500
# Name: amount, dtype: int64

# %% observed
visits = pd.DataFrame({
    "day": pd.Categorical(["пн", "ср", "пн"], categories=["пн", "вт", "ср"]),
    "guests": [40, 55, 35],
})
print(visits.groupby("day")["guests"].sum())
visits.groupby("day", observed=False)["guests"].sum()   # все категории, даже пустые
# ─── вывод ───
# day
# пн    75
# ср    55
# Name: guests, dtype: int64
# day
# пн    75
# вт     0
# ср    55
# Name: guests, dtype: int64
