# Урок pd-cut. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% intervals
import pandas as pd

weather = pd.read_csv("data/weather.csv", parse_dates=["date"])
moscow = weather[weather["city"] == "Москва"].copy()
pd.cut(moscow["temp_max"], bins=[-50, 0, 15, 25, 50]).head(3)

# %% interval-counts
pd.cut(moscow["temp_max"], bins=[-50, 0, 15, 25, 50]).value_counts().sort_index()

# %% labels
names = ["ниже нуля", "прохладно", "тепло", "жарко"]
moscow["kind"] = pd.cut(moscow["temp_max"], bins=[-50, 0, 15, 25, 50], labels=names)
moscow[["date", "temp_max", "kind"]].head(3)

# %% label-counts
moscow["kind"].value_counts().sort_index()

# %% sochi [exercise]
sochi = weather[weather["city"] == "Сочи"].copy()
sochi["kind"] = pd.cut(sochi["temp_max"], bins=[-50, 0, 15, 25, 50], labels=["ниже нуля", "прохладно", "тепло", "жарко"])
kinds = sochi["kind"].value_counts().sort_index()
# ─── заготовка ───
sochi = weather[weather["city"] == "Сочи"].copy()
# добавьте в sochi столбец kind
kinds = ...
# ─── проверка ───
def test_kind():
    "kind — тип дня по дневному максимуму"
    assert "kind" in sochi.columns, "в sochi нет столбца kind"
    assert sochi["kind"].isna().sum() == 0, "в kind есть пропуски: границы должны покрывать все температуры"
    found = sorted(map(str, sochi["kind"].unique()))
    assert set(found) <= {"ниже нуля", "прохладно", "тепло", "жарко"}, f"в kind значения {found}, а нужны подписи типов дней: вспомните параметр labels"
    assert (sochi["kind"] == "жарко").sum() == 50, "границы не те: сверьте их с условием"


def test_kinds():
    "kinds — сколько дней каждого типа, по порядку шкалы"
    assert isinstance(kinds, pd.Series), f"kinds — это {type(kinds).__name__}, а нужен результат value_counts()"
    assert list(kinds.index) != ["тепло", "прохладно", "жарко", "ниже нуля"], "типы идут по убыванию числа дней, а нужны по порядку шкалы: отсортируйте по индексу"
    assert list(kinds.index) == ["ниже нуля", "прохладно", "тепло", "жарко"], f"порядок сейчас {list(kinds.index)}, а нужен от «ниже нуля» к «жарко»"
    assert kinds.tolist() == [0, 137, 178, 50], f"значения сейчас {kinds.tolist()}"
# ─── другое решение ───
sochi = weather[weather["city"] == "Сочи"].copy()
sochi = sochi.assign(kind=pd.cut(sochi["temp_max"], [-50, 0, 15, 25, 50], labels=["ниже нуля", "прохладно", "тепло", "жарко"]))
kinds = sochi["kind"].value_counts(sort=False)
# ─── ошибка ───
sochi = weather[weather["city"] == "Сочи"].copy()
sochi["kind"] = pd.cut(sochi["temp_max"], bins=[-50, 0, 15, 25, 50], labels=["ниже нуля", "прохладно", "тепло", "жарко"])
kinds = sochi["kind"].value_counts()
# ─── ошибка ───
sochi = weather[weather["city"] == "Сочи"].copy()
sochi["kind"] = pd.cut(sochi["temp_max"], bins=[0, 15, 25, 50], labels=["прохладно", "тепло", "жарко"])
kinds = sochi["kind"].value_counts().sort_index()

# %% edges
marks = pd.Series([0, 15, 15.1, 25])
print(pd.cut(marks, bins=[0, 15, 25]).tolist())

# %% edges-left
print(pd.cut(marks, bins=[0, 15, 25], right=False).tolist())

# %% outside
ages = pd.Series([5, 15, 30, 60])
pd.cut(ages, bins=[0, 15, 30], labels=["дети", "молодые"])

# %% edge-quiz [quiz]
print(pd.cut(pd.Series([10]), bins=[0, 10, 20], labels=["низкий", "высокий"]).tolist()[0])

# %% speed [exercise]
delivery = pd.read_csv("data/delivery_h1.csv")
delivery["speed"] = pd.cut(delivery["days"], bins=[0, 3, 5, 14], labels=["быстро", "нормально", "долго"])
speed_share = delivery["speed"].value_counts(normalize=True).sort_index()
# ─── заготовка ───
delivery = pd.read_csv("data/delivery_h1.csv")
# добавьте в delivery столбец speed
speed_share = ...
# ─── проверка ───
def test_speed():
    "speed — быстро (до 3 дней), нормально (4–5), долго (6 и больше)"
    assert "speed" in delivery.columns, "в delivery нет столбца speed"
    assert (delivery["speed"] == "быстро").sum() != 119, "3 дня должны считаться «быстро»: интервал (0, 3] включает правую границу"
    assert (delivery["speed"] == "быстро").sum() == 309, "границы не те: сверьте их с условием"
    assert delivery["speed"].isna().sum() != 43, "заказы, которые везли дольше 10 дней, стали пропусками: последняя граница должна покрывать самый долгий срок"
    assert delivery["speed"].isna().sum() == 36, f"в speed {delivery['speed'].isna().sum()} пропусков: пропуски должны остаться только там, где срок неизвестен"


