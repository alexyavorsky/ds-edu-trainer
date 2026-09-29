# Примеры к статье pandas/corr.

# %% setup
cafe = pd.DataFrame({
    "temp":   [12, 15, 18, 22, 25, 28, 31],     # температура
    "iced":   [20, 28, 35, 52, 60, 71, 80],     # холодные напитки
    "hot":    [95, 90, 82, 70, 64, 55, 50],     # горячие напитки
    "promo":  [0, 1, 0, 1, 0, 1, 0],            # была ли акция
})

# %% matrix
cafe.corr().round(2)
# ─── вывод ───
#        temp  iced   hot  promo
# temp   1.00  1.00 -1.00   0.01
# iced   1.00  1.00 -1.00   0.04
# hot   -1.00 -1.00  1.00  -0.03
# promo  0.01  0.04 -0.03   1.00

# %% pair
cafe["temp"].corr(cafe["iced"]).round(3)
# ─── вывод ───
# np.float64(0.998)

# %% spearman
rank_data = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [1, 4, 9, 16, 100]})
print(rank_data.corr().loc["x", "y"].round(3))                     # Пирсон: линейная связь
rank_data.corr(method="spearman").loc["x", "y"]                    # Спирмен: монотонная
# ─── вывод ───
# 0.795
# np.float64(1.0)

# %% corrwith
targets = cafe[["iced", "hot"]]
targets.corrwith(cafe["temp"]).round(2)
# ─── вывод ───
# iced    1.0
# hot    -1.0
# dtype: float64

# %% cov
cafe[["temp", "iced"]].cov()
# ─── вывод ───
#             temp        iced
# temp   48.285714  156.380952
# iced  156.380952  508.619048

# %% nonlinear
x = pd.Series(range(-5, 6))
y = x ** 2                                                          # сильная, но не линейная связь
x.corr(y)
# ─── вывод ───
# np.float64(0.0)

# %% text
cafe.assign(day=list("пвсчпсв")).corr(numeric_only=True).shape     # текст исключён
# ─── вывод ───
# (4, 4)
