# Урок oop-exceptions. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% own
class RegisterClosedError(Exception):
    pass


def open_check(hour):
    if hour < 8 or hour >= 22:
        raise RegisterClosedError(f"касса закрыта в {hour}:00")
    return "чек открыт"


print(open_check(9))
try:
    open_check(23)
except RegisterClosedError as error:
    print(type(error).__name__, "—", error)

# %% hierarchy
class DeliveryError(Exception):
    pass


class CourierLateError(DeliveryError):
    pass


class AddressError(DeliveryError):
    pass


for problem in [CourierLateError("курьер опаздывает"), AddressError("нет такого дома")]:
    try:
        raise problem
    except DeliveryError as error:  # перехватит оба подкласса
        print(type(error).__name__, "→", error)
print(issubclass(AddressError, DeliveryError), issubclass(AddressError, Exception))

# %% errors [exercise]
class ShopError(Exception):
    pass


class OutOfStockError(ShopError):
    pass


class PaymentError(ShopError):
    pass
# ─── заготовка ───
# объявите ShopError, OutOfStockError и PaymentError
# ─── проверка ───
def _cls(name):
    cls = globals().get(name)
    assert isinstance(cls, type), f"класса {name} нет — объявите его"
    return cls


def test_base():
    "ShopError — подкласс Exception"
    shop = _cls("ShopError")
    assert issubclass(shop, Exception), "ShopError должен наследовать от Exception: class ShopError(Exception):"


def test_children():
    "OutOfStockError и PaymentError — подклассы ShopError"
    shop = _cls("ShopError")
    for name in ["OutOfStockError", "PaymentError"]:
        cls = _cls(name)
        assert issubclass(cls, shop), f"{name} должен наследовать от ShopError, а не прямо от Exception — иначе except ShopError его не перехватит"
    assert not issubclass(_cls("PaymentError"), _cls("OutOfStockError")), "PaymentError и OutOfStockError — разные ветки, оба наследуют от ShopError"
# ─── другое решение ───
class ShopError(Exception):
    """Любая ошибка кассы."""


class OutOfStockError(ShopError):
    """Не хватает товара на складе."""


class PaymentError(ShopError):
    """Оплата не прошла."""
# ─── ошибка ───
class ShopError(Exception):
    pass


class OutOfStockError(Exception):
    pass


class PaymentError(Exception):
    pass

# %% attrs
class PaymentDeclinedError(Exception):
    def __init__(self, amount, reason):
        super().__init__(f"оплата {amount} ₽ отклонена: {reason}")
        self.amount = amount
        self.reason = reason


try:
    raise PaymentDeclinedError(640, "нет связи с банком")
except PaymentDeclinedError as error:
    print(error)
    print(error.amount, error.reason)

# %% out-of-stock [exercise]
class OutOfStockError(ShopError):
    def __init__(self, name, requested, available):
        super().__init__(f"мало «{name}»: нужно {requested}, есть {available}")
        self.name = name
        self.requested = requested
        self.available = available
# ─── заготовка ───
class OutOfStockError(ShopError):
    def __init__(self, name, requested, available):
        ...
# ─── проверка ───
def _error():
    try:
        return OutOfStockError("Сироп", 2, 1)
    except TypeError as e:
        assert False, f"OutOfStockError(\"Сироп\", 2, 1) не создаётся: {e}"


def test_attrs():
    "name, requested, available"
    assert issubclass(OutOfStockError, ShopError), "OutOfStockError должен по-прежнему наследовать от ShopError"
    e = _error()
    got = (getattr(e, "name", None), getattr(e, "requested", None), getattr(e, "available", None))
    assert got == ("Сироп", 2, 1), f"атрибуты name, requested, available = {got}"


def test_message():
    "str(error) — понятный текст"
    got = str(_error())
    assert got != "", "у исключения пустой текст — передайте его в super().__init__(…)"
    assert got == "мало «Сироп»: нужно 2, есть 1", f"str(error) = {got!r}"
# ─── другое решение ───
class OutOfStockError(ShopError):
    def __init__(self, name, requested, available):
        self.name = name
        self.requested = requested
        self.available = available
        message = "мало «" + name + "»: нужно " + str(requested) + ", есть " + str(available)
        super().__init__(message)
# ─── ошибка ───
class OutOfStockError(ShopError):
    def __init__(self, name, requested, available):
        self.name = name
        self.requested = requested
        self.available = available
# ─── ошибка ───
class OutOfStockError(Exception):
    def __init__(self, name, requested, available):
        super().__init__(f"мало «{name}»: нужно {requested}, есть {available}")
        self.name = name
        self.requested = requested
        self.available = available

