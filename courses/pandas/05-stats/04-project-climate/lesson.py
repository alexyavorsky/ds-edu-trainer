# Урок pd-project-climate. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
weather.head(3)

# %% prep [exercise]
gaps = weather.isna().sum()
weather["temp_avg"] = (weather["temp_min"] + weather["temp_max"]) / 2
no_avg = weather["temp_avg"].isna().sum()
# ─── заготовка ───
gaps = ...
# добавьте в weather столбец temp_avg
no_avg = ...
# ─── проверка ───
def test_gaps():
    "gaps — пропуски по столбцам"
    assert isinstance(gaps, pd.Series), f"gaps — это {type(gaps).__name__}, а нужен Series: weather.isna().sum()"
    assert gaps["temp_min"] == 3 and gaps["wind_ms"] == 4 and gaps["date"] == 0, "числа не те: weather.isna().sum()"


def test_avg():
    "temp_avg — средняя температура дня"
    assert "temp_avg" in weather.columns, "в weather нет столбца temp_avg"
    assert abs(weather.loc[0, "temp_avg"] - (-13.1)) > 1e-9, "минимум и максимум сложены, но не разделены на 2: сумму возьмите в скобки"
    assert abs(weather.loc[0, "temp_avg"] - (-11.5)) > 1e-9, "делится только максимум: сумму двух столбцов возьмите в скобки, потом делите на 2"
    assert abs(weather.loc[0, "temp_avg"] - (-6.55)) < 1e-9, f"temp_avg в первой строке — {weather.loc[0, 'temp_avg']}, а должно быть −6.55: (−9.9 + −3.2) / 2"
    assert no_avg == 5, f"no_avg = {no_avg!r}, а пропусков в temp_avg 5: там, где неизвестен минимум или максимум"
# ─── другое решение ───
gaps = len(weather) - weather.count()
weather["temp_avg"] = weather[["temp_min", "temp_max"]].sum(axis=1, skipna=False) / 2
no_avg = len(weather) - weather["temp_avg"].count()
# ─── ошибка ───
gaps = weather.isna().sum()
weather["temp_avg"] = weather["temp_min"] + weather["temp_max"] / 2
no_avg = weather["temp_avg"].isna().sum()
# ─── ошибка ───
gaps = weather.isna().sum()
weather["temp_avg"] = (weather["temp_min"] + weather["temp_max"]) / 2
no_avg = gaps["temp_min"]

# %% compare [exercise]
sochi = weather[weather["city"] == "Сочи"].copy()
nsk = weather[weather["city"] == "Новосибирск"].copy()
sochi_mean = sochi["temp_avg"].mean()
nsk_mean = nsk["temp_avg"].mean()
sochi_std = sochi["temp_avg"].std()
nsk_std = nsk["temp_avg"].std()
# ─── заготовка ───
sochi = ...
nsk = ...
sochi_mean = ...
nsk_mean = ...
sochi_std = ...
nsk_std = ...
# ─── проверка ───
def test_tables():
    "sochi и nsk — погода двух городов"
    assert isinstance(sochi, pd.DataFrame) and len(sochi) == 365 and (sochi["city"] == "Сочи").all(), "sochi — 365 строк Сочи: weather[weather[\"city\"] == \"Сочи\"].copy()"
    assert isinstance(nsk, pd.DataFrame) and len(nsk) == 365 and (nsk["city"] == "Новосибирск").all(), "nsk — 365 строк Новосибирска"
    assert "temp_avg" in sochi.columns and "temp_avg" in nsk.columns, "в таблицах нет столбца temp_avg: отбирайте строки из weather после шага 1"


def test_numbers():
    "средняя температура и её разброс"
    assert abs(sochi_mean - 14.9526) < 1e-3, f"sochi_mean = {sochi_mean!r}, а средняя температура в Сочи ≈ 14.95"
    assert abs(nsk_mean - 1.6303) < 1e-3, f"nsk_mean = {nsk_mean!r}, а средняя температура в Новосибирске ≈ 1.63"
    assert abs(sochi_std - 6.2736) < 1e-3, f"sochi_std = {sochi_std!r}, а стандартное отклонение в Сочи ≈ 6.27: метод std()"
    assert abs(nsk_std - 13.9545) < 1e-3, f"nsk_std = {nsk_std!r}, а стандартное отклонение в Новосибирске ≈ 13.95"
