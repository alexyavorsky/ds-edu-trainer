# Урок pd-project-clean (часть 1). Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
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

# %% text-done
print(customers["customer_id"].nunique(), customers["city"].nunique(), customers["segment"].nunique())
print(customers.duplicated().sum())
customers["city"].value_counts()
