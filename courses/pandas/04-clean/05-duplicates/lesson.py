# Урок pd-duplicates. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

returns = pd.read_csv("data/returns_raw.csv")
print(len(returns))
returns.head(4)

# %% small
visits = pd.DataFrame({
    "client": ["Анна", "Олег", "Анна", "Анна", "Олег"],
    "drink": ["латте", "эспрессо", "латте", "какао", "эспрессо"],
})
visits["repeat"] = visits.duplicated()
visits

# %% count
print(visits["repeat"].sum())

# %% show
returns[returns.duplicated(keep=False)].sort_values("return_id").head(6)

# %% exact [exercise]
n_exact = returns.duplicated().sum()
unique_rows = returns.drop_duplicates()
# ─── заготовка ───
n_exact = ...
unique_rows = ...
# ─── проверка ───
def test_count():
    "n_exact — сколько строк-повторов"
    assert n_exact != 14, "14 — все строки, у которых есть двойник; лишних строк вдвое меньше"
    assert n_exact == 7, f"n_exact = {n_exact!r} — это не число строк-повторов"


def test_unique():
    "unique_rows — таблица без полных повторов"
    assert isinstance(unique_rows, pd.DataFrame), f"unique_rows — это {type(unique_rows).__name__}, а нужна таблица"
    assert len(unique_rows) != 149, "удалены все строки, у которых был двойник, — вместе с оригиналами. Одну из каждой пары нужно оставить"
    assert len(unique_rows) == 156, f"в unique_rows {len(unique_rows)} строк: удалять нужно только повторы"
    assert unique_rows.duplicated().sum() == 0, "в unique_rows остались повторы"


def test_returns_kept():
    "таблица returns не изменилась"
    assert len(returns) == 163, "таблица returns изменилась: результат drop_duplicates нужно сохранить в unique_rows. Выполните ячейку «Журнал возвратов» ещё раз"
# ─── другое решение ───
n_exact = len(returns) - len(returns.drop_duplicates())
unique_rows = returns[~returns.duplicated()]
# ─── ошибка ───
n_exact = returns.duplicated(keep=False).sum()
unique_rows = returns.drop_duplicates()
# ─── ошибка ───
n_exact = returns.duplicated().sum()
unique_rows = returns.drop_duplicates(keep=False)

# %% id-unique
print(unique_rows["return_id"].nunique(), len(unique_rows))
print(unique_rows.duplicated(subset=["order_id", "product_id"]).sum())

# %% twice [exercise]
doubles = unique_rows[unique_rows.duplicated(subset=["order_id", "product_id"], keep=False)]
doubles = doubles.sort_values(["order_id", "product_id"])
# ─── заготовка ───
doubles = ...
# ─── проверка ───
def test_doubles():
    "doubles — возвраты, оформленные дважды: обе записи каждой пары"
    assert isinstance(doubles, pd.DataFrame), f"doubles — это {type(doubles).__name__}, а нужна таблица"
    assert len(doubles) != 6, "в doubles только вторые записи каждой пары, а нужны обе: вспомните параметр keep"
    assert len(doubles) == 12, f"в doubles {len(doubles)} строк: нужны обе записи каждой пары"
    assert doubles["return_id"].nunique() == 12, "у записей в doubles должны быть разные return_id: искать повторы нужно в unique_rows по столбцам order_id и product_id"
    orders_list = doubles["order_id"].tolist()
    assert orders_list == sorted(orders_list), "отсортируйте doubles по order_id и product_id — пары встанут рядом"
# ─── другое решение ───
mask = unique_rows.duplicated(subset=["order_id", "product_id"], keep=False)
doubles = unique_rows.loc[mask].sort_values(["order_id", "product_id", "return_id"])
# ─── ошибка ───
doubles = unique_rows[unique_rows.duplicated(subset=["order_id", "product_id"])]
doubles = doubles.sort_values(["order_id", "product_id"])
# ─── ошибка ───
doubles = unique_rows[unique_rows.duplicated(subset=["order_id", "product_id"], keep=False)]

# %% doubles-view
doubles.head(4)

# %% keep
first = unique_rows.drop_duplicates(subset=["order_id", "product_id"])
last = unique_rows.drop_duplicates(subset=["order_id", "product_id"], keep="last")
print(len(first), len(last))
print(first["return_id"].tail(3).tolist())
print(last["return_id"].tail(3).tolist())

# %% too-wide
len(unique_rows.drop_duplicates(subset=["order_id"]))

# %% dup-quiz [quiz]
print(pd.Series([1, 1, 2, 1]).duplicated().sum())

# %% reset
first.tail(3)

