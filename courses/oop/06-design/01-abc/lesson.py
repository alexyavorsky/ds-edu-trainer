# Урок oop-abc. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% abc
from abc import ABC, abstractmethod


class Delivery(ABC):
    def __init__(self, title):
        self.title = title

    @abstractmethod
    def cost(self, km):
        ...  # реализацию дадут подклассы

    def describe(self, km):  # обычный метод — пользуется абстрактным
        return f"{self.title}: {self.cost(km)} ₽"


print(Delivery.__name__, issubclass(Delivery, ABC))

# %% no-instance [raises=TypeError]
Delivery("какая-то доставка")

# %% subclasses
class Pickup(Delivery):
    def cost(self, km):
        return 0


class BrokenCourier(Delivery):
    def cots(self, km):  # опечатка: cost так и не реализован
        return 150 + 30 * km


print(Pickup("самовывоз").describe(5))
try:
    BrokenCourier("курьер")
except TypeError as error:
    print("TypeError:", error)

# %% beverage [exercise]
from abc import ABC, abstractmethod


class Beverage(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def ingredients(self):
        ...

    def card(self):
        return f"{self.name}: {', '.join(self.ingredients())}"
# ─── заготовка ───
from abc import ABC, abstractmethod


class Beverage:  # сделайте класс абстрактным
    def __init__(self, name):
        ...

    def ingredients(self):  # сделайте метод абстрактным
        ...

    def card(self):
        ...
# ─── проверка ───
def _cannot_create(cls, *args):
    try:
        cls(*args)
    except TypeError:
        return True
    return False


def test_abstract():
    "Beverage — абстрактный класс"
    assert issubclass(Beverage, ABC), "Beverage должен наследовать от ABC: class Beverage(ABC):"
    assert "ingredients" in getattr(Beverage, "__abstractmethods__", set()), "ingredients должен быть абстрактным — поставьте над ним @abstractmethod"
    assert _cannot_create(Beverage, "Латте"), "экземпляр Beverage создаётся, а у абстрактного класса не должен"


def test_card():
    "card собирает строку из ingredients подкласса"
    assert issubclass(Beverage, ABC), "сначала сделайте Beverage абстрактным"

    class Tea(Beverage):
        def ingredients(self):
            return ["чай", "вода"]
    tea = Tea("Чай")
    assert getattr(tea, "name", None) == "Чай", "название хранится в атрибуте name"
    got = tea.card()
    assert got == "Чай: чай, вода", f"card() вернул {got!r}, а для ингредиентов [\"чай\", \"вода\"] нужно \"Чай: чай, вода\""
# ─── другое решение ───
from abc import ABC, abstractmethod


class Beverage(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def ingredients(self):
        """Список ингредиентов напитка."""

    def card(self):
        return self.name + ": " + ", ".join(self.ingredients())
# ─── ошибка ───
from abc import ABC, abstractmethod


class Beverage(ABC):
    def __init__(self, name):
        self.name = name

    def ingredients(self):
        return []

    def card(self):
        return f"{self.name}: {', '.join(self.ingredients())}"
# ─── ошибка ───
from abc import ABC, abstractmethod


class Beverage(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def ingredients(self):
        ...

    def card(self):
        return f"{self.name}: {self.ingredients()}"

# %% drinks [exercise]
class Espresso(Beverage):
    def ingredients(self):
        return ["эспрессо"]


class Latte(Beverage):
    def ingredients(self):
        return ["эспрессо", "молоко"]
# ─── заготовка ───
class Espresso(Beverage):
    def ingredients(self):
        ...


class Latte(Beverage):
    def ingredients(self):
        ...
# ─── проверка ───
def _make(cls, name):
    try:
        return cls(name)
    except TypeError as e:
        assert False, f"{cls.__name__}(\"{name}\") не создаётся: {e}"


def test_espresso():
    "Espresso — один ингредиент"
    assert issubclass(Espresso, Beverage), "Espresso должен наследовать от Beverage"
    got = _make(Espresso, "Эспрессо").card()
    assert got == "Эспрессо: эспрессо", f"card() эспрессо = {got!r}"


def test_latte():
    "Latte — эспрессо и молоко"
    assert issubclass(Latte, Beverage), "Latte должен наследовать от Beverage"
    latte = _make(Latte, "Латте")
    assert latte.ingredients() == ["эспрессо", "молоко"], f"ingredients() латте = {latte.ingredients()!r}"
    assert latte.card() == "Латте: эспрессо, молоко", f"card() латте = {latte.card()!r}"
# ─── другое решение ───
class Espresso(Beverage):
    INGREDIENTS = ["эспрессо"]

    def ingredients(self):
        return list(self.INGREDIENTS)


class Latte(Espresso):
    def ingredients(self):
        return super().ingredients() + ["молоко"]
# ─── ошибка ───
class Espresso(Beverage):
    def ingredients(self):
        return ["эспрессо"]


class Latte(Beverage):
    def ingredient(self):
        return ["эспрессо", "молоко"]
# ─── ошибка ───
class Espresso(Beverage):
    def ingredients(self):
        return "эспрессо"


class Latte(Beverage):
    def ingredients(self):
        return ["эспрессо", "молоко"]

# %% template
class Report(ABC):
    def render(self):  # шаблон: порядок задан здесь
        lines = [self.title(), "-" * len(self.title())]
        lines += self.lines()
        return "\n".join(lines)

    @abstractmethod
    def title(self):
        ...

    @abstractmethod
    def lines(self):
        ...


class StockReport(Report):
    def __init__(self, stock):
        self.stock = stock

    def title(self):
        return "Остатки"

    def lines(self):
        return [f"{name} — {left} шт." for name, left in self.stock.items()]


print(StockReport({"зёрна": 12, "молоко": 4}).render())

# %% sales-report [exercise]
class SalesReport(Report):
    def __init__(self, sales):
        self.sales = sales

    def title(self):
        return "Продажи за день"

    def lines(self):
        return [f"{name}: {count}" for name, count in self.sales.items()]
# ─── заготовка ───
class SalesReport(Report):
    def __init__(self, sales):
        ...

    def title(self):
        ...

    def lines(self):
        ...
# ─── проверка ───
def _report():
    try:
        return SalesReport({"Латте": 41, "Раф": 17})
    except TypeError as e:
        assert False, f"SalesReport(...) не создаётся: {e}"


def test_parts():
    "title и lines"
    assert issubclass(SalesReport, Report), "SalesReport должен наследовать от Report"
    report = _report()
    assert getattr(report, "sales", None) == {"Латте": 41, "Раф": 17}, "словарь продаж хранится в атрибуте sales"
    assert report.title() == "Продажи за день", f"title() = {report.title()!r}"
    assert report.lines() == ["Латте: 41", "Раф: 17"], f"lines() = {report.lines()!r}"


def test_render():
    "render из базового класса"
    assert "render" not in SalesReport.__dict__, "render переопределять не нужно — он уже есть в Report"
    got = _report().render()
    assert got == "Продажи за день\n---------------\nЛатте: 41\nРаф: 17", f"render() дал:\n{got}"
# ─── другое решение ───
class SalesReport(Report):
    TITLE = "Продажи за день"

    def __init__(self, sales):
        self.sales = dict(sales)

    def title(self):
        return self.TITLE

    def lines(self):
        result = []
        for name in self.sales:
            result.append(name + ": " + str(self.sales[name]))
        return result
# ─── ошибка ───
class SalesReport(Report):
    def __init__(self, sales):
        self.sales = sales

    def title(self):
        return "Продажи за день"

    def lines(self):
        return [f"{name}: {count}" for name, count in self.sales.items()]

    def render(self):
        return self.title() + "\n" + "\n".join(self.lines())
# ─── ошибка ───
class SalesReport(Report):
    def __init__(self, sales):
        self.sales = sales

    def title(self):
        return "Продажи за день"

    def lines(self):
        return "\n".join(f"{name}: {count}" for name, count in self.sales.items())

# %% abc-quiz [quiz]
class Half(Report):
    def lines(self):
        return []


try:
    Half()
    print("создался")
except TypeError:
    print("при создании экземпляра подкласса")
