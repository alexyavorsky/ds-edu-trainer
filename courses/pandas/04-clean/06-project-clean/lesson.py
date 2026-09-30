# Урок pd-project-clean. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

customers = pd.read_csv("data/customers_raw.csv")
customers.head(8)

# %% info [platform]
customers.info()

# %% survey
print(customers.duplicated().sum())
print(customers["customer_id"].nunique())
customers["city"].value_counts().head(8)

# %% ids [exercise]
customers["customer_id"] = customers["customer_id"].str.strip().str.upper()
customers["name"] = customers["name"].str.strip().str.replace("  ", " ").str.title()
n_ids = customers["customer_id"].nunique()
# ─── заготовка ───
# почистите столбцы customer_id и name
n_ids = ...
# ─── проверка ───
def test_ids():
    "customer_id — без пробелов, заглавная C"
    ids = customers["customer_id"].tolist()
    assert all(i == i.strip() for i in ids), "в customer_id остались пробелы: .str.strip() — и запишите результат обратно в столбец"
    assert all(i == i.upper() for i in ids), "в customer_id остались строчные буквы (c017): .str.upper()"
    assert n_ids != 243 and n_ids != 257, "n_ids нужно считать после очистки: customers[\"customer_id\"].nunique()"
    assert n_ids == 240, f"n_ids = {n_ids!r}, а разных клиентов после очистки 240"


def test_names():
    "name — без лишних пробелов, вид «Имя Ф.»"
    names = customers["name"].tolist()
    assert all(n == n.strip() for n in names), "в name остались пробелы по краям: .str.strip()"
    assert not any("  " in n for n in names), "в name остались двойные пробелы внутри: .str.replace(\"  \", \" \")"
    assert not any(n == n.upper() for n in names), "в name остались имена заглавными буквами (КСЕНИЯ О.): .str.title()"
    assert names[:3] == ["Сергей Ю.", "Сергей В.", "Максим С."], f"первые имена сейчас {names[:3]}"
    assert customers["name"].str.len().sum() == 2249, "не все имена приведены к виду «Имя Ф.»"
# ─── другое решение ───
customers["customer_id"] = customers["customer_id"].str.upper().str.strip()
customers["name"] = customers["name"].str.split().str.join(" ").str.title()
n_ids = len(customers["customer_id"].unique())
# ─── ошибка ───
customers["customer_id"] = customers["customer_id"].str.strip()
customers["name"] = customers["name"].str.strip().str.replace("  ", " ").str.title()
n_ids = customers["customer_id"].nunique()
# ─── ошибка ───
customers["customer_id"] = customers["customer_id"].str.strip().str.upper()
customers["name"] = customers["name"].str.strip().str.title()
n_ids = customers["customer_id"].nunique()

# %% city-before
sorted(customers["city"].str.strip().str.title().unique())

# %% city [exercise]
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers["city"] = customers["city"].str.strip().str.title().replace(short)
customers["segment"] = customers["segment"].str.strip().str.lower()
# ─── заготовка ───
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
# почистите столбцы city и segment
# ─── проверка ───
def test_city():
    "city — пять городов"
    cities = sorted(customers["city"].unique())
    assert not any(c != c.strip() for c in cities), "в city остались пробелы по краям: .str.strip()"
    assert "москва" not in cities and "МОСКВА" not in cities, "в city остались варианты с другим регистром: .str.title()"
    assert "Спб" not in cities and "Екб" not in cities and "С.-Петербург" not in cities, "в city остались сокращения: после .str.title() добавьте .replace(short) — без .str, замена значения целиком"
    assert cities == ["Екатеринбург", "Казань", "Москва", "Новосибирск", "Санкт-Петербург"], f"в city сейчас значения {cities}"


def test_segment():
    "segment — три значения строчными буквами"
    segments = sorted(customers["segment"].unique())
    assert segments == ["новый", "оптовый", "постоянный"], f"в segment сейчас значения {segments}, а нужны три: .str.strip().str.lower()"
# ─── другое решение ───
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers["city"] = customers["city"].str.title().str.strip()
customers["city"] = customers["city"].replace(short)
customers["segment"] = customers["segment"].str.lower().str.strip()
# ─── ошибка ───
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers["city"] = customers["city"].str.strip().str.title()
customers["segment"] = customers["segment"].str.strip().str.lower()
# ─── ошибка ───
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers["city"] = customers["city"].str.strip().str.title().replace(short)
customers["segment"] = customers["segment"].str.lower()

