# Урок oop-p5-discounts. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% cart
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Cart:
    def __init__(self, items=None):
        self.items = list(items) if items is not None else []

    def add(self, product):
        self.items.append(product)

    @property
    def subtotal(self):
        return sum(p.price for p in self.items)


cart = Cart([Product("Латте", 220), Product("Круассан", 140)])
print(cart.items, cart.subtotal)

# %% base [exercise]
class Discount:
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title

    def amount(self, cart):
        return 0
# ─── заготовка ───
class Discount:
    def __init__(self, title):
        ...

    def __str__(self):
        ...

    def amount(self, cart):
        ...
# ─── проверка ───
def test_title():
    "title и str"
    d = Discount("без скидки")
    assert getattr(d, "title", None) == "без скидки", "название хранится в атрибуте title"
    assert "__str__" in Discount.__dict__, "в классе нет __str__"
    assert str(d) == "без скидки", f"str(Discount(\"без скидки\")) = {str(d)!r}"


def test_amount():
    "базовая скидка — 0"
    got = Discount("без скидки").amount(Cart([Product("Латте", 220)]))
    assert got == 0, f"amount у базовой скидки = {got!r}, а нужно 0"
# ─── другое решение ───
class Discount:
    def __init__(self, title="без скидки"):
        self.title = title

    def __str__(self):
        return f"{self.title}"

    def amount(self, cart):
        return 0 * cart.subtotal
# ─── ошибка ───
class Discount:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return self.title

    def amount(self, cart):
        return 0
# ─── ошибка ───
class Discount:
    def __init__(self, title):
        self.title = title

    def __str__(self):
        return self.title

    def amount(self, cart):
        return cart.subtotal

# %% percent [exercise]
class PercentDiscount(Discount):
    def __init__(self, percent):
        super().__init__(f"скидка {percent} %")
        self.percent = percent

    def amount(self, cart):
        return round(cart.subtotal * self.percent / 100)
# ─── заготовка ───
class PercentDiscount(Discount):
    def __init__(self, percent):
        ...

    def amount(self, cart):
        ...
# ─── проверка ───
def test_init():
    "percent и название"
    d = PercentDiscount(10)
    assert issubclass(PercentDiscount, Discount), "PercentDiscount должен наследовать от Discount"
    assert getattr(d, "percent", None) == 10, "процент хранится в атрибуте percent"
    assert getattr(d, "title", None) == "скидка 10 %", "название передайте в __init__ базового класса: super().__init__(f\"скидка {percent} %\")"
    assert str(d) == "скидка 10 %", f"str(PercentDiscount(10)) = {str(d)!r} — __str__ наследуется от Discount"


def test_amount():
    "процент от суммы, округлённый"
    cart = Cart([Product("Латте", 220), Product("Круассан", 140), Product("Чай", 120)])
    got = PercentDiscount(10).amount(cart)
    assert got != 432, "это сумма после скидки, а amount — размер самой скидки"
    assert got == 48, f"10 % от 480 = {got!r}, а нужно 48"
    got = PercentDiscount(15).amount(Cart([Product("Торт", 1063)]))
    assert got == 159, f"15 % от 1063 = {got!r}, а нужно 159 (159.45, округлите)"
# ─── другое решение ───
class PercentDiscount(Discount):
    def __init__(self, percent):
        self.percent = percent
        super().__init__("скидка " + str(percent) + " %")

    def amount(self, cart):
        return round(cart.subtotal / 100 * self.percent)
# ─── ошибка ───
class PercentDiscount(Discount):
    def __init__(self, percent):
        super().__init__(f"скидка {percent} %")
        self.percent = percent

    def amount(self, cart):
        return round(cart.subtotal * (100 - self.percent) / 100)
# ─── ошибка ───
class PercentDiscount(Discount):
    def __init__(self, percent):
        self.percent = percent

    def amount(self, cart):
        return round(cart.subtotal * self.percent / 100)

# %% fixed [exercise]
class FixedDiscount(Discount):
    def __init__(self, value):
        super().__init__(f"минус {value} ₽")
        self.value = value

    def amount(self, cart):
        return min(self.value, cart.subtotal)
# ─── заготовка ───
class FixedDiscount(Discount):
    def __init__(self, value):
        ...

    def amount(self, cart):
        ...
# ─── проверка ───
def test_init():
    "value и название"
    d = FixedDiscount(150)
    assert issubclass(FixedDiscount, Discount), "FixedDiscount должен наследовать от Discount"
    assert getattr(d, "value", None) == 150, "сумма хранится в атрибуте value"
    assert str(d) == "минус 150 ₽", f"str(FixedDiscount(150)) = {str(d)!r}, а нужно \"минус 150 ₽\""


