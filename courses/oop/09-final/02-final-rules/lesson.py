# Урок oop-final-rules. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% model
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class ShopError(Exception):
    pass


@dataclass(frozen=True)
class Product:
    name: str
    price: int
    category: str


@dataclass
class Line:
    product: Product
    qty: int

    @property
    def cost(self):
        return self.product.price * self.qty


@dataclass
class Cart:
    lines: list = field(default_factory=list)

    def __len__(self):
        return len(self.lines)

    def __iter__(self):
        return iter(self.lines)

    @property
    def subtotal(self):
        return sum(line.cost for line in self.lines)


class PaymentError(ShopError):
    pass


class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        ...


class Cash(PaymentMethod):
    def __init__(self, given):
        self.given = given

    def pay(self, amount):
        if self.given < amount:
            raise PaymentError("недостаточно наличных")
        return f"наличные {self.given} ₽, сдача {self.given - amount} ₽"


latte = Product("Латте", 240, "кофе")
croissant = Product("Круассан", 140, "выпечка")
muffin = Product("Маффин", 130, "выпечка")
tea = Product("Чай", 120, "чай")
raf = Product("Раф", 260, "кофе")

sample = Cart([Line(latte, 3), Line(croissant, 2)])
print(sample.subtotal, len(sample), [line.cost for line in sample])
print(Cash(1000).pay(900))

# %% discount [exercise]
class Discount(ABC):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title

    @abstractmethod
    def amount(self, cart):
        ...
# ─── заготовка ───
class Discount:
    def __init__(self, title):
        ...

    def __str__(self):
        ...

    def amount(self, cart):
        ...
# ─── проверка ───
def test_abstract():
    "Discount — абстрактный"
    assert issubclass(Discount, ABC), "Discount должен наследовать от ABC"
    assert "amount" in getattr(Discount, "__abstractmethods__", set()), "amount должен быть абстрактным — @abstractmethod"


def test_title():
    "title и str"
    class Zero(Discount):
        def amount(self, cart):
            return 0
    zero = Zero("без скидки")
    assert getattr(zero, "title", None) == "без скидки", "название хранится в title"
    assert str(zero) == "без скидки", f"str = {str(zero)!r}"
# ─── другое решение ───
class Discount(ABC):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f"{self.title}"

    @abstractmethod
    def amount(self, cart):
        """Скидка в рублях для корзины."""
# ─── ошибка ───
class Discount(ABC):
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title

    def amount(self, cart):
        return 0

# %% discounts [exercise]
class PercentDiscount(Discount):
    def __init__(self, percent):
        super().__init__(f"скидка {percent} %")
        self.percent = percent

    def amount(self, cart):
        return round(cart.subtotal * self.percent / 100)


class CategoryDiscount(Discount):
    def __init__(self, category, percent):
        super().__init__(f"{category} -{percent} %")
        self.category = category
        self.percent = percent

    def amount(self, cart):
        base = sum(line.cost for line in cart if line.product.category == self.category)
        return round(base * self.percent / 100)
# ─── заготовка ───
class PercentDiscount(Discount):
    def __init__(self, percent):
        ...

    def amount(self, cart):
        ...


class CategoryDiscount(Discount):
    def __init__(self, category, percent):
        ...

    def amount(self, cart):
        ...
# ─── проверка ───
def test_percent():
    "PercentDiscount"
    d = PercentDiscount(10)
    assert hasattr(d, "title"), "у скидки нет title — вызовите super().__init__(название)"
    assert str(d) == "скидка 10 %", f"название {str(d)!r}"
    got = d.amount(Cart([Line(latte, 3), Line(croissant, 2)]))
    assert isinstance(got, int), f"скидка {got!r} — дробное число; округлите до целых: round(...)"
    assert got == 100, "10 % от корзины на 1000 ₽ — 100"