# %% signup [exercise]
iso = pd.to_datetime(customers["signup_date"], format="%Y-%m-%d", errors="coerce")
dotted = pd.to_datetime(customers["signup_date"], format="%d.%m.%Y", errors="coerce")
customers["signup"] = iso.fillna(dotted)
no_date = customers["signup"].isna().sum()
# ─── заготовка ───
# добавьте в customers столбец signup — дату регистрации
no_date = ...
# ─── проверка ───
def test_signup():
    "signup — даты регистрации"
    assert "signup" in customers.columns, "в customers нет столбца signup"
    assert str(customers["signup"].dtype).startswith("datetime64"), f"тип signup — {customers['signup'].dtype}, а нужны даты: pd.to_datetime"
    assert customers["signup"].isna().sum() < 50, "распознан только один формат: соберите оба через fillna — дат с точками в файле тоже много"
    assert customers["signup"].isna().sum() == 6, f"в signup {customers['signup'].isna().sum()} пропусков, а должно остаться 6 — только там, где даты не было"
    assert customers["signup"].max() <= pd.to_datetime("2025-06-30"), "есть даты позже июня 2025 года — день и месяц перепутаны: разбирайте каждый формат явно, с format="
    assert customers["signup"].dt.year.value_counts()[2023] == 109, "даты прочитаны неверно: форматы — \"%Y-%m-%d\" и \"%d.%m.%Y\""


def test_no_date():
    "no_date — у скольких строк даты нет"
    assert no_date == 6, f"no_date = {no_date!r}, а строк без даты регистрации 6"
# ─── другое решение ───
dotted = pd.to_datetime(customers["signup_date"], format="%d.%m.%Y", errors="coerce")
iso = pd.to_datetime(customers["signup_date"], format="%Y-%m-%d", errors="coerce")
customers["signup"] = dotted.fillna(iso)
no_date = len(customers) - customers["signup"].count()
# ─── ошибка ───
customers["signup"] = pd.to_datetime(customers["signup_date"], format="%Y-%m-%d", errors="coerce")
no_date = customers["signup"].isna().sum()
# ─── ошибка ───
customers["signup"] = pd.to_datetime(customers["signup_date"], format="mixed")
no_date = customers["signup"].isna().sum()

# %% bonus-before
customers["bonus"].value_counts().head(8)

# %% points [exercise]
points = pd.to_numeric(customers["bonus"].str.replace(" ", ""), errors="coerce")
customers["points"] = points.fillna(0).astype("int64")
total_points = customers["points"].sum()
# ─── заготовка ───
# добавьте в customers столбец points — бонусные баллы целым числом
total_points = ...
# ─── проверка ───
def test_points():
    "points — баллы целыми числами, «нет» и пропуск — ноль"
    assert "points" in customers.columns, "в customers нет столбца points"
    assert customers["points"].isna().sum() == 0, "в points остались пропуски: «нет» и пустое поле значат ноль баллов — fillna(0)"
    assert str(customers["points"].dtype) in ("int64", "int32"), f"тип points — {customers['points'].dtype}, а нужен целый: после fillna(0) добавьте astype(\"int64\")"
    assert customers["points"].max() == 3100, "наибольшее число баллов должно быть 3100: уберите пробел между тысячами до перевода в числа"
    assert customers.loc[1, "points"] == 2400, f"у клиента в строке 1 баллов {customers.loc[1, 'points']}, а в файле записано «2 400»: .str.replace(\" \", \"\")"


def test_total():
    "total_points — сумма баллов"
    assert total_points != 138910, "значения с пробелом («2 400») превратились в пропуски и потом в нули: сначала .str.replace(\" \", \"\"), потом pd.to_numeric"
    assert total_points == 219360, f"total_points = {total_points!r}, а сумма баллов по всем строкам — 219360"
# ─── другое решение ───
text = customers["bonus"].fillna("0").replace({"нет": "0"}).str.replace(" ", "")
customers["points"] = text.astype("int64")
total_points = sum(customers["points"])
# ─── ошибка ───
customers["points"] = pd.to_numeric(customers["bonus"], errors="coerce").fillna(0).astype("int64")
total_points = customers["points"].sum()
# ─── ошибка ───
customers["points"] = pd.to_numeric(customers["bonus"].str.replace(" ", ""), errors="coerce")
total_points = customers["points"].sum()

# %% email [exercise]
customers["email"] = customers["email"].str.lower()
no_email = customers["email"].isna().sum()
# ─── заготовка ───
# приведите столбец email к строчным буквам
no_email = ...
# ─── проверка ───
def test_email():
    "email — строчными буквами, пропуски остались пропусками"
    known = customers["email"].dropna().tolist()
    assert all(e == e.lower() for e in known), "в email остались заглавные буквы: .str.lower() — и запишите результат обратно"
    assert customers["email"].isna().sum() != 0, "пропуски в email заполнять не нужно: адрес неизвестен, и придумать его нельзя"
    assert customers["email"].isna().sum() == 49, "число пропусков в email изменилось, а должно остаться 49"
    assert no_email == 49, f"no_email = {no_email!r}, а строк без адреса 49"