# %% sell [exercise]
def sell(stock, name, qty):
    available = stock.get(name, 0)
    if available < qty:
        raise OutOfStockError(name, qty, available)
    stock[name] = available - qty
# ─── заготовка ───
def sell(stock, name, qty):
    ...
# ─── проверка ───
def test_ok():
    "хватает — количество уменьшается"
    stock = {"Сироп": 3}
    sell(stock, "Сироп", 2)
    assert stock == {"Сироп": 1}, f"после sell(…, \"Сироп\", 2) склад {stock}, а нужно {{'Сироп': 1}}"


def test_short():
    "не хватает — OutOfStockError, склад прежний"
    stock = {"Сироп": 1}
    try:
        sell(stock, "Сироп", 2)
    except OutOfStockError as e:
        assert (e.name, e.requested, e.available) == ("Сироп", 2, 1), f"в исключении name, requested, available = {e.name!r}, {e.requested!r}, {e.available!r}"
    except KeyError:
        assert False, "sell упал с KeyError — сколько есть, узнайте через stock.get(name, 0)"
    else:
        assert False, "sell(…, \"Сироп\", 2) при одной бутылке не выбросил OutOfStockError"
    assert stock == {"Сироп": 1}, f"после отказа склад {stock} — он не должен меняться"


def test_missing():
    "товара нет вовсе — тоже OutOfStockError"
    try:
        sell({}, "Корица", 1)
    except OutOfStockError as e:
        assert e.available == 0, f"товара нет — available должен быть 0, а он {e.available!r}"
    except KeyError:
        assert False, "sell упал с KeyError — для отсутствующего товара считайте количество 0: stock.get(name, 0)"
    else:
        assert False, "sell для отсутствующего товара не выбросил OutOfStockError"
# ─── другое решение ───
def sell(stock, name, qty):
    if name not in stock or stock[name] < qty:
        raise OutOfStockError(name, qty, stock.get(name, 0))
    stock[name] -= qty
# ─── ошибка ───
def sell(stock, name, qty):
    stock[name] = stock.get(name, 0) - qty
    if stock[name] < 0:
        raise OutOfStockError(name, qty, stock[name] + qty)
# ─── ошибка ───
def sell(stock, name, qty):
    available = stock[name]
    if available < qty:
        raise OutOfStockError(name, qty, available)
    stock[name] = available - qty

# %% chain
class PriceFormatError(Exception):
    pass


def parse_price(text):
    try:
        return int(text.replace("₽", ""))
    except ValueError as err:
        raise PriceFormatError(f"цена не разобрана: {text}") from err


try:
    parse_price("двести ₽")
except PriceFormatError as error:
    print(error)
    print("причина:", type(error.__cause__).__name__, "—", error.__cause__)

# %% parse [exercise]
class OrderFormatError(ShopError):
    pass


def parse_qty(text):
    try:
        return int(text[1:])
    except ValueError as err:
        raise OrderFormatError(f"неверное количество: {text}") from err
# ─── заготовка ───
class OrderFormatError(ShopError):
    pass


def parse_qty(text):
    ...
# ─── проверка ───
def test_ok():
    "x2 → 2"
    got = parse_qty("x2")
    assert got == 2, f"parse_qty(\"x2\") = {got!r}, а нужно 2"
    assert parse_qty("x12") == 12, "parse_qty(\"x12\") должно быть 12"


def test_error():
    "неверное число — OrderFormatError от ValueError"
    try:
        parse_qty("x два")
    except OrderFormatError as e:
        assert str(e) == "неверное количество: x два", f"сообщение {str(e)!r}"
        assert isinstance(e.__cause__, ValueError), "у OrderFormatError нет причины — выбросите его через raise … from err"
    except ValueError:
        assert False, "parse_qty выбросил ValueError — перехватите его и выбросите OrderFormatError"
    else:
        assert False, "parse_qty(\"x два\") не выбросил исключение"
# ─── другое решение ───
class OrderFormatError(ShopError):
    pass


def parse_qty(text):
    digits = text.removeprefix("x")
    try:
        qty = int(digits)
    except ValueError as err:
        raise OrderFormatError("неверное количество: " + text) from err
    return qty
# ─── ошибка ───
class OrderFormatError(ShopError):
    pass


def parse_qty(text):
    try:
        return int(text[1:])
    except ValueError:
        raise OrderFormatError(f"неверное количество: {text}") from None

# %% catch-quiz [quiz]
try:
    sell({"Сироп": 1}, "Сироп", 10)
except ShopError:
    print("ошибка кассы")
except OutOfStockError:
    print("нет товара")
