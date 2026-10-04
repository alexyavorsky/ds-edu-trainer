# Урок pd-project-clean-2 (часть 2). Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% prepare
import pandas as pd

customers = pd.read_csv("data/customers_raw.csv")
raw_duplicates = customers.duplicated().sum()
short = {"Спб": "Санкт-Петербург", "С.-Петербург": "Санкт-Петербург", "Екб": "Екатеринбург"}
customers["customer_id"] = customers["customer_id"].str.strip().str.upper()
customers["name"] = customers["name"].str.strip().str.replace("  ", " ").str.title()
customers["city"] = customers["city"].str.strip().str.title().replace(short)
customers["segment"] = customers["segment"].str.strip().str.lower()
customers["email"] = customers["email"].str.lower()
print("полных повторов в сырой выгрузке:", raw_duplicates)
customers.head(5)

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
    assert str(customers["signup"].dtype).startswith("datetime64"), f"тип signup — {customers['signup'].dtype}, а нужны даты"
    assert customers["signup"].isna().sum() < 50, "распознан только один формат: соберите оба через fillna — дат с точками в файле тоже много"
    assert customers["signup"].isna().sum() == 6, f"в signup {customers['signup'].isna().sum()} пропусков: пропуски должны остаться только там, где даты не было"
    assert customers["signup"].max() <= pd.to_datetime("2025-06-30"), "есть даты позже июня 2025 года — день и месяц перепутаны: разбирайте каждый формат явно"
    assert customers["signup"].dt.year.value_counts()[2023] == 109, "даты прочитаны неверно: проверьте оба формата"


def test_no_date():
    "no_date — у скольких строк даты нет"
    assert no_date == 6, f"no_date = {no_date!r} — это не число строк без даты регистрации"
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
print("пустых полей:", customers["bonus"].isna().sum())
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
    assert customers["points"].isna().sum() == 0, "в points остались пропуски: «нет» и пустое поле значат ноль баллов"
    assert str(customers["points"].dtype) in ("int64", "int32"), f"тип points — {customers['points'].dtype}, а нужен целый"
    assert customers["points"].max() == 3100, "баллы с пробелом между тысячами потерялись: уберите пробел до перевода в числа"
    assert customers.loc[1, "points"] == 2400, f"у клиента в строке 1 баллов {customers.loc[1, 'points']}, а в файле записано «2 400»: уберите пробел до перевода в числа"


def test_total():
    "total_points — сумма баллов"
    assert total_points != 138910, "значения с пробелом («2 400») превратились в пропуски и потом в нули: сначала уберите пробел, потом переводите в числа"
    assert total_points == 219360, f"total_points = {total_points!r} не совпадает с суммой баллов всех строк: проверьте, что points посчитан для каждой строки"
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
    assert len(clean) != 257, "в clean все 257 строк: дубликаты не удалены"
    assert len(clean) != 245, "осталось 5 лишних строк: drop_duplicates вызван до отбора columns — сравнились и сырые signup_date и bonus"
    assert len(clean) == 240, f"в clean {len(clean)} строк — должна остаться одна строка на клиента"
    assert clean["customer_id"].nunique() == 240, "в clean повторяются customer_id"


def test_order():
    "clean отсортирована по customer_id, индекс с нуля"
    ids = clean["customer_id"].tolist()
    assert ids == sorted(ids), "clean должна быть отсортирована по customer_id"
    assert list(clean.index) == list(range(len(clean))), "индекс clean должен идти с нуля подряд: сбросьте индекс после сортировки"
# ─── другое решение ───
columns = ["customer_id", "name", "city", "signup", "segment", "email", "points"]
clean = customers.drop_duplicates(subset=["customer_id"])[columns].sort_values("customer_id").reset_index(drop=True)
# ─── ошибка ───
columns = ["customer_id", "name", "city", "signup", "segment", "email", "points"]
clean = customers[columns].sort_values("customer_id").reset_index(drop=True)
# ─── ошибка ───
columns = ["customer_id", "name", "city", "signup", "segment", "email", "points"]
clean = customers.drop_duplicates()[columns].sort_values("customer_id").reset_index(drop=True)
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
    assert by_city.sum() == 240, f"в by_city всего {by_city.sum()} клиентов: считайте по таблице clean"
    assert len(by_city) == 5 and by_city["Москва"] == 89, "числа не те: нужны подсчёты по столбцу city таблицы clean"


def test_rest():
    "wholesale — оптовые клиенты, avg_points — средний бонус"
    assert isinstance(wholesale, pd.DataFrame), f"wholesale — это {type(wholesale).__name__}, а нужна таблица"
    assert len(wholesale) == 26 and (wholesale["segment"] == "оптовый").all(), f"в wholesale {len(wholesale)} строк — нужны оптовые клиенты из clean"
    assert abs(avg_points - 862.1666667) < 1e-4, f"avg_points = {avg_points!r} — это не средний бонус клиентов clean"
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
