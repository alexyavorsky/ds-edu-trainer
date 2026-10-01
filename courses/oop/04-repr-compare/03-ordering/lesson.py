# Урок oop-ordering. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% no-order [raises=TypeError]
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


products = [Product("Раф", 260), Product("Чай", 120), Product("Латте", 220)]
sorted(products)

# %% lt
class PricedProduct:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"PricedProduct({self.name!r}, {self.price})"

    def __lt__(self, other):
        if not isinstance(other, PricedProduct):
            return NotImplemented
        return self.price < other.price


shelf = [PricedProduct("Раф", 260), PricedProduct("Чай", 120), PricedProduct("Латте", 220)]
print(sorted(shelf))
print(min(shelf), max(shelf))
print(shelf[0] > shelf[1])  # Python спросил shelf[1] < shelf[0]

# %% drink-lt [exercise]
class Drink:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

    def __repr__(self):
        return f"Drink({self.name!r}, {self.volume})"

    def __lt__(self, other):
        if not isinstance(other, Drink):
            return NotImplemented
        return self.volume < other.volume


menu = [Drink("Латте", 400), Drink("Эспрессо", 60), Drink("Капучино", 300)]
ordered = sorted(menu)
biggest = max(menu)
# ─── заготовка ───
class Drink:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

    def __repr__(self):
        return f"Drink({self.name!r}, {self.volume})"

    def __lt__(self, other):
        ...


menu = [Drink("Латте", 400), Drink("Эспрессо", 60), Drink("Капучино", 300)]
ordered = ...
biggest = ...
# ─── проверка ───
def test_lt():
    "__lt__ сравнивает объём"
    assert "__lt__" in Drink.__dict__, "в классе нет __lt__ — объявите его"
    small, big = Drink("Эспрессо", 60), Drink("Латте", 400)
    assert (small < big) is True, "Drink(\"Эспрессо\", 60) < Drink(\"Латте\", 400) должно быть True"
    assert (big < small) is False, "Drink(\"Латте\", 400) < Drink(\"Эспрессо\", 60) должно быть False"
    assert (Drink("А", 300) < Drink("Б", 300)) is False, "при равных объёмах ни один напиток не меньше другого — сравнение строгое: <"


def test_foreign():
    "чужой тип — NotImplemented"
    assert "__lt__" in Drink.__dict__, "сначала объявите __lt__"
    try:
        got = Drink.__dict__["__lt__"](Drink("Латте", 400), 500)
    except AttributeError:
        assert False, "сравнение с числом падает — сначала проверьте тип: isinstance(other, Drink)"
    assert got is NotImplemented, f"для чужого типа __lt__ вернул {got!r}, а нужно NotImplemented"


def test_sorted():
    "ordered и biggest"
    assert isinstance(ordered, list), f"ordered — это {type(ordered).__name__}, а нужен список: sorted(menu)"
    assert [d.name for d in ordered] == ["Эспрессо", "Капучино", "Латте"], f"порядок в ordered: {[d.name for d in ordered]}"
    assert isinstance(biggest, Drink), f"biggest — это {type(biggest).__name__}, а нужен сам напиток: max(menu)"
    assert biggest.name == "Латте", f"biggest — {biggest.name}, а больше всех латте"
# ─── другое решение ───
class Drink:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

    def __repr__(self):
        return f"Drink({self.name!r}, {self.volume})"

    def __lt__(self, other):
        if isinstance(other, Drink):
            return self.volume < other.volume
        return NotImplemented


menu = [Drink("Латте", 400), Drink("Эспрессо", 60), Drink("Капучино", 300)]
ordered = list(menu)
ordered.sort()
biggest = ordered[-1]
# ─── ошибка ───
class Drink:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

    def __repr__(self):
        return f"Drink({self.name!r}, {self.volume})"

    def __lt__(self, other):
        if not isinstance(other, Drink):
            return NotImplemented
        return self.volume <= other.volume


