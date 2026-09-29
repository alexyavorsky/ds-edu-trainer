# Примеры к статье pandas/copy-on-write.

# %% setup
stock = pd.DataFrame({"item": ["латте", "чай", "раф"], "qty": [12, 40, 7]})

# %% subset
low = stock[stock["qty"] < 20]
low["qty"] = 0                           # меняем выборку…
stock                                    # …исходная таблица не изменилась
# ─── вывод ───
#     item  qty
# 0  латте   12
# 1    чай   40
# 2    раф    7

# %% column
qty = stock["qty"]
qty[0] = 999                             # Series из столбца — тоже как копия
stock
# ─── вывод ───
#     item  qty
# 0  латте   12
# 1    чай   40
# 2    раф    7

# %% chained [warns]
stock["qty"][0] = 100                    # цепочечное присваивание: две пары скобок
stock                                    # ничего не изменилось
# ─── вывод ───
# ChainedAssignmentError: A value is being set on a copy of a DataFrame or Series through chained assignment.
# Such chained assignment never works to update the original DataFrame or Series, because the intermediate object on which we are setting values always behaves as a copy (due to Copy-on-Write).
#
# Try using '.loc[row_indexer, col_indexer] = value' instead, to perform the assignment in a single step.
#
# See the documentation for a more detailed explanation: https://pandas.pydata.org/pandas-docs/stable/user_guide/copy_on_write.html#chained-assignment
#     item  qty
# 0  латте   12
# 1    чай   40
# 2    раф    7

# %% loc
stock.loc[0, "qty"] = 100                # правильно: одна операция loc
stock.loc[stock["item"] == "чай", "qty"] += 5
stock
# ─── вывод ───
#     item  qty
# 0  латте  100
# 1    чай   45
# 2    раф    7

# %% lazy-copy
same = stock.reset_index(drop=True)
print(np.shares_memory(stock["qty"].to_numpy(), same["qty"].to_numpy()))   # пока данные общие
same.loc[0, "qty"] = -1                                                    # копия — при изменении
np.shares_memory(stock["qty"].to_numpy(), same["qty"].to_numpy())
# ─── вывод ───
# True
# False

# %% readonly [raises=ValueError]
arr = stock["qty"].to_numpy()
arr[0] = 5                               # массив смотрит в данные таблицы — только чтение
# ─── вывод ───
# ValueError: assignment destination is read-only

# %% option [deprecated]
pd.set_option("mode.copy_on_write", False)   # отключить Copy-on-Write нельзя
# ─── вывод ───
# Pandas4Warning: The 'mode.copy_on_write' option is deprecated. Copy-on-Write can no longer be disabled (it is always enabled with pandas >= 3.0), and setting the option has no impact. This option will be removed in pandas 4.0.

# %% no-warning-class [raises=AttributeError]
pd.errors.SettingWithCopyWarning
# ─── вывод ───
# AttributeError: module 'pandas.errors' has no attribute 'SettingWithCopyWarning'
