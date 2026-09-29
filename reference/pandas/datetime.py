# Примеры к статье pandas/datetime.

# %% setup
orders = pd.DataFrame({
    "created": ["2024-03-01 09:15", "2024-03-02 18:40", "2024-03-09 11:05"],
    "shipped": ["2024-03-03 10:00", "2024-03-02 21:10", "2024-03-12 16:30"],
})

# %% to-datetime
created = pd.to_datetime(orders["created"])
created
# ─── вывод ───
# 0   2024-03-01 09:15:00
# 1   2024-03-02 18:40:00
# 2   2024-03-09 11:05:00
# Name: created, dtype: datetime64[us]

# %% format
print(pd.to_datetime(["01.03.2024", "15.04.2024"], format="%d.%m.%Y"))
pd.to_datetime(["01.03.2024"], dayfirst=True)
# ─── вывод ───
# DatetimeIndex(['2024-03-01', '2024-04-15'], dtype='datetime64[us]', freq=None)
# DatetimeIndex(['2024-03-01'], dtype='datetime64[us]', freq=None)

# %% errors
pd.to_datetime(pd.Series(["2024-03-01", "не указано"]), errors="coerce")
# ─── вывод ───
# 0   2024-03-01
# 1          NaT
# dtype: datetime64[us]

# %% dt
created = pd.to_datetime(orders["created"])
pd.DataFrame({
    "date": created.dt.date,
    "month": created.dt.month,
    "weekday": created.dt.day_name(),
    "hour": created.dt.hour,
})
# ─── вывод ───
#          date  month   weekday  hour
# 0  2024-03-01      3    Friday     9
# 1  2024-03-02      3  Saturday    18
# 2  2024-03-09      3  Saturday    11

# %% timedelta
created = pd.to_datetime(orders["created"])
shipped = pd.to_datetime(orders["shipped"])
delay = shipped - created
print(delay)
delay.dt.total_seconds() / 3600                 # в часах
# ─── вывод ───
# 0   2 days 00:45:00
# 1   0 days 02:30:00
# 2   3 days 05:25:00
# dtype: timedelta64[us]
# 0    48.750000
# 1     2.500000
# 2    77.416667
# dtype: float64

# %% floor-strftime
created = pd.to_datetime(orders["created"])
print(created.dt.floor("D").tolist())           # до начала дня
created.dt.strftime("%d.%m.%Y")
# ─── вывод ───
# [Timestamp('2024-03-01 00:00:00'), Timestamp('2024-03-02 00:00:00'), Timestamp('2024-03-09 00:00:00')]
# 0    01.03.2024
# 1    02.03.2024
# 2    09.03.2024
# Name: created, dtype: str

# %% offset
created = pd.to_datetime(orders["created"])
created + pd.DateOffset(months=1)               # плюс календарный месяц
# ─── вывод ───
# 0   2024-04-01 09:15:00
# 1   2024-04-02 18:40:00
# 2   2024-04-09 11:05:00
# Name: created, dtype: datetime64[us]

# %% unit
created = pd.to_datetime(orders["created"])
print(created.dtype)                            # pandas 3: микросекунды
created.astype("int64").iloc[0]                 # число в микросекундах, а не наносекундах
# ─── вывод ───
# datetime64[us]
# np.int64(1709284500000000)

# %% mixed-format [raises=ValueError]
pd.to_datetime(pd.Series(["2024-03-01 10:00", "2024-03-05"]))   # формат определяется по первой строке
# ─── вывод ───
# ValueError: time data "2024-03-05" doesn't match format "%Y-%m-%d %H:%M". You might want to try:
#     - passing `format` if your strings have a consistent format;
#     - passing `format='ISO8601'` if your strings are all ISO8601 but not necessarily in exactly the same format;
#     - passing `format='mixed'`, and the format will be inferred for each element individually. You might want to use `dayfirst` alongside this.

# %% iso8601
pd.to_datetime(pd.Series(["2024-03-01 10:00", "2024-03-05"]), format="ISO8601")
# ─── вывод ───
# 0   2024-03-01 10:00:00
# 1   2024-03-05 00:00:00
# dtype: datetime64[us]