# ─── другое решение ───
sochi = weather.query("city == 'Сочи'").copy()
nsk = weather.query("city == 'Новосибирск'").copy()
sochi_mean = sochi["temp_avg"].describe()["mean"]
nsk_mean = nsk["temp_avg"].describe()["mean"]
sochi_std = sochi["temp_avg"].describe()["std"]
nsk_std = nsk["temp_avg"].describe()["std"]
# ─── ошибка ───
sochi = weather[weather["city"] == "Сочи"].copy()
nsk = weather[weather["city"] == "Новосибирск"].copy()
sochi_mean = sochi["temp_max"].mean()
nsk_mean = nsk["temp_max"].mean()
sochi_std = sochi["temp_max"].std()
nsk_std = nsk["temp_max"].std()

# %% kinds [exercise]
bins = [-50, 0, 15, 25, 50]
names = ["ниже нуля", "прохладно", "тепло", "жарко"]
nsk["kind"] = pd.cut(nsk["temp_max"], bins=bins, labels=names)
sochi["kind"] = pd.cut(sochi["temp_max"], bins=bins, labels=names)
nsk_kinds = nsk["kind"].value_counts(normalize=True).sort_index()
sochi_kinds = sochi["kind"].value_counts(normalize=True).sort_index()
# ─── заготовка ───
bins = [-50, 0, 15, 25, 50]
names = ["ниже нуля", "прохладно", "тепло", "жарко"]
# добавьте столбец kind в nsk и в sochi
nsk_kinds = ...
sochi_kinds = ...
# ─── проверка ───
def test_kind():
    "столбец kind в обеих таблицах"
    assert "kind" in nsk.columns and "kind" in sochi.columns, "столбец kind нужен в обеих таблицах: pd.cut(таблица[\"temp_max\"], bins=bins, labels=names)"
    assert (nsk["kind"] == "ниже нуля").sum() == 148, "в nsk типы дней не те: делить нужно столбец temp_max по границам bins"
    assert (sochi["kind"] == "жарко").sum() == 50, "в sochi типы дней не те: делить нужно столбец temp_max по границам bins"


def test_shares():
    "nsk_kinds и sochi_kinds — доли типов дней по порядку шкалы"
    for name, s in [("nsk_kinds", nsk_kinds), ("sochi_kinds", sochi_kinds)]:
        assert isinstance(s, pd.Series), f"{name} — это {type(s).__name__}, а нужен Series: value_counts(normalize=True).sort_index()"
        assert list(s.index) == ["ниже нуля", "прохладно", "тепло", "жарко"], f"в {name} порядок {list(s.index)}, а нужен по шкале: sort_index()"
        assert abs(s.sum() - 1) < 1e-9, f"в {name} числа дней, а нужны доли: normalize=True"
    assert abs(nsk_kinds["ниже нуля"] - 148 / 365) < 1e-9, "доли для Новосибирска не те"
    assert abs(sochi_kinds["жарко"] - 50 / 365) < 1e-9, "доли для Сочи не те"
# ─── другое решение ───
bins = [-50, 0, 15, 25, 50]
names = ["ниже нуля", "прохладно", "тепло", "жарко"]
nsk = nsk.assign(kind=pd.cut(nsk["temp_max"], bins, labels=names))
sochi = sochi.assign(kind=pd.cut(sochi["temp_max"], bins, labels=names))
nsk_kinds = (nsk["kind"].value_counts() / len(nsk)).sort_index()
sochi_kinds = (sochi["kind"].value_counts() / len(sochi)).sort_index()
# ─── ошибка ───
bins = [-50, 0, 15, 25, 50]
names = ["ниже нуля", "прохладно", "тепло", "жарко"]
nsk["kind"] = pd.cut(nsk["temp_max"], bins=bins, labels=names)
sochi["kind"] = pd.cut(sochi["temp_max"], bins=bins, labels=names)
nsk_kinds = nsk["kind"].value_counts().sort_index()
sochi_kinds = sochi["kind"].value_counts().sort_index()
# ─── ошибка ───
bins = [-50, 0, 15, 25, 50]
names = ["ниже нуля", "прохладно", "тепло", "жарко"]
nsk["kind"] = pd.cut(nsk["temp_max"], bins=bins, labels=names)
sochi["kind"] = pd.cut(sochi["temp_max"], bins=bins, labels=names)
nsk_kinds = nsk["kind"].value_counts(normalize=True)
sochi_kinds = sochi["kind"].value_counts(normalize=True)

