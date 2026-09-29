# Примеры к статье numpy/statistics.

# %% setup
salaries = np.array([52, 48, 61, 55, 300, 58, 50])   # тыс. руб.; один руководитель

# %% center
print(np.mean(salaries))       # выброс сильно тянет среднее
np.median(salaries)            # медиана устойчива к выбросам
# ─── вывод ───
# 89.14285714285714
# np.float64(55.0)

# %% spread
print(np.std(salaries))        # ddof=0 — по генеральной совокупности
np.std(salaries, ddof=1)       # ddof=1 — выборочное, как в pandas
# ─── вывод ───
# 86.18324094862159
# np.float64(93.08853952273712)

# %% percentile
print(np.percentile(salaries, [25, 50, 75]))
np.quantile(salaries, 0.9)     # то же, но в долях
# ─── вывод ───
# [51.  55.  59.5]
# np.float64(156.60000000000008)

# %% method
data = np.array([1, 2, 3, 4])
print(np.percentile(data, 50))                    # linear: между 2 и 3
np.percentile(data, 50, method="lower")           # ближайшее снизу из данных
# ─── вывод ───
# 2.5
# np.int64(2)

# %% average
grades = np.array([5, 4, 3])
weights = np.array([2, 1, 1])  # вес оценки
np.average(grades, weights=weights)
# ─── вывод ───
# np.float64(4.25)

# %% corrcoef
hours = np.array([1, 2, 3, 4, 5])
score = np.array([52, 55, 61, 70, 74])
print(np.corrcoef(hours, score).round(3))         # матрица 2 × 2
np.cov(hours, score)
# ─── вывод ───
# [[1.    0.987]
#  [0.987 1.   ]]
# array([[ 2.5 , 14.75],
#        [14.75, 89.3 ]])

# %% interpolation-removed [raises=TypeError]
np.percentile(salaries, 50, interpolation="lower")
# ─── вывод ───
# TypeError: percentile() got an unexpected keyword argument 'interpolation'
