# Урок oop-p6-payments. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% payment [exercise]
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title

    @abstractmethod
    def pay(self, amount):
        ...
# ─── заготовка ───
from abc import ABC, abstractmethod


class PaymentMethod:
    def __init__(self, title):
        ...

    def __str__(self):
        ...

    def pay(self, amount):
        ...
# ─── проверка ───
def test_abstract():
    "PaymentMethod — абстрактный, pay обязателен"
    assert issubclass(PaymentMethod, ABC), "PaymentMethod должен наследовать от ABC"
    assert "pay" in getattr(PaymentMethod, "__abstractmethods__", set()), "pay должен быть абстрактным — @abstractmethod"
    try:
        PaymentMethod("что-то")
    except TypeError:
        pass
    else:
        assert False, "экземпляр PaymentMethod создаётся, а у абстрактного класса не должен"


def test_title():
    "title и str у подкласса"
    class Free(PaymentMethod):
        def pay(self, amount):
            return "бесплатно"
    free = Free("подарок")
    assert getattr(free, "title", None) == "подарок", "название хранится в атрибуте title"
    assert str(free) == "подарок", f"str() способа оплаты = {str(free)!r}, а нужно название"
# ─── другое решение ───
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f"{self.title}"

    @abstractmethod
    def pay(self, amount):
        """Провести оплату и вернуть строку для чека."""
# ─── ошибка ───
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title

    def pay(self, amount):
        return ""

# %% cash [exercise]
class Cash(PaymentMethod):
    def __init__(self, given):
        super().__init__("наличные")
        self.given = given

    def pay(self, amount):
        if self.given < amount:
            raise ValueError("недостаточно наличных")
        return f"наличные {self.given} ₽, сдача {self.given - amount} ₽"
# ─── заготовка ───
class Cash(PaymentMethod):
    def __init__(self, given):
        ...

    def pay(self, amount):
        ...
# ─── проверка ───
def test_cash():
    "сдача и строка чека"
    cash = Cash(1000)
    assert str(cash) == "наличные", f"название наличных — {str(cash)!r}, а нужно \"наличные\": super().__init__(\"наличные\")"
    assert getattr(cash, "given", None) == 1000, "сумма от покупателя хранится в атрибуте given"
    got = cash.pay(640)
    assert got == "наличные 1000 ₽, сдача 360 ₽", f"pay(640) вернул {got!r}"
    assert Cash(640).pay(640) == "наличные 640 ₽, сдача 0 ₽", "без сдачи — «сдача 0 ₽»"


def test_not_enough():
    "дали меньше — ValueError"
    try:
        Cash(500).pay(640)
    except ValueError as e:
        assert str(e) == "недостаточно наличных", f"сообщение {str(e)!r}, а нужно \"недостаточно наличных\""
        return
    assert False, "Cash(500).pay(640) не выбросил ValueError"
# ─── другое решение ───
class Cash(PaymentMethod):
    def __init__(self, given):
        self.given = given
        super().__init__("наличные")

    def pay(self, amount):
        change = self.given - amount
        if change < 0:
            raise ValueError("недостаточно наличных")
        return f"наличные {self.given} ₽, сдача {change} ₽"
# ─── ошибка ───
class Cash(PaymentMethod):
    def __init__(self, given):
        super().__init__("наличные")
        self.given = given

    def pay(self, amount):
        return f"наличные {self.given} ₽, сдача {self.given - amount} ₽"

# %% card [exercise]
class Card(PaymentMethod):
    def __init__(self, number, balance):
        super().__init__(f"карта *{number[-4:]}")
        self.number = number
        self.balance = balance

    def pay(self, amount):
        if amount > self.balance:
            raise ValueError("недостаточно средств на карте")
        self.balance -= amount
        return f"{self.title}: списано {amount} ₽"
# ─── заготовка ───
class Card(PaymentMethod):
    def __init__(self, number, balance):
        ...

    def pay(self, amount):
        ...
# ─── проверка ───
def _card():
    return Card("2200 1234 5678 9012", 2000)


def test_title():
    "название — последние 4 цифры"
    assert str(_card()) == "карта *9012", f"название карты — {str(_card())!r}, а нужно \"карта *9012\""


def test_pay():
    "списание и строка чека"
    card = _card()
    got = card.pay(1250)
    assert got == "карта *9012: списано 1250 ₽", f"pay(1250) вернул {got!r}"
    assert card.balance == 750, f"после оплаты 1250 ₽ остаток {card.balance}, а нужно 750"


def test_not_enough():
    "не хватает — ValueError, остаток прежний"
    card = _card()
    try:
        card.pay(2100)
    except ValueError as e:
        assert str(e) == "недостаточно средств на карте", f"сообщение {str(e)!r}"
    else:
        assert False, "pay(2100) при остатке 2000 не выбросил ValueError"
    assert card.balance == 2000, f"после отказа остаток {card.balance} — он не должен меняться"
