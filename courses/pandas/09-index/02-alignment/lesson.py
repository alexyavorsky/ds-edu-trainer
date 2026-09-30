# Урок pd-alignment. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% same
import pandas as pd

stock = pd.Series({"кофе": 40, "чай": 25, "какао": 10})
sold = pd.Series({"чай": 5, "кофе": 12, "какао": 4})
stock - sold

# %% different
sold = pd.Series({"чай": 5, "кофе": 12, "сироп": 3})
stock - sold

# %% fill
stock.sub(sold, fill_value=0)

# %% align-quiz [quiz]
x = pd.Series([1, 2], index=["a", "b"])
y = pd.Series([10, 20], index=["b", "c"])
print((x + y).isna().sum())

# %% warehouse [exercise]
start = pd.Series({"эспрессо": 50, "латте": 30, "какао": 12, "чай": 20})
delivered = pd.Series({"латте": 10, "чай": 15, "раф": 8})
wrong_total = start + delivered
total = start.add(delivered, fill_value=0)
# ─── заготовка ───
start = pd.Series({"эспрессо": 50, "латте": 30, "какао": 12, "чай": 20})
delivered = pd.Series({"латте": 10, "чай": 15, "раф": 8})
wrong_total = ...
total = ...
# ─── проверка ───
def test_wrong():
    "wrong_total — простая сумма с пропусками"
    assert isinstance(wrong_total, pd.Series), f"wrong_total — это {type(wrong_total).__name__}, а нужен Series: start + delivered"
    assert len(wrong_total) == 5, f"в wrong_total {len(wrong_total)} значений, а разных напитков в двух Series пять"
    assert wrong_total.isna().sum() == 3, "в wrong_total должно быть три пропуска — там, где напиток есть только в одном из двух Series: сложите оператором +"
    assert wrong_total["латте"] == 40 and wrong_total["чай"] == 35, "значения не те: start + delivered"


def test_total():
    "total — остаток после поставки, без пропусков"
    assert isinstance(total, pd.Series), f"total — это {type(total).__name__}, а нужен Series: start.add(delivered, fill_value=0)"
    assert total.isna().sum() == 0, "в total остались пропуски: недостающее значение нужно считать нулём — метод add с fill_value=0"
    assert total["эспрессо"] == 50 and total["раф"] == 8 and total["латте"] == 40, "значения не те: эспрессо — 50, раф — 8, латте — 40"
    assert total.sum() == 145, "сумма остатков должна быть 145"
# ─── другое решение ───
start = pd.Series({"эспрессо": 50, "латте": 30, "какао": 12, "чай": 20})
delivered = pd.Series({"латте": 10, "чай": 15, "раф": 8})
wrong_total = delivered + start
names = sorted(set(start.index) | set(delivered.index))
total = start.reindex(names, fill_value=0) + delivered.reindex(names, fill_value=0)
# ─── ошибка ───
start = pd.Series({"эспрессо": 50, "латте": 30, "какао": 12, "чай": 20})
delivered = pd.Series({"латте": 10, "чай": 15, "раф": 8})
wrong_total = start + delivered
total = (start + delivered).fillna(0)

# %% fact-plan
orders = pd.read_csv("data/shop_orders.csv")
orders["revenue"] = orders["price"] * orders["quantity"]
fact = orders.groupby("city")["revenue"].sum()
plan_table = pd.read_csv("data/plan.csv")
plan = plan_table.groupby("city")["plan"].sum()
print(fact)
print(plan)

# %% fact-minus-plan
fact - plan

# %% reindex
print(fact.reindex(["Москва", "Сочи", "Казань"]))
print(fact.reindex(["Москва", "Сочи", "Казань"], fill_value=0))

# %% reindex-fill
plan.reindex(fact.index)

# %% gap [exercise]
fact_full = fact.reindex(plan.index, fill_value=0)
gap = fact_full - plan
done = (fact_full / plan).round(3)
best_city = done.idxmax()
# ─── заготовка ───
fact_full = ...
gap = ...
done = ...
best_city = ...
# ─── проверка ───
def test_full():
    "fact_full — факт по всем городам из плана; где продаж не было — ноль"
    assert isinstance(fact_full, pd.Series), f"fact_full — это {type(fact_full).__name__}, а нужен Series: fact.reindex(plan.index, fill_value=0)"
    assert list(fact_full.index) == list(plan.index), "метки fact_full должны совпадать с метками plan: fact.reindex(plan.index, ...)"
    assert fact_full.isna().sum() == 0, "в fact_full пропуск: в Сочи продаж не было — это ноль, fill_value=0"
    assert fact_full["Сочи"] == 0 and fact_full["Москва"] == 1310110, "значения не те: Сочи — 0, Москва — 1310110"


