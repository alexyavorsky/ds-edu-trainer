# Примеры к статье pandas/shift-diff.

# %% setup
days = pd.date_range("2024-03-01", periods=6, freq="D")
price = pd.Series([100.0, 102.0, 101.0, 105.0, 105.0, 99.0], index=days, name="price")
trades = pd.DataFrame({                    # сделки по двум тикерам вперемешку
    "ticker": ["A", "B", "A", "B", "A"],
    "price": [10.0, 50.0, 11.0, 48.0, 12.5],
})

# %% shift
pd.DataFrame({"price": price, "yesterday": price.shift(1), "tomorrow": price.shift(-1)})
# ─── вывод ───
#             price  yesterday  tomorrow
# 2024-03-01  100.0        NaN     102.0
# 2024-03-02  102.0      100.0     101.0
# 2024-03-03  101.0      102.0     105.0
# 2024-03-04  105.0      101.0     105.0
# 2024-03-05  105.0      105.0      99.0
# 2024-03-06   99.0      105.0       NaN

# %% diff
price.diff()                              # price − вчерашняя цена
# ─── вывод ───
# 2024-03-01    NaN
# 2024-03-02    2.0
# 2024-03-03   -1.0
# 2024-03-04    4.0
# 2024-03-05    0.0
# 2024-03-06   -6.0
# Freq: D, Name: price, dtype: float64

# %% pct-change
(price.pct_change() * 100).round(2)       # изменение в процентах
# ─── вывод ───
# 2024-03-01     NaN
# 2024-03-02    2.00
# 2024-03-03   -0.98
# 2024-03-04    3.96
# 2024-03-05    0.00
# 2024-03-06   -5.71
# Freq: D, Name: price, dtype: float64

# %% periods
price.diff(periods=3)                     # к значению 3 дня назад
# ─── вывод ───
# 2024-03-01    NaN
# 2024-03-02    NaN
# 2024-03-03    NaN
# 2024-03-04    5.0
# 2024-03-05    3.0
# 2024-03-06   -2.0
# Freq: D, Name: price, dtype: float64

# %% shift-freq
price.shift(1, freq="D").head(3)          # сдвинулись даты, а не значения
# ─── вывод ───
# 2024-03-02    100.0
# 2024-03-03    102.0
# 2024-03-04    101.0
# Freq: D, Name: price, dtype: float64

# %% groups
trades.assign(change=trades.groupby("ticker")["price"].diff())   # внутри каждого тикера
# ─── вывод ───
#   ticker  price  change
# 0      A   10.0     NaN
# 1      B   50.0     NaN
# 2      A   11.0     1.0
# 3      B   48.0    -2.0
# 4      A   12.5     1.5

# %% no-group
trades.assign(change=trades["price"].diff())   # без группировки — разница между разными тикерами
# ─── вывод ───
#   ticker  price  change
# 0      A   10.0     NaN
# 1      B   50.0    40.0
# 2      A   11.0   -39.0
# 3      B   48.0    37.0
# 4      A   12.5   -35.5

# %% pct-nan
s = pd.Series([100.0, None, 110.0])
print(s.pct_change())                     # у пропуска и после него — NaN
s.ffill().pct_change()                    # старое поведение — явный ffill перед расчётом
# ─── вывод ───
# 0   NaN
# 1   NaN
# 2   NaN
# dtype: float64
# 0    NaN
# 1    0.0
# 2    0.1
# dtype: float64
