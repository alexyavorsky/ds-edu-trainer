# Урок pd-strings. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% load
import pandas as pd

supplier = pd.read_csv("data/supplier_prices.csv")
supplier["name"].head(6).tolist()

# %% no-str [raises=AttributeError]
supplier["name"].lower()

# %% lower
supplier["name"].str.lower().head(4)

# %% len
print(supplier["name"].str.len().head(6).tolist())
print(supplier["name"].str.strip().str.len().head(6).tolist())

# %% invisible
print((supplier["name"] == "Шоколад горький").sum())
print((supplier["name"].str.strip() == "Шоколад горький").sum())

# %% chain
stripped = supplier["name"].str.strip()
print(stripped.str.upper().head(3).tolist())
print(stripped.str.title().head(3).tolist())

# %% names [exercise]
supplier["name"] = supplier["name"].str.strip().str.capitalize()
# ─── заготовка ───
# приведите в порядок столбец name таблицы supplier
# ─── проверка ───
def test_names():
    "названия без лишних пробелов, с заглавной буквы"
    names = supplier["name"].tolist()
    assert all(isinstance(n, str) for n in names), "в столбце name должен остаться текст"
    assert all(n == n.strip() for n in names), "в названиях остались пробелы в начале или в конце: .str.strip(). Результат нужно записать обратно в supplier[\"name\"]"
    assert "БРАЗИЛИЯ 1 КГ" not in names, "остались названия заглавными буквами: .str.capitalize()"
    assert "Бразилия 1 Кг" not in names, "каждое слово стало с заглавной (title), а нужна заглавной только первая буква названия: capitalize"
    assert "эфиопия 250 г" not in names, "остались названия со строчной буквы: .str.capitalize()"
    assert names[:4] == ["Эспрессо-смесь 1 кг", "Колумбия 250 г", "Эфиопия 250 г", "Бразилия 1 кг"], f"первые названия сейчас {names[:4]}"
    assert supplier["name"].nunique() == 20 and names[13] == "Кружка 350 мл", "не все названия приведены к виду «Кружка 350 мл»"
# ─── другое решение ───
supplier["name"] = supplier["name"].str.lower().str.strip().str.capitalize()
# ─── ошибка ───
supplier["name"].str.strip().str.capitalize()
# ─── ошибка ───
supplier["name"] = supplier["name"].str.capitalize()
# ─── ошибка ───
supplier["name"] = supplier["name"].str.strip().str.title()

# %% replace
supplier["price"].str.replace(" ₽", "").head(3).tolist()

# %% replace-whole
supplier["price"].replace(" ₽", "").head(3).tolist()

# %% price [exercise]
supplier["price"] = supplier["price"].str.replace(" ₽", "").str.replace(" ", "").astype("int64")
price_total = supplier["price"].sum()
# ─── заготовка ───
# превратите столбец price таблицы supplier в числа
price_total = ...
# ─── проверка ───
def test_price():
    "price — целые числа"
    assert str(supplier["price"].dtype) != "str", "столбец price всё ещё текстовый: после замен добавьте astype(\"int64\") и запишите результат в supplier[\"price\"]"
    assert supplier["price"].isna().sum() == 0, "в price появились пропуски: сначала уберите из текста пробелы и знак ₽, потом меняйте тип"
    assert str(supplier["price"].dtype) in ("int64", "int32"), f"тип price — {supplier['price'].dtype}, а нужен целый"
    assert supplier["price"].tolist()[:4] == [1560, 760, 830, 1370], f"первые цены — {supplier['price'].tolist()[:4]}, а должны быть [1560, 760, 830, 1370]"


def test_total():
    "price_total — сумма цен"
    assert not isinstance(price_total, str), "price_total — склеенная строка: сумму считают после перевода в числа"
    assert price_total == 19490, f"price_total = {price_total!r}, а сумма цен — 19490"
# ─── другое решение ───
digits = supplier["price"].astype(str).str.replace("₽", "").str.replace(" ", "")
supplier["price"] = pd.to_numeric(digits)
price_total = sum(supplier["price"])
# ─── ошибка ───
supplier["price"] = pd.to_numeric(supplier["price"], errors="coerce")
price_total = supplier["price"].sum()
# ─── ошибка ───
supplier["price"] = supplier["price"].str.replace(" ₽", "").str.replace(" ", "")
price_total = supplier["price"].sum()

