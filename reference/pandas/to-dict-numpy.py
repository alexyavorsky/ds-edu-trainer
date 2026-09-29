# Примеры к статье pandas/to-dict-numpy.

# %% setup
prices = pd.DataFrame(
    {"price": [180, 90], "qty": [12, 40]},
    index=["латте", "чай"],
)

# %% to-dict
prices.to_dict()                         # {столбец: {метка: значение}}
# ─── вывод ───
# {'price': {'латте': 180, 'чай': 90}, 'qty': {'латте': 12, 'чай': 40}}

# %% orients
print(prices.to_dict("list"))            # {столбец: [значения]}
print(prices.to_dict("records"))         # [{столбец: значение}, ...] — по строкам
prices.to_dict("index")                  # {метка: {столбец: значение}}
# ─── вывод ───
# {'price': [180, 90], 'qty': [12, 40]}
# [{'price': 180, 'qty': 12}, {'price': 90, 'qty': 40}]
# {'латте': {'price': 180, 'qty': 12}, 'чай': {'price': 90, 'qty': 40}}

# %% series
prices["price"].to_dict()
# ─── вывод ───
# {'латте': 180, 'чай': 90}

# %% to-numpy
prices.to_numpy()
# ─── вывод ───
# array([[180,  12],
#        [ 90,  40]])

# %% mixed
mixed = prices.reset_index()             # появился текстовый столбец
mixed.to_numpy()                         # общий тип — object
# ─── вывод ───
# array([['латте', 180, 12],
#        ['чай', 90, 40]], dtype=object)

# %% tolist
prices["qty"].tolist()                   # обычные int Python
# ─── вывод ───
# [12, 40]

# %% nullable
counts = pd.Series([3, None, 5], dtype="Int64")
print(counts.to_numpy())                 # с пропуском целые стали float
counts.to_numpy(dtype="int64", na_value=0)   # целые, пропуск → 0
# ─── вывод ───
# [ 3. nan  5.]
# array([3, 0, 5])
