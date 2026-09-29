# Примеры к статье pandas/inspect.

# %% setup
sales = pd.DataFrame({
    "city": ["Омск", "Тула", "Омск", "Сочи", "Тула", "Омск", None],
    "drink": ["латте", "чай", "латте", "раф", "латте", "чай", "латте"],
    "cups": [30, 12, 18, 25, 20, 16, 9],
    "rating": [4.5, 4.0, None, 4.8, 3.9, 4.2, 4.1],
})

# %% head-tail
print(sales.head(3))
sales.tail(2)
# ─── вывод ───
#    city  drink  cups  rating
# 0  Омск  латте    30     4.5
# 1  Тула    чай    12     4.0
# 2  Омск  латте    18     NaN
#    city  drink  cups  rating
# 5  Омск    чай    16     4.2
# 6   NaN  латте     9     4.1

# %% shape
print(sales.shape)
sales.columns
# ─── вывод ───
# (7, 4)
# Index(['city', 'drink', 'cups', 'rating'], dtype='str')

# %% info
sales.info()
# ─── вывод ───
# <class 'pandas.DataFrame'>
# RangeIndex: 7 entries, 0 to 6
# Data columns (total 4 columns):
#  #   Column  Non-Null Count  Dtype
# ---  ------  --------------  -----
#  0   city    6 non-null      str
#  1   drink   7 non-null      str
#  2   cups    7 non-null      int64
#  3   rating  6 non-null      float64
# dtypes: float64(1), int64(1), str(2)
# memory usage: 463.0 bytes

# %% describe
sales.describe()
# ─── вывод ───
#             cups    rating
# count   7.000000  6.000000
# mean   18.571429  4.250000
# std     7.253899  0.339116
# min     9.000000  3.900000
# 25%    14.000000  4.025000
# 50%    18.000000  4.150000
# 75%    22.500000  4.425000
# max    30.000000  4.800000

# %% describe-all
sales.describe(include="all")
# ─── вывод ───
#         city  drink       cups    rating
# count      6      7   7.000000  6.000000
# unique     3      3        NaN       NaN
# top     Омск  латте        NaN       NaN
# freq       3      4        NaN       NaN
# mean     NaN    NaN  18.571429  4.250000
# std      NaN    NaN   7.253899  0.339116
# min      NaN    NaN   9.000000  3.900000
# 25%      NaN    NaN  14.000000  4.025000
# 50%      NaN    NaN  18.000000  4.150000
# 75%      NaN    NaN  22.500000  4.425000
# max      NaN    NaN  30.000000  4.800000

# %% value-counts
print(sales["city"].value_counts())
sales["city"].value_counts(normalize=True).round(2)
# ─── вывод ───
# city
# Омск    3
# Тула    2
# Сочи    1
# Name: count, dtype: int64
# city
# Омск    0.50
# Тула    0.33
# Сочи    0.17
# Name: proportion, dtype: float64

# %% nunique
sales.nunique()
# ─── вывод ───
# city      3
# drink     3
# cups      7
# rating    6
# dtype: int64

# %% value-counts-nan
sales["city"].value_counts(dropna=False)
# ─── вывод ───
# city
# Омск    3
# Тула    2
# Сочи    1
# NaN     1
# Name: count, dtype: int64