# %% contains
supplier[supplier["name"].str.contains("кофе")]

# %% contains-case
supplier.loc[supplier["name"].str.contains("кофе", case=False), "name"].tolist()

# %% strip-quiz [quiz]
print(pd.Series([" кофе", "кофе ", "Кофе"]).str.strip().nunique())

# %% tea [exercise]
with_tea = supplier[supplier["name"].str.contains("чай", case=False)]
real_tea = supplier[supplier["category"] == "Чай"]
# ─── заготовка ───
with_tea = ...
real_tea = ...
# ─── проверка ───
def test_with_tea():
    "with_tea — товары со словом «чай» в названии"
    assert isinstance(with_tea, pd.DataFrame), f"with_tea — это {type(with_tea).__name__}, а нужна таблица: supplier[маска]"
    assert len(with_tea) != 2, "найдено два товара: «Чайник» пишется с заглавной буквы — добавьте case=False"
    assert len(with_tea) == 3, f"в with_tea {len(with_tea)} строк, а «чай» без учёта регистра встречается в трёх названиях"
    assert "Чайник заварочный" in with_tea["name"].tolist(), "в with_tea должен попасть и заварочный чайник — в его названии тоже есть «чай»"


def test_real_tea():
    "real_tea — товары категории «Чай»"
    assert isinstance(real_tea, pd.DataFrame), f"real_tea — это {type(real_tea).__name__}, а нужна таблица"
    assert len(real_tea) == 4 and (real_tea["category"] == "Чай").all(), f"в real_tea {len(real_tea)} строк, а товаров категории «Чай» четыре"
# ─── другое решение ───
with_tea = supplier[supplier["name"].str.lower().str.contains("чай")]
real_tea = supplier.query("category == 'Чай'")
# ─── ошибка ───
with_tea = supplier[supplier["name"].str.contains("чай")]
real_tea = supplier[supplier["category"] == "Чай"]
# ─── ошибка ───
with_tea = supplier[supplier["name"].str.contains("чай", case=False)]
real_tea = supplier[supplier["name"].str.contains("чай", case=False)]

# %% split
words = supplier["name"].str.split()
words.head(3).tolist()

# %% split-item
print(words.str[0].head(3).tolist())
print(words.str[-1].head(3).tolist())

# %% slice
print(supplier["updated"].head(3).tolist())
print(supplier["updated"].str[:2].head(3).tolist())

# %% concat
(supplier["product_id"] + ": " + supplier["name"]).head(3).tolist()

# %% units [exercise]
supplier["unit"] = supplier["name"].str.split().str[-1]
n_grams = (supplier["unit"] == "г").sum()
# ─── заготовка ───
# добавьте в supplier столбец unit — последнее слово названия
n_grams = ...
# ─── проверка ───
def test_unit():
    "unit — последнее слово названия"
    assert "unit" in supplier.columns, "в supplier нет столбца unit"
    assert supplier.loc[0, "unit"] != "Эспрессо-смесь", "в unit попало первое слово, а нужно последнее: индекс -1"
    assert isinstance(supplier.loc[0, "unit"], str), "в unit лежат списки слов: достаньте из списка последний элемент — .str[-1]"
    assert supplier["unit"].tolist()[:4] == ["кг", "г", "г", "кг"], f"первые значения unit — {supplier['unit'].tolist()[:4]}, а должны быть ['кг', 'г', 'г', 'кг']"
    assert supplier.loc[12, "unit"] == "Зефир", "у названия из одного слова последнее слово — оно само"


def test_grams():
    "n_grams — сколько товаров продаётся в граммах"
    assert n_grams != 9, "9 — названия, которые заканчиваются на букву «г», включая «кг». Сравнивайте слово целиком: supplier[\"unit\"] == \"г\""
    assert n_grams == 7, f"n_grams = {n_grams!r}, а товаров в граммах 7"
# ─── другое решение ───
supplier["unit"] = [name.split()[-1] for name in supplier["name"]]
n_grams = supplier["unit"].value_counts()["г"]
# ─── ошибка ───
supplier["unit"] = supplier["name"].str.split().str[0]
n_grams = (supplier["unit"] == "г").sum()
# ─── ошибка ───
supplier["unit"] = supplier["name"].str.split().str[-1]
n_grams = supplier["name"].str.endswith("г").sum()