menu = [Drink("Латте", 400), Drink("Эспрессо", 60), Drink("Капучино", 300)]
ordered = sorted(menu)
biggest = max(menu)
# ─── ошибка ───
class Drink:
    def __init__(self, name, volume):
        self.name = name
        self.volume = volume

    def __repr__(self):
        return f"Drink({self.name!r}, {self.volume})"

    def __lt__(self, other):
        if not isinstance(other, Drink):
            return NotImplemented
        return self.volume < other.volume


menu = [Drink("Латте", 400), Drink("Эспрессо", 60), Drink("Капучино", 300)]
ordered = sorted(menu)
biggest = min(menu)

# %% no-le [raises=TypeError]
shelf[0] <= shelf[1]

# %% total-ordering
from functools import total_ordering


@total_ordering
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __repr__(self):
        return f"Version({self.major}, {self.minor})"

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) < (other.major, other.minor)


old, new = Version(1, 9), Version(2, 0)
print(old < new, old <= new, old >= new, old != new)

# %% booking [exercise]
from functools import total_ordering


@total_ordering
class Booking:
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def __eq__(self, other):
        if not isinstance(other, Booking):
            return NotImplemented
        return (self.time, self.name) == (other.time, other.name)

    def __lt__(self, other):
        if not isinstance(other, Booking):
            return NotImplemented
        return (self.time, self.name) < (other.time, other.name)
# ─── заготовка ───
from functools import total_ordering


class Booking:
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def __eq__(self, other):
        ...

    def __lt__(self, other):
        ...
# ─── проверка ───
def test_methods():
    "__eq__ и __lt__ объявлены"
    for name in ["__eq__", "__lt__"]:
        assert name in Booking.__dict__, f"в классе нет {name} — объявите его"


def test_order():
    "по времени, при равном времени — по имени"
    assert "__lt__" in Booking.__dict__, "сначала объявите __lt__"
    early, late = Booking("Борис", "09:30"), Booking("Анна", "18:30")
    assert early < late, "бронь на 09:30 должна быть раньше брони на 18:30 — сравнивайте сначала время"
    assert Booking("Анна", "18:30") < Booking("Борис", "18:30"), "при одинаковом времени раньше та бронь, где имя по алфавиту раньше"
    got = [b.name for b in sorted([Booking("Вера", "12:00"), Booking("Борис", "09:30"), Booking("Анна", "12:00")])]
    assert got == ["Борис", "Анна", "Вера"], f"после сортировки брони идут так: {got}"


def test_equal():
    "равны — то же время и имя"
    assert "__eq__" in Booking.__dict__, "сначала объявите __eq__"
    assert Booking("Анна", "18:30") == Booking("Анна", "18:30"), "брони с одинаковыми именем и временем должны быть равны"
    assert Booking("Анна", "18:30") != Booking("Борис", "18:30"), "брони разных гостей на одно время не равны"
    got = Booking.__dict__["__eq__"](Booking("Анна", "18:30"), "18:30")
    assert got is NotImplemented, f"для чужого типа __eq__ вернул {got!r}, а нужно NotImplemented"


def test_total_ordering():
    "<= и >= работают"
    a, b = Booking("Анна", "09:30"), Booking("Борис", "18:30")
    try:
        result = (a <= b, b >= a, a >= b)
    except TypeError:
        assert False, "<= и >= не работают — поставьте над классом декоратор @total_ordering"
    assert result == (True, True, False), f"a <= b, b >= a, a >= b дали {result}"
# ─── другое решение ───
from functools import total_ordering


@total_ordering
class Booking:
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def _key(self):
        return (self.time, self.name)

    def __eq__(self, other):
        if isinstance(other, Booking):
            return self._key() == other._key()
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Booking):
            return self._key() < other._key()
        return NotImplemented
# ─── ошибка ───
from functools import total_ordering


