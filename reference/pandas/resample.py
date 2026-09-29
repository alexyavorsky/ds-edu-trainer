# Примеры к статье pandas/resample.

# %% setup
hours = pd.date_range("2024-03-01 08:00", periods=10, freq="6h")
orders = pd.Series([5, 12, 9, 3, 7, 15, 8, 2, 6, 11], index=hours, name="orders")

# %% daily
orders.resample("D").sum()                      # по дням
# ─── вывод ───
# 2024-03-01    26
# 2024-03-02    33
# 2024-03-03    19
# Freq: D, Name: orders, dtype: int64

# %% several
orders.resample("D").agg(["sum", "max", "count"])
# ─── вывод ───
#             sum  max  count
# 2024-03-01   26   12      3
# 2024-03-02   33   15      4
# 2024-03-03   19   11      3

# %% month-end
days = pd.date_range("2024-01-25", periods=10, freq="D")
pd.Series(range(10), index=days).resample("ME").sum()   # по месяцам; метка — последний день
# ─── вывод ───
# 2024-01-31    21
# 2024-02-29    24
# Freq: ME, dtype: int64

# %% month-start
days = pd.date_range("2024-01-25", periods=10, freq="D")
pd.Series(range(10), index=days).resample("MS").sum()   # метка — первый день месяца
# ─── вывод ───
# 2024-01-01    21
# 2024-02-01    24
# Freq: MS, dtype: int64

# %% upsample
daily = pd.Series([100, 130, 90], index=pd.date_range("2024-03-01", periods=3, freq="D"))
daily.resample("12h").ffill()                   # чаще, чем данные: заполняем предыдущим
# ─── вывод ───
# 2024-03-01 00:00:00    100
# 2024-03-01 12:00:00    100
# 2024-03-02 00:00:00    130
# 2024-03-02 12:00:00    130
# 2024-03-03 00:00:00     90
# Freq: 12h, dtype: int64

# %% interpolate
daily = pd.Series([100, 130, 90], index=pd.date_range("2024-03-01", periods=3, freq="D"))
daily.resample("12h").interpolate()             # или линейно между точками
# ─── вывод ───
# 2024-03-01 00:00:00    100.0
# 2024-03-01 12:00:00    115.0
# 2024-03-02 00:00:00    130.0
# 2024-03-02 12:00:00    110.0
# 2024-03-03 00:00:00     90.0
# Freq: 12h, dtype: float64

# %% asfreq
orders.asfreq("12h")                            # просто выбрать моменты, без агрегации
# ─── вывод ───
# 2024-03-01 08:00:00    5
# 2024-03-01 20:00:00    9
# 2024-03-02 08:00:00    7
# 2024-03-02 20:00:00    8
# 2024-03-03 08:00:00    6
# Freq: 12h, Name: orders, dtype: int64

# %% frame
df = pd.DataFrame({"orders": orders, "revenue": orders * 350})
df.resample("D").agg({"orders": "sum", "revenue": "mean"})
# ─── вывод ───
#             orders      revenue
# 2024-03-01      26  3033.333333
# 2024-03-02      33  2887.500000
# 2024-03-03      19  2216.666667

# %% column-on
events = orders.reset_index().rename(columns={"index": "time"})
events.resample("D", on="time")["orders"].sum()   # даты в столбце, а не в индексе
# ─── вывод ───
# time
# 2024-03-01    26
# 2024-03-02    33
# 2024-03-03    19
# Freq: D, Name: orders, dtype: int64

# %% no-datetime [raises=TypeError]
pd.Series([1, 2, 3]).resample("D").sum()
# ─── вывод ───
# TypeError: Only valid with DatetimeIndex, TimedeltaIndex or PeriodIndex, but got an instance of 'RangeIndex'