def test_category():
    "CategoryDiscount — только своя категория"
    d = CategoryDiscount("выпечка", 20)
    assert hasattr(d, "title"), "у скидки нет title — вызовите super().__init__(название)"
    assert str(d) == "выпечка -20 %", f"название {str(d)!r}, а нужно \"выпечка -20 %\""
    cart = Cart([Line(latte, 3), Line(croissant, 2)])
    got = d.amount(cart)
    assert isinstance(got, int), f"скидка {got!r} — дробное число; округлите до целых: round(...)"
    assert got != 200, "скидка посчитана от всей корзины, а нужно только от строк категории «выпечка»"
    assert got == 56, f"20 % от выпечки (280 ₽) = {got!r}, а нужно 56"
    assert d.amount(Cart([Line(tea, 1)])) == 0, "без выпечки скидка 0"
# ─── другое решение ───
class PercentDiscount(Discount):
    def __init__(self, percent):
        self.percent = percent
        super().__init__("скидка " + str(percent) + " %")

    def amount(self, cart):
        return round(cart.subtotal / 100 * self.percent)


class CategoryDiscount(Discount):
    def __init__(self, category, percent):
        self.category = category
        self.percent = percent
        super().__init__(f"{category} -{percent} %")

    def amount(self, cart):
        base = 0
        for line in cart:
            if line.product.category == self.category:
                base += line.cost
        return round(base * self.percent / 100)
# ─── ошибка ───
class PercentDiscount(Discount):
    def __init__(self, percent):
        super().__init__(f"скидка {percent} %")
        self.percent = percent

    def amount(self, cart):
        return round(cart.subtotal * self.percent / 100)


class CategoryDiscount(Discount):
    def __init__(self, category, percent):
        super().__init__(f"{category} -{percent} %")
        self.category = category
        self.percent = percent

    def amount(self, cart):
        return round(cart.subtotal * self.percent / 100)

# %% payments [exercise]
class Card(PaymentMethod):
    def __init__(self, balance):
        self.balance = balance

    def pay(self, amount):
        if amount > self.balance:
            raise PaymentError("недостаточно средств")
        self.balance -= amount
        return f"карта: {amount} ₽"
# ─── заготовка ───
class Card(PaymentMethod):
    def __init__(self, balance):
        ...

    def pay(self, amount):
        ...
# ─── проверка ───
def _payment_error(action):
    try:
        action()
    except PaymentError as e:
        return str(e)
    except Exception as e:
        assert False, f"выброшен {type(e).__name__}, а нужен PaymentError"
    return None


def test_card():
    "оплата картой"
    assert issubclass(Card, PaymentMethod), "Card должен наследовать от PaymentMethod"
    card = Card(2000)
    assert card.pay(664) == "карта: 664 ₽", "Card(2000).pay(664) должен вернуть \"карта: 664 ₽\""
    assert card.balance == 1336, f"после оплаты баланс {card.balance}, а нужно 1336"


def test_not_enough():
    "не хватает — PaymentError, баланс прежний"
    card = Card(1000)
    assert _payment_error(lambda: card.pay(5000)) == "недостаточно средств", "оплата больше баланса должна выбросить PaymentError(\"недостаточно средств\")"
    assert card.balance == 1000, "после отказа баланс не должен меняться"
# ─── другое решение ───
class Card(PaymentMethod):
    def __init__(self, balance):
        self.balance = balance

    def pay(self, amount):
        if self.balance - amount < 0:
            raise PaymentError("недостаточно средств")
        self.balance = self.balance - amount
        return "карта: " + str(amount) + " ₽"
# ─── ошибка ───
class Card(PaymentMethod):
    def __init__(self, balance):
        self.balance = balance

    def pay(self, amount):
        self.balance -= amount
        if self.balance < 0:
            raise PaymentError("недостаточно средств")
        return f"карта: {amount} ₽"
# ─── ошибка ───
class Card(PaymentMethod):
    def __init__(self, balance):
        self.balance = balance

    def pay(self, amount):
        if amount > self.balance:
            raise ValueError("недостаточно средств")
        self.balance -= amount
        return f"карта: {amount} ₽"

