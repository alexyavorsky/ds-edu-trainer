# Урок oop-p8-order. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% errors [exercise]
class ShopError(Exception):
    pass


class InvalidLineError(ShopError):
    pass


class EmptyOrderError(ShopError):
    pass
# ─── заготовка ───
# объявите ShopError, InvalidLineError и EmptyOrderError
# ─── проверка ───
def _cls(name):
    cls = globals().get(name)
    assert isinstance(cls, type), f"класса {name} нет — объявите его"
    return cls


def test_hierarchy():
    "ShopError → InvalidLineError, EmptyOrderError"
    shop = _cls("ShopError")
    assert issubclass(shop, Exception), "ShopError должен наследовать от Exception"
    for name in ["InvalidLineError", "EmptyOrderError"]:
        assert issubclass(_cls(name), shop), f"{name} должен наследовать от ShopError"
# ─── другое решение ───
class ShopError(Exception):
    """Ошибка кассы."""


class InvalidLineError(ShopError):
    """Неверная строка заказа."""


class EmptyOrderError(ShopError):
    """Пустой заказ."""
# ─── ошибка ───
class ShopError(Exception):
    pass


class InvalidLineError(ValueError):
    pass


class EmptyOrderError(ShopError):
    pass

# %% line [exercise]
from dataclasses import dataclass, field


@dataclass(frozen=True)
class OrderLine:
    product: str
    price: int
    qty: int = 1

    def __post_init__(self):
        if self.price <= 0 or self.qty <= 0:
            raise InvalidLineError(f"неверная строка: {self.product}, цена {self.price}, количество {self.qty}")

    @property
    def cost(self):
        return self.price * self.qty
# ─── заготовка ───
from dataclasses import dataclass, field


class OrderLine:
    ...
# ─── проверка ───
from dataclasses import fields, is_dataclass


def test_fields():
    "dataclass, frozen, поля"
    assert is_dataclass(OrderLine), "OrderLine — не dataclass"
    assert [f.name for f in fields(OrderLine)] == ["product", "price", "qty"], f"поля: {[f.name for f in fields(OrderLine)]}"
    line = OrderLine("Латте", 220)
    assert line.qty == 1, "qty по умолчанию — 1"
    try:
        line.price = 1
    except AttributeError:
        pass
    else:
        assert False, "поле price удалось изменить — нужен @dataclass(frozen=True)"


def test_cost():
    "cost — цена на количество"
    assert isinstance(OrderLine.__dict__.get("cost"), property), "cost должен быть свойством"
    assert OrderLine("Латте", 220, 2).cost == 440, "у двух латте по 220 ₽ cost — 440"


def test_invalid():
    "неверная цена или количество — InvalidLineError"
    for args in [("Чай", -120, 1), ("Чай", 120, 0)]:
        try:
            OrderLine(*args)
        except InvalidLineError as e:
            expected = f"неверная строка: {args[0]}, цена {args[1]}, количество {args[2]}"
            assert str(e) == expected, f"сообщение {str(e)!r}, а нужно {expected!r}"
        except ValueError:
            assert False, "выброшен ValueError, а нужен InvalidLineError из шага 1"
        else:
            assert False, f"OrderLine{args} создалась — проверьте цену и количество в __post_init__"
# ─── другое решение ───
from dataclasses import dataclass, field


@dataclass(frozen=True)
class OrderLine:
    product: str
    price: int
    qty: int = 1

    def __post_init__(self):
        if min(self.price, self.qty) < 1:
            raise InvalidLineError("неверная строка: " + f"{self.product}, цена {self.price}, количество {self.qty}")

    @property
    def cost(self):
        return self.qty * self.price
# ─── ошибка ───
from dataclasses import dataclass, field


@dataclass(frozen=True)
class OrderLine:
    product: str
    price: int
    qty: int = 1

    def __post_init__(self):
        if self.price <= 0:
            raise InvalidLineError(f"неверная строка: {self.product}, цена {self.price}, количество {self.qty}")

    @property
    def cost(self):
        return self.price * self.qty

