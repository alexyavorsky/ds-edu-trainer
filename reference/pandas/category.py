# Примеры к статье pandas/category.

# %% setup
sizes = pd.Series(["M", "S", "L", "M", "M", "S"], name="size")

# %% create
cat = sizes.astype("category")
print(cat.cat.categories)            # набор допустимых значений
cat.cat.codes.tolist()               # внутри хранятся номера
# ─── вывод ───
# Index(['L', 'M', 'S'], dtype='str')
# [1, 2, 0, 1, 1, 2]

# %% ordered
order = pd.CategoricalDtype(["S", "M", "L"], ordered=True)
ordered = sizes.astype(order)
print(ordered.sort_values().tolist())   # по заданному порядку, а не по алфавиту
ordered[ordered > "S"].tolist()          # сравнения по порядку
# ─── вывод ───
# ['S', 'S', 'M', 'M', 'M', 'L']
# ['M', 'L', 'M', 'M']

# %% memory
big = pd.Series(["Москва", "Санкт-Петербург", "Казань"] * 100_000)
before = big.memory_usage(deep=True, index=False)
after = big.astype("category").memory_usage(deep=True, index=False)
print(f"{before / 2**20:.1f} МБ → {after / 2**20:.1f} МБ")
before // after                      # во сколько раз меньше
# ─── вывод ───
# 7.3 МБ → 0.3 МБ
# 25

# %% groupby
cat = sizes.astype(pd.CategoricalDtype(["S", "M", "L", "XL"]))
print(cat.value_counts())                          # value_counts показывает и пустую категорию
pd.DataFrame({"size": cat, "n": 1}).groupby("size").size()   # groupby — нет (observed=True)
# ─── вывод ───
# size
# M     3
# S     2
# L     1
# XL    0
# Name: count, dtype: int64
# size
# S    2
# M    3
# L    1
# dtype: int64

# %% new-value [raises=TypeError]
cat = sizes.astype("category")
cat[0] = "XXL"                                     # значения нет среди категорий
# ─── вывод ───
# TypeError: Cannot setitem on a Categorical with a new category (XXL), set the categories first

# %% add-category
cat = sizes.astype("category").cat.add_categories(["XXL"])
cat[0] = "XXL"
cat.tolist()
# ─── вывод ───
# ['XXL', 'S', 'L', 'M', 'M', 'S']

# %% unique-values
ids = pd.Series([f"id{i}" for i in range(10_000)])   # 10 000 разных строк
before = ids.memory_usage(deep=True, index=False)
after = ids.astype("category").memory_usage(deep=True, index=False)
after > before
# ─── вывод ───
# True
