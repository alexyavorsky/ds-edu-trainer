# Урок pd-plot. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% data
import pandas as pd

orders = pd.read_csv("data/shop_orders.csv", parse_dates=["date"])
orders["revenue"] = orders["price"] * orders["quantity"]
orders["month"] = orders["date"].dt.month
monthly = orders.groupby("month")["revenue"].sum()
monthly.head(3)

# %% first
monthly.plot()

# %% titled
ax = monthly.plot(title="Выручка по месяцам, 2025")
ax.set_xlabel("месяц")
ax.set_ylabel("₽")

# %% line [exercise]
items = orders.groupby("month")["quantity"].sum()
ax = items.plot(title="Продано штук по месяцам")
ax.set_ylabel("штук")
# ─── заготовка ───
items = orders.groupby("month")["quantity"].sum()
ax = ...
# ─── проверка ───
def test_line():
    "ax — линейный график ряда items"
    assert hasattr(ax, "get_title") and hasattr(ax, "lines"), f"ax — это {type(ax).__name__}, а нужен график: ax = items.plot(...)"
    assert len(ax.lines) == 1, f"на графике линий: {len(ax.lines)}, а нужна одна. Если вы вызвали plot в этой ячейке дважды, линии сложились на одном графике — оставьте один вызов"
    assert list(ax.lines[0].get_ydata()) == items.tolist(), "на графике не те значения: строить нужно ряд items"


def test_labels():
    "заголовок и подпись оси Y"
    assert hasattr(ax, "get_title"), "сначала постройте график и сохраните его в ax"
    assert ax.get_title() == "Продано штук по месяцам", f"заголовок сейчас {ax.get_title()!r}, а нужен «Продано штук по месяцам»: параметр title="
    assert ax.get_ylabel() == "штук", f"подпись оси Y сейчас {ax.get_ylabel()!r}, а нужна «штук»: ax.set_ylabel(\"штук\")"
# ─── другое решение ───
items = orders.groupby("month")["quantity"].sum()
ax = items.plot(kind="line")
ax.set_title("Продано штук по месяцам")
ax.set_ylabel("штук")
# ─── ошибка ───
items = orders.groupby("month")["quantity"].sum()
ax = items.plot()
# ─── ошибка ───
items = orders.groupby("month")["quantity"].sum()
ax = monthly.plot(title="Продано штук по месяцам")
ax.set_ylabel("штук")

# %% bar-wrong
by_category = orders.groupby("category")["revenue"].sum()
by_category.plot(title="Линия для категорий — плохая идея")

# %% bar
by_category.sort_values(ascending=False).plot(kind="bar", title="Выручка по категориям", rot=0)

# %% barh
by_product = orders.groupby("product")["revenue"].sum().sort_values()
by_product.tail(8).plot(kind="barh", title="Восемь товаров с наибольшей выручкой")

# %% bars [exercise]
by_city = orders.groupby("city")["revenue"].sum().sort_values(ascending=False)
ax = by_city.plot(kind="bar", title="Выручка по городам", rot=0)
# ─── заготовка ───
by_city = ...
ax = ...
# ─── проверка ───
def test_series():
    "by_city — выручка по городам, по убыванию"
    assert isinstance(by_city, pd.Series) and len(by_city) == 5, "by_city — Series по пяти городам: orders.groupby(\"city\")[\"revenue\"].sum()"
    assert by_city.tolist() == sorted(by_city.tolist(), reverse=True), "отсортируйте by_city по убыванию: sort_values(ascending=False)"
    assert by_city.index[0] == "Москва" and by_city.iloc[0] == 1310110, "первой должна быть Москва с выручкой 1310110"


def test_bars():
    "ax — столбчатая диаграмма с заголовком"
    assert hasattr(ax, "patches") and hasattr(ax, "get_title"), f"ax — это {type(ax).__name__}, а нужен график: ax = by_city.plot(kind=\"bar\", ...)"
    assert len(ax.patches) != 0, "на графике нет столбцов: похоже, построена линия — нужен kind=\"bar\""
    assert len(ax.patches) == 5, f"столбцов на графике: {len(ax.patches)}, а городов пять"
    heights = [p.get_height() for p in ax.patches]
    assert heights == by_city.tolist(), "высоты столбцов должны совпадать со значениями by_city — от большего к меньшему"
    assert ax.get_title() == "Выручка по городам", f"заголовок сейчас {ax.get_title()!r}, а нужен «Выручка по городам»"
# ─── другое решение ───
by_city = orders.groupby("city")["revenue"].sum().sort_values(ascending=False)
ax = by_city.plot.bar(title="Выручка по городам")
# ─── ошибка ───
by_city = orders.groupby("city")["revenue"].sum().sort_values(ascending=False)
ax = by_city.plot(title="Выручка по городам")
# ─── ошибка ───
by_city = orders.groupby("city")["revenue"].sum()
ax = by_city.plot(kind="bar", title="Выручка по городам", rot=0)

# %% hist
orders["revenue"].plot(kind="hist", bins=30, title="Выручка одной строки заказа")

# %% hist-quiz [quiz]
ax_q = pd.Series([1, 2, 2, 3, 3, 3]).plot(kind="hist", bins=3)
print(int(max(p.get_height() for p in ax_q.patches)))

