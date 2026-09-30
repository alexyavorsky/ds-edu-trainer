# Урок pd-pivot-table. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% long
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
orders.groupby(["city", "channel"])["revenue"].sum().head(6)

# %% pivot
table = orders.pivot_table(values="revenue", index="city", columns="channel", aggfunc="sum")
table

# %% pivot-use
print(table.loc["Казань", "сайт"])
print(table["сайт"].idxmax())
print(table.shape)

# %% categories [exercise]
by_city = orders.pivot_table(values="revenue", index="category", columns="city", aggfunc="sum")
spb_tea = by_city.loc["Чай", "Санкт-Петербург"]
# ─── заготовка ───
by_city = ...
spb_tea = ...
# ─── проверка ───
def test_table():
    "by_city — выручка: категории в строках, города в столбцах"
    assert isinstance(by_city, pd.DataFrame), f"by_city — это {type(by_city).__name__}, а нужна таблица: orders.pivot_table(...)"
    assert by_city.shape != (5, 5) or "Чай" in by_city.index, "в строках должны быть категории, а в столбцах города: index=\"category\", columns=\"city\""
    assert by_city.shape == (5, 5) and "Москва" in by_city.columns, f"у by_city размер {by_city.shape}, а нужно 5 категорий × 5 городов"
    assert abs(by_city.loc["Кофе", "Москва"] - 1968.6) > 100, "в ячейках средние, а нужны суммы: aggfunc=\"sum\""
    assert by_city.loc["Кофе", "Москва"] == 774640, "значения не те: values=\"revenue\", aggfunc=\"sum\""


def test_cell():
    "spb_tea — выручка от чая в Санкт-Петербурге"
    assert spb_tea == 152710, f"spb_tea = {spb_tea!r}, а выручка от чая в Санкт-Петербурге — 152710: by_city.loc[\"Чай\", \"Санкт-Петербург\"]"
# ─── другое решение ───
by_city = orders.groupby(["category", "city"])["revenue"].sum().unstack()
spb_tea = by_city["Санкт-Петербург"]["Чай"]
# ─── ошибка ───
by_city = orders.pivot_table(values="revenue", index="category", columns="city")
spb_tea = by_city.loc["Чай", "Санкт-Петербург"]
# ─── ошибка ───
by_city = orders.pivot_table(values="revenue", index="city", columns="category", aggfunc="sum")
spb_tea = by_city.loc["Санкт-Петербург", "Чай"]

# %% default-mean
orders.pivot_table(values="revenue", index="city", columns="channel").round(1)

# %% default-quiz [quiz]
small = pd.DataFrame({"city": ["Омск", "Омск", "Тула"], "cups": [10, 30, 5]})
print(small.pivot_table(values="cups", index="city").loc["Омск", "cups"])

# %% margins
orders.pivot_table(values="revenue", index="city", columns="channel", aggfunc="sum", margins=True, margins_name="Всего")

# %% items [exercise]
items = orders.pivot_table(values="quantity", index="category", columns="channel", aggfunc="sum", margins=True, margins_name="Всего")
site_share = items.loc["Всего", "сайт"] / items.loc["Всего", "Всего"]
# ─── заготовка ───
items = ...
site_share = ...
# ─── проверка ───
def test_items():
    "items — продано штук: категории × каналы, с итогами"
    assert isinstance(items, pd.DataFrame), f"items — это {type(items).__name__}, а нужна таблица: orders.pivot_table(...)"
    assert "Всего" in items.index and "Всего" in items.columns, "в items нет строки и столбца «Всего»: margins=True, margins_name=\"Всего\""
    assert items.shape == (6, 4), f"у items размер {items.shape}, а нужно 6 строк (5 категорий и итог) и 4 столбца (3 канала и итог)"
    assert items.loc["Кофе", "сайт"] != 469, "в ячейках число строк, а нужна сумма штук: values=\"quantity\", aggfunc=\"sum\""
    assert items.loc["Кофе", "сайт"] == 1026 and items.loc["Всего", "Всего"] == 5210, "значения не те: values=\"quantity\", aggfunc=\"sum\""


def test_share():
    "site_share — доля сайта в проданных штуках"
    assert abs(site_share - 2466 / 5210) < 1e-9, f"site_share = {site_share!r}, а доля сайта ≈ 0.473: итог столбца «сайт», делённый на общий итог"
# ─── другое решение ───
items = orders.pivot_table(values="quantity", index="category", columns="channel", aggfunc="sum", margins=True, margins_name="Всего")
site_share = orders.loc[orders["channel"] == "сайт", "quantity"].sum() / orders["quantity"].sum()
# ─── ошибка ───
items = orders.pivot_table(values="quantity", index="category", columns="channel", aggfunc="sum")
site_share = 2466 / 5210
# ─── ошибка ───
items = orders.pivot_table(values="quantity", index="category", columns="channel", aggfunc="count", margins=True, margins_name="Всего")
site_share = items.loc["Всего", "сайт"] / items.loc["Всего", "Всего"]

