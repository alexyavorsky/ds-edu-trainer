# Урок pd-project-plan. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
orders["month"] = pd.to_datetime(orders["date"]).dt.month
plan_table = pd.read_csv("data/plan.csv")
plan_table.head(4)

# %% series [exercise]
fact_m = orders.groupby(["city", "month"])["revenue"].sum()
plan_m = plan_table.set_index(["city", "month"])["plan"]
# ─── заготовка ───
fact_m = ...
plan_m = ...
# ─── проверка ───
def test_fact():
    "fact_m — выручка по парам «город, месяц»"
    assert isinstance(fact_m, pd.Series), f"fact_m — это {type(fact_m).__name__}, а нужен Series"
    assert list(fact_m.index.names) == ["city", "month"], f"уровни индекса fact_m сейчас {list(fact_m.index.names)}, а нужны city и month — в этом порядке"
    assert len(fact_m) == 60 and fact_m.sum() == 3301420, "в fact_m 60 пар, сумма — выручка года"


def test_plan():
    "plan_m — план с тем же двухуровневым индексом"
    assert not isinstance(plan_m, pd.DataFrame), "plan_m — таблица, а нужен Series: после set_index возьмите один столбец"
    assert isinstance(plan_m, pd.Series), f"plan_m — это {type(plan_m).__name__}, а нужен Series"
    assert list(plan_m.index.names) == ["city", "month"], f"уровни индекса plan_m сейчас {list(plan_m.index.names)}, а нужны city и month"
    assert len(plan_m) == 61 and plan_m.loc[("Москва", 1)] == 132000, "в plan_m должны быть все 61 пара плана со значениями столбца plan"
# ─── другое решение ───
fact_m = orders.pivot_table(values="revenue", index=["city", "month"], aggfunc="sum")["revenue"]
plan_m = plan_table.groupby(["city", "month"])["plan"].sum()
# ─── ошибка ───
fact_m = orders.groupby(["city", "month"])["revenue"].sum()
plan_m = plan_table.set_index(["city", "month"])
# ─── ошибка ───
fact_m = orders.groupby(["month", "city"])["revenue"].sum()
plan_m = plan_table.set_index(["month", "city"])["plan"]

# %% frame
left = pd.Series([1, 2], index=["x", "y"])
right = pd.Series([30, 40], index=["y", "z"])
pd.DataFrame({"left": left, "right": right})

# %% table [exercise]
pf = pd.DataFrame({"plan": plan_m, "fact": fact_m})
no_plan = pf["plan"].isna().sum()
no_fact = pf["fact"].isna().sum()
pf["fact"] = pf["fact"].fillna(0)
# ─── заготовка ───
pf = ...
no_plan = ...
no_fact = ...
# замените пропуски в столбце fact нулями
# ─── проверка ───
def test_pf():
    "pf — план и факт рядом, по всем парам"
    assert isinstance(pf, pd.DataFrame), f"pf — это {type(pf).__name__}, а нужна таблица"
    assert list(pf.columns)[:2] == ["plan", "fact"], f"столбцы сейчас {list(pf.columns)}, а первые два должны быть plan и fact"
    assert len(pf) == 63, f"в pf {len(pf)} строк: нужны все пары «город, месяц» из плана и факта вместе"


def test_gaps():
    "no_plan и no_fact — сколько пар без плана и без факта; пропуски факта — нули"
    assert no_plan == 2, f"no_plan = {no_plan!r} — это не число пар без плана"
    assert no_fact == 3, f"no_fact = {no_fact!r}: посчитайте пропуски до заполнения"
    assert pf["fact"].isna().sum() == 0, "в pf[\"fact\"] остались пропуски: нет продаж — значит, выручка ноль. Результат запишите обратно в столбец"
    assert pf["plan"].isna().sum() == 2, "пропуски в plan заполнять не нужно: «плана не было» — не то же самое, что «план равен нулю»"
# ─── другое решение ───
pf = pd.concat([plan_m, fact_m.rename("fact")], axis=1)
no_plan = len(pf) - pf["plan"].count()
no_fact = len(pf) - pf["fact"].count()
pf["fact"] = pf["fact"].fillna(0)
# ─── ошибка ───
pf = pd.DataFrame({"plan": plan_m, "fact": fact_m})
no_plan = pf["plan"].isna().sum()
no_fact = pf["fact"].isna().sum()
pf = pf.fillna(0)
# ─── ошибка ───
pf = pd.DataFrame({"plan": plan_m, "fact": fact_m})
no_plan = pf["plan"].isna().sum()
no_fact = pf["fact"].isna().sum()