# ─── другое решение ───
customers["email"] = customers["email"].str.strip().str.lower()
no_email = len(customers) - customers["email"].count()
# ─── ошибка ───
customers["email"] = customers["email"].str.lower().fillna("")
no_email = (customers["email"] == "").sum()

# %% dups
print(customers.duplicated().sum())
print(customers.duplicated(subset=["customer_id"]).sum())

# %% dedupe [exercise]
columns = ["customer_id", "name", "city", "signup", "segment", "email", "points"]
clean = customers[columns].drop_duplicates().sort_values("customer_id").reset_index(drop=True)
# ─── заготовка ───
columns = ["customer_id", "name", "city", "signup", "segment", "email", "points"]
clean = ...
# ─── проверка ───
def test_clean():
    "clean — по одной строке на клиента"
    assert isinstance(clean, pd.DataFrame), f"clean — это {type(clean).__name__}, а нужна таблица"
    assert list(clean.columns) == ["customer_id", "name", "city", "signup", "segment", "email", "points"], f"столбцы сейчас {list(clean.columns)}, а нужны из списка columns"
    assert len(clean) != 257, "в clean все 257 строк: дубликаты не удалены — drop_duplicates()"
    assert len(clean) == 240, f"в clean {len(clean)} строк, а клиентов 240"
    assert clean["customer_id"].nunique() == 240, "в clean повторяются customer_id"


def test_order():
    "clean отсортирована по customer_id, индекс с нуля"
    ids = clean["customer_id"].tolist()
    assert ids == sorted(ids), "clean должна быть отсортирована по customer_id: sort_values(\"customer_id\")"
    assert list(clean.index) == list(range(len(clean))), "индекс clean должен идти с нуля подряд: reset_index(drop=True) — после сортировки"
# ─── другое решение ───
columns = ["customer_id", "name", "city", "signup", "segment", "email", "points"]
clean = customers.drop_duplicates(subset=["customer_id"])[columns].sort_values("customer_id").reset_index(drop=True)
# ─── ошибка ───
columns = ["customer_id", "name", "city", "signup", "segment", "email", "points"]
clean = customers[columns].sort_values("customer_id").reset_index(drop=True)
# ─── ошибка ───
columns = ["customer_id", "name", "city", "signup", "segment", "email", "points"]
clean = customers[columns].drop_duplicates().reset_index(drop=True).sort_values("customer_id")

# %% check
reference = pd.read_csv("data/customers.csv")
print((clean["customer_id"] == reference["customer_id"]).all())
print((clean["name"] == reference["name"]).all())
print((clean["city"] == reference["city"]).all())
print((clean["segment"] == reference["segment"]).all())

# %% report [exercise]
by_city = clean["city"].value_counts()
wholesale = clean[clean["segment"] == "оптовый"]
avg_points = clean["points"].mean()
# ─── заготовка ───
by_city = ...
wholesale = ...
avg_points = ...
# ─── проверка ───
def test_city():
    "by_city — клиентов по городам"
    assert isinstance(by_city, pd.Series), f"by_city — это {type(by_city).__name__}, а нужен результат value_counts()"
    assert by_city.sum() == 240, f"в by_city всего {by_city.sum()} клиентов, а в clean их 240: считайте по таблице clean"
    assert len(by_city) == 5 and by_city["Москва"] == 89, "числа не те: clean[\"city\"].value_counts()"


def test_rest():
    "wholesale — оптовые клиенты, avg_points — средний бонус"
    assert isinstance(wholesale, pd.DataFrame), f"wholesale — это {type(wholesale).__name__}, а нужна таблица: clean[маска]"
    assert len(wholesale) == 26 and (wholesale["segment"] == "оптовый").all(), f"в wholesale {len(wholesale)} строк, а оптовых клиентов 26"
    assert abs(avg_points - 862.1666667) < 1e-4, f"avg_points = {avg_points!r}, а средний бонус ≈ 862.17: clean[\"points\"].mean()"
# ─── другое решение ───
by_city = clean.value_counts("city")
wholesale = clean.query("segment == 'оптовый'")
avg_points = clean["points"].sum() / len(clean)
# ─── ошибка ───
by_city = customers["city"].value_counts()
wholesale = customers[customers["segment"] == "оптовый"]
avg_points = customers["points"].mean()

# %% summary
print("строк в выгрузке:", len(customers), "→ клиентов:", len(clean))
print("без даты регистрации:", clean["signup"].isna().sum(), "· без email:", clean["email"].isna().sum())
print("оптовых:", len(wholesale), "· средний бонус:", round(avg_points))
print(by_city)
