# Примеры к статье numpy/nan-inf.

# %% setup
temps = np.array([12.5, np.nan, 14.0, 11.0, np.nan])   # два дня без данных

# %% propagate
print(temps.sum())            # один NaN — и сумма тоже NaN
temps.mean()
# ─── вывод ───
# nan
# np.float64(nan)

# %% nan-functions
print(np.nansum(temps))
print(np.nanmean(temps))
np.nanmax(temps)
# ─── вывод ───
# 37.5
# 12.5
# np.float64(14.0)

# %% isnan
mask = np.isnan(temps)
print(mask)
print(mask.sum())             # сколько пропусков
temps[~mask]                  # только известные значения
# ─── вывод ───
# [False  True False False  True]
# 2
# array([12.5, 14. , 11. ])

# %% nan-eq
print(np.nan == np.nan)
temps == np.nan               # всегда False — так пропуски не найти
# ─── вывод ───
# False
# array([False, False, False, False, False])

# %% fill
print(np.nan_to_num(temps))                        # NaN → 0
np.where(np.isnan(temps), np.nanmean(temps), temps)   # NaN → среднее
# ─── вывод ───
# [12.5  0.  14.  11.   0. ]
# array([12.5, 12.5, 14. , 11. , 12.5])

# %% inf [warns]
x = np.array([np.inf, -np.inf, 5.0])
print(np.isinf(x), np.isfinite(x))
print(x - x)                  # inf − inf = nan
x.max()
# ─── вывод ───
# [ True  True False] [False False  True]
# RuntimeWarning: invalid value encountered in subtract
# [nan nan  0.]
# np.float64(inf)

# %% all-nan [warns]
np.nanmean(np.array([np.nan, np.nan]))
# ─── вывод ───
# RuntimeWarning: Mean of empty slice
# np.float64(nan)

# %% int-nan [raises=ValueError]
days = np.array([1, 2, 3])
days[0] = np.nan              # в целом массиве нет NaN
# ─── вывод ───
# ValueError: cannot convert float NaN to integer
