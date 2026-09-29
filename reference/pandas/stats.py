# Примеры к статье pandas/stats.

# %% setup
# продажи по месяцам: 3 магазина
sales = pd.DataFrame(
    {"jan": [120, 95, 140], "feb": [130, None, 150], "mar": [110, 105, 160]},
    index=["Омск", "Тула", "Сочи"],
)

# %% columns
sales.mean()                         # по каждому столбцу (axis=0); NaN пропускается
# ─── вывод ───
# jan    118.333333
# feb    140.000000
# mar    125.000000
# dtype: float64

# %% rows
sales.sum(axis=1)                    # по каждой строке
# ─── вывод ───
# Омск    360.0
# Тула    200.0
# Сочи    450.0
# dtype: float64

# %% skipna
print(sales["feb"].mean())
sales["feb"].mean(skipna=False)      # с пропуском результат — NaN
# ─── вывод ───
# 140.0
# np.float64(nan)

# %% several
sales.agg(["min", "max", "median"])
# ─── вывод ───
#           jan    feb    mar
# min      95.0  130.0  105.0
# max     140.0  150.0  160.0
# median  120.0  140.0  110.0

# %% idxmax
print(sales.idxmax())                # магазин с максимумом в каждом месяце
sales.idxmax(axis=1)                 # лучший месяц каждого магазина
# ─── вывод ───
# jan    Сочи
# feb    Сочи
# mar    Сочи
# dtype: str
# Омск    feb
# Тула    mar
# Сочи    mar
# dtype: str

# %% quantile
sales["jan"].quantile([0.25, 0.5, 0.75])
# ─── вывод ───
# 0.25    107.5
# 0.50    120.0
# 0.75    130.0
# Name: jan, dtype: float64

# %% cumulative
sales.cumsum(axis=1)                 # нарастающий итог по месяцам
# ─── вывод ───
#         jan    feb    mar
# Омск  120.0  250.0  360.0
# Тула   95.0    NaN  200.0
# Сочи  140.0  290.0  450.0

# %% std-ddof
print(sales["jan"].std())            # ddof=1 — выборочное
np.std(sales["jan"].to_numpy())      # NumPy: ddof=0
# ─── вывод ───
# 22.546248764114473
# np.float64(18.408935028645434)

# %% numeric-only
shops = sales.assign(manager=["Аня", "Борис", "Вика"])
shops.mean(numeric_only=True)        # без numeric_only падает на тексте
# ─── вывод ───
# jan    118.333333
# feb    140.000000
# mar    125.000000
# dtype: float64

# %% text-column [raises=TypeError]
shops = sales.assign(manager=["Аня", "Борис", "Вика"])
shops.mean()
# ─── вывод ───
# TypeError: Cannot perform reduction 'mean' with string dtype
