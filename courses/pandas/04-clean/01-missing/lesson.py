# Урок pd-missing. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

delivery = pd.read_csv("data/delivery_h1.csv")
delivery.head()

# %% isna
delivery["rating"].isna().head()

# %% isna-sum
delivery.isna().sum()

# %% count
print(len(delivery))
print(delivery["rating"].count())
delivery.count()

# %% gaps [exercise]
gap_share = delivery.isna().mean()
no_rating = delivery[delivery["rating"].isna()]
# ─── заготовка ───
gap_share = ...
no_rating = ...
# ─── проверка ───
def test_share():
    "gap_share — доля пропусков в каждом столбце"
    assert isinstance(gap_share, pd.Series), f"gap_share — это {type(gap_share).__name__}, а нужен Series: среднее маски isna() по столбцам"
    assert list(gap_share.index) == ["order_id", "days", "rating"], f"метки сейчас {list(gap_share.index)}, а нужны названия трёх столбцов: delivery.isna().mean()"
    assert gap_share["rating"] != 287, "это число пропусков (sum), а нужна доля — mean"
    assert abs(gap_share["rating"] - 287 / 816) < 1e-9, f"доля пропусков в rating — {gap_share['rating']}, а должна быть ≈ 0.352"
    assert abs(gap_share["days"] - 36 / 816) < 1e-9, "доля пропусков в days должна быть ≈ 0.044"


def test_rows():
    "no_rating — строки без оценки"
    assert isinstance(no_rating, pd.DataFrame), f"no_rating — это {type(no_rating).__name__}, а нужна таблица: delivery[маска]"
    assert len(no_rating) != 529, "в no_rating строки С оценкой, а нужны без неё: маска isna(), а не notna()"
    assert len(no_rating) == 287 and no_rating["rating"].isna().all(), f"в no_rating {len(no_rating)} строк, а заказов без оценки 287"
# ─── другое решение ───
gap_share = delivery.isna().sum() / len(delivery)
no_rating = delivery[~delivery["rating"].notna()]
# ─── ошибка ───
gap_share = delivery.isna().sum()
no_rating = delivery[delivery["rating"].isna()]
# ─── ошибка ───
gap_share = delivery.isna().mean()
no_rating = delivery[delivery["rating"].notna()]

# %% nan
import numpy as np

print(np.nan == np.nan)
print((delivery["rating"] == np.nan).sum())
print(np.nan + 1)

# %% skip
print(delivery["rating"].sum())
print(delivery["rating"].mean())
print(delivery["rating"].sum() / len(delivery))

# %% compare
print((delivery["days"] > 5).sum())
print((delivery["days"] > 5).mean())

# %% mean-quiz [quiz]
print(pd.Series([1, np.nan, 3]).mean())

# %% late [exercise]
known_days = delivery.loc[delivery["days"].notna(), "days"]
late_share = (known_days > 5).mean()
# ─── заготовка ───
known_days = ...
late_share = ...
# ─── проверка ───
def test_known():
    "known_days — известные сроки"
    assert isinstance(known_days, pd.Series), f"known_days — это {type(known_days).__name__}, а нужен Series: столбец days без пропусков"
    assert known_days.notna().all(), "в known_days остались пропуски: отберите строки маской notna() или уберите их dropna()"
    assert len(known_days) == 780, f"в known_days {len(known_days)} значений, а известных сроков 780"


def test_share():
    "late_share — доля опозданий среди известных сроков"
    assert abs(late_share - 150 / 816) > 1e-9, "доля посчитана по всем заказам: 36 заказов без срока записаны в «доставленные вовремя». Считайте по known_days"
    assert late_share != 150, "150 — число опозданий, а нужна доля: среднее маски"
    assert abs(late_share - 150 / 780) < 1e-9, f"late_share = {late_share!r}, а доля опозданий ≈ 0.192"
# ─── другое решение ───
known_days = delivery["days"].dropna()
late_share = (known_days > 5).sum() / len(known_days)
# ─── ошибка ───
known_days = delivery["days"].dropna()
late_share = (delivery["days"] > 5).mean()