# %% order [exercise]
@dataclass
class Order:
    number: int
    lines: list = field(default_factory=list)

    def add(self, line):
        self.lines.append(line)

    @property
    def total(self):
        return sum(line.cost for line in self.lines)

    def close(self):
        if not self.lines:
            raise EmptyOrderError(f"заказ №{self.number} пуст")
        return self.total
# ─── заготовка ───
class Order:
    ...
# ─── проверка ───
from dataclasses import fields, is_dataclass


def test_fields():
    "dataclass с number и своим списком lines"
    assert is_dataclass(Order), "Order — не dataclass"
    a, b = Order(17), Order(18)
    assert a.lines == [] and b.lines == [], "у нового заказа lines — пустой список"
    a.lines.append("x")
    assert b.lines == [], "строка одного заказа появилась в другом — нужен field(default_factory=list)"


def test_total():
    "add и total"
    order = Order(17)
    order.add(OrderLine("Латте", 220, 2))
    order.add(OrderLine("Круассан", 140))
    assert isinstance(Order.__dict__.get("total"), property), "total должен быть свойством"
    assert order.total == 580, f"total = {order.total!r}, а нужно 580"
    assert order.close() == 580, "close() возвращает сумму заказа"


def test_empty():
    "пустой заказ — EmptyOrderError"
    try:
        Order(18).close()
    except EmptyOrderError as e:
        assert str(e) == "заказ №18 пуст", f"сообщение {str(e)!r}, а нужно \"заказ №18 пуст\""
    else:
        assert False, "close() пустого заказа не выбросил EmptyOrderError"
# ─── другое решение ───
@dataclass
class Order:
    number: int
    lines: list = field(default_factory=list)

    def add(self, line):
        self.lines = self.lines + [line]

    @property
    def total(self):
        result = 0
        for line in self.lines:
            result += line.cost
        return result

    def close(self):
        if len(self.lines) == 0:
            raise EmptyOrderError("заказ №" + str(self.number) + " пуст")
        return self.total
# ─── ошибка ───
@dataclass
class Order:
    number: int
    lines: list = field(default_factory=list)

    def add(self, line):
        self.lines.append(line)

    @property
    def total(self):
        return sum(line.cost for line in self.lines)

    def close(self):
        return self.total

# %% parse [exercise]
def parse_line(text):
    parts = text.split(";")
    if len(parts) != 3:
        raise InvalidLineError(f"не разобрать строку: {text}")
    name, price, qty = parts
    try:
        price, qty = int(price), int(qty)
    except ValueError as err:
        raise InvalidLineError(f"не разобрать строку: {text}") from err
    return OrderLine(name, price, qty)
# ─── заготовка ───
def parse_line(text):
    ...
# ─── проверка ───
def _error(text):
    try:
        parse_line(text)
    except InvalidLineError as e:
        return e
    except ValueError as e:
        assert False, f"parse_line({text!r}) выбросил {type(e).__name__}, а нужен InvalidLineError"
    return None


def test_ok():
    "правильная строка"
    got = parse_line("Латте;220;2")
    assert got == OrderLine("Латте", 220, 2), f"parse_line(\"Латте;220;2\") = {got!r}"


def test_bad_format():
    "не три части или не число"
    e = _error("Латте;220")
    assert e is not None and str(e) == "не разобрать строку: Латте;220", "для строки из двух частей нужен InvalidLineError(\"не разобрать строку: Латте;220\")"
    e = _error("Какао;190;x2")
    assert e is not None, "parse_line(\"Какао;190;x2\") не выбросил InvalidLineError"
    assert str(e) == "не разобрать строку: Какао;190;x2", f"сообщение {str(e)!r}"
    assert isinstance(e.__cause__, ValueError), "причина ошибки int потеряна — выбрасывайте через raise … from err"


def test_line_error():
    "ошибки OrderLine уходят как есть"
    e = _error("Чай;-120;1")
    assert e is not None, "parse_line(\"Чай;-120;1\") не выбросил InvalidLineError"
    assert str(e) == "неверная строка: Чай, цена -120, количество 1", f"сообщение {str(e)!r} — OrderLine создавайте вне try, чтобы её ошибка не превращалась в «не разобрать строку»"
