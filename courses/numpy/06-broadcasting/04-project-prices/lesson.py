# Урок np-project-prices. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% data
import numpy as np

goods = ["эспрессо-смесь 1 кг", "колумбия 250 г", "эфиопия 250 г", "чёрный чай 100 г", "фильтры"]
cost = np.array([870, 380, 430, 150, 250])              # себестоимость штуки, ₽
markup = np.array([1.5, 1.6, 1.6, 2.0, 2.2])            # наценка товара
amounts = np.array([1, 5, 10, 50])                      # варианты количества
volume_discount = np.array([0, 0.05, 0.10, 0.20])       # скидка за объём
print(cost.shape, markup.shape, amounts.shape, volume_discount.shape)

# %% base [exercise]
base = cost[:, np.newaxis] * amounts
# ─── заготовка ───
base = ...
# ─── проверка ───
def test_base():
    "base — таблица 5 товаров × 4 количества"
    assert isinstance(base, np.ndarray), f"base — это {type(base).__name__}, а нужна таблица"
    assert base.shape != (4, 5), "товары оказались в столбцах: себестоимость должна быть столбцом"
    assert base.shape == (5, 4), f"форма base — {base.shape}, а нужно (5, 4)"
    assert base[0].tolist() == [870, 4350, 8700, 43500], f"первая строка — {base[0].tolist()}: в строке — себестоимость 1, 5, 10 и 50 штук первого товара"
# ─── другое решение ───
base = np.outer(cost, amounts)
# ─── ошибка ───
base = cost * amounts[:, np.newaxis]

# %% volume [exercise]
discounted = base * (1 - volume_discount)
# ─── заготовка ───
discounted = ...
# ─── проверка ───
def test_discounted():
    "discounted — себестоимость со скидками за объём"
    assert isinstance(discounted, np.ndarray) and discounted.shape == (5, 4), "discounted — таблица 5 × 4"
    assert not np.allclose(discounted[0], [0, 217.5, 870, 8700]), "получилась сама скидка; нужна цена после скидки"
    assert np.allclose(discounted[0], [870, 4132.5, 7830, 34800]), f"первая строка — {discounted[0].tolist()}: скидка за объём применена неверно"
# ─── другое решение ───
discounted = base - base * volume_discount
# ─── ошибка ───
discounted = base * volume_discount
# ─── ошибка ───
discounted = base * (1 - volume_discount.mean())

# %% markup [exercise]
price = discounted * markup[:, np.newaxis]
# ─── заготовка ───
price = ...
# ─── проверка ───
def test_price():
    "price — цена с наценкой своего товара"
    assert isinstance(price, np.ndarray) and price.shape == (5, 4), "price — таблица 5 × 4"
    assert np.allclose(price[:, 0], [1305, 608, 688, 300, 550]), f"цены одной штуки — {price[:, 0].tolist()}: у каждого товара (строки) своя наценка"
    assert np.allclose(price[4], [550, 2612.5, 4950, 22000]), f"строка фильтров — {price[4].tolist()}"
# ─── другое решение ───
price = markup.reshape(-1, 1) * discounted
# ─── ошибка ───
price = discounted * markup.mean()

# %% rubles [exercise]
price_list = np.round(price).astype(int)
# ─── заготовка ───
price_list = ...
# ─── проверка ───
def test_int():
    "price_list — целые рубли"
    assert isinstance(price_list, np.ndarray) and price_list.shape == (5, 4), "price_list — таблица 5 × 4"
    assert price_list.dtype.kind == "i", f"тип price_list — {price_list.dtype}, а нужен целый"
    assert price_list[0, 1] != 6198, "6198.75 превратилось в 6198: astype(int) без округления отбрасывает дробь — сначала округлите"
    assert price_list[0, 1] == 6199, f"цена 5 штук первого товара — {price_list[0, 1]}: проверьте округление"
# ─── другое решение ───
price_list = np.array(np.round(price), dtype=int)
# ─── ошибка ───
price_list = price.astype(int)

# %% half
print(price[4, 1], "→", price_list[4, 1])

# %% per-unit [exercise]
per_unit = price_list / amounts
# ─── заготовка ───
per_unit = ...
# ─── проверка ───
def test_per_unit():
    "per_unit — цена одной штуки в каждой ячейке"
    assert isinstance(per_unit, np.ndarray) and per_unit.shape == (5, 4), "per_unit — таблица 5 × 4"
    assert np.allclose(per_unit[3], [300, 285, 270, 240]), f"для чая получилось {np.round(per_unit[3], 1).tolist()}, а цена одной штуки — это цена партии, делённая на число штук в ней"
# ─── другое решение ───
per_unit = price_list / amounts[np.newaxis, :]
# ─── ошибка ───
per_unit = price_list / amounts.sum()

# %% budget [exercise]
affordable = (price_list <= 5000).sum(axis=1)
# ─── заготовка ───
affordable = ...
# ─── проверка ───
def test_affordable():
    "affordable — сколько вариантов влезает в бюджет у каждого товара"
    assert isinstance(affordable, np.ndarray), f"affordable — это {type(affordable).__name__}, а нужен массив из 5 чисел"
    assert affordable.shape != (4,), "получилось 4 числа — по количеству; нужно по товару"
    assert affordable.tolist() == [1, 2, 2, 3, 3], f"affordable = {affordable.tolist()}: посчитайте для каждого товара, сколько цен не выше 5000"
# ─── другое решение ───
affordable = np.sum(price_list <= 5000, axis=1)
# ─── ошибка ───
affordable = (price_list <= 5000).sum(axis=0)
# ─── ошибка ───
affordable = (price_list < 5000).sum()

# %% savings [exercise]
full = base * markup[:, np.newaxis]
savings = (full - price)[:, 2]
# ─── заготовка ───
savings = ...
# ─── проверка ───
def test_savings():
    "savings — экономия на 10 штуках каждого товара"
    assert isinstance(savings, np.ndarray), f"savings — это {type(savings).__name__}, а нужен массив из 5 чисел"
    assert savings.shape == (5,), f"у savings форма {savings.shape}, а нужно 5 чисел — по одному на товар"
    assert np.allclose(savings, [1305, 608, 688, 300, 550]), f"savings = {np.round(savings, 1).tolist()} — это не экономия на 10 штуках"
# ─── другое решение ───
savings = (base * markup[:, np.newaxis])[:, 2] - price[:, 2]
# ─── ошибка ───
full = base * markup[:, np.newaxis]
savings = (full - price)[2]

# %% summary
print("количество:", amounts)
for name, row in zip(goods, price_list):
    print(f"{name:>20}: {row}")     # :>20 — выровнять название по правому краю на 20 символов
print("экономия на 10 штуках всего ассортимента:", round(savings.sum()), "₽")
