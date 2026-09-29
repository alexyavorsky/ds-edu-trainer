# Примеры к статье pandas/series.

# %% from-list
pd.Series([12, 15, 9])                            # индекс по умолчанию 0, 1, 2
# ─── вывод ───
# 0    12
# 1    15
# 2     9
# dtype: int64

# %% with-index
visits = pd.Series([120, 85, 240], index=["пн", "вт", "ср"], name="visits")
visits
# ─── вывод ───
# пн    120
# вт     85
# ср    240
# Name: visits, dtype: int64

# %% from-dict
pd.Series({"Омск": 1.2, "Тула": 0.5, "Сочи": 0.4})   # ключи стали индексом
# ─── вывод ───
# Омск    1.2
# Тула    0.5
# Сочи    0.4
# dtype: float64

# %% scalar
pd.Series(0, index=["a", "b", "c"])
# ─── вывод ───
# a    0
# b    0
# c    0
# dtype: int64

# %% access
visits = pd.Series([120, 85, 240], index=["пн", "вт", "ср"])
print(visits["вт"])           # по метке
print(visits.iloc[0])         # по позиции
visits[visits > 100]          # по условию
# ─── вывод ───
# 85
# 120
# пн    120
# ср    240
# dtype: int64

# %% parts
visits = pd.Series([120, 85, 240], index=["пн", "вт", "ср"], name="visits")
print(visits.index)
print(visits.to_numpy())
visits.name, visits.dtype
# ─── вывод ───
# Index(['пн', 'вт', 'ср'], dtype='str')
# [120  85 240]
# ('visits', dtype('int64'))

# %% none-to-nan
pd.Series([3, None, 5])        # пропуск превращает целые в float
# ─── вывод ───
# 0    3.0
# 1    NaN
# 2    5.0
# dtype: float64

# %% positional [raises=KeyError]
visits = pd.Series([120, 85, 240], index=["пн", "вт", "ср"])
visits[0]                      # 0 — это метка, а такой метки нет
# ─── вывод ───
# KeyError: 0