# %% metrics [exercise]
pf["gap"] = pf["fact"] - pf["plan"]
pf["done"] = (pf["fact"] / pf["plan"]).round(3)
flat = pf.reset_index()
# ─── заготовка ───
# добавьте в pf столбцы gap и done
flat = ...
# ─── проверка ───
def test_metrics():
    "gap — факт минус план, done — доля выполнения"
    assert "gap" in pf.columns and "done" in pf.columns, "в pf нужны столбцы gap и done"
    assert pf.loc[("Казань", 3), "gap"] == -3000, "gap не тот: нужен факт минус план"
    assert abs(pf.loc[("Казань", 3), "done"] - 0.935) < 1e-9, "done не тот: нужна доля выполнения плана с округлением до трёх знаков"
    assert pf["done"].isna().sum() == 2, "у двух пар без плана доля выполнения должна остаться пропуском"


def test_flat():
    "flat — плоская таблица: city и month в столбцах"
    assert isinstance(flat, pd.DataFrame), f"flat — это {type(flat).__name__}, а нужна таблица"
    assert list(flat.columns) == ["city", "month", "plan", "fact", "gap", "done"], f"столбцы сейчас {list(flat.columns)}, а нужны city, month, plan, fact, gap, done: индекс нужно вернуть в столбцы после добавления gap и done"
    assert len(flat) == 63, "в flat должны быть все 63 пары"
# ─── другое решение ───
pf = pf.assign(gap=pf["fact"] - pf["plan"])
pf["done"] = round(pf["fact"] / pf["plan"], 3)
flat = pf.reset_index()
# ─── ошибка ───
pf["gap"] = pf["plan"] - pf["fact"]
pf["done"] = (pf["fact"] / pf["plan"]).round(3)
flat = pf.reset_index()
# ─── ошибка ───
pf["gap"] = pf["fact"] - pf["plan"]
pf["done"] = (pf["fact"] / pf["plan"]).round(3)
flat = pf.reset_index(drop=True)

# %% flat-view
flat[flat["city"] == "Екатеринбург"].head(4)

# %% months [exercise]
by_month = flat.groupby("month").agg(plan=("plan", "sum"), fact=("fact", "sum"))
by_month["done"] = (by_month["fact"] / by_month["plan"]).round(3)
months_ok = (by_month["fact"] >= by_month["plan"]).sum()
worst_month = by_month["done"].idxmin()
# ─── заготовка ───
by_month = ...
months_ok = ...
worst_month = ...
# ─── проверка ───
def test_by_month():
    "by_month — план, факт и выполнение по месяцам"
    assert isinstance(by_month, pd.DataFrame), f"by_month — это {type(by_month).__name__}, а нужна таблица"
    assert list(by_month.columns) == ["plan", "fact", "done"], f"столбцы сейчас {list(by_month.columns)}, а нужны plan, fact, done"
    assert len(by_month) == 12 and by_month.loc[1, "plan"] == 269000 and by_month.loc[1, "fact"] == 318940, "в by_month 12 месяцев, план и факт — суммы за месяц"
    assert abs(by_month.loc[1, "done"] - 1.186) < 1e-9, "done не тот: нужна доля выполнения плана с округлением до трёх знаков"


def test_answers():
    "months_ok — в скольких месяцах план выполнен, worst_month — худший месяц"
    assert months_ok != 6, "months_ok = 6: похоже, вы считали по округлённой доле done >= 1 — в июле 183 950 / 184 000 = 0.9997 округлилось до 1.0. Сравнивайте сами суммы факта и плана"
    assert months_ok == 5, f"months_ok = {months_ok!r} — это не число месяцев, где факт не меньше плана"
    assert worst_month == 10, f"worst_month = {worst_month!r} — это не месяц с наименьшим выполнением плана"
# ─── другое решение ───
by_month = flat.pivot_table(values=["plan", "fact"], index="month", aggfunc="sum")[["plan", "fact"]]
by_month["done"] = (by_month["fact"] / by_month["plan"]).round(3)
months_ok = len(by_month[by_month["fact"] >= by_month["plan"]])
worst_month = by_month.sort_values("done").index[0]
# ─── ошибка ───
by_month = flat.groupby("month").agg(plan=("plan", "sum"), fact=("fact", "sum"))
by_month["done"] = (by_month["fact"] / by_month["plan"]).round(3)
months_ok = (by_month["done"] > 1).sum()
worst_month = by_month["done"].idxmax()
# ─── ошибка ───
by_month = flat.groupby("month").agg(plan=("plan", "sum"), fact=("fact", "sum"))
by_month["done"] = (by_month["fact"] / by_month["plan"]).round(3)
months_ok = (by_month["done"] >= 1).sum()
worst_month = by_month["done"].idxmin()