def test_share():
    "speed_share — доли по порядку шкалы"
    assert isinstance(speed_share, pd.Series), f"speed_share — это {type(speed_share).__name__}, а нужен Series"
    assert list(speed_share.index) == ["быстро", "нормально", "долго"], f"порядок сейчас {list(speed_share.index)}, а нужен быстро, нормально, долго"
    assert abs(speed_share["быстро"] - 309) > 1, "в speed_share числа заказов, а нужны доли"
    assert abs(speed_share["быстро"] - 309 / 780) < 1e-9 and abs(speed_share["долго"] - 150 / 780) < 1e-9, "доли не те: нужны доли заказов в каждой группе speed"
# ─── другое решение ───
delivery = pd.read_csv("data/delivery_h1.csv")
delivery["speed"] = pd.cut(delivery["days"], bins=[1, 4, 6, 20], labels=["быстро", "нормально", "долго"], right=False)
speed_share = (delivery["speed"].value_counts() / delivery["speed"].count()).sort_index()
# ─── ошибка ───
delivery = pd.read_csv("data/delivery_h1.csv")
delivery["speed"] = pd.cut(delivery["days"], bins=[0, 3, 5, 10], labels=["быстро", "нормально", "долго"])
speed_share = delivery["speed"].value_counts(normalize=True).sort_index()
# ─── ошибка ───
delivery = pd.read_csv("data/delivery_h1.csv")
delivery["speed"] = pd.cut(delivery["days"], bins=[0, 3, 5, 14], labels=["быстро", "нормально", "долго"], right=False)
speed_share = delivery["speed"].value_counts(normalize=True).sort_index()

# %% equal-width
pd.cut(moscow["wind_ms"], bins=3).value_counts().sort_index()

# %% qcut
orders = pd.read_csv("data/shop_orders.csv")
revenue = orders["price"] * orders["quantity"]
pd.qcut(revenue, 4).value_counts().sort_index()

# %% size [exercise]
orders["size"] = pd.qcut(revenue, 4, labels=["малая", "средняя", "крупная", "очень крупная"])
big = orders[orders["size"] == "очень крупная"]
big_min = (big["price"] * big["quantity"]).min()
# ─── заготовка ───
# добавьте в orders столбец size
big = ...
big_min = ...
# ─── проверка ───
def test_size():
    "size — четверть, в которую попала выручка строки"
    assert "size" in orders.columns, "в orders нет столбца size"
    found = set(map(str, orders["size"].unique()))
    assert found == {"малая", "средняя", "крупная", "очень крупная"}, f"в size значения {sorted(found)}, а нужны четыре подписи: малая, средняя, крупная, очень крупная"
    assert (orders["size"] == "малая").sum() < 2000, "использован pd.cut — он делит на интервалы равной ширины, и почти все строки попали в первый. Равные по числу строк группы делает pd.qcut"
    assert (orders["size"] == "малая").sum() == 612 and (orders["size"] == "очень крупная").sum() == 573, "группы не те: нужны четыре равные по числу строк группы по выручке, подписи — от малой к очень крупной"


def test_big():
    "big — строки верхней четверти, big_min — с какой выручки она начинается"
    assert isinstance(big, pd.DataFrame), f"big — это {type(big).__name__}, а нужна таблица"
    assert len(big) == 573, f"в big {len(big)} строк: нужны все строки группы «очень крупная»"
    assert big_min > 1580 and big_min <= 1600, f"big_min = {big_min!r} — это не наименьшая выручка в верхней четверти"
# ─── другое решение ───
orders["size"] = pd.qcut(revenue, [0, 0.25, 0.5, 0.75, 1], labels=["малая", "средняя", "крупная", "очень крупная"])
big = orders[revenue > revenue.quantile(0.75)]
big_min = revenue[revenue > revenue.quantile(0.75)].min()
# ─── ошибка ───
orders["size"] = pd.cut(revenue, 4, labels=["малая", "средняя", "крупная", "очень крупная"])
big = orders[orders["size"] == "очень крупная"]
big_min = (big["price"] * big["quantity"]).min()
# ─── ошибка ───
orders["size"] = pd.qcut(revenue, 4, labels=["очень крупная", "крупная", "средняя", "малая"])
big = orders[orders["size"] == "очень крупная"]
big_min = (big["price"] * big["quantity"]).min()