# %% receipt [exercise]
@dataclass
class Receipt:
    number: int
    subtotal: int
    discount: str
    saved: int
    payment: str

    @property
    def total(self):
        return self.subtotal - self.saved

    def __str__(self):
        lines = [
            f"Чек №{self.number}",
            f"Сумма: {self.subtotal} ₽",
            f"Скидка «{self.discount}»: -{self.saved} ₽",
            f"К оплате: {self.total} ₽",
            f"Оплата: {self.payment}",
        ]
        return "\n".join(lines)
# ─── заготовка ───
@dataclass
class Receipt:
    number: int
    subtotal: int
    discount: str
    saved: int
    payment: str

    @property
    def total(self):
        return self.subtotal - self.saved

    def __str__(self):
        ...
# ─── проверка ───
from dataclasses import fields, is_dataclass


def _receipt():
    return Receipt(1, 1000, "скидка 10 %", 100, "наличные 1000 ₽, сдача 100 ₽")


def test_fields():
    "dataclass и total"
    assert is_dataclass(Receipt), "Receipt — не dataclass"
    assert [f.name for f in fields(Receipt)] == ["number", "subtotal", "discount", "saved", "payment"], f"поля: {[f.name for f in fields(Receipt)]}"
    assert isinstance(Receipt.__dict__.get("total"), property), "total должен быть свойством"
    assert _receipt().total == 900, f"total = {_receipt().total!r}, а нужно 900"


def test_str():
    "текст чека"
    assert is_dataclass(Receipt), "сначала объявите Receipt dataclass'ом"
    expected = "Чек №1\nСумма: 1000 ₽\nСкидка «скидка 10 %»: -100 ₽\nК оплате: 900 ₽\nОплата: наличные 1000 ₽, сдача 100 ₽"
    got = str(_receipt())
    assert got.split("\n")[0] == "Чек №1", f"первая строка чека: {got.split(chr(10))[0]!r}"
    assert got == expected, f"текст чека:\n{got}"
# ─── другое решение ───
@dataclass
class Receipt:
    number: int
    subtotal: int
    discount: str
    saved: int
    payment: str

    @property
    def total(self):
        return self.subtotal - self.saved

    def __str__(self):
        return (
            f"Чек №{self.number}\n"
            f"Сумма: {self.subtotal} ₽\n"
            f"Скидка «{self.discount}»: -{self.saved} ₽\n"
            f"К оплате: {self.total} ₽\n"
            f"Оплата: {self.payment}"
        )
# ─── ошибка ───
@dataclass
class Receipt:
    number: int
    subtotal: int
    discount: str
    saved: int
    payment: str

    @property
    def total(self):
        return self.subtotal - self.saved

    def __repr__(self):
        return f"Чек №{self.number}"

# %% register [exercise]
class Register:
    def __init__(self, discounts):
        self.discounts = list(discounts)
        self.receipts = []

    def best_discount(self, cart):
        return max(self.discounts, key=lambda d: d.amount(cart))

    def checkout(self, cart, method):
        if cart.subtotal == 0:
            raise ShopError("пустая корзина")
        discount = self.best_discount(cart)
        saved = discount.amount(cart)
        payment = method.pay(cart.subtotal - saved)
        receipt = Receipt(len(self.receipts) + 1, cart.subtotal, str(discount), saved, payment)
        self.receipts.append(receipt)
        return receipt
# ─── заготовка ───
class Register:
    def __init__(self, discounts):
        ...

    def best_discount(self, cart):
        ...

    def checkout(self, cart, method):
        ...
# ─── проверка ───
def _register():
    return Register([PercentDiscount(10), CategoryDiscount("выпечка", 20)])


def test_best():
    "best_discount — наибольшая скидка"
    reg = _register()
    assert getattr(reg, "receipts", None) == [], "у новой кассы receipts — пустой список"
    got = reg.best_discount(Cart([Line(croissant, 3), Line(muffin, 2), Line(tea, 1)]))
    assert isinstance(got, Discount), f"best_discount вернул {got!r}, а нужна сама скидка"
    assert str(got) == "выпечка -20 %", f"для корзины с выпечкой лучшая скидка — «выпечка -20 %» (136 ₽ против 80 ₽), а выбрана {got}"


