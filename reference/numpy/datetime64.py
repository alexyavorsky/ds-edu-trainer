# Примеры к статье numpy/datetime64.

# %% setup
start = np.datetime64("2024-02-27")      # начало проекта
deadline = np.datetime64("2024-03-31")   # срок сдачи

# %% create
print(np.datetime64("2024-03-15"))
print(np.datetime64("2024-03-15T14:30"))
np.array(["2024-01-10", "2024-02-29"], dtype="datetime64[D]")
# ─── вывод ───
# 2024-03-15
# 2024-03-15T14:30
# array(['2024-01-10', '2024-02-29'], dtype='datetime64[D]')

# %% arithmetic
print(start + np.timedelta64(3, "D"))              # високосный год: будет 1 марта
deadline - start                                   # разница — timedelta64
# ─── вывод ───
# 2024-03-01
# np.timedelta64(33,'D')

# %% arange
np.arange("2024-02-26", "2024-03-03", dtype="datetime64[D]")   # все дни подряд
# ─── вывод ───
# array(['2024-02-26', '2024-02-27', '2024-02-28', '2024-02-29',
#        '2024-03-01', '2024-03-02'], dtype='datetime64[D]')

# %% units
d = np.datetime64("2024-03-15T14:30")
print(d.astype("datetime64[D]"))                   # отбросить время
print(d.astype("datetime64[M]"))                   # до месяца
(deadline - start) / np.timedelta64(1, "D")        # разница в днях числом
# ─── вывод ───
# 2024-03-15
# 2024-03
# np.float64(33.0)

# %% busday
print(np.is_busday(np.datetime64("2024-03-16")))   # суббота
np.busday_count("2024-03-01", "2024-04-01")        # рабочих дней в марте
# ─── вывод ───
# False
# np.int64(21)

# %% month-add [raises=TypeError]
np.datetime64("2024-01-31") + np.timedelta64(1, "M")   # месяцы разной длины
# ─── вывод ───
# UFuncTypeError: Cannot cast ufunc 'add' input 1 from dtype('<m8[M]') to dtype('<m8[D]') with casting rule 'same_kind'

# %% generic-unit [deprecated]
np.timedelta64(5)                                  # без единицы измерения
# ─── вывод ───
# DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future. This includes implicit conversion of bare integers (e.g. `+ 1`). Please use a specific unit instead.
# np.timedelta64(5)
