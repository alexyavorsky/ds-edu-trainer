# Урок pd-dataframe. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% dict
import pandas as pd

menu = pd.DataFrame({
    "drink": ["эспрессо", "капучино", "латте", "какао"],
    "price": [150, 240, 260, 220],
    "volume": [0.06, 0.25, 0.35, 0.3],
})
menu

# %% use
print(menu.shape)
print(menu["price"].mean())

# %% uneven [raises=ValueError]
pd.DataFrame({
    "drink": ["эспрессо", "капучино", "латте"],
    "price": [150, 240],
})

# %% staff [exercise]
staff = pd.DataFrame({
    "name": ["Анна", "Олег", "Мария"],
    "role": ["бариста", "бариста", "управляющий"],
    "salary": [62000, 58000, 95000],
})
# ─── заготовка ───
staff = ...
# ─── проверка ───
def test_frame():
    "staff — таблица 3 × 3"
    assert not isinstance(staff, dict), "staff — словарь, а нужна таблица: передайте словарь в pd.DataFrame(...)"
    assert isinstance(staff, pd.DataFrame), f"staff — это {type(staff).__name__}, а нужна таблица: pd.DataFrame({{...}})"
    assert list(staff.columns) == ["name", "role", "salary"], f"столбцы сейчас {list(staff.columns)}, а нужны name, role, salary — в этом порядке"
    assert len(staff) == 3, f"в staff {len(staff)} строк, а сотрудников трое"


def test_values():
    "в staff — данные трёх сотрудников"
    assert isinstance(staff, pd.DataFrame) and list(staff.columns) == ["name", "role", "salary"], "сначала исправьте то, о чём говорит проверка выше"
    assert staff["name"].tolist() == ["Анна", "Олег", "Мария"], f"в столбце name сейчас {staff['name'].tolist()}, а нужно Анна, Олег, Мария"
    assert staff["role"].tolist() == ["бариста", "бариста", "управляющий"], f"в столбце role сейчас {staff['role'].tolist()}"
    assert staff["salary"].tolist() != ["62000", "58000", "95000"], "зарплаты записаны строками в кавычках — с ними нельзя считать; пишите числа без кавычек"
    assert staff["salary"].tolist() == [62000, 58000, 95000], f"в столбце salary сейчас {staff['salary'].tolist()}"
# ─── другое решение ───
staff = pd.DataFrame([
    {"name": "Анна", "role": "бариста", "salary": 62000},
    {"name": "Олег", "role": "бариста", "salary": 58000},
    {"name": "Мария", "role": "управляющий", "salary": 95000},
])
# ─── ошибка ───
staff = {
    "name": ["Анна", "Олег", "Мария"],
    "role": ["бариста", "бариста", "управляющий"],
    "salary": [62000, 58000, 95000],
}
# ─── ошибка ───
staff = pd.DataFrame({
    "name": ["Анна", "Олег", "Мария"],
    "role": ["бариста", "бариста", "управляющий"],
    "salary": ["62000", "58000", "95000"],
})

# %% dtypes
menu.dtypes

# %% mixed-quiz [quiz]
print(pd.DataFrame({"x": [1, 2.5, 3]})["x"].dtype)

# %% records
visits = pd.DataFrame([
    {"day": "пн", "guests": 84, "rain": False},
    {"day": "вт", "guests": 91, "rain": True},
    {"day": "ср", "guests": 77, "rain": True},
])
visits

# %% stock [exercise]
stock = pd.DataFrame([
    {"item": "молоко", "liters": 12.5},
    {"item": "сливки", "liters": 3.0},
    {"item": "сироп", "liters": 1.5},
])
total_liters = stock["liters"].sum()
# ─── заготовка ───
stock = ...
total_liters = ...
# ─── проверка ───
def test_stock():
    "stock — таблица из трёх строк"
    assert isinstance(stock, pd.DataFrame), f"stock — это {type(stock).__name__}, а нужна таблица: pd.DataFrame([...])"
    assert list(stock.columns) == ["item", "liters"], f"столбцы сейчас {list(stock.columns)}, а нужны item и liters"
    assert stock["item"].tolist() == ["молоко", "сливки", "сироп"], f"в столбце item сейчас {stock['item'].tolist()}"
    assert stock["liters"].tolist() == [12.5, 3.0, 1.5], f"в столбце liters сейчас {stock['liters'].tolist()}"


def test_total():
    "total_liters — сколько всего литров"
    assert not isinstance(total_liters, pd.Series), "total_liters — столбец, а нужно одно число: сумма столбца liters"
    assert abs(total_liters - 17.0) < 1e-9, f"total_liters = {total_liters}, а всего 17.0 литров"
# ─── другое решение ───
stock = pd.DataFrame({"item": ["молоко", "сливки", "сироп"], "liters": [12.5, 3.0, 1.5]})
total_liters = sum(stock["liters"])
# ─── ошибка ───
stock = pd.DataFrame([
    {"item": "молоко", "liters": 12.5},
    {"item": "сливки", "liters": 3.0},
    {"item": "сироп", "liters": 1.5},
])
total_liters = stock["liters"]

# %% labels
sizes = pd.DataFrame(
    {"volume": [0.25, 0.35, 0.45], "extra": [0, 30, 60]},
    index=["S", "M", "L"],
)
sizes

# %% labels-index
print(sizes.index)
print(menu.index)

# %% series
tips = pd.Series([120, 80, 200, 150], index=["пн", "вт", "ср", "чт"], name="tips")
tips

# %% by-label
print(tips["ср"])
print(tips.sum())

# %% week [exercise]
guests = pd.Series([84, 91, 77, 102, 130], index=["пн", "вт", "ср", "чт", "пт"], name="guests")
friday = guests["пт"]
# ─── заготовка ───
guests = ...
friday = ...
# ─── проверка ───
def test_series():
    "guests — Series с днями недели в индексе"
    assert isinstance(guests, pd.Series), f"guests — это {type(guests).__name__}, а нужен pd.Series(...)"
    assert guests.tolist() == [84, 91, 77, 102, 130], f"значения сейчас {guests.tolist()}, а нужны 84, 91, 77, 102, 130"
    assert list(guests.index) != [0, 1, 2, 3, 4], "индекс — номера 0…4, а нужны дни недели: передайте их параметром index="
    assert list(guests.index) == ["пн", "вт", "ср", "чт", "пт"], f"индекс сейчас {list(guests.index)}, а нужен пн, вт, ср, чт, пт"
    assert guests.name == "guests", f"название сейчас {guests.name!r}, а нужно \"guests\": параметр name="


def test_friday():
    "friday — гостей в пятницу"
    assert friday == 130, f"friday = {friday!r}, а в пятницу было 130 гостей: guests[\"пт\"]"
# ─── другое решение ───
guests = pd.Series({"пн": 84, "вт": 91, "ср": 77, "чт": 102, "пт": 130}, name="guests")
friday = guests["пт"]
# ─── ошибка ───
guests = pd.Series([84, 91, 77, 102, 130], name="guests")
friday = guests[4]
# ─── ошибка ───
guests = pd.Series([84, 91, 77, 102, 130], index=["пн", "вт", "ср", "чт", "пт"])
friday = guests["пт"]