def test_amount():
    "фиксированная сумма, но не больше корзины"
    assert FixedDiscount(150).amount(Cart([Product("Латте", 220), Product("Чай", 120)])) == 150, "для корзины на 340 ₽ скидка — 150"
    got = FixedDiscount(150).amount(Cart([Product("Печенье", 90)]))
    assert got != 150, "скидка больше суммы корзины: для корзины на 90 ₽ она должна быть 90"
    assert got == 90, f"для корзины на 90 ₽ amount = {got!r}, а нужно 90"
# ─── другое решение ───
class FixedDiscount(Discount):
    def __init__(self, value):
        super().__init__(f"минус {value} ₽")
        self.value = value

    def amount(self, cart):
        if cart.subtotal < self.value:
            return cart.subtotal
        return self.value
# ─── ошибка ───
class FixedDiscount(Discount):
    def __init__(self, value):
        super().__init__(f"минус {value} ₽")
        self.value = value

    def amount(self, cart):
        return self.value

# %% buy-n [exercise]
class BuyNGetOne(Discount):
    def __init__(self, name, n):
        super().__init__(f"каждый {n}-й {name} в подарок")
        self.name = name
        self.n = n

    def amount(self, cart):
        same = [p for p in cart.items if p.name == self.name]
        if not same:
            return 0
        return len(same) // self.n * same[0].price
# ─── заготовка ───
class BuyNGetOne(Discount):
    def __init__(self, name, n):
        ...

    def amount(self, cart):
        ...
# ─── проверка ───
def _latte_cart(k):
    return Cart([Product("Латте", 220) for _ in range(k)] + [Product("Чай", 120)])


def test_init():
    "name, n и название"
    d = BuyNGetOne("Латте", 3)
    assert issubclass(BuyNGetOne, Discount), "BuyNGetOne должен наследовать от Discount"
    assert (getattr(d, "name", None), getattr(d, "n", None)) == ("Латте", 3), "название товара и n хранятся в атрибутах name и n"
    assert str(d) == "каждый 3-й Латте в подарок", f"str(BuyNGetOne(\"Латте\", 3)) = {str(d)!r}"


def test_amount():
    "по одному бесплатному на каждые n"
    d = BuyNGetOne("Латте", 3)
    assert d.amount(_latte_cart(2)) == 0, "из двух латте бесплатных нет — скидка 0"
    assert d.amount(_latte_cart(3)) == 220, f"из трёх латте один бесплатный — скидка 220, а получилось {d.amount(_latte_cart(3))!r}"
    got = d.amount(_latte_cart(7))
    assert got != 7 // 3, "получилось число бесплатных, а нужна скидка в рублях — умножьте на цену"
    assert got == 440, f"из семи латте бесплатных два — скидка 440, а получилось {got!r}"


def test_absent():
    "товара нет — скидка 0"
    got = BuyNGetOne("Раф", 2).amount(_latte_cart(3))
    assert got == 0, f"рафа в корзине нет, а скидка {got!r}"
    assert BuyNGetOne("Раф", 2).amount(Cart()) == 0, "у пустой корзины скидка 0"
# ─── другое решение ───
class BuyNGetOne(Discount):
    def __init__(self, name, n):
        super().__init__(f"каждый {n}-й {name} в подарок")
        self.name = name
        self.n = n

    def amount(self, cart):
        count = 0
        price = 0
        for p in cart.items:
            if p.name == self.name:
                count += 1
                price = p.price
        return count // self.n * price
# ─── ошибка ───
class BuyNGetOne(Discount):
    def __init__(self, name, n):
        super().__init__(f"каждый {n}-й {name} в подарок")
        self.name = name
        self.n = n

    def amount(self, cart):
        same = [p for p in cart.items if p.name == self.name]
        if not same:
            return 0
        return len(same) // self.n
# ─── ошибка ───
class BuyNGetOne(Discount):
    def __init__(self, name, n):
        super().__init__(f"каждый {n}-й {name} в подарок")
        self.name = name
        self.n = n

    def amount(self, cart):
        same = [p for p in cart.items if p.name == self.name]
        if not same:
            return 0
        return round(len(same) / self.n) * same[0].price

# %% checkout [exercise]
def to_pay(cart, discount):
    return cart.subtotal - discount.amount(cart)


def best_discount(cart, discounts):
    return max(discounts, key=lambda d: d.amount(cart))
# ─── заготовка ───
def to_pay(cart, discount):
    ...


