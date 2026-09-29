# Примеры к статье pandas/read-csv.
# Каждый пример выполняется в своей временной папке; файлы создаёт setup.

# %% setup
from pathlib import Path

Path("sales.csv").write_text(
    "date,city,cups,price\n"
    "2024-03-01,Омск,120,180.5\n"
    "2024-03-01,Тула,85,\n"
    "2024-03-02,Омск,132,181.0\n",
    encoding="utf-8",
)
Path("excel_ru.csv").write_text(      # так сохраняет CSV русский Excel
    "Город;Выручка\n"
    "Омск;1 250,50\n"
    "Тула;980,00\n",
    encoding="utf-8",
)

# %% basic
pd.read_csv("sales.csv")
# ─── вывод ───
#          date  city  cups  price
# 0  2024-03-01  Омск   120  180.5
# 1  2024-03-01  Тула    85    NaN
# 2  2024-03-02  Омск   132  181.0

# %% dtypes
pd.read_csv("sales.csv").dtypes
# ─── вывод ───
# date         str
# city         str
# cups       int64
# price    float64
# dtype: object

# %% usecols-index
pd.read_csv("sales.csv", usecols=["city", "cups"], nrows=2)
# ─── вывод ───
#    city  cups
# 0  Омск   120
# 1  Тула    85

# %% parse-dates
df = pd.read_csv("sales.csv", parse_dates=["date"], index_col="date")
print(df.index.dtype)
df
# ─── вывод ───
# datetime64[us]
#             city  cups  price
# date
# 2024-03-01  Омск   120  180.5
# 2024-03-01  Тула    85    NaN
# 2024-03-02  Омск   132  181.0

# %% russian-excel
pd.read_csv("excel_ru.csv", sep=";", decimal=",", thousands=" ")
# ─── вывод ───
#   Город  Выручка
# 0  Омск   1250.5
# 1  Тула    980.0

# %% names
pd.read_csv("sales.csv", header=0, names=["день", "город", "чашки", "цена"])
# ─── вывод ───
#          день город  чашки   цена
# 0  2024-03-01  Омск    120  180.5
# 1  2024-03-01  Тула     85    NaN
# 2  2024-03-02  Омск    132  181.0

# %% na-values
pd.read_csv("sales.csv", na_values={"cups": [85]})   # 85 считать пропуском
# ─── вывод ───
#          date  city   cups  price
# 0  2024-03-01  Омск  120.0  180.5
# 1  2024-03-01  Тула    NaN    NaN
# 2  2024-03-02  Омск  132.0  181.0

# %% to-csv
df = pd.read_csv("sales.csv")
df.to_csv("out.csv", index=False)
print(Path("out.csv").read_text())
# ─── вывод ───
# date,city,cups,price
# 2024-03-01,Омск,120,180.5
# 2024-03-01,Тула,85,
# 2024-03-02,Омск,132,181.0

# %% index-column
df = pd.read_csv("sales.csv")
df.to_csv("out.csv")                  # индекс записан первым столбцом
pd.read_csv("out.csv").columns
# ─── вывод ───
# Index(['Unnamed: 0', 'date', 'city', 'cups', 'price'], dtype='str')

# %% encoding [raises=UnicodeDecodeError]
Path("win.csv").write_text("Город\nОмск\n", encoding="cp1251")
pd.read_csv("win.csv")                # по умолчанию ожидается UTF-8
# ─── вывод ───
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc3 in position 0: invalid continuation byte
