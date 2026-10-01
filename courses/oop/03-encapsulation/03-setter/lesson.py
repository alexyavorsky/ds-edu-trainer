# Урок oop-setter. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% setter
class Cup:
    def __init__(self, volume):
        self._volume = volume

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        print(f"сеттер получил {value}")
        if value < 50:
            print("слишком мало — объём не изменён")
            return
        self._volume = value


cup = Cup(300)
cup.volume = 400  # вызывается сеттер
print(cup.volume)
cup.volume = 10
print(cup.volume)

# %% raise [raises=ValueError]
class Cup:
    def __init__(self, volume):
        self._volume = volume

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if value < 50:
            raise ValueError(f"объём {value} мл — меньше 50 мл не бывает")
        self._volume = value


cup = Cup(300)
cup.volume = 10

# %% catch
try:
    cup.volume = 10
    print("записали")  # не выполнится
except ValueError as error:
    print("не получилось:", error)
print(cup.volume)

# %% price [exercise]
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("цена должна быть больше нуля")
        self._price = value
# ─── заготовка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price  # запись через свойство: сработает сеттер

    @property
    def price(self):
        ...

    @price.setter
    def price(self, value):
        ...
# ─── проверка ───
def _raises_value_error(action):
    "True, если action() выбросил ValueError"
    try:
        action()
    except ValueError:
        return True
    return False


def test_property():
    "price — свойство с сеттером"
    prop = Product.__dict__.get("price")
    assert isinstance(prop, property), "price должен быть свойством: @property над геттером"
    assert prop.fset is not None, "у свойства нет сеттера — объявите второй метод price с декоратором @price.setter"


def test_valid():
    "верная цена записывается"
    p = Product("Латте", 220)
    assert p.price == 220, f"у Product(\"Латте\", 220) price = {p.price!r}, а нужно 220"
    p.price = 250
    assert p.price == 250, f"после p.price = 250 цена {p.price!r}"


def test_invalid():
    "цена 0 и меньше — ValueError, старая цена на месте"
    p = Product("Латте", 220)
    for bad in [0, -50]:
        def assign(bad=bad):
            p.price = bad
        assert _raises_value_error(assign), f"p.price = {bad} не выбросил ValueError — проверьте значение в сеттере: raise ValueError(…)"
        assert p.price == 220, f"после неудачной записи {bad} цена стала {p.price!r} — сначала проверка, потом запись"


def test_init():
    "Product с неверной ценой не создаётся"
    assert _raises_value_error(lambda: Product("Чай", -5)), "Product(\"Чай\", -5) создался — в __init__ запись должна идти через свойство: self.price = price"
# ─── другое решение ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value > 0:
            self._price = value
        else:
            raise ValueError("цена должна быть больше нуля")
# ─── ошибка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value > 0:
            self._price = value
# ─── ошибка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
        if value <= 0:
            raise ValueError("цена должна быть больше нуля")
# ─── ошибка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("цена должна быть больше нуля")
        self._price = value

# %% init-check [raises=ValueError]
class Cup:
    def __init__(self, volume):
        self.volume = volume  # через свойство — с проверкой

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if value < 50:
            raise ValueError(f"объём {value} мл — меньше 50 мл не бывает")
        self._volume = value


tiny = Cup(20)

# %% init-quiz [quiz]
class Product2:
    def __init__(self, name, price):
        self.name = name
        self._price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("цена должна быть больше нуля")
        self._price = value


print(f"экземпляр создастся с ценой {Product2('Чай', -5).price}")

# %% review [exercise]
class Review:
    def __init__(self, author, stars):
        self.author = author
        self.stars = stars

    @property
    def stars(self):
        return self._stars

    @stars.setter
    def stars(self, value):
        if not isinstance(value, int) or value < 1 or value > 5:
            raise ValueError("оценка — целое число от 1 до 5")
        self._stars = value
# ─── заготовка ───
class Review:
    def __init__(self, author, stars):
        ...
# ─── проверка ───
def _value_error(action):
    try:
        action()
    except ValueError:
        return True
    return False


