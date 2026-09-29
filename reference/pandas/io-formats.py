# Примеры к статье pandas/io-formats.
# Каждый пример выполняется в своей временной папке.

# %% setup
from io import StringIO

sales = pd.DataFrame({
    "city": ["Омск", "Тула"],
    "date": pd.to_datetime(["2024-03-01", "2024-03-02"]),
    "cups": [120, 85],
})

# %% excel
sales.to_excel("report.xlsx", sheet_name="март", index=False)
pd.read_excel("report.xlsx", sheet_name="март")
# ─── вывод ───
#    city       date  cups
# 0  Омск 2024-03-01   120
# 1  Тула 2024-03-02    85

# %% excel-sheets
with pd.ExcelWriter("report.xlsx") as writer:
    sales.to_excel(writer, sheet_name="март", index=False)
    sales.head(1).to_excel(writer, sheet_name="итоги", index=False)
sheets = pd.read_excel("report.xlsx", sheet_name=None)   # все листы — словарь
list(sheets)
# ─── вывод ───
# ['март', 'итоги']

# %% json
text = sales.to_json(orient="records", force_ascii=False, date_format="iso")
print(text)
pd.read_json(StringIO(text), orient="records")
# ─── вывод ───
# [{"city":"Омск","date":"2024-03-01T00:00:00.000","cups":120},{"city":"Тула","date":"2024-03-02T00:00:00.000","cups":85}]
#    city       date  cups
# 0  Омск 2024-03-01   120
# 1  Тула 2024-03-02    85

# %% json-lines
sales.to_json("log.jsonl", orient="records", lines=True, force_ascii=False, date_format="iso")
with open("log.jsonl", encoding="utf-8") as f:
    print(f.read())
pd.read_json("log.jsonl", lines=True)
# ─── вывод ───
# {"city":"Омск","date":"2024-03-01T00:00:00.000","cups":120}
# {"city":"Тула","date":"2024-03-02T00:00:00.000","cups":85}
#
#    city       date  cups
# 0  Омск 2024-03-01   120
# 1  Тула 2024-03-02    85

# %% parquet
sales.to_parquet("sales.parquet")
pd.read_parquet("sales.parquet").dtypes              # типы, включая даты, сохранены
# ─── вывод ───
# city               str
# date    datetime64[us]
# cups             int64
# dtype: object

# %% csv-loses-types
sales.to_csv("sales.csv", index=False)
pd.read_csv("sales.csv").dtypes                      # дата снова строка
# ─── вывод ───
# city      str
# date      str
# cups    int64
# dtype: object

# %% json-string [raises=FileNotFoundError]
pd.read_json('[{"city": "Омск"}]')                   # строку воспринимает как путь к файлу
# ─── вывод ───
# FileNotFoundError: File [{"city": "Омск"}] does not exist