# %% kinds-view
print(nsk_kinds.round(2))
print(sochi_kinds.round(2))

# %% rain [exercise]
sochi_rainy = (sochi["precip_mm"] > 0).mean()
nsk_rainy = (nsk["precip_mm"] > 0).mean()
sochi_total = sochi["precip_mm"].sum()
nsk_total = nsk["precip_mm"].sum()
sochi_heavy = (sochi["precip_mm"] >= 10).sum()
# ─── заготовка ───
sochi_rainy = ...
nsk_rainy = ...
sochi_total = ...
nsk_total = ...
sochi_heavy = ...
# ─── проверка ───
def test_rainy():
    "доля дней с осадками"
    assert abs(sochi_rainy - 110 / 365) < 1e-9, f"sochi_rainy = {sochi_rainy!r}, а доля дней с осадками в Сочи ≈ 0.30: среднее маски precip_mm > 0"
    assert abs(nsk_rainy - 145 / 365) < 1e-9, f"nsk_rainy = {nsk_rainy!r}, а доля дней с осадками в Новосибирске ≈ 0.40"


def test_totals():
    "сумма осадков за год и число дней с сильными осадками"
    assert abs(sochi_total - 795.0) < 1e-6, f"sochi_total = {sochi_total!r}, а за год в Сочи выпало 795 мм"
    assert abs(nsk_total - 520.5) < 1e-6, f"nsk_total = {nsk_total!r}, а за год в Новосибирске выпало 520.5 мм"
    assert sochi_heavy != 28, "условие «10 мм и больше» — это >=, а не >"
    assert sochi_heavy == 29, f"sochi_heavy = {sochi_heavy!r}, а дней с осадками от 10 мм в Сочи — 29"
# ─── другое решение ───
sochi_rainy = len(sochi[sochi["precip_mm"] > 0]) / len(sochi)
nsk_rainy = len(nsk[nsk["precip_mm"] > 0]) / len(nsk)
sochi_total = sum(sochi["precip_mm"].dropna())
nsk_total = sum(nsk["precip_mm"].dropna())
sochi_heavy = len(sochi.query("precip_mm >= 10"))
# ─── ошибка ───
sochi_rainy = (sochi["precip_mm"] > 0).sum()
nsk_rainy = (nsk["precip_mm"] > 0).sum()
sochi_total = sochi["precip_mm"].sum()
nsk_total = nsk["precip_mm"].sum()
sochi_heavy = (sochi["precip_mm"] >= 10).sum()

# %% season [exercise]
nsk["month"] = nsk["date"].dt.month
january = nsk.loc[nsk["month"] == 1, "temp_avg"].mean()
july = nsk.loc[nsk["month"] == 7, "temp_avg"].mean()
amplitude = july - january
# ─── заготовка ───
# добавьте в nsk столбец month
january = ...
july = ...
amplitude = ...
# ─── проверка ───
def test_month():
    "month — номер месяца"
    assert "month" in nsk.columns, "в nsk нет столбца month: nsk[\"date\"].dt.month"
    assert nsk["month"].min() == 1 and nsk["month"].max() == 12 and (nsk["month"] == 2).sum() == 28, "в month должны быть номера месяцев: .dt.month"


def test_amplitude():
    "january, july и amplitude — средняя температура января, июля и их разность"
    assert abs(january - (-17.554839)) < 1e-5, f"january = {january!r}, а средняя температура января ≈ −17.55: среднее temp_avg по строкам с month == 1"
    assert abs(july - 22.546774) < 1e-5, f"july = {july!r}, а средняя температура июля ≈ 22.55"
    assert amplitude > 0, "amplitude получилась отрицательной: из июля вычитают январь"
    assert abs(amplitude - 40.101613) < 1e-5, f"amplitude = {amplitude!r}, а годовая амплитуда ≈ 40.1 градуса"