# ─── другое решение ───
def parse_line(text):
    parts = text.split(";")
    if len(parts) == 3:
        try:
            numbers = [int(p) for p in parts[1:]]
        except ValueError as err:
            raise InvalidLineError("не разобрать строку: " + text) from err
        return OrderLine(parts[0], numbers[0], numbers[1])
    raise InvalidLineError("не разобрать строку: " + text)
# ─── ошибка ───
def parse_line(text):
    try:
        name, price, qty = text.split(";")
        return OrderLine(name, int(price), int(qty))
    except (ValueError, InvalidLineError) as err:
        raise InvalidLineError(f"не разобрать строку: {text}") from err
# ─── ошибка ───
def parse_line(text):
    parts = text.split(";")
    if len(parts) != 3:
        raise InvalidLineError(f"не разобрать строку: {text}")
    name, price, qty = parts
    try:
        price, qty = int(price), int(qty)
    except ValueError:
        raise InvalidLineError(f"не разобрать строку: {text}") from None
    return OrderLine(name, price, qty)

# %% day [exercise]
day = {
    17: ["Латте;220;2", "Круассан;140;1"],
    18: [],
    19: ["Раф;260;1", "Чай;-120;1"],
    20: ["Какао;190;x2"],
    21: ["Эспрессо;150;3"],
}
results = []
for number, texts in day.items():
    try:
        order = Order(number)
        for text in texts:
            order.add(parse_line(text))
        results.append(f"№{number}: {order.close()} ₽")
    except ShopError as error:
        results.append(f"№{number}: ошибка — {error}")
# ─── заготовка ───
day = {
    17: ["Латте;220;2", "Круассан;140;1"],
    18: [],
    19: ["Раф;260;1", "Чай;-120;1"],
    20: ["Какао;190;x2"],
    21: ["Эспрессо;150;3"],
}
results = ...
# ─── проверка ───
def test_results():
    "results — по строке на заказ"
    assert isinstance(results, list), f"results — это {type(results).__name__}, а нужен список строк"
    assert len(results) == 5, f"в results {len(results)} строк, а заказов 5 — по одной строке на заказ, даже если в нём ошибка"
    expected = [
        "№17: 580 ₽",
        "№18: ошибка — заказ №18 пуст",
        "№19: ошибка — неверная строка: Чай, цена -120, количество 1",
        "№20: ошибка — не разобрать строку: Какао;190;x2",
        "№21: 450 ₽",
    ]
    for got, want in zip(results, expected):
        assert got == want, f"строка отчёта {got!r}, а нужно {want!r}"
# ─── другое решение ───
day = {
    17: ["Латте;220;2", "Круассан;140;1"],
    18: [],
    19: ["Раф;260;1", "Чай;-120;1"],
    20: ["Какао;190;x2"],
    21: ["Эспрессо;150;3"],
}


def run(number, texts):
    order = Order(number)
    for text in texts:
        order.add(parse_line(text))
    return f"{order.close()} ₽"


results = []
for number in day:
    try:
        line = run(number, day[number])
    except ShopError as error:
        line = f"ошибка — {error}"
    results.append(f"№{number}: {line}")
# ─── ошибка ───
day = {
    17: ["Латте;220;2", "Круассан;140;1"],
    18: [],
    19: ["Раф;260;1", "Чай;-120;1"],
    20: ["Какао;190;x2"],
    21: ["Эспрессо;150;3"],
}
results = []
for number, texts in day.items():
    order = Order(number)
    for text in texts:
        try:
            order.add(parse_line(text))
        except ShopError:
            pass
    try:
        results.append(f"№{number}: {order.close()} ₽")
    except ShopError as error:
        results.append(f"№{number}: ошибка — {error}")

# %% summary
print("Касса за день")
for line in results:
    print(" ", line)
closed = [line for line in results if "ошибка" not in line]
print(f"проведено заказов: {len(closed)} из {len(results)}")