def test_valid():
    "Review(\"Анна\", 5) — автор и оценка"
    r = Review("Анна", 5)
    assert getattr(r, "author", None) == "Анна", "у отзыва должен быть атрибут author с именем автора"
    assert getattr(r, "stars", None) == 5, "у Review(\"Анна\", 5) stars должно быть 5"


def test_is_property():
    "stars — свойство с сеттером"
    prop = Review.__dict__.get("stars")
    assert isinstance(prop, property), "stars должен быть свойством: @property и @stars.setter"
    assert prop.fset is not None, "у свойства stars нет сеттера — объявите @stars.setter"


def test_create_invalid():
    "неверная оценка при создании — ValueError"
    for bad in [0, 6, 4.5]:
        assert _value_error(lambda bad=bad: Review("Анна", bad)), f"Review(\"Анна\", {bad}) создался — в __init__ пишите через свойство: self.stars = stars"


def test_change():
    "изменить оценку можно, неверную — нельзя"
    r = Review("Анна", 4)
    r.stars = 5
    assert r.stars == 5, "оценку 5 должно быть можно записать"

    def bad():
        r.stars = 10
    assert _value_error(bad), "r.stars = 10 не выбросил ValueError"
    assert r.stars == 5, "после неудачной записи оценка не должна меняться"
# ─── другое решение ───
class Review:
    def __init__(self, author, stars):
        self.author = author
        self.stars = stars

    @property
    def stars(self):
        return self._stars

    @stars.setter
    def stars(self, value):
        if value not in [1, 2, 3, 4, 5] or isinstance(value, float):
            raise ValueError("оценка — целое число от 1 до 5")
        self._stars = value
# ─── ошибка ───
class Review:
    def __init__(self, author, stars):
        self.author = author
        self._stars = stars

    @property
    def stars(self):
        return self._stars

    @stars.setter
    def stars(self, value):
        if not isinstance(value, int) or value < 1 or value > 5:
            raise ValueError("оценка — целое число от 1 до 5")
        self._stars = value
# ─── ошибка ───
class Review:
    def __init__(self, author, stars):
        self.author = author
        self.stars = stars

    @property
    def stars(self):
        return self._stars

    @stars.setter
    def stars(self, value):
        if value < 1 or value > 5:
            raise ValueError("оценка — целое число от 1 до 5")
        self._stars = value

# %% import [exercise]
rows = [("Эспрессо", 150), ("Капучино", -220), ("Чай", 120), ("Раф", 0), ("Какао", 190)]
products = []
skipped = []
for name, price in rows:
    try:
        products.append(Product(name, price))
    except ValueError:
        skipped.append(name)
# ─── заготовка ───
rows = [("Эспрессо", 150), ("Капучино", -220), ("Чай", 120), ("Раф", 0), ("Какао", 190)]
products = ...
skipped = ...
# ─── проверка ───
def test_products():
    "products — товары из верных строк"
    assert isinstance(products, list), f"products — это {type(products).__name__}, а нужен список"
    assert all(isinstance(p, Product) for p in products), "в products должны быть экземпляры Product"
    names = [p.name for p in products]
    assert names == ["Эспрессо", "Чай", "Какао"], f"в products {names}, а верные строки — эспрессо, чай и какао"


def test_skipped():
    "skipped — названия ошибочных строк"
    assert isinstance(skipped, list), f"skipped — это {type(skipped).__name__}, а нужен список названий"
    assert skipped == ["Капучино", "Раф"], f"skipped = {skipped}, а ошибочные строки — капучино (-220) и раф (0)"
# ─── другое решение ───
rows = [("Эспрессо", 150), ("Капучино", -220), ("Чай", 120), ("Раф", 0), ("Какао", 190)]
products, skipped = [], []
for row in rows:
    try:
        product = Product(row[0], row[1])
    except ValueError:
        skipped.append(row[0])
    else:
        products.append(product)
# ─── ошибка ───
rows = [("Эспрессо", 150), ("Капучино", -220), ("Чай", 120), ("Раф", 0), ("Какао", 190)]
products = []
skipped = []
for name, price in rows:
    if price < 0:
        skipped.append(name)
    else:
        products.append(Product(name, max(price, 1)))
