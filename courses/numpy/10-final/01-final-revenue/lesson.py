# Урок np-final-revenue. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% peek
with open("data/shop_orders.csv") as f:
    lines = f.read().splitlines()
print(len(lines) - 1, "строк")
for line in lines[:4]:
    print(line)

# %% totals [exercise]
import numpy as np

path = "data/shop_orders.csv"
nums = np.loadtxt(path, delimiter=",", skiprows=1, usecols=(7, 8))
revenue = nums[:, 0] * nums[:, 1]
total = revenue.sum()
order_ids = np.loadtxt(path, delimiter=",", skiprows=1, usecols=0)
n_orders = len(np.unique(order_ids))
avg_check = total / n_orders
# ─── заготовка ───
import numpy as np

path = "data/shop_orders.csv"
revenue = ...
total = ...
n_orders = ...
avg_check = ...
# ─── проверка ───
def test_revenue():
    "revenue — выручка каждой строки"
    assert isinstance(revenue, np.ndarray), f"revenue — это {type(revenue).__name__}, а нужен массив: цена × количество"
    assert revenue.shape == (2448,), f"у revenue форма {revenue.shape}, а строк в файле 2448"
    assert revenue[0] == 6400, f"revenue[0] = {revenue[0]}, а в первой строке 3200 ₽ × 2 = 6400: столбцы 7 и 8"


def test_total():
    "total — выручка за год"
    assert total == 3301420, f"total = {total}, а выручка года — 3 301 420 ₽"


def test_orders():
    "n_orders и avg_check — заказы и средний чек"
    assert n_orders != 2448, "2448 — число строк; в заказе бывает несколько товаров: считайте уникальные номера"
    assert n_orders == 1576, f"n_orders = {n_orders}, а разных заказов 1576"
    assert abs(avg_check - 2094.809645) < 1e-5, f"avg_check = {avg_check}, а средний чек ≈ 2094.81 ₽"
# ─── другое решение ───
import numpy as np

path = "data/shop_orders.csv"
price = np.loadtxt(path, delimiter=",", skiprows=1, usecols=7)
quantity = np.loadtxt(path, delimiter=",", skiprows=1, usecols=8)
revenue = price * quantity
total = np.sum(revenue)
n_orders = np.unique(np.loadtxt(path, delimiter=",", skiprows=1, usecols=0)).size
avg_check = total / n_orders
# ─── ошибка ───
import numpy as np

path = "data/shop_orders.csv"
nums = np.loadtxt(path, delimiter=",", skiprows=1, usecols=(7, 8))
revenue = nums[:, 0] * nums[:, 1]
total = revenue.sum()
n_orders = len(revenue)
avg_check = total / n_orders

# %% inverse
sample = np.array(["чай", "кофе", "чай", "какао", "кофе"])
names, codes = np.unique(sample, return_inverse=True)
print(names)
print(codes)
print(names[codes])       # коды → обратно в названия

# %% weights
amounts = np.array([100, 250, 50, 80, 300])
print(np.bincount(codes))
print(np.bincount(codes, weights=amounts))

# %% categories [exercise]
category = np.loadtxt(path, delimiter=",", skiprows=1, usecols=5, dtype=str)
cat_names, cat_codes = np.unique(category, return_inverse=True)
cat_revenue = np.bincount(cat_codes, weights=revenue)
cat_share = cat_revenue / cat_revenue.sum()
# ─── заготовка ───
category = ...
cat_names = ...
cat_revenue = ...
cat_share = ...
# ─── проверка ───
def test_names():
    "cat_names — пять категорий"
    assert isinstance(category, np.ndarray) and category.shape == (2448,), "category — столбец 5 как текст: dtype=str"
    assert list(cat_names) == ["Аксессуары", "Кофе", "Посуда", "Сладости", "Чай"], f"cat_names = {list(cat_names)}: уникальные значения category"


def test_revenue():
    "cat_revenue — выручка категорий"
    assert isinstance(cat_revenue, np.ndarray) and cat_revenue.shape == (5,), "cat_revenue — пять сумм, по категории"
    assert cat_revenue.tolist() != [108, 975, 183, 500, 682], "это количества строк: добавьте weights=revenue"
    assert cat_revenue.tolist() == [173500, 1914440, 385640, 220190, 607650], f"cat_revenue = {cat_revenue.tolist()}"


def test_share():
    "cat_share — доли категорий"
    assert np.shape(cat_share) == (5,), "cat_share — пять долей"
    assert abs(cat_share.sum() - 1) < 1e-9, f"доли в сумме {cat_share.sum()}, а должны давать 1: делите на cat_revenue.sum()"
    assert abs(cat_share[1] - 0.579884) < 1e-5, f"доля кофе — {cat_share[1]:.4f}, а должна быть ≈ 0.58"
