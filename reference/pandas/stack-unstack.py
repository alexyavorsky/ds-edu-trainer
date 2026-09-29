# Примеры к статье pandas/stack-unstack.

# %% setup
wide = pd.DataFrame(
    {"jan": [120, 95], "feb": [130, 105]},
    index=pd.Index(["Омск", "Тула"], name="city"),
)
wide.columns.name = "month"

# %% stack
wide.stack()                             # столбцы → внутренний уровень индекса
# ─── вывод ───
# city  month
# Омск  jan      120
#       feb      130
# Тула  jan       95
#       feb      105
# dtype: int64

# %% unstack
wide.stack().unstack()                   # внутренний уровень индекса → столбцы
# ─── вывод ───
# month  jan  feb
# city
# Омск   120  130
# Тула    95  105

# %% unstack-level
wide.stack().unstack(level="city")       # в столбцы можно перенести любой уровень
# ─── вывод ───
# city   Омск  Тула
# month
# jan     120    95
# feb     130   105

# %% groupby
sales = pd.DataFrame({
    "city": ["Омск", "Омск", "Тула", "Тула", "Омск"],
    "drink": ["латте", "чай", "латте", "латте", "латте"],
    "cups": [30, 12, 18, 25, 20],
})
sales.groupby(["city", "drink"])["cups"].sum().unstack(fill_value=0)   # частый приём после groupby
# ─── вывод ───
# drink  латте  чай
# city
# Омск      50   12
# Тула      43    0

# %% nan-kept
with_gap = wide.astype(float)
with_gap.loc["Тула", "feb"] = np.nan
with_gap.stack()                         # pandas 3: строка с NaN сохраняется
# ─── вывод ───
# city  month
# Омск  jan      120.0
#       feb      130.0
# Тула  jan       95.0
#       feb        NaN
# dtype: float64

# %% dropna-arg [raises=ValueError]
wide.stack(dropna=True)
# ─── вывод ───
# ValueError: dropna must be unspecified as the new implementation does not introduce rows of NA values. This argument will be removed in a future version of pandas.