# %% cities [exercise]
flat["ok"] = flat["fact"] >= flat["plan"]
by_city = flat.groupby("city").agg(plan=("plan", "sum"), fact=("fact", "sum"), months_ok=("ok", "sum"))
by_city["gap"] = by_city["fact"] - by_city["plan"]
steadiest = by_city["months_ok"].idxmax()
# ─── заготовка ───
# добавьте в flat столбец ok
by_city = ...
# добавьте в by_city столбец gap
steadiest = ...
# ─── проверка ───
def test_ok():
    "ok — план месяца выполнен"
    assert "ok" in flat.columns and flat["ok"].dtype == bool, "в flat нужен столбец-маска ok"
    assert flat["ok"].sum() != 23, "сравнивать нужно сами суммы, а не округлённую долю done: 0.9997 округляется до 1.0, хотя план не выполнен"
    assert flat["ok"].sum() == 22, "маска не та: план выполнен, когда факт не меньше плана"


def test_by_city():
    "by_city — план, факт, число выполненных месяцев и отклонение по городам"
    assert isinstance(by_city, pd.DataFrame), f"by_city — это {type(by_city).__name__}, а нужна таблица"
    assert list(by_city.columns) == ["plan", "fact", "months_ok", "gap"], f"столбцы сейчас {list(by_city.columns)}, а нужны plan, fact, months_ok, gap"
    assert len(by_city) == 6 and by_city.loc["Москва", "months_ok"] == 7, "в by_city шесть городов; months_ok — число месяцев, где план выполнен"
    assert by_city.loc["Сочи", "gap"] == -60000 and by_city.loc["Екатеринбург", "gap"] == 25350, "gap не тот: нужен факт минус план за год"
    assert steadiest == "Москва", f"steadiest = {steadiest!r} — это не город, чаще всех выполнявший план"
# ─── другое решение ───
flat["ok"] = ~(flat["fact"] < flat["plan"]) & flat["plan"].notna()
g = flat.groupby("city")
by_city = pd.DataFrame({"plan": g["plan"].sum(), "fact": g["fact"].sum(), "months_ok": g["ok"].sum()})
by_city["gap"] = by_city["fact"] - by_city["plan"]
steadiest = by_city.sort_values("months_ok").index[-1]
# ─── ошибка ───
flat["ok"] = flat["fact"] >= flat["plan"]
by_city = flat.groupby("city").agg(plan=("plan", "sum"), fact=("fact", "sum"), months_ok=("ok", "count"))
by_city["gap"] = by_city["fact"] - by_city["plan"]
steadiest = by_city["months_ok"].idxmax()
# ─── ошибка ───
flat["ok"] = flat["done"] >= 1
by_city = flat.groupby("city").agg(plan=("plan", "sum"), fact=("fact", "sum"), months_ok=("ok", "sum"))
by_city["gap"] = by_city["fact"] - by_city["plan"]
steadiest = by_city["months_ok"].idxmax()

# %% cities-view
by_city.sort_values("gap")

# %% heat [exercise]
heat = flat.pivot_table(values="done", index="city", columns="month", aggfunc="mean").round(2)
moscow_worst = heat.loc["Москва"].idxmin()
# ─── заготовка ───
heat = ...
moscow_worst = ...
# ─── проверка ───
def test_heat():
    "heat — выполнение плана: города × месяцы"
    assert isinstance(heat, pd.DataFrame), f"heat — это {type(heat).__name__}, а нужна таблица"
    assert heat.shape == (6, 12), f"у heat размер {heat.shape}, а нужно 6 городов × 12 месяцев"
    assert "Москва" in heat.index and 12 in heat.columns, "в строках — города, в столбцах — месяцы"
    assert heat.loc["Москва", 2] == 0.85 and heat.loc["Казань", 1] == 1.16, "в ячейках — done с округлением до двух знаков"


def test_moscow():
    "moscow_worst — худший месяц Москвы"
    assert moscow_worst == 2, f"moscow_worst = {moscow_worst!r} — это не худший месяц Москвы"
# ─── другое решение ───
heat = flat.pivot(index="city", columns="month", values="done").round(2)
moscow_worst = flat[flat["city"] == "Москва"].sort_values("done").iloc[0]["month"]
# ─── ошибка ───
heat = flat.pivot_table(values="done", index="month", columns="city", aggfunc="mean").round(2)
moscow_worst = heat["Москва"].idxmin()
# ─── ошибка ───
heat = flat.pivot_table(values="done", index="city", columns="month", aggfunc="mean").round(2)
moscow_worst = heat.loc["Москва"].idxmax()

# %% heat-view
heat