def best_discount(cart, discounts):
    ...
# ─── проверка ───
class _Coupon:
    "скидка, о которой касса заранее не знает"

    def amount(self, cart):
        return 70


def test_to_pay():
    "к оплате — сумма минус скидка"
    cart = Cart([Product("Латте", 220), Product("Чай", 120)])
    got = to_pay(cart, FixedDiscount(100))
    assert got is not None, "to_pay ничего не возвращает — нужен return"
    assert got == 240, f"to_pay для корзины 340 ₽ и скидки 100 ₽ = {got!r}, а нужно 240"
    assert to_pay(cart, _Coupon()) == 270, "to_pay должна работать с любой скидкой, у которой есть amount(cart)"


def test_best():
    "лучшая — с наибольшей скидкой"
    cart = Cart([Product("Латте", 220), Product("Чай", 120)])
    percent, fixed, coupon = PercentDiscount(10), FixedDiscount(50), _Coupon()
    got = best_discount(cart, [percent, fixed, coupon])
    assert not isinstance(got, (int, float)), f"best_discount вернула число {got!r}, а нужна сама скидка"
    assert got is coupon, "из скидок 34, 50 и 70 ₽ лучшая — 70 ₽: сравнивайте amount(cart) любых скидок, без проверок класса"
# ─── другое решение ───
def to_pay(cart, discount):
    return cart.subtotal - discount.amount(cart)


def best_discount(cart, discounts):
    best = discounts[0]
    for d in discounts:
        if d.amount(cart) > best.amount(cart):
            best = d
    return best
# ─── ошибка ───
def to_pay(cart, discount):
    return cart.subtotal - discount.amount(cart)


def best_discount(cart, discounts):
    return min(discounts, key=lambda d: d.amount(cart))
# ─── ошибка ───
def to_pay(cart, discount):
    return discount.amount(cart)


def best_discount(cart, discounts):
    return max(discounts, key=lambda d: d.amount(cart))

# %% anna [exercise]
anna = Cart([Product("Латте", 220)] * 3 + [Product("Круассан", 140)] * 2 + [Product("Чай", 120)])
offers = [PercentDiscount(10), FixedDiscount(150), BuyNGetOne("Латте", 3)]
prices = {str(d): to_pay(anna, d) for d in offers}
best = str(best_discount(anna, offers))
# ─── заготовка ───
anna = Cart([Product("Латте", 220)] * 3 + [Product("Круассан", 140)] * 2 + [Product("Чай", 120)])
offers = [PercentDiscount(10), FixedDiscount(150), BuyNGetOne("Латте", 3)]
prices = ...
best = ...
# ─── проверка ───
def test_prices():
    "prices — к оплате по каждой акции"
    assert isinstance(prices, dict), f"prices — это {type(prices).__name__}, а нужен словарь"
    assert set(prices) == {"скидка 10 %", "минус 150 ₽", "каждый 3-й Латте в подарок"}, f"ключи prices: {list(prices)} — используйте str(акция)"
    assert prices["скидка 10 %"] != 106, "в словаре размер скидки, а нужна сумма к оплате: to_pay(anna, акция)"
    assert prices == {"скидка 10 %": 954, "минус 150 ₽": 910, "каждый 3-й Латте в подарок": 840}, f"prices = {prices}"


def test_best():
    "best — название лучшей акции"
    assert isinstance(best, str), f"best — это {type(best).__name__}, а нужно название акции строкой: str(...)"
    assert best == "каждый 3-й Латте в подарок", f"best = {best!r}, а выгоднее всего третий латте в подарок"
# ─── другое решение ───
anna = Cart([Product("Латте", 220)] * 3 + [Product("Круассан", 140)] * 2 + [Product("Чай", 120)])
offers = [PercentDiscount(10), FixedDiscount(150), BuyNGetOne("Латте", 3)]
prices = {}
for offer in offers:
    prices[offer.title] = to_pay(anna, offer)
best = min(prices, key=lambda title: prices[title])
# ─── ошибка ───
anna = Cart([Product("Латте", 220)] * 3 + [Product("Круассан", 140)] * 2 + [Product("Чай", 120)])
offers = [PercentDiscount(10), FixedDiscount(150), BuyNGetOne("Латте", 3)]
prices = {str(d): d.amount(anna) for d in offers}
best = str(best_discount(anna, offers))

# %% summary
print(f"корзина Анны без скидки: {anna.subtotal} ₽")
for offer in offers:
    print(f"{offer}: скидка {offer.amount(anna)} ₽, к оплате {to_pay(anna, offer)} ₽")
print("лучшая акция:", best)