# ─── другое решение ───
nsk = nsk.assign(month=nsk["date"].dt.month)
january = nsk[nsk["date"] < "2025-02-01"]["temp_avg"].mean()
july = nsk.query("month == 7")["temp_avg"].mean()
amplitude = july - january
# ─── ошибка ───
nsk["month"] = nsk["date"].dt.month
january = nsk.loc[nsk["month"] == 1, "temp_avg"].mean()
july = nsk.loc[nsk["month"] == 7, "temp_avg"].mean()
amplitude = january - july
# ─── ошибка ───
nsk["month"] = nsk["date"].dt.month
january = nsk.loc[nsk["month"] == 1, "temp_max"].mean()
july = nsk.loc[nsk["month"] == 7, "temp_max"].mean()
amplitude = july - january

# %% thaw [exercise]
moscow = weather[weather["city"] == "Москва"]
winter = moscow[moscow["date"].dt.month.isin([12, 1, 2])]
thaws = winter.loc[winter["temp_max"] > 0, ["date", "temp_max"]]
warmest_date = winter.loc[winter["temp_max"].idxmax(), "date"]
# ─── заготовка ───
moscow = weather[weather["city"] == "Москва"]
winter = ...
thaws = ...
warmest_date = ...
# ─── проверка ───
def test_winter():
    "winter — зимние дни в Москве"
    assert isinstance(winter, pd.DataFrame), f"winter — это {type(winter).__name__}, а нужна таблица: moscow[маска]"
    assert len(winter) == 90, f"в winter {len(winter)} строк, а зимних дней (декабрь, январь, февраль) 90: месяц .isin([12, 1, 2])"
    assert set(winter["date"].dt.month) == {12, 1, 2}, "в winter должны быть только декабрь, январь и февраль"


def test_thaws():
    "thaws — оттепели, warmest_date — самый тёплый зимний день"
    assert isinstance(thaws, pd.DataFrame), f"thaws — это {type(thaws).__name__}, а нужна таблица"
    assert list(thaws.columns) == ["date", "temp_max"], f"столбцы thaws сейчас {list(thaws.columns)}, а нужны date и temp_max"
    assert len(thaws) == 5 and thaws["temp_max"].min() > 0, f"в thaws {len(thaws)} строк, а зимних дней с максимумом выше нуля 5"
    assert not isinstance(warmest_date, pd.Series), "warmest_date — целая строка, а нужна одна дата: winter.loc[метка, \"date\"]"
    assert warmest_date == pd.to_datetime("2025-12-03"), f"warmest_date = {warmest_date}, а самый тёплый зимний день — 3 декабря"
# ─── другое решение ───
moscow = weather[weather["city"] == "Москва"]
winter = moscow[(moscow["date"] < "2025-03-01") | (moscow["date"] >= "2025-12-01")]
thaws = winter[winter["temp_max"] > 0][["date", "temp_max"]]
warmest_date = winter.nlargest(1, "temp_max")["date"].iloc[0]
# ─── ошибка ───
moscow = weather[weather["city"] == "Москва"]
winter = moscow[moscow["date"].dt.month.isin([12, 1, 2])]
thaws = winter.loc[winter["temp_max"] > 0]
warmest_date = winter.loc[winter["temp_max"].idxmax(), "date"]
# ─── ошибка ───
moscow = weather[weather["city"] == "Москва"]
winter = moscow[moscow["date"].dt.month.isin([1, 2])]
thaws = winter.loc[winter["temp_max"] > 0, ["date", "temp_max"]]
warmest_date = winter.loc[winter["temp_max"].idxmax(), "date"]

# %% summary
print("Средняя температура: Сочи", round(sochi_mean, 1), "· Новосибирск", round(nsk_mean, 1))
print("Разброс (std): Сочи", round(sochi_std, 1), "· Новосибирск", round(nsk_std, 1))
print("Осадки за год, мм: Сочи", round(sochi_total), "· Новосибирск", round(nsk_total))
print("Дней с осадками: Сочи", round(sochi_rainy * 100), "% · Новосибирск", round(nsk_rainy * 100), "%")
print("Годовая амплитуда в Новосибирске:", round(amplitude, 1), "градуса")
print("Оттепелей в Москве за зиму:", len(thaws))