# ─── другое решение ───
class Card(PaymentMethod):
    def __init__(self, number, balance):
        self.number = number
        self.balance = balance
        super().__init__("карта *" + number[-4:])

    def pay(self, amount):
        if self.balance - amount < 0:
            raise ValueError("недостаточно средств на карте")
        self.balance = self.balance - amount
        return str(self) + f": списано {amount} ₽"
# ─── ошибка ───
class Card(PaymentMethod):
    def __init__(self, number, balance):
        super().__init__(f"карта *{number[-4:]}")
        self.number = number
        self.balance = balance

    def pay(self, amount):
        self.balance -= amount
        if self.balance < 0:
            raise ValueError("недостаточно средств на карте")
        return f"{self.title}: списано {amount} ₽"
# ─── ошибка ───
class Card(PaymentMethod):
    def __init__(self, number, balance):
        super().__init__(f"карта *{number[:4]}")
        self.number = number
        self.balance = balance

    def pay(self, amount):
        if amount > self.balance:
            raise ValueError("недостаточно средств на карте")
        self.balance -= amount
        return f"{self.title}: списано {amount} ₽"

# %% points [exercise]
class LoyaltyPoints(PaymentMethod):
    def __init__(self, points):
        super().__init__("баллы")
        self.points = points

    def pay(self, amount):
        if amount > self.points:
            raise ValueError("недостаточно баллов")
        self.points -= amount
        return f"баллы: списано {amount}, осталось {self.points}"
# ─── заготовка ───
class LoyaltyPoints(PaymentMethod):
    def __init__(self, points):
        ...

    def pay(self, amount):
        ...
# ─── проверка ───
def test_pay():
    "списание баллов"
    points = LoyaltyPoints(500)
    assert str(points) == "баллы", f"название — {str(points)!r}, а нужно \"баллы\""
    got = points.pay(380)
    assert got == "баллы: списано 380, осталось 120", f"pay(380) вернул {got!r}"
    assert points.points == 120, f"после оплаты осталось {points.points} баллов, а нужно 120"


def test_not_enough():
    "не хватает — ValueError"
    points = LoyaltyPoints(100)
    try:
        points.pay(380)
    except ValueError as e:
        assert str(e) == "недостаточно баллов", f"сообщение {str(e)!r}"
    else:
        assert False, "pay(380) при 100 баллах не выбросил ValueError"
    assert points.points == 100, "после отказа баллы не должны меняться"
# ─── другое решение ───
class LoyaltyPoints(PaymentMethod):
    def __init__(self, points):
        super().__init__("баллы")
        self.points = points

    def pay(self, amount):
        if self.points < amount:
            raise ValueError("недостаточно баллов")
        self.points = self.points - amount
        return "баллы: списано " + str(amount) + ", осталось " + str(self.points)
# ─── ошибка ───
class LoyaltyPoints(PaymentMethod):
    def __init__(self, points):
        super().__init__("баллы")
        self.points = points

    def pay(self, amount):
        if amount > self.points:
            raise ValueError("недостаточно баллов")
        return f"баллы: списано {amount}, осталось {self.points - amount}"

# %% order [exercise]
class Order:
    def __init__(self, number, total, method):
        self.number = number
        self.total = total
        self.method = method
        self.paid = False

    def pay(self):
        receipt = self.method.pay(self.total)
        self.paid = True
        return f"заказ №{self.number}: {receipt}"

    @classmethod
    def from_line(cls, line, method):
        number, total = line.split(";")
        return cls(int(number), int(total), method)
# ─── заготовка ───
class Order:
    def __init__(self, number, total, method):
        ...

    def pay(self):
        ...

    @classmethod
    def from_line(cls, line, method):
        ...
# ─── проверка ───
def test_new():
    "новый заказ не оплачен"
    order = Order(17, 640, Cash(1000))
    assert (getattr(order, "number", None), getattr(order, "total", None)) == (17, 640), "номер и сумма — в атрибутах number и total"
    assert getattr(order, "paid", None) is False, "у нового заказа paid = False"


def test_pay():
    "pay делегирует способу оплаты"
    order = Order(17, 640, Cash(1000))
    got = order.pay()
    assert got == "заказ №17: наличные 1000 ₽, сдача 360 ₽", f"pay() вернул {got!r}"
    assert order.paid is True, "после оплаты paid должен стать True"


def test_failed():
    "ValueError уходит дальше, paid остаётся False"
    order = Order(18, 640, Cash(500))
    try:
        order.pay()
    except ValueError:
        pass
    else:
        assert False, "оплата наличными 500 ₽ за 640 ₽ прошла — pay заказа должен пропустить ValueError способа оплаты дальше"
    assert order.paid is False, "оплата не прошла, а paid стал True — ставьте его только после успешной оплаты"


