# Примеры к статье pandas/method-chaining.

# %% setup
raw = pd.DataFrame({
    "Город": ["омск", "тула", "омск", "сочи", "тула", "омск"],
    "Чашки": [30, 12, None, 25, 20, 16],
    "Цена": [180, 165, 180, 210, 165, 190],
})

# %% steps
df = raw.rename(columns={"Город": "city", "Чашки": "cups", "Цена": "price"})
df = df.dropna(subset=["cups"])
df["city"] = df["city"].str.title()
df["revenue"] = df["cups"] * df["price"]
df = df[df["revenue"] > 3000]
df.groupby("city")["revenue"].sum()
# ─── вывод ───
# city
# Омск    8440.0
# Сочи    5250.0
# Тула    3300.0
# Name: revenue, dtype: float64

# %% chain
(
    raw
    .rename(columns={"Город": "city", "Чашки": "cups", "Цена": "price"})
    .dropna(subset=["cups"])
    .assign(
        city=lambda d: d["city"].str.title(),
        revenue=lambda d: d["cups"] * d["price"],
    )
    .query("revenue > 3000")
    .groupby("city")["revenue"]
    .sum()
)
# ─── вывод ───
# city
# Омск    8440.0
# Сочи    5250.0
# Тула    3300.0
# Name: revenue, dtype: float64

# %% pd-col
(
    raw
    .rename(columns={"Город": "city", "Чашки": "cups", "Цена": "price"})
    .assign(revenue=pd.col("cups") * pd.col("price"))   # pandas 3.0
    .loc[lambda d: d["revenue"] > 3000, ["city", "revenue"]]
)
# ─── вывод ───
#    city  revenue
# 0  омск   5400.0
# 3  сочи   5250.0
# 4  тула   3300.0
# 5  омск   3040.0

# %% pipe
def top(df, n, by):
    return df.nlargest(n, by)

(
    raw
    .rename(columns={"Город": "city", "Чашки": "cups"})
    .pipe(top, n=2, by="cups")
)
# ─── вывод ───
#    city  cups  Цена
# 0  омск  30.0   180
# 3  сочи  25.0   210

# %% debug
def show_shape(df, label):
    print(label, df.shape)
    return df

(
    raw
    .pipe(show_shape, "исходно:")
    .dropna()
    .pipe(show_shape, "без пропусков:")
    .query("Цена > 170")
    .pipe(show_shape, "дороже 170:")
    ["Чашки"].sum()
)
# ─── вывод ───
# исходно: (6, 3)
# без пропусков: (5, 3)
# дороже 170: (3, 3)
# np.float64(71.0)