# %% gaps
orders["month"] = pd.to_datetime(orders["date"]).dt.month
gadgets = orders[orders["category"] == "Аксессуары"]
gadgets.pivot_table(values="revenue", index="month", columns="city", aggfunc="sum").head(4)

# %% fill
gadgets.pivot_table(values="revenue", index="month", columns="city", aggfunc="sum", fill_value=0).head(4)

# %% seasons [exercise]
monthly = orders.pivot_table(values="revenue", index="month", columns="category", aggfunc="sum", fill_value=0)
tea_peak = monthly["Чай"].idxmax()
december_top = monthly.loc[12].idxmax()
# ─── заготовка ───
monthly = ...
tea_peak = ...
december_top = ...
# ─── проверка ───
def test_monthly():
    "monthly — выручка: месяцы в строках, категории в столбцах"
    assert isinstance(monthly, pd.DataFrame), f"monthly — это {type(monthly).__name__}, а нужна таблица"
    assert monthly.shape == (12, 5), f"у monthly размер {monthly.shape}, а нужно 12 месяцев × 5 категорий: index=\"month\", columns=\"category\""
    assert "Чай" in monthly.columns and list(monthly.index) == list(range(1, 13)), "в строках — месяцы 1–12, в столбцах — категории"
    assert monthly.loc[12, "Чай"] == 103630 and monthly.loc[1, "Кофе"] == 164800, "значения не те: values=\"revenue\", aggfunc=\"sum\""


def test_peaks():
    "tea_peak — лучший месяц чая, december_top — главная категория декабря"
    assert tea_peak == 12, f"tea_peak = {tea_peak!r}, а больше всего чая продано в декабре (12): monthly[\"Чай\"].idxmax()"
    assert isinstance(december_top, str), f"december_top — это {type(december_top).__name__}, а нужно название категории: monthly.loc[12].idxmax()"
    assert december_top == "Кофе", f"december_top = {december_top!r}, а наибольшая выручка в декабре — у другой категории"
# ─── другое решение ───
monthly = orders.groupby(["month", "category"])["revenue"].sum().unstack(fill_value=0)
tea_peak = monthly["Чай"].sort_values().index[-1]
december_top = monthly.loc[12].sort_values().index[-1]
# ─── ошибка ───
monthly = orders.pivot_table(values="revenue", index="category", columns="month", aggfunc="sum", fill_value=0)
tea_peak = 12
december_top = "Кофе"
# ─── ошибка ───
monthly = orders.pivot_table(values="revenue", index="month", columns="category", aggfunc="sum", fill_value=0)
tea_peak = monthly["Чай"].max()
december_top = monthly.loc[12].idxmax()

# %% grades
grades = pd.read_csv("data/grades.csv")
grades.head(4)

# %% subjects [exercise]
group_subject = grades.pivot_table(values="score", index="group", columns="subject", aggfunc="mean").round(1)
best_subject = group_subject.loc["ИТ-22"].idxmax()
# ─── заготовка ───
group_subject = ...
best_subject = ...
# ─── проверка ───
def test_table():
    "group_subject — средний балл: группы × предметы, один знак"
    assert isinstance(group_subject, pd.DataFrame), f"group_subject — это {type(group_subject).__name__}, а нужна таблица"
    assert group_subject.shape == (3, 5), f"у group_subject размер {group_subject.shape}, а нужно 3 группы × 5 предметов: index=\"group\", columns=\"subject\""
    assert "ИТ-22" in group_subject.index and "Физика" in group_subject.columns, "в строках — группы, в столбцах — предметы"
    assert group_subject.loc["ИТ-22", "Программирование"] != 1548, "в ячейках суммы, а нужны средние баллы: aggfunc=\"mean\""
    assert abs(group_subject.loc["ИТ-22", "Программирование"] - 77.4) < 1e-9, "значения не те или не округлены: средний балл с round(1) — у ИТ-22 по программированию 77.4"


def test_best():
    "best_subject — лучший предмет группы ИТ-22"
    assert best_subject == "Программирование", f"best_subject = {best_subject!r}, а самый высокий средний балл у ИТ-22 — по другому предмету: group_subject.loc[\"ИТ-22\"].idxmax()"
# ─── другое решение ───
group_subject = grades.groupby(["group", "subject"])["score"].mean().unstack().round(1)
best_subject = group_subject.loc["ИТ-22"].sort_values(ascending=False).index[0]
# ─── ошибка ───
group_subject = grades.pivot_table(values="score", index="group", columns="subject", aggfunc="sum")
best_subject = group_subject.loc["ИТ-22"].idxmax()
# ─── ошибка ───
group_subject = grades.pivot_table(values="score", index="subject", columns="group", aggfunc="mean").round(1)
best_subject = group_subject["ИТ-22"].idxmax()