# %% dropna
print(len(delivery.dropna()))
print(len(delivery.dropna(subset=["days"])))

# %% fillna
delivery["rating"].fillna(0).head()

# %% fillna-trap
print(delivery["rating"].mean())
print(delivery["rating"].fillna(0).mean())

# %% fillna-median
median_days = delivery["days"].median()
print(median_days)
print(delivery["days"].fillna(median_days).isna().sum())

# %% rated [exercise]
rated = delivery.dropna(subset=["rating"])
avg_rating = rated["rating"].mean()
# ─── заготовка ───
rated = ...
avg_rating = ...
# ─── проверка ───
def test_rated():
    "rated — заказы с оценкой"
    assert isinstance(rated, pd.DataFrame), f"rated — это {type(rated).__name__}, а нужна таблица: delivery.dropna(...)"
    assert len(rated) != 505, "в rated 505 строк: dropna() без subset убрал и заказы, у которых пропущен только срок. Нужен subset=[\"rating\"]"
    assert len(rated) == 529, f"в rated {len(rated)} строк, а заказов с оценкой 529"
    assert rated["rating"].notna().all(), "в rated остались строки без оценки"


def test_avg():
    "avg_rating — средняя оценка"
    assert abs(avg_rating - 2.39338) > 1e-4, "это среднее с нулями вместо пропусков: нули — не оценки. Считайте среднее по rated"
    assert abs(avg_rating - 3.691871) < 1e-5, f"avg_rating = {avg_rating!r}, а средняя оценка ≈ 3.69"
# ─── другое решение ───
rated = delivery[delivery["rating"].notna()]
avg_rating = delivery["rating"].mean()
# ─── ошибка ───
rated = delivery.dropna()
avg_rating = rated["rating"].mean()
# ─── ошибка ───
rated = delivery.dropna(subset=["rating"])
avg_rating = delivery["rating"].fillna(0).mean()

# %% fill [exercise]
filled = delivery.copy()
filled["days"] = filled["days"].fillna(filled["days"].median())
n_gaps_left = filled["days"].isna().sum()
# ─── заготовка ───
filled = delivery.copy()
# заполните пропуски в столбце days таблицы filled медианой
n_gaps_left = ...
# ─── проверка ───
def test_filled():
    "в filled пропуски days заполнены медианой"
    assert isinstance(filled, pd.DataFrame) and filled.shape == (816, 3), "filled должна остаться таблицей 816 × 3"
    assert filled["days"].isna().sum() != 36, "пропуски в filled[\"days\"] остались. fillna возвращает новый Series — его нужно записать обратно: filled[\"days\"] = filled[\"days\"].fillna(...)"
    assert filled["days"].isna().sum() == 0, "в filled[\"days\"] ещё есть пропуски"
    assert filled["days"].sum() != 3257, "пропуски заполнены нулями, а нужна медиана столбца"
    assert filled["days"].sum() == 3401, "пропуски нужно заполнить медианой срока — 4 дня: filled[\"days\"].median()"
    assert filled["rating"].isna().sum() == 287, "столбец rating заполнять не нужно"


def test_left():
    "n_gaps_left — сколько пропусков осталось в days"
    assert n_gaps_left == 0, f"n_gaps_left = {n_gaps_left!r}, а после заполнения пропусков быть не должно: filled[\"days\"].isna().sum()"


def test_delivery_kept():
    "таблица delivery не изменилась"
    assert delivery["days"].isna().sum() == 36, "пропуски в delivery тоже заполнены, а менять нужно только filled. Выполните ячейку «Доставка: первое полугодие» ещё раз"
# ─── другое решение ───
filled = delivery.copy()
filled = filled.fillna({"days": filled["days"].median()})
n_gaps_left = len(filled) - filled["days"].count()
# ─── ошибка ───
filled = delivery.copy()
filled["days"].fillna(filled["days"].median())
n_gaps_left = 0
# ─── ошибка ───
filled = delivery.copy()
filled["days"] = filled["days"].fillna(0)
n_gaps_left = filled["days"].isna().sum()
