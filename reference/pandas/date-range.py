# Примеры к статье pandas/date-range.

# %% setup
days = pd.date_range("2024-02-26", periods=10, freq="D")
visits = pd.Series([120, 135, 128, 150, 162, 90, 85, 140, 155, 149], index=days)

# %% date-range
pd.date_range("2024-03-01", "2024-03-05")        # по дням от и до
# ─── вывод ───
# DatetimeIndex(['2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04',
#                '2024-03-05'],
#               dtype='datetime64[us]', freq='D')

# %% freq
print(pd.date_range("2024-01-01", periods=4, freq="W-MON"))   # по понедельникам
print(pd.date_range("2024-01-01", periods=3, freq="ME"))      # концы месяцев
pd.date_range("2024-03-01 09:00", periods=3, freq="2h")       # каждые 2 часа
# ─── вывод ───
# DatetimeIndex(['2024-01-01', '2024-01-08', '2024-01-15', '2024-01-22'], dtype='datetime64[us]', freq='W-MON')
# DatetimeIndex(['2024-01-31', '2024-02-29', '2024-03-31'], dtype='datetime64[us]', freq='ME')
# DatetimeIndex(['2024-03-01 09:00:00', '2024-03-01 11:00:00',
#                '2024-03-01 13:00:00'],
#               dtype='datetime64[us]', freq='2h')

# %% series
visits
# ─── вывод ───
# 2024-02-26    120
# 2024-02-27    135
# 2024-02-28    128
# 2024-02-29    150
# 2024-03-01    162
# 2024-03-02     90
# 2024-03-03     85
# 2024-03-04    140
# 2024-03-05    155
# 2024-03-06    149
# Freq: D, dtype: int64

# %% select-string
print(visits.loc["2024-03"])                     # весь март
visits.loc["2024-02-28":"2024-03-01"]            # диапазон дат, конец включён
# ─── вывод ───
# 2024-03-01    162
# 2024-03-02     90
# 2024-03-03     85
# 2024-03-04    140
# 2024-03-05    155
# 2024-03-06    149
# Freq: D, dtype: int64
# 2024-02-28    128
# 2024-02-29    150
# 2024-03-01    162
# Freq: D, dtype: int64

# %% index-parts
visits[visits.index.dayofweek >= 5]              # только выходные
# ─── вывод ───
# 2024-03-02    90
# 2024-03-03    85
# Freq: D, dtype: int64

# %% bdate
pd.bdate_range("2024-03-01", "2024-03-12")       # рабочие дни
# ─── вывод ───
# DatetimeIndex(['2024-03-01', '2024-03-04', '2024-03-05', '2024-03-06',
#                '2024-03-07', '2024-03-08', '2024-03-11', '2024-03-12'],
#               dtype='datetime64[us]', freq='B')

# %% period
pd.period_range("2024-01", periods=3, freq="M")  # периоды: месяц целиком, а не момент
# ─── вывод ───
# PeriodIndex(['2024-01', '2024-02', '2024-03'], dtype='period[M]')

# %% old-alias [raises=ValueError]
pd.date_range("2024-01-01", periods=3, freq="M")
# ─── вывод ───
# ValueError: Invalid frequency: M. Failed to parse with error message: ValueError("'M' is no longer supported for offsets. Please use 'ME' instead.")
