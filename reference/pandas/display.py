# Примеры к статье pandas/display.

# %% setup
orders = pd.DataFrame({
    "order": range(1, 101),
    "amount": [round(100 + i * 12.345, 3) for i in range(100)],
})

# %% truncated
orders                                   # 100 строк > max_rows: показаны края
# ─── вывод ───
#     order    amount
# 0       1   100.000
# 1       2   112.345
# 2       3   124.690
# 3       4   137.035
# 4       5   149.380
# ..    ...       ...
# 95     96  1272.775
# 96     97  1285.120
# 97     98  1297.465
# 98     99  1309.810
# 99    100  1322.155
#
# [100 rows x 2 columns]

# %% option-context
with pd.option_context("display.max_rows", 6, "display.min_rows", 4):
    print(orders)
# ─── вывод ───
#     order    amount
# 0       1   100.000
# 1       2   112.345
# ..    ...       ...
# 98     99  1309.810
# 99    100  1322.155
#
# [100 rows x 2 columns]

# %% precision
ratios = pd.DataFrame({"share": [1 / 3, 2 / 3, 1 / 7]})
with pd.option_context("display.precision", 2):
    print(ratios)
ratios.loc[0, "share"]                   # данные не округлены
# ─── вывод ───
#    share
# 0   0.33
# 1   0.67
# 2   0.14
# np.float64(0.3333333333333333)

# %% float-format
with pd.option_context("display.float_format", "{:,.1f}".format):
    print(orders.tail(3))
# ─── вывод ───
#     order  amount
# 97     98 1,297.5
# 98     99 1,309.8
# 99    100 1,322.2

# %% wide
wide = pd.DataFrame([range(30)], columns=[f"c{i}" for i in range(30)])
wide                                     # 30 столбцов > max_columns
# ─── вывод ───
#    c0  c1  c2  c3  c4  c5  c6  c7  c8  c9  ...  c20  c21  c22  c23  c24  c25  \
# 0   0   1   2   3   4   5   6   7   8   9  ...   20   21   22   23   24   25
#
#    c26  c27  c28  c29
# 0   26   27   28   29
#
# [1 rows x 30 columns]

# %% colwidth
notes = pd.DataFrame({"note": ["Очень длинный комментарий покупателя о доставке и упаковке заказа"]})
with pd.option_context("display.max_colwidth", 25):
    print(notes)
# ─── вывод ───
#                        note
# 0  Очень длинный коммент...

# %% get-option
pd.get_option("display.max_rows")
# ─── вывод ───
# 60

# %% to-string
print(orders.head(12).to_string(index=False, max_rows=6))
# ─── вывод ───
#  order  amount
#      1 100.000
#      2 112.345
#      3 124.690
#    ...     ...
#     10 211.105
#     11 223.450
#     12 235.795
