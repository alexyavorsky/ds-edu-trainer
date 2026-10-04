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
    assert revenue[0] == 6400, f"revenue[0] = {revenue[0]}, а в первой строке должно быть 6400: проверьте столбцы цены и количества"


def test_total():
    "total — выручка за год"
    assert total == 3301420, f"total = {total} — это не сумма выручки всех строк"


def test_orders():
    "n_orders и avg_check — заказы и средний чек"
    assert n_orders != 2448, "2448 — число строк; в заказе бывает несколько товаров: считайте уникальные номера"
    assert n_orders == 1576, f"n_orders = {n_orders} — это не число разных заказов"
    assert abs(avg_check - 2094.809645) < 1e-5, f"avg_check = {avg_check} — это не средний чек: выручка года на один заказ"
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
amounts = np.array([100, 250, 50, 80, 300])    # суммы тех же пяти покупок из sample
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
    assert isinstance(category, np.ndarray) and category.shape == (2448,), "category — это должен быть столбец категорий, прочитанный как текст"
    assert list(cat_names) == ["Аксессуары", "Кофе", "Посуда", "Сладости", "Чай"], f"cat_names = {list(cat_names)}"


def test_revenue():
    "cat_revenue — выручка категорий"
    assert isinstance(cat_revenue, np.ndarray) and cat_revenue.shape == (5,), "cat_revenue — пять сумм, по категории"
    assert cat_revenue.tolist() != [108, 975, 183, 500, 682], "это количества строк, а нужна выручка: вспомните параметр weights"
    assert cat_revenue.tolist() == [173500, 1914440, 385640, 220190, 607650], f"cat_revenue = {cat_revenue.tolist()}"


def test_share():
    "cat_share — доли категорий"
    assert np.shape(cat_share) == (5,), "cat_share — пять долей"
    assert abs(cat_share.sum() - 1) < 1e-9, f"доли в сумме {cat_share.sum()}, а должны давать 1: делите на выручку всех категорий"
    assert abs(cat_share[1] - 0.579884) < 1e-5, f"доля кофе — {cat_share[1]:.4f} — это не доля выручки кофе"
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
    assert got != ["Фильтры бумажные", "Печенье овсяное", "Шоколад горький", "Термокружка", "Зефир"], "это пять худших: argsort упорядочивает по возрастанию"
    assert got == ["Эфиопия 250 г", "Бразилия 1 кг", "Эспрессо-смесь 1 кг", "Колумбия 250 г", "Кофе без кофеина 250 г"], (
        f"top5 = {got}: сортируйте товары по выручке, от большей к меньшей"
    )


def test_worst():
    "worst — товар с наименьшей выручкой"
    assert str(worst) == "Фильтры бумажные", f"worst = {worst} — это не товар с наименьшей выручкой"
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
    assert [str(x) for x in city_names] == ["Екатеринбург", "Казань", "Москва", "Новосибирск", "Санкт-Петербург"], "city_names — это должны быть уникальные города"
    assert np.shape(city_revenue) == (5,), "city_revenue — пять сумм"
    assert city_revenue.tolist() == [423350, 440150, 1310110, 324090, 803720], f"city_revenue = {city_revenue.tolist()}: нужна выручка, а не число строк"


def test_moscow():
    "moscow_share — доля Москвы"
    assert np.shape(moscow_share) == (), "moscow_share — массив, а нужно одно число"
    assert abs(moscow_share - 0.396832) < 1e-5, f"moscow_share = {moscow_share} — это не доля Москвы в выручке года"
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

# %% peek-delivery
with open("data/delivery_h1.csv") as f:
    lines = f.read().splitlines()
print(len(lines) - 1, "заказов в первом полугодии")
for line in lines[:6]:
    print(line)

# %% delivery [exercise]
h1 = np.genfromtxt("data/delivery_h1.csv", delimiter=",", skip_header=1)
h2 = np.genfromtxt("data/delivery_h2.csv", delimiter=",", skip_header=1)
delivery = np.vstack([h1, h2])
gaps = np.isnan(delivery).sum(axis=0)
avg_days = np.nanmean(delivery[:, 1])
# ─── заготовка ───
delivery = ...
gaps = ...
avg_days = ...
# ─── проверка ───
def test_delivery():
    "delivery — все заказы года: 1576 × 3"
    assert isinstance(delivery, np.ndarray), f"delivery — это {type(delivery).__name__}, а нужна таблица из двух файлов"
    assert delivery.shape != (1578, 3), "в delivery 1578 строк: заголовки стали строками nan — пропустите их при чтении обоих файлов"
    assert delivery.shape != (816, 6), "файлы склеены рядом; нужно друг под другом"
    assert delivery.shape == (1576, 3), f"у delivery форма {delivery.shape}, а нужна (1576, 3): 816 заказов первого полугодия и 760 второго"
    assert delivery[0, 0] == 10001, "delivery начинается не с первого полугодия: проверьте порядок"
    assert np.isnan(delivery).any(), "в delivery нет пропусков: пропуски нужно сохранить, чтобы их посчитать"