def test_checkout():
    "checkout выдаёт чек и сохраняет его"
    reg = _register()
    receipt = reg.checkout(Cart([Line(latte, 3), Line(croissant, 2)]), Cash(1000))
    assert isinstance(receipt, Receipt), f"checkout вернул {type(receipt).__name__}, а нужен Receipt"
    assert isinstance(receipt.saved, int), f"скидка в чеке {receipt.saved!r} — дробное число: округлите скидку в amount через round"
    assert (receipt.number, receipt.subtotal, receipt.discount, receipt.saved, receipt.total) == (1, 1000, "скидка 10 %", 100, 900), f"чек: {receipt!r}"
    assert receipt.payment == "наличные 1000 ₽, сдача 100 ₽", f"строка оплаты: {receipt.payment!r} — платить нужно сумму после скидки"
    second = reg.checkout(Cart([Line(tea, 2)]), Card(1000))
    assert second.number == 2 and reg.receipts == [receipt, second], "второй чек — №2, оба чека в receipts"


def test_errors():
    "пустая корзина и неудачная оплата — без чека"
    reg = _register()
    try:
        reg.checkout(Cart(), Cash(100))
    except ShopError as e:
        assert str(e) == "пустая корзина", f"сообщение {str(e)!r}"
    else:
        assert False, "пустую корзину касса провела — нужен ShopError(\"пустая корзина\")"
    try:
        reg.checkout(Cart([Line(raf, 1)]), Cash(200))
    except PaymentError:
        pass
    else:
        assert False, "оплата 200 ₽ за 234 ₽ прошла — ошибка оплаты должна уйти из checkout"
    assert reg.receipts == [], "после неудачных покупок чеков быть не должно"
    ok = reg.checkout(Cart([Line(tea, 1)]), Cash(200))
    assert ok.number == 1, f"первый успешный чек — №{ok.number}, а должен быть №1: номер берите после оплаты"
# ─── другое решение ───
class Register:
    def __init__(self, discounts):
        self.discounts = discounts
        self.receipts = []

    def best_discount(self, cart):
        best = self.discounts[0]
        for d in self.discounts:
            if d.amount(cart) > best.amount(cart):
                best = d
        return best

    def checkout(self, cart, method):
        subtotal = cart.subtotal
        if not subtotal:
            raise ShopError("пустая корзина")
        discount = self.best_discount(cart)
        saved = discount.amount(cart)
        payment = method.pay(subtotal - saved)
        self.receipts.append(Receipt(len(self.receipts) + 1, subtotal, discount.title, saved, payment))
        return self.receipts[-1]
# ─── ошибка ───
class Register:
    def __init__(self, discounts):
        self.discounts = list(discounts)
        self.receipts = []
        self.counter = 0

    def best_discount(self, cart):
        return max(self.discounts, key=lambda d: d.amount(cart))

    def checkout(self, cart, method):
        if cart.subtotal == 0:
            raise ShopError("пустая корзина")
        self.counter += 1
        discount = self.best_discount(cart)
        saved = discount.amount(cart)
        payment = method.pay(cart.subtotal - saved)
        receipt = Receipt(self.counter, cart.subtotal, str(discount), saved, payment)
        self.receipts.append(receipt)
        return receipt
# ─── ошибка ───
class Register:
    def __init__(self, discounts):
        self.discounts = list(discounts)
        self.receipts = []

    def best_discount(self, cart):
        return max(self.discounts, key=lambda d: d.amount(cart))

    def checkout(self, cart, method):
        if cart.subtotal == 0:
            raise ShopError("пустая корзина")
        discount = self.best_discount(cart)
        saved = discount.amount(cart)
        payment = method.pay(cart.subtotal)
        receipt = Receipt(len(self.receipts) + 1, cart.subtotal, str(discount), saved, payment)
        self.receipts.append(receipt)
        return receipt

