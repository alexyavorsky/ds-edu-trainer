# Примеры к статье numpy/masked.

# %% setup
# количество заказов по дням; -1 — магазин закрыт, данных нет
orders = np.array([12, 15, -1, 9, -1, 20])

# %% create
m = np.ma.masked_array(orders, mask=orders < 0)
m
# ─── вывод ───
# masked_array(data=[12, 15, --, 9, --, 20],
#              mask=[False, False,  True, False,  True, False],
#        fill_value=999999)

# %% aggregations
m = np.ma.masked_equal(orders, -1)
print(m.mean(), m.sum(), m.count())     # маскированные элементы не учитываются
orders.mean()                           # обычный массив учитывает −1
# ─── вывод ───
# 14.0 56 4
# np.float64(9.0)

# %% invalid
temps = np.array([12.5, np.nan, 14.0, np.inf])
np.ma.masked_invalid(temps).mean()      # маскирует NaN и inf
# ─── вывод ───
# np.float64(13.25)

# %% arithmetic
m = np.ma.masked_equal(orders, -1)
m * 10                                  # маска сохраняется
# ─── вывод ───
# masked_array(data=[120, 150, --, 90, --, 200],
#              mask=[False, False,  True, False,  True, False],
#        fill_value=-1)

# %% filled
m = np.ma.masked_equal(orders, -1)
print(m.filled(0))                      # обычный массив, пропуски — 0
m.compressed()                          # только известные значения
# ─── вывод ───
# [12 15  0  9  0 20]
# array([12, 15,  9, 20])

# %% int-missing
m = np.ma.masked_equal(orders, -1)
m.dtype                                 # тип остался целым — в отличие от замены на NaN
# ─── вывод ───
# dtype('int64')

# %% outside-ma
m = np.ma.masked_equal(orders, -1)
print(np.concatenate([m, m]).mean())     # маска потеряна: −1 участвуют в среднем
np.ma.concatenate([m, m]).mean()
# ─── вывод ───
# 9.0
# np.float64(14.0)
