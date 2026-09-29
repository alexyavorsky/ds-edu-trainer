# Примеры к статье pandas/groupby-agg.

# %% setup
sales = pd.DataFrame({
    "city":   ["Омск", "Тула", "Омск", "Пермь", "Тула", "Омск"],
    "drink":  ["латте", "капучино", "капучино", "латте", "латте", "латте"],
    "cups":   [30, 12, 18, 25, 20, 12],
    "rating": [4.5, 4.0, None, 4.8, 3.9, 4.2],
})

# %% list
sales.groupby("city")["cups"].agg(["sum", "mean", "count"])
# ─── вывод ───
#        sum  mean  count
# city
# Омск    60  20.0      3
# Пермь   25  25.0      1
# Тула    32  16.0      2

# %% dict
sales.groupby("city").agg({"cups": "sum", "rating": ["mean", "max"]})   # столбцы — MultiIndex
# ─── вывод ───
#       cups rating
#        sum   mean  max
# city
# Омск    60   4.35  4.5
# Пермь   25   4.80  4.8
# Тула    32   3.95  4.0

# %% named
sales.groupby("city").agg(
    total_cups=("cups", "sum"),
    avg_rating=("rating", "mean"),
    drinks=("drink", "nunique"),
)
# ─── вывод ───
#        total_cups  avg_rating  drinks
# city
# Омск           60        4.35       2
# Пермь          25        4.80       1
# Тула           32        3.95       2

# %% custom
sales.groupby("city").agg(
    spread=("cups", lambda s: s.max() - s.min()),
    top_drink=("drink", lambda s: s.value_counts().index[0]),
)
# ─── вывод ───
#        spread top_drink
# city
# Омск       18     латте
# Пермь       0     латте
# Тула        8  капучино

# %% as-frame
sales.groupby("city", as_index=False).agg(total=("cups", "sum"))
# ─── вывод ───
#     city  total
# 0   Омск     60
# 1  Пермь     25
# 2   Тула     32

# %% first-last
sales.groupby("city")["drink"].agg(["first", "last", "size"])
# ─── вывод ───
#           first   last  size
# city
# Омск      латте  латте     3
# Пермь     латте  латте     1
# Тула   капучино  латте     2

# %% flatten
res = sales.groupby("city").agg({"cups": ["sum", "max"]})
res.columns = ["_".join(col) for col in res.columns]     # ("cups", "sum") → "cups_sum"
res
# ─── вывод ───
#        cups_sum  cups_max
# city
# Омск         60        30
# Пермь        25        25
# Тула         32        20

# %% lambda-name
sales.groupby("city")["cups"].agg([lambda s: s.max() - s.min()])   # столбец назван <lambda>
# ─── вывод ───
#        <lambda>
# city
# Омск         18
# Пермь         0
# Тула          8