# %% temps [exercise]
weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
moscow_temp = weather.loc[weather["city"] == "Москва", "temp_max"]
ax = moscow_temp.plot(kind="hist", bins=20, title="Дневной максимум в Москве")
ax.set_xlabel("°C")
# ─── заготовка ───
weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
moscow_temp = ...
ax = ...
# ─── проверка ───
def test_temp():
    "moscow_temp — дневной максимум в Москве"
    assert isinstance(moscow_temp, pd.Series) and len(moscow_temp) == 365, "moscow_temp — столбец temp_max по строкам Москвы: weather.loc[weather[\"city\"] == \"Москва\", \"temp_max\"]"
    assert abs(moscow_temp.max() - 27.2) < 1e-9, "в moscow_temp должен быть столбец temp_max"


def test_hist():
    "ax — гистограмма из 20 столбцов с подписями"
    assert hasattr(ax, "patches") and hasattr(ax, "get_title"), f"ax — это {type(ax).__name__}, а нужен график: ax = moscow_temp.plot(kind=\"hist\", ...)"
    assert len(ax.patches) != 10, "на гистограмме 10 столбцов — это значение по умолчанию; нужно 20: bins=20"
    assert len(ax.patches) == 20, f"столбцов на гистограмме: {len(ax.patches)}, а нужно 20: kind=\"hist\", bins=20"
    assert sum(p.get_height() for p in ax.patches) == 365, "в гистограмму должны попасть все 365 дней"
    assert ax.get_title() == "Дневной максимум в Москве", f"заголовок сейчас {ax.get_title()!r}, а нужен «Дневной максимум в Москве»"
    assert ax.get_xlabel() == "°C", f"подпись оси X сейчас {ax.get_xlabel()!r}, а нужна «°C»: ax.set_xlabel(\"°C\")"
# ─── другое решение ───
weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
moscow_temp = weather[weather["city"] == "Москва"]["temp_max"]
ax = moscow_temp.plot.hist(bins=20)
ax.set_title("Дневной максимум в Москве")
ax.set_xlabel("°C")
# ─── ошибка ───
weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
moscow_temp = weather.loc[weather["city"] == "Москва", "temp_max"]
ax = moscow_temp.plot(kind="hist", title="Дневной максимум в Москве")
ax.set_xlabel("°C")
# ─── ошибка ───
weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
moscow_temp = weather.loc[weather["city"] == "Москва", "temp_max"]
ax = moscow_temp.plot(title="Дневной максимум в Москве")
ax.set_xlabel("°C")

# %% table
by_channel = orders.pivot_table(values="revenue", index="month", columns="channel", aggfunc="sum")
by_channel.head(3)

# %% table-plot
by_channel.plot(title="Выручка по каналам")

# %% smooth
daily = orders.groupby("date")["revenue"].sum().reindex(pd.date_range("2025-01-01", "2025-12-31"), fill_value=0)
ax = daily.plot(title="Выручка по дням и среднее за 7 дней", alpha=0.35)
daily.rolling(7).mean().plot(ax=ax)

# %% cities [exercise]
weather["month"] = weather["date"].dt.month
month_temp = weather.pivot_table(values="temp_max", index="month", columns="city", aggfunc="mean")
ax = month_temp[["Сочи", "Москва", "Новосибирск"]].plot(title="Средний дневной максимум по месяцам")
ax.set_ylabel("°C")
# ─── заготовка ───
weather["month"] = weather["date"].dt.month
month_temp = ...
ax = ...
# ─── проверка ───
def test_table():
    "month_temp — средний дневной максимум: месяцы × города"
    assert isinstance(month_temp, pd.DataFrame), f"month_temp — это {type(month_temp).__name__}, а нужна таблица: weather.pivot_table(...)"
    assert month_temp.shape == (12, 5), f"у month_temp размер {month_temp.shape}, а нужно 12 месяцев × 5 городов: index=\"month\", columns=\"city\""
    assert list(month_temp.index) == list(range(1, 13)) and "Сочи" in month_temp.columns, "в строках — месяцы 1–12, в столбцах — города"
    assert abs(month_temp.loc[7, "Сочи"] - 24.35) < 0.01, "в ячейках должен быть средний temp_max за месяц: values=\"temp_max\", aggfunc=\"mean\""


def test_plot():
    "ax — три линии: Сочи, Москва, Новосибирск"
    assert hasattr(ax, "lines") and hasattr(ax, "get_title"), f"ax — это {type(ax).__name__}, а нужен график: ax = month_temp[[...]].plot(...)"
    assert len(ax.lines) != 5, "на графике пять линий, а нужны три города: выберите столбцы списком до .plot"
    assert len(ax.lines) == 3, f"линий на графике: {len(ax.lines)}, а нужны три. Если вы строили график в этой ячейке дважды, оставьте один вызов plot"
    labels = [line.get_label() for line in ax.lines]
    assert labels == ["Сочи", "Москва", "Новосибирск"], f"линии сейчас {labels}, а нужны Сочи, Москва, Новосибирск — в этом порядке"
    assert ax.get_title() == "Средний дневной максимум по месяцам", f"заголовок сейчас {ax.get_title()!r}"
    assert ax.get_ylabel() == "°C", f"подпись оси Y сейчас {ax.get_ylabel()!r}, а нужна «°C»"
# ─── другое решение ───
weather["month"] = weather["date"].dt.month
month_temp = weather.groupby(["month", "city"])["temp_max"].mean().unstack()
ax = month_temp.loc[:, ["Сочи", "Москва", "Новосибирск"]].plot()
ax.set_title("Средний дневной максимум по месяцам")
ax.set_ylabel("°C")
# ─── ошибка ───
weather["month"] = weather["date"].dt.month
month_temp = weather.pivot_table(values="temp_max", index="month", columns="city", aggfunc="mean")
ax = month_temp.plot(title="Средний дневной максимум по месяцам")
ax.set_ylabel("°C")
