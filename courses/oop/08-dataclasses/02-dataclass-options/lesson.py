# Урок oop-dataclass-options. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% post-init
from dataclasses import dataclass


@dataclass
class Cup:
    name: str
    volume: int

    def __post_init__(self):  # вызывается в конце __init__
        self.name = self.name.title()
        if self.volume < 50:
            raise ValueError(f"объём {self.volume} мл — меньше 50 мл не бывает")


print(Cup("капучино", 300))
try:
    Cup("эспрессо", 30)
except ValueError as error:
    print("ValueError:", error)

# %% product [exercise]
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int

    def __post_init__(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("пустое название")
        if self.price <= 0:
            raise ValueError("цена должна быть больше нуля")
# ─── заготовка ───
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int

    def __post_init__(self):
        ...
# ─── проверка ───
def _value_error(*args):
    try:
        Product(*args)
    except ValueError:
        return True
    except Exception as e:
        assert False, f"Product{args} выбросил {type(e).__name__}, а нужен ValueError"
    return False


def test_strip():
    "пробелы по краям убираются"
    got = Product("  Латте ", 220)
    assert got.name == "Латте", f"название {got.name!r}, а пробелы по краям нужно убрать: self.name.strip()"
    assert got.price == 220


def test_invalid():
    "пустое название и цена ≤ 0 — ValueError"
    assert _value_error("   ", 220), "Product(\"   \", 220) создался — название из одних пробелов должно давать ValueError"
    assert _value_error("Чай", 0), "Product(\"Чай\", 0) создался — цена должна быть больше нуля"
    assert _value_error("Чай", -5), "Product(\"Чай\", -5) создался — цена должна быть больше нуля"
# ─── другое решение ───
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int

    def __post_init__(self):
        name = self.name.strip()
        if name == "" or self.price < 1:
            raise ValueError("неверный товар")
        self.name = name
# ─── ошибка ───
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int

    def __post_init__(self):
        if not self.name:
            raise ValueError("пустое название")
        if self.price <= 0:
            raise ValueError("цена должна быть больше нуля")
        self.name = self.name.strip()
# ─── ошибка ───
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int

    def __post_init__(self):
        self.name = self.name.strip()
        if self.price <= 0:
            raise ValueError("цена должна быть больше нуля")

# %% frozen
@dataclass(frozen=True)
class Coupon:
    code: str
    percent: int


autumn = Coupon("ОСЕНЬ", 10)
try:
    autumn.percent = 50
except AttributeError as error:
    print(type(error).__name__, error)
used = {autumn, Coupon("ОСЕНЬ", 10), Coupon("ЗИМА", 15)}
print(len(used), Coupon("ОСЕНЬ", 10) in used)

# %% money [exercise]
from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    rubles: int
# ─── заготовка ───
from dataclasses import dataclass


class Money:
    ...
# ─── проверка ───
from dataclasses import fields, is_dataclass


def test_fields():
    "dataclass с полем rubles"
    assert is_dataclass(Money), "Money — не dataclass: поставьте над классом @dataclass(frozen=True)"
    assert [f.name for f in fields(Money)] == ["rubles"], f"поля: {[f.name for f in fields(Money)]}, а нужно одно поле rubles"
    assert Money(220) == Money(220), "одинаковые суммы должны быть равны"


def test_frozen():
    "rubles нельзя изменить"
    assert is_dataclass(Money), "сначала сделайте Money dataclass'ом"
    m = Money(220)
    try:
        m.rubles = 0
    except AttributeError:
        pass
    else:
        assert False, "поле rubles удалось изменить — нужен @dataclass(frozen=True)"


def test_hashable():
    "Money — ключ словаря"
    assert is_dataclass(Money), "сначала сделайте Money dataclass'ом"
    try:
        prices = {Money(220): "латте"}
    except TypeError:
        assert False, "Money нельзя сделать ключом словаря — с frozen=True dataclass сам пишет __hash__"
    assert prices[Money(220)] == "латте"
# ─── другое решение ───
import dataclasses


@dataclasses.dataclass(frozen=True, eq=True)
class Money:
    rubles: int
# ─── ошибка ───
from dataclasses import dataclass


@dataclass
class Money:
    rubles: int

# %% replace
from dataclasses import replace

winter = replace(autumn, code="ЗИМА", percent=15)
print(autumn)
print(winter)

# %% booking [exercise]
from dataclasses import dataclass


@dataclass(order=True)
class Booking:
    time: str
    name: str


bookings = [Booking("18:30", "Вера"), Booking("09:30", "Борис"), Booking("18:30", "Анна")]
ordered = [b.name for b in sorted(bookings)]
# ─── заготовка ───
from dataclasses import dataclass


class Booking:
    ...


bookings = [Booking("18:30", "Вера"), Booking("09:30", "Борис"), Booking("18:30", "Анна")]
ordered = ...
# ─── проверка ───
from dataclasses import fields, is_dataclass


def test_class():
    "Booking — сортируемый dataclass"
    assert is_dataclass(Booking), "Booking — не dataclass: поставьте @dataclass(order=True)"
    assert [f.name for f in fields(Booking)] == ["time", "name"], f"поля: {[f.name for f in fields(Booking)]} — первым должно идти time: по нему сортируют"
    try:
        less = Booking("09:30", "Борис") < Booking("18:30", "Анна")
    except TypeError:
        assert False, "брони не сравниваются — нужен @dataclass(order=True)"
    assert less, "бронь на 09:30 должна быть раньше брони на 18:30"


def test_ordered():
    "ordered — имена по времени и имени"
    assert ordered == ["Борис", "Анна", "Вера"], f"ordered = {ordered}, а нужно ['Борис', 'Анна', 'Вера']"
# ─── другое решение ───
from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Booking:
    time: str
    name: str


bookings = [Booking("18:30", "Вера"), Booking("09:30", "Борис"), Booking("18:30", "Анна")]
ordered = []
for booking in sorted(bookings):
    ordered.append(booking.name)
# ─── ошибка ───
from dataclasses import dataclass


@dataclass(order=True)
class Booking:
    name: str
    time: str


bookings = [Booking("Вера", "18:30"), Booking("Борис", "09:30"), Booking("Анна", "18:30")]
ordered = [b.name for b in sorted(bookings)]

# %% price-change [exercise]
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Price:
    name: str
    price: int


menu = [Price("Латте", 220), Price("Чай", 120), Price("Какао", 190), Price("Маффин", 133)]
new_menu = [replace(p, price=round(p.price * 110 / 100)) for p in menu]
# ─── заготовка ───
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Price:
    name: str
    price: int


menu = [Price("Латте", 220), Price("Чай", 120), Price("Какао", 190), Price("Маффин", 133)]
new_menu = ...
# ─── проверка ───
def test_new():
    "new_menu — цены выше на 10 %"
    assert isinstance(new_menu, list) and all(isinstance(p, Price) for p in new_menu), "new_menu — список товаров Price"
    got = [(p.name, p.price) for p in new_menu]
    assert got == [("Латте", 242), ("Чай", 132), ("Какао", 209), ("Маффин", 146)], f"new_menu: {got}"


def test_old():
    "старое меню не изменилось"
    assert [p.price for p in menu] == [220, 120, 190, 133], "исходное меню изменилось"
    assert all(a is not b for a, b in zip(menu, new_menu)), "в new_menu должны быть новые объекты — replace создаёт копию"
# ─── другое решение ───
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Price:
    name: str
    price: int


menu = [Price("Латте", 220), Price("Чай", 120), Price("Какао", 190), Price("Маффин", 133)]
new_menu = [Price(p.name, round(p.price * 1.1)) for p in menu]
# ─── ошибка ───
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Price:
    name: str
    price: int


menu = [Price("Латте", 220), Price("Чай", 120), Price("Какао", 190), Price("Маффин", 133)]
new_menu = [replace(p, price=p.price * 110 // 100 + 1) for p in menu]

# %% frozen-quiz [quiz]
print("у экземпляра нельзя менять поля, но можно получить изменённую копию через `replace`")