def test_gap():
    "gap — факт минус план, done — доля выполнения плана"
    assert isinstance(gap, pd.Series) and gap.isna().sum() == 0, "gap — Series без пропусков: fact_full - plan"
    assert gap["Сочи"] == -60000 and gap["Екатеринбург"] == 25350, "gap — факт минус план: Сочи — −60000, Екатеринбург — 25350"
    assert isinstance(done, pd.Series) and abs(done["Москва"] - 0.998) < 1e-9 and done["Сочи"] == 0, "done — факт, делённый на план, с округлением до трёх знаков: Москва — 0.998, Сочи — 0"
    assert best_city == "Екатеринбург", f"best_city = {best_city!r}, а план лучше всех выполнил другой город: done.idxmax()"
# ─── другое решение ───
fact_full = fact.reindex(plan.index).fillna(0)
gap = fact.sub(plan, fill_value=0)
done = round(fact.div(plan, fill_value=0), 3)
best_city = done.sort_values().index[-1]
# ─── ошибка ───
fact_full = fact.reindex(plan.index)
gap = fact_full - plan
done = (fact_full / plan).round(3)
best_city = done.idxmax()
# ─── ошибка ───
fact_full = fact.reindex(plan.index, fill_value=0)
gap = plan - fact_full
done = (fact_full / plan).round(3)
best_city = done.idxmax()

# %% compare-fail [raises=ValueError]
fact > plan

# %% compare-ok
fact.reindex(plan.index, fill_value=0) >= plan

# %% column-align
cities = pd.DataFrame({"city": ["Москва", "Казань", "Сочи"]})
cities["fact"] = fact
cities

# %% column-map
cities["fact"] = cities["city"].map(fact)
cities

# %% two-level
orders["month"] = pd.to_datetime(orders["date"]).dt.month
fact_m = orders.groupby(["city", "month"])["revenue"].sum()
plan_m = plan_table.set_index(["city", "month"])["plan"]
print(len(fact_m), len(plan_m))
plan_m.head(3)

# %% two-level-diff
diff = fact_m - plan_m
print(len(diff), diff.isna().sum())
diff.loc["Екатеринбург"].head(4)

# %% monthly [exercise]
gap_m = fact_m.sub(plan_m, fill_value=0)
kazan_march = gap_m.loc[("Казань", 3)]
no_plan = gap_m.loc["Екатеринбург"].loc[1:2].sum()
# ─── заготовка ───
gap_m = ...
kazan_march = ...
no_plan = ...
# ─── проверка ───
def test_gap_m():
    "gap_m — факт минус план по парам «город, месяц», без пропусков"
    assert isinstance(gap_m, pd.Series), f"gap_m — это {type(gap_m).__name__}, а нужен Series: fact_m.sub(plan_m, fill_value=0)"
    assert len(gap_m) == 63, f"в gap_m {len(gap_m)} значений, а разных пар «город, месяц» в факте и плане вместе — 63"
    assert gap_m.isna().sum() == 0, "в gap_m остались пропуски: там, где нет плана или нет факта, недостающее — ноль. Метод sub с fill_value=0"
    assert gap_m.loc[("Сочи", 10)] == -20000, "в Сочи продаж не было, а план был: разность должна быть −20000"


def test_cells():
    "kazan_march — Казань, март; no_plan — продажи Екатеринбурга за месяцы без плана"
    assert kazan_march == -3000, f"kazan_march = {kazan_march!r}, а в марте Казань недобрала до плана 3000: gap_m.loc[(\"Казань\", 3)]"
    assert no_plan == 53540, f"no_plan = {no_plan!r}, а за январь и февраль Екатеринбург продал на 53540 ₽ сверх (отсутствующего) плана"
# ─── другое решение ───
pairs = fact_m.index.union(plan_m.index)
gap_m = fact_m.reindex(pairs, fill_value=0) - plan_m.reindex(pairs, fill_value=0)
kazan_march = gap_m["Казань"][3]
no_plan = gap_m.loc[("Екатеринбург", 1)] + gap_m.loc[("Екатеринбург", 2)]
# ─── ошибка ───
gap_m = fact_m - plan_m
kazan_march = gap_m.loc[("Казань", 3)]
no_plan = gap_m.loc["Екатеринбург"].loc[1:2].sum()