def test_from_line():
    "from_line — метод класса"
    assert isinstance(Order.__dict__.get("from_line"), classmethod), "from_line должен быть методом класса — @classmethod"
    cash = Cash(1000)
    order = Order.from_line("17;640", cash)
    assert isinstance(order, Order), f"from_line вернул {type(order).__name__}"
    assert (order.number, order.total) == (17, 640), f"номер и сумма = {order.number!r}, {order.total!r}, а нужны числа 17 и 640"
    assert order.method is cash, "способ оплаты — переданный объект"
# ─── другое решение ───
class Order:
    def __init__(self, number, total, method):
        self.number = number
        self.total = total
        self.method = method
        self.paid = False

    def pay(self):
        try:
            receipt = self.method.pay(self.total)
        except ValueError:
            self.paid = False
            raise
        self.paid = True
        return "заказ №" + str(self.number) + ": " + receipt

    @classmethod
    def from_line(cls, line, method):
        parts = [int(x) for x in line.split(";")]
        return cls(parts[0], parts[1], method)
# ─── ошибка ───
class Order:
    def __init__(self, number, total, method):
        self.number = number
        self.total = total
        self.method = method
        self.paid = False

    def pay(self):
        self.paid = True
        receipt = self.method.pay(self.total)
        return f"заказ №{self.number}: {receipt}"

    @classmethod
    def from_line(cls, line, method):
        number, total = line.split(";")
        return cls(int(number), int(total), method)
# ─── ошибка ───
class Order:
    def __init__(self, number, total, method):
        self.number = number
        self.total = total
        self.method = method
        self.paid = False

    def pay(self):
        try:
            receipt = self.method.pay(self.total)
        except ValueError:
            return f"заказ №{self.number}: не оплачен"
        self.paid = True
        return f"заказ №{self.number}: {receipt}"

    @classmethod
    def from_line(cls, line, method):
        number, total = line.split(";")
        return cls(int(number), int(total), method)

# %% day [exercise]
card = Card("2200 1234 5678 9012", 2000)
lines = ["17;1250", "18;640", "19;380", "20;1800"]
methods = [card, Cash(1000), LoyaltyPoints(500), card]
receipts = []
failed = []
for line, method in zip(lines, methods):
    order = Order.from_line(line, method)
    try:
        receipts.append(order.pay())
    except ValueError:
        failed.append(order.number)
# ─── заготовка ───
card = Card("2200 1234 5678 9012", 2000)
lines = ["17;1250", "18;640", "19;380", "20;1800"]
methods = [card, Cash(1000), LoyaltyPoints(500), card]
receipts = ...
failed = ...
# ─── проверка ───
def test_receipts():
    "receipts — чеки оплаченных"
    assert isinstance(receipts, list), f"receipts — это {type(receipts).__name__}, а нужен список строк"
    assert receipts == [
        "заказ №17: карта *9012: списано 1250 ₽",
        "заказ №18: наличные 1000 ₽, сдача 360 ₽",
        "заказ №19: баллы: списано 380, осталось 120",
    ], f"receipts = {receipts}"


def test_failed():
    "failed — номера неоплаченных"
    assert failed != ["20"], "номер заказа — число 20, а не строка"
    assert failed != [], "все заказы оплачены, а заказ №20 должен был не пройти: первый и четвёртый покупатель платят одной картой card — после заказа №17 на ней 750 ₽"
    assert failed == [20], f"failed = {failed}, а не прошёл только заказ №20 — на карте осталось 750 ₽"
    assert card.balance == 750, f"на карте осталось {card.balance} ₽, а должно 750 — оплачивайте каждый заказ один раз"
# ─── другое решение ───
card = Card("2200 1234 5678 9012", 2000)
lines = ["17;1250", "18;640", "19;380", "20;1800"]
methods = [card, Cash(1000), LoyaltyPoints(500), card]
receipts, failed = [], []
for i in range(len(lines)):
    order = Order.from_line(lines[i], methods[i])
    try:
        line = order.pay()
    except ValueError:
        failed.append(order.number)
    else:
        receipts.append(line)
# ─── ошибка ───
card = Card("2200 1234 5678 9012", 2000)
lines = ["17;1250", "18;640", "19;380", "20;1800"]
methods = [card, Cash(1000), LoyaltyPoints(500), Card("2200 1234 5678 9012", 2000)]
receipts = []
failed = []
for line, method in zip(lines, methods):
    order = Order.from_line(line, method)
    try:
        receipts.append(order.pay())
    except ValueError:
        failed.append(order.number)

# %% summary
print("Касса за утро")
for line in receipts:
    print(" ", line)
print("не оплачены:", ", ".join(f"№{n}" for n in failed))
print(f"на карте *9012 осталось {card.balance} ₽")