def test_gaps():
    "gaps — пропуски по столбцам"
    assert np.shape(gaps) == (3,), f"у gaps форма {np.shape(gaps)}, а столбцов три"
    assert gaps.tolist() == [0, 65, 552], f"gaps = {gaps.tolist()} — это не число пропусков в каждом столбце"


def test_avg():
    "avg_days — средний срок доставки"
    assert not np.isnan(avg_days), "avg_days = nan: обычный mean не пропускает пропуски — нужен np.nanmean"
    assert abs(avg_days - 4.293845) < 1e-5, f"avg_days = {avg_days} — это не средний срок доставки по известным заказам"
# ─── другое решение ───
parts = [np.genfromtxt("data/delivery_h" + half + ".csv", delimiter=",", skip_header=1) for half in ["1", "2"]]
delivery = np.concatenate(parts)
gaps = np.sum(np.isnan(delivery), axis=0)
known_days = delivery[:, 1][~np.isnan(delivery[:, 1])]
avg_days = known_days.mean()
# ─── ошибка ───
h1 = np.genfromtxt("data/delivery_h1.csv", delimiter=",")
h2 = np.genfromtxt("data/delivery_h2.csv", delimiter=",")
delivery = np.vstack([h1, h2])
gaps = np.isnan(delivery).sum(axis=0)
avg_days = np.nanmean(delivery[:, 1])
# ─── ошибка ───
h1 = np.genfromtxt("data/delivery_h1.csv", delimiter=",", skip_header=1, filling_values=0)
h2 = np.genfromtxt("data/delivery_h2.csv", delimiter=",", skip_header=1, filling_values=0)
delivery = np.vstack([h1, h2])
gaps = np.isnan(delivery).sum(axis=0)
avg_days = delivery[:, 1].mean()

# %% quality [exercise]
days = delivery[:, 1]
rating = delivery[:, 2]
late_share = (days[~np.isnan(days)] > 5).mean()
avg_rating = np.nanmean(rating)
fast_rating = np.nanmean(rating[days <= 3])
slow_rating = np.nanmean(rating[days > 5])
# ─── заготовка ───
days = delivery[:, 1]
rating = delivery[:, 2]
late_share = ...
avg_rating = ...
fast_rating = ...
slow_rating = ...
# ─── проверка ───
def test_late():
    "late_share — доля опозданий среди известных сроков"
    assert abs(late_share - 0.205584) > 1e-5, "это доля среди всех 1576 заказов: пропуски посчитаны как «вовремя» — сначала уберите их"
    assert abs(late_share - 0.214428) < 1e-5, f"late_share = {late_share} — это не доля заказов дольше 5 дней среди известных сроков"


def test_rating():
    "avg_rating — средняя оценка среди поставленных"
    assert not np.isnan(avg_rating), "avg_rating = nan: нужен np.nanmean"
    assert abs(avg_rating - 2.371827) > 1e-5, "пропуски заменены нулями и попали в среднее: оценки 0 не существует — пропуски нужно пропускать"
    assert abs(avg_rating - 3.650391) < 1e-5, f"avg_rating = {avg_rating} — это не средняя поставленная оценка"


def test_speed():
    "fast_rating и slow_rating — оценки быстрых и медленных доставок"
    assert not np.isnan(fast_rating) and not np.isnan(slow_rating), "получился nan: в отобранных оценках есть пропуски"
    assert abs(fast_rating - 4.216374) < 1e-5, f"fast_rating = {fast_rating} — это не средняя оценка доставок за 3 дня и быстрее"
    assert abs(slow_rating - 2.717489) < 1e-5, f"slow_rating = {slow_rating} — это не средняя оценка доставок дольше 5 дней"
# ─── другое решение ───
days = delivery[:, 1]
rating = delivery[:, 2]
known = ~np.isnan(days)
late_share = (days > 5).sum() / known.sum()
rated = ~np.isnan(rating)
avg_rating = rating[rated].mean()
fast_rating = rating[rated & (days <= 3)].mean()
slow_rating = rating[rated & (days > 5)].mean()
# ─── ошибка ───
days = delivery[:, 1]
rating = delivery[:, 2]
late_share = (days > 5).mean()
avg_rating = np.nanmean(rating)
fast_rating = np.nanmean(rating[days <= 3])
slow_rating = np.nanmean(rating[days > 5])
# ─── ошибка ───
days = delivery[:, 1]
rating = delivery[:, 2]
late_share = (days[~np.isnan(days)] > 5).mean()
avg_rating = np.nan_to_num(rating).mean()
fast_rating = np.nan_to_num(rating)[days <= 3].mean()
slow_rating = np.nan_to_num(rating)[days > 5].mean()

# %% summary
print(f"выручка за год: {total:,.0f} ₽".replace(",", " "))
print(f"заказов: {n_orders}, средний чек: {avg_check:.0f} ₽")
for name, share in zip(cat_names, np.round(cat_share * 100, 1)):
    print(f"  {name}: {share} %")
print(f"доставка: в среднем {avg_days:.1f} дня, дольше 5 дней — {late_share * 100:.0f} % заказов")
print(f"оценка быстрых доставок {fast_rating:.1f}, медленных {slow_rating:.1f}")