# ─── другое решение ───
category = np.loadtxt(path, delimiter=",", skiprows=1, usecols=5, dtype=str)
cat_names = np.unique(category)
cat_revenue = np.array([revenue[category == name].sum() for name in cat_names])
cat_share = cat_revenue / total
# ─── ошибка ───
category = np.loadtxt(path, delimiter=",", skiprows=1, usecols=5, dtype=str)
cat_names, cat_codes = np.unique(category, return_inverse=True)
cat_revenue = np.bincount(cat_codes)
cat_share = cat_revenue / cat_revenue.sum()

# %% weights-quiz [quiz]
print(np.bincount(np.array([0, 2, 0]), weights=np.array([5.0, 1.0, 3.0])))

# %% products [exercise]
product = np.loadtxt(path, delimiter=",", skiprows=1, usecols=6, dtype=str)
prod_names, prod_codes = np.unique(product, return_inverse=True)
prod_revenue = np.bincount(prod_codes, weights=revenue)
top5 = prod_names[np.argsort(prod_revenue)[::-1][:5]]
worst = prod_names[prod_revenue.argmin()]
# ─── заготовка ───
top5 = ...
worst = ...
# ─── проверка ───
def test_top():
    "top5 — пять товаров с наибольшей выручкой"
    assert len(top5) == 5, f"в top5 {len(top5)} названий, а нужно пять"
    got = [str(x) for x in top5]
    assert got != ["Фильтры бумажные", "Печенье овсяное", "Шоколад горький", "Турка медная", "Кружка 350 мл"], "это пять худших: argsort упорядочивает по возрастанию — разверните [::-1]"
    assert got == ["Эфиопия 250 г", "Бразилия 1 кг", "Эспрессо-смесь 1 кг", "Колумбия 250 г", "Кофе без кофеина 250 г"], (
        f"top5 = {got}: сортируйте товары по выручке (weights=revenue), от большей к меньшей"
    )


def test_worst():
    "worst — товар с наименьшей выручкой"
    assert str(worst) == "Фильтры бумажные", f"worst = {worst}, а меньше всех принесли бумажные фильтры"
# ─── другое решение ───
product = np.loadtxt(path, delimiter=",", skiprows=1, usecols=6, dtype=str)
names_p, codes_p = np.unique(product, return_inverse=True)
sums = np.bincount(codes_p, weights=revenue)
order = np.argsort(-sums)
top5 = names_p[order[:5]]
worst = names_p[order[-1]]
# ─── ошибка ───
product = np.loadtxt(path, delimiter=",", skiprows=1, usecols=6, dtype=str)
prod_names, prod_codes = np.unique(product, return_inverse=True)
prod_revenue = np.bincount(prod_codes, weights=revenue)
top5 = prod_names[np.argsort(prod_revenue)[:5]]
worst = prod_names[prod_revenue.argmin()]

# %% cities [exercise]
city = np.loadtxt(path, delimiter=",", skiprows=1, usecols=3, dtype=str)
city_names, city_codes = np.unique(city, return_inverse=True)
city_revenue = np.bincount(city_codes, weights=revenue)
moscow_share = city_revenue[city_names == "Москва"][0] / total
# ─── заготовка ───
city_names = ...
city_revenue = ...
moscow_share = ...
# ─── проверка ───
def test_cities():
    "city_names и city_revenue — выручка городов"
    assert [str(x) for x in city_names] == ["Екатеринбург", "Казань", "Москва", "Новосибирск", "Санкт-Петербург"], "city_names — уникальные значения столбца 3"
    assert np.shape(city_revenue) == (5,), "city_revenue — пять сумм"
    assert city_revenue.tolist() == [423350, 440150, 1310110, 324090, 803720], f"city_revenue = {city_revenue.tolist()}: веса — revenue"


def test_moscow():
    "moscow_share — доля Москвы"
    assert np.shape(moscow_share) == (), "moscow_share — массив, а нужно одно число: возьмите [0]"
    assert abs(moscow_share - 0.396832) < 1e-5, f"moscow_share = {moscow_share}, а доля Москвы ≈ 0.397"
# ─── другое решение ───
city = np.loadtxt(path, delimiter=",", skiprows=1, usecols=3, dtype=str)
city_names, city_codes = np.unique(city, return_inverse=True)
city_revenue = np.bincount(city_codes, weights=revenue)
moscow_share = revenue[city == "Москва"].sum() / revenue.sum()
# ─── ошибка ───
city = np.loadtxt(path, delimiter=",", skiprows=1, usecols=3, dtype=str)
city_names, city_codes = np.unique(city, return_inverse=True)
city_revenue = np.bincount(city_codes, weights=revenue)
moscow_share = (city == "Москва").mean()

# %% summary
print(f"выручка за год: {total:,.0f} ₽".replace(",", " "))
print(f"заказов: {n_orders}, средний чек: {avg_check:.0f} ₽")
for name, share in zip(cat_names, np.round(cat_share * 100, 1)):
    print(f"  {name}: {share} %")
