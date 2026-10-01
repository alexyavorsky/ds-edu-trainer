# Урок oop-dataclass. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% dataclass
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int


latte = Product("Латте", 220)
print(latte)
print(latte == Product("Латте", 220), latte == Product("Латте", 250))
print(latte.name, latte.price)

# %% drink [exercise]
from dataclasses import dataclass


@dataclass
class Drink:
    name: str
    price: int
    volume: int
# ─── заготовка ───
from dataclasses import dataclass


class Drink:
    ...
# ─── проверка ───
from dataclasses import fields, is_dataclass


def test_is_dataclass():
    "Drink — dataclass с тремя полями"
    assert is_dataclass(Drink), "Drink — не dataclass: поставьте над классом @dataclass"
    names = [f.name for f in fields(Drink)]
    assert names == ["name", "price", "volume"], f"поля Drink: {names}, а нужны name, price, volume — по порядку"


def test_generated():
    "__init__, __repr__ и __eq__ от декоратора"
    assert is_dataclass(Drink), "сначала сделайте Drink dataclass'ом"
    assert [f.name for f in fields(Drink)] == ["name", "price", "volume"], "сначала объявите три поля (проверка выше)"
    latte = Drink("Латте", 220, 300)
    assert repr(latte) == "Drink(name='Латте', price=220, volume=300)", f"repr = {latte!r}"
    assert latte == Drink("Латте", 220, 300), "два одинаковых напитка должны быть равны — __eq__ сравнивает поля"
    assert latte != Drink("Латте", 220, 400), "напитки с разным объёмом не равны"
# ─── другое решение ───
import dataclasses


@dataclasses.dataclass
class Drink:
    name: str
    price: int
    volume: int
# ─── ошибка ───
from dataclasses import dataclass


@dataclass
class Drink:
    name: str
    price: int
# ─── ошибка ───
from dataclasses import dataclass


@dataclass
class Drink:
    name: str
    volume: int
    price: int

# %% defaults
@dataclass
class Cup:
    name: str
    volume: int = 250


print(Cup("Капучино"), Cup("Капучино", 400))

# %% line [exercise]
@dataclass
class OrderLine:
    product: str
    price: int
    qty: int = 1

    @property
    def cost(self):
        return self.price * self.qty
# ─── заготовка ───
class OrderLine:
    ...
# ─── проверка ───
from dataclasses import fields, is_dataclass


def test_fields():
    "поля и значение по умолчанию"
    assert is_dataclass(OrderLine), "OrderLine — не dataclass: поставьте над классом @dataclass"
    assert [f.name for f in fields(OrderLine)] == ["product", "price", "qty"], f"поля: {[f.name for f in fields(OrderLine)]}"
    try:
        line = OrderLine("Латте", 220)
    except TypeError:
        assert False, "OrderLine(\"Латте\", 220) не создаётся — у qty должно быть значение по умолчанию 1"
    assert line.qty == 1, f"qty по умолчанию = {line.qty!r}, а нужно 1"


def test_cost():
    "cost — свойство"
    assert isinstance(OrderLine.__dict__.get("cost"), property), "cost должен быть свойством — с @property"
    assert OrderLine("Латте", 220, 3).cost == 660, "у трёх латте по 220 ₽ cost — 660"
# ─── другое решение ───
from dataclasses import dataclass


@dataclass
class OrderLine:
    product: str
    price: int
    qty: int = 1

    @property
    def cost(self):
        return self.qty * self.price
# ─── ошибка ───
from dataclasses import dataclass


@dataclass
class OrderLine:
    product: str
    price: int
    qty: int = 1

    def cost(self):
        return self.price * self.qty

# %% mutable [raises=ValueError]
@dataclass
class Basket:
    customer: str
    items: list = []

# %% factory
from dataclasses import dataclass, field


@dataclass
class Basket:
    customer: str
    items: list = field(default_factory=list)


anna, boris = Basket("Анна"), Basket("Борис")
anna.items.append("Латте")
print(anna)
print(boris)

# %% customer [exercise]
from dataclasses import dataclass, field


@dataclass
class Customer:
    name: str
    phone: str
    points: int = 0
    visits: list = field(default_factory=list)

    def visit(self, date):
        self.visits.append(date)
        self.points += 10
# ─── заготовка ───
class Customer:
    def __init__(self, name, phone, points=0, visits=None):
        self.name = name
        self.phone = phone
        self.points = points
        self.visits = [] if visits is None else visits

    def __repr__(self):
        return f"Customer(name={self.name!r}, phone={self.phone!r}, points={self.points!r}, visits={self.visits!r})"

    def __eq__(self, other):
        if not isinstance(other, Customer):
            return NotImplemented
        return (self.name, self.phone, self.points, self.visits) == (other.name, other.phone, other.points, other.visits)

    def visit(self, date):
        self.visits.append(date)
        self.points += 10
# ─── проверка ───
from dataclasses import MISSING, fields, is_dataclass


def test_dataclass():
    "Customer — dataclass с четырьмя полями"
    assert is_dataclass(Customer), "Customer — не dataclass: поставьте @dataclass над классом"
    assert [f.name for f in fields(Customer)] == ["name", "phone", "points", "visits"], f"поля: {[f.name for f in fields(Customer)]} — объявите их с аннотациями"
    assert fields(Customer)[3].default_factory is not MISSING, "поле visits объявите через field(default_factory=list) — так у каждого покупателя будет свой список"
    # методы, которые написал декоратор, скомпилированы из «<string>» (__repr__ обёрнут — берём __wrapped__)
    own = [m for m in ["__init__", "__repr__", "__eq__"] if not getattr(getattr(Customer, m), "__wrapped__", getattr(Customer, m)).__code__.co_filename.startswith("<")]
    assert not own, f"в классе остались написанные вручную методы: {', '.join(own)} — удалите их, их напишет декоратор"


def test_defaults():
    "points = 0, visits — свой пустой список"
    a, b = Customer("Анна", "1"), Customer("Борис", "2")
    assert a.points == 0 and a.visits == [], f"у нового покупателя points = {a.points!r}, visits = {a.visits!r}"
    a.visits.append("01.10")
    assert b.visits == [], "визит Анны появился у Бориса — используйте field(default_factory=list)"


def test_visit():
    "visit и сравнение"
    a = Customer("Анна", "1")
    a.visit("01.10")
    assert a.visits == ["01.10"] and a.points == 10, f"после visit: visits = {a.visits!r}, points = {a.points!r}"
    assert repr(Customer("Анна", "1")) == "Customer(name='Анна', phone='1', points=0, visits=[])", f"repr = {Customer('Анна', '1')!r}"
    assert Customer("Анна", "1") == Customer("Анна", "1"), "одинаковые покупатели должны быть равны"
# ─── другое решение ───
from dataclasses import dataclass, field


@dataclass
class Customer:
    name: str
    phone: str
    points: int = 0
    visits: list = field(default_factory=lambda: [])

    def visit(self, date):
        self.visits = self.visits + [date]
        self.points = self.points + 10
# ─── ошибка ───
from dataclasses import dataclass

SHARED = []


@dataclass
class Customer:
    name: str
    phone: str
    points: int = 0
    visits: list = None

    def __post_init__(self):
        if self.visits is None:
            self.visits = SHARED

    def visit(self, date):
        self.visits.append(date)
        self.points += 10