# %% reset-index
first.reset_index(drop=True).tail(3)

# %% clean [exercise]
clean = unique_rows.drop_duplicates(subset=["order_id", "product_id"]).reset_index(drop=True)
items_raw = returns["quantity"].sum()
items_clean = clean["quantity"].sum()
# ─── заготовка ───
clean = ...
items_raw = ...
items_clean = ...
# ─── проверка ───
def test_clean():
    "clean — по одной записи на возврат, индекс с нуля"
    assert isinstance(clean, pd.DataFrame), f"clean — это {type(clean).__name__}, а нужна таблица"
    assert len(clean) != 146, "осталось 146 строк: повторы искали только по order_id и удалили возвраты разных товаров из одного заказа. Нужны оба столбца: order_id и product_id"
    assert len(clean) == 150, f"в clean {len(clean)} строк — проверьте, по каким столбцам ищете повторы"
    assert "index" not in clean.columns, "в clean появился столбец index: вспомните параметр drop у reset_index"
    assert list(clean.index) == list(range(150)), "индекс clean должен идти от 0 до 149 подряд"
    assert clean["return_id"].iloc[-1] == "R150", "из двух записей одного возврата нужно оставить первую (так делает drop_duplicates по умолчанию)"


def test_items():
    "items_raw и items_clean — возвращено штук до и после очистки"
    assert items_raw == 230, f"items_raw = {items_raw!r}: нужна сумма quantity исходной таблицы returns"
    assert items_clean == 214, f"items_clean = {items_clean!r}: нужна сумма quantity таблицы clean"
# ─── другое решение ───
clean = returns.drop_duplicates(subset=["order_id", "product_id"]).reset_index(drop=True)
items_raw = sum(returns["quantity"])
items_clean = sum(clean["quantity"])
# ─── ошибка ───
clean = unique_rows.drop_duplicates(subset=["order_id"]).reset_index(drop=True)
items_raw = returns["quantity"].sum()
items_clean = clean["quantity"].sum()
# ─── ошибка ───
clean = unique_rows.drop_duplicates(subset=["order_id", "product_id"])
items_raw = returns["quantity"].sum()
items_clean = clean["quantity"].sum()
# ─── ошибка ───
clean = unique_rows.drop_duplicates(subset=["order_id", "product_id"]).reset_index()
items_raw = returns["quantity"].sum()
items_clean = clean["quantity"].sum()

# %% hidden
signups = pd.DataFrame({
    "email": ["anna@lavka.example", "Anna@lavka.example ", "oleg@lavka.example", "OLEG@LAVKA.EXAMPLE", "maria@lavka.example"],
    "city": ["Казань", "Казань", "Москва", "Москва", "Казань"],
})
print(signups.duplicated().sum())
print(signups["email"].nunique())

# %% people [exercise]
signups["email"] = signups["email"].str.strip().str.lower()
people = signups.drop_duplicates().reset_index(drop=True)
n_people = len(people)
# ─── заготовка ───
# приведите signups["email"] к единому виду
people = ...
n_people = ...
# ─── проверка ───
def test_email():
    "email — без пробелов, строчными буквами"
    emails = signups["email"].tolist()
    assert all(e == e.strip() for e in emails), "в email остались пробелы по краям: запишите результат обратно в столбец"
    assert all(e == e.lower() for e in emails), "в email остались заглавные буквы"
    assert len(signups) == 5, "из signups строки удалять не нужно: результат drop_duplicates сохраните в people"


def test_people():
    "people — по одной строке на человека"
    assert isinstance(people, pd.DataFrame), f"people — это {type(people).__name__}, а нужна таблица"
    assert len(people) != 5, "в people остались все 5 строк: сначала почистите email, потом удаляйте дубликаты"
    assert len(people) == 3 and n_people == 3, f"в people {len(people)} строк, n_people = {n_people!r}: сначала почистите email"
    assert sorted(people["email"]) == ["anna@lavka.example", "maria@lavka.example", "oleg@lavka.example"], f"в people адреса {sorted(people['email'])}: в каждом адресе — один человек"
    assert list(people.index) == [0, 1, 2], "индекс people должен идти с нуля подряд"
# ─── другое решение ───
signups["email"] = signups["email"].str.lower().str.strip()
people = signups.drop_duplicates(subset=["email"]).reset_index(drop=True)
n_people = signups["email"].nunique()
# ─── ошибка ───
people = signups.drop_duplicates().reset_index(drop=True)
n_people = len(people)
# ─── ошибка ───
signups["email"] = signups["email"].str.strip()
people = signups.drop_duplicates().reset_index(drop=True)
n_people = len(people)
