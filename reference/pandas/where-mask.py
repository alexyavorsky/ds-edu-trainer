# Примеры к статье pandas/where-mask.

# %% setup
temps = pd.Series([12.5, -45.0, 18.0, 99.0, 21.5], name="temp")   # два значения — сбой датчика

# %% where
temps.where(temps.between(-40, 50))          # оставить, где условие True; иначе NaN
# ─── вывод ───
# 0    12.5
# 1     NaN
# 2    18.0
# 3     NaN
# 4    21.5
# Name: temp, dtype: float64

# %% mask
temps.mask(temps > 50, 50)                    # заменить, где условие True
# ─── вывод ───
# 0    12.5
# 1   -45.0
# 2    18.0
# 3    50.0
# 4    21.5
# Name: temp, dtype: float64

# %% other-series
forecast = pd.Series([13.0, 11.0, 17.5, 20.0, 22.0])
temps.where(temps.between(-40, 50), forecast)   # замена значениями другого Series
# ─── вывод ───
# 0    12.5
# 1    11.0
# 2    18.0
# 3    20.0
# 4    21.5
# Name: temp, dtype: float64

# %% frame
scores = pd.DataFrame({"math": [5, 2, 4], "phys": [3, 5, 1]})
scores.where(scores >= 3, 0)                  # по всей таблице
# ─── вывод ───
#    math  phys
# 0     5     3
# 1     0     5
# 2     4     0

# %% clip
temps.clip(lower=-40, upper=50)               # ограничить диапазоном
# ─── вывод ───
# 0    12.5
# 1   -40.0
# 2    18.0
# 3    50.0
# 4    21.5
# Name: temp, dtype: float64

# %% clip-series
prices = pd.DataFrame({"low": [10, 20], "price": [5, 30], "high": [15, 25]})
prices["price"].clip(lower=prices["low"], upper=prices["high"])   # границы свои для каждой строки
# ─── вывод ───
# 0    10
# 1    25
# Name: price, dtype: int64

# %% np-where
np.where(temps > 20, "тепло", "прохладно")    # NumPy: условие → одно из двух значений
# ─── вывод ───
# array(['прохладно', 'прохладно', 'прохладно', 'тепло', 'тепло'],
#       dtype='<U9')