class Booking:
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def __eq__(self, other):
        if not isinstance(other, Booking):
            return NotImplemented
        return (self.time, self.name) == (other.time, other.name)

    def __lt__(self, other):
        if not isinstance(other, Booking):
            return NotImplemented
        return (self.time, self.name) < (other.time, other.name)
# ─── ошибка ───
from functools import total_ordering


@total_ordering
class Booking:
    def __init__(self, name, time):
        self.name = name
        self.time = time

    def __eq__(self, other):
        if not isinstance(other, Booking):
            return NotImplemented
        return (self.time, self.name) == (other.time, other.name)

    def __lt__(self, other):
        if not isinstance(other, Booking):
            return NotImplemented
        return (self.name, self.time) < (other.name, other.time)

# %% key
def price_of(p):
    return p.price


print(sorted(products, key=price_of))
print(sorted(products, key=lambda p: p.price))  # то же самое
print(max(products, key=lambda p: len(p.name)))

# %% key-sort [exercise]
products = [Product("Раф", 260), Product("Чай", 120), Product("Латте", 220), Product("Какао", 190)]
by_name = [p.name for p in sorted(products, key=lambda p: p.name)]
by_price_desc = [p.name for p in sorted(products, key=lambda p: p.price, reverse=True)]
cheapest = min(products, key=lambda p: p.price)
# ─── заготовка ───
products = [Product("Раф", 260), Product("Чай", 120), Product("Латте", 220), Product("Какао", 190)]
by_name = ...
by_price_desc = ...
cheapest = ...
# ─── проверка ───
def test_by_name():
    "by_name — названия по алфавиту"
    assert isinstance(by_name, list), f"by_name — это {type(by_name).__name__}, а нужен список названий"
    assert all(isinstance(x, str) for x in by_name), "в by_name должны быть названия-строки, а не товары: [p.name for p in …]"
    assert by_name == ["Какао", "Латте", "Раф", "Чай"], f"by_name = {by_name}"


def test_by_price():
    "by_price_desc — от дорогого к дешёвому"
    assert isinstance(by_price_desc, list) and all(isinstance(x, str) for x in by_price_desc), "в by_price_desc нужен список названий"
    assert by_price_desc != ["Чай", "Какао", "Латте", "Раф"], "порядок от дешёвого к дорогому — нужен обратный: reverse=True"
    assert by_price_desc == ["Раф", "Латте", "Какао", "Чай"], f"by_price_desc = {by_price_desc}"


def test_cheapest():
    "cheapest — сам самый дешёвый товар"
    assert not isinstance(cheapest, (int, str)), f"cheapest = {cheapest!r}, а нужен сам товар"
    assert isinstance(cheapest, Product) and cheapest.name == "Чай", f"cheapest = {cheapest!r}, а дешевле всех чай"
# ─── другое решение ───
def name_of(p):
    return p.name


def price_of(p):
    return p.price


products = [Product("Раф", 260), Product("Чай", 120), Product("Латте", 220), Product("Какао", 190)]
by_name = sorted(p.name for p in products)
by_price_desc = [p.name for p in sorted(products, key=price_of)][::-1]
cheapest = sorted(products, key=price_of)[0]
# ─── ошибка ───
products = [Product("Раф", 260), Product("Чай", 120), Product("Латте", 220), Product("Какао", 190)]
by_name = [p.name for p in sorted(products, key=lambda p: p.name)]
by_price_desc = [p.name for p in sorted(products, key=lambda p: p.price)]
cheapest = min(products, key=lambda p: p.price)
# ─── ошибка ───
products = [Product("Раф", 260), Product("Чай", 120), Product("Латте", 220), Product("Какао", 190)]
by_name = [p.name for p in sorted(products, key=lambda p: p.name)]
by_price_desc = [p.name for p in sorted(products, key=lambda p: p.price, reverse=True)]
cheapest = min(p.price for p in products)
