# Примеры к статье pandas/loc-iloc.

# %% setup
stock = pd.DataFrame(
    {"price": [180, 90, 220, 150], "qty": [12, 40, 7, 20], "shelf": ["A", "B", "A", "C"]},
    index=["латте", "чай", "раф", "какао"],
)

# %% loc-row
stock.loc["чай"]                        # строка по метке — Series
# ─── вывод ───
# price    90
# qty      40
# shelf     B
# Name: чай, dtype: object

# %% loc-cell
stock.loc["раф", "price"]               # одна ячейка
# ─── вывод ───
# np.int64(220)

# %% loc-slice
stock.loc["чай":"какао", ["price", "qty"]]   # срез по меткам ВКЛЮЧАЕТ конец
# ─── вывод ───
#        price  qty
# чай       90   40
# раф      220    7
# какао    150   20

# %% iloc
print(stock.iloc[0])                    # первая строка
stock.iloc[1:3, :2]                     # строки 1–2, столбцы 0–1: конец не входит
# ─── вывод ───
# price    180
# qty       12
# shelf      A
# Name: латте, dtype: object
#      price  qty
# чай     90   40
# раф    220    7

# %% mask
stock.loc[stock["qty"] < 15, "price"]   # строки по условию, один столбец
# ─── вывод ───
# латте    180
# раф      220
# Name: price, dtype: int64

# %% set
stock.loc["чай", "price"] = 95          # изменить ячейку
stock.loc[stock["shelf"] == "A", "qty"] += 5
stock
# ─── вывод ───
#        price  qty shelf
# латте    180   17     A
# чай       95   40     B
# раф      220   12     A
# какао    150   20     C

# %% at-iat
print(stock.at["латте", "qty"])         # одна ячейка по метке — быстрее loc
stock.iat[0, 1]                         # одна ячейка по позиции
# ─── вывод ───
# 12
# np.int64(12)

# %% new-row
stock.loc["мокко"] = [200, 5, "B"]      # несуществующая метка — новая строка
stock
# ─── вывод ───
#        price  qty shelf
# латте    180   12     A
# чай       90   40     B
# раф      220    7     A
# какао    150   20     C
# мокко    200    5     B

# %% iloc-label [raises=TypeError]
stock.iloc["чай"]                       # iloc понимает только позиции
# ─── вывод ───
# TypeError: Cannot index by location index with a non-integer key