# %% day [exercise]
card = Card(2000)
queue = [
    (Cart([Line(latte, 3), Line(croissant, 2)]), Cash(1000)),
    (Cart([Line(croissant, 3), Line(muffin, 2), Line(tea, 1)]), card),
    (Cart([Line(raf, 1)]), Cash(200)),
    (Cart(), Cash(500)),
    (Cart([Line(tea, 2), Line(muffin, 1)]), card),
]
register = Register([PercentDiscount(10), CategoryDiscount("выпечка", 20)])
failed = 0
for cart, method in queue:
    try:
        register.checkout(cart, method)
    except ShopError:
        failed += 1
revenue = sum(r.total for r in register.receipts)
biggest = max(register.receipts, key=lambda r: r.total).number
# ─── заготовка ───
card = Card(2000)
queue = [
    (Cart([Line(latte, 3), Line(croissant, 2)]), Cash(1000)),
    (Cart([Line(croissant, 3), Line(muffin, 2), Line(tea, 1)]), card),
    (Cart([Line(raf, 1)]), Cash(200)),
    (Cart(), Cash(500)),
    (Cart([Line(tea, 2), Line(muffin, 1)]), card),
]
register = ...
failed = ...
revenue = ...
biggest = ...
# ─── проверка ───
def test_register():
    "три чека"
    assert isinstance(register, Register), f"register — это {type(register).__name__}, а нужна касса Register([...])"
    assert len(register.receipts) == 3, f"у кассы {len(register.receipts)} чеков, а прошли 3 покупки из 5"
    assert [r.total for r in register.receipts] == [900, 664, 333], f"суммы чеков: {[r.total for r in register.receipts]}"


def test_report():
    "failed, revenue, biggest"
    assert failed == 2, f"failed = {failed!r}, а не прошли 2 покупки: раф (не хватило наличных) и пустая корзина"
    assert revenue == 1897, f"revenue = {revenue!r}, а выручка — 1897 ₽"
    assert biggest == 1, f"biggest = {biggest!r}, а больше всего — в чеке №1 (900 ₽)"
# ─── другое решение ───
card = Card(2000)
queue = [
    (Cart([Line(latte, 3), Line(croissant, 2)]), Cash(1000)),
    (Cart([Line(croissant, 3), Line(muffin, 2), Line(tea, 1)]), card),
    (Cart([Line(raf, 1)]), Cash(200)),
    (Cart(), Cash(500)),
    (Cart([Line(tea, 2), Line(muffin, 1)]), card),
]
register = Register([PercentDiscount(10), CategoryDiscount("выпечка", 20)])
receipts = []
for cart, method in queue:
    try:
        receipts.append(register.checkout(cart, method))
    except ShopError:
        pass
failed = len(queue) - len(receipts)
revenue = 0
for r in receipts:
    revenue += r.total
biggest = sorted(receipts, key=lambda r: r.total)[-1].number
# ─── ошибка ───
card = Card(2000)
queue = [
    (Cart([Line(latte, 3), Line(croissant, 2)]), Cash(1000)),
    (Cart([Line(croissant, 3), Line(muffin, 2), Line(tea, 1)]), card),
    (Cart([Line(raf, 1)]), Cash(200)),
    (Cart(), Cash(500)),
    (Cart([Line(tea, 2), Line(muffin, 1)]), card),
]
register = Register([PercentDiscount(10), CategoryDiscount("выпечка", 20)])
failed = 0
for cart, method in queue:
    try:
        register.checkout(cart, method)
    except ShopError:
        failed += 1
revenue = sum(r.subtotal for r in register.receipts)
biggest = max(register.receipts, key=lambda r: r.total).number

# %% summary
for receipt in register.receipts:
    print(receipt)
    print()
print(f"не прошло покупок: {failed}; выручка: {revenue} ₽; самый большой чек — №{biggest}")
