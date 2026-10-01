# Урок oop-composition. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% delegate
class Boiler:
    def __init__(self):
        self.temperature = 20

    def heat(self, target):
        self.temperature = target
        return f"вода нагрета до {target} °C"


class CoffeeMachine:
    def __init__(self):
        self.boiler = Boiler()  # кофемашина содержит бойлер

    def brew(self, drink):
        step = self.boiler.heat(93)  # делегирует нагрев бойлеру
        return f"{step}; {drink} готов"


machine = CoffeeMachine()
print(machine.brew("американо"))
print(machine.boiler.temperature)

# %% parts
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    @property
    def subtotal(self):
        return sum(p.price for p in self.items)


cart = Cart()
cart.add(Product("Латте", 220))
print(cart.items, cart.subtotal)

# %% order [exercise]
class Order:
    def __init__(self, customer_name, cart):
        self.customer_name = customer_name
        self.cart = cart

    def add(self, product):
        self.cart.add(product)

    @property
    def total(self):
        return self.cart.subtotal
# ─── заготовка ───
class Order:
    def __init__(self, customer_name, cart):
        ...

    def add(self, product):
        ...

    @property
    def total(self):
        ...
# ─── проверка ───
def _order():
    try:
        return Order("Анна", Cart())
    except TypeError as e:
        assert False, f"Order(\"Анна\", Cart()) не создаётся: {e}"


def test_parts():
    "customer_name и cart"
    assert not issubclass(Order, Cart), "заказ не является корзиной — не наследуйте Order от Cart, храните корзину в атрибуте"
    basket = Cart()
    order = Order("Анна", basket)
    assert getattr(order, "customer_name", None) == "Анна", "имя покупателя хранится в атрибуте customer_name"
    assert getattr(order, "cart", None) is basket, "в атрибуте cart должна быть переданная корзина — тот же объект"


def test_delegates():
    "add и total работают через корзину"
    assert isinstance(Order.__dict__.get("total"), property), "total должен быть свойством — с @property"
    order = _order()
    order.add(Product("Латте", 220))
    order.add(Product("Чай", 120))
    assert len(order.cart.items) == 2, "add должен класть товар в корзину заказа: self.cart.add(product)"
    assert order.total == 340, f"total = {order.total!r}, а латте и чай стоят 340"
# ─── другое решение ───
class Order:
    def __init__(self, customer_name, cart):
        self.customer_name = customer_name
        self.cart = cart

    def add(self, product):
        return self.cart.add(product)

    @property
    def total(self):
        return sum(p.price for p in self.cart.items)
# ─── ошибка ───
class Order(Cart):
    def __init__(self, customer_name, cart):
        super().__init__()
        self.customer_name = customer_name
        self.cart = cart

    @property
    def total(self):
        return self.subtotal
# ─── ошибка ───
class Order:
    def __init__(self, customer_name, cart):
        self.customer_name = customer_name
        self.cart = cart
        self.items = []

    def add(self, product):
        self.items.append(product)

    @property
    def total(self):
        return self.cart.subtotal

# %% menu-list
class ListMenu(list):  # ошибка: меню — не список
    pass


menu = ListMenu()
menu.append(Product("Латте", 220))
menu.append("кирпич")  # и это тоже можно
print(len(menu), type(menu + []).__name__)
menu.clear()
print(menu)

# %% menu [exercise]
class Menu:
    def __init__(self):
        self._items = []

    def add(self, product):
        if not isinstance(product, Product):
            raise TypeError("в меню можно добавить только товар")
        self._items.append(product)

    def names(self):
        return [p.name for p in self._items]

    def find(self, name):
        for p in self._items:
            if p.name == name:
                return p
        return None
# ─── заготовка ───
class Menu:
    def __init__(self):
        ...

    def add(self, product):
        ...

    def names(self):
        ...

    def find(self, name):
        ...
# ─── проверка ───
def test_not_list():
    "Menu — не подкласс list"
    assert not issubclass(Menu, list), "Menu наследует от list — храните товары во внутреннем списке _items"
    assert not hasattr(Menu(), "append"), "у меню есть append — оно не должно открывать методы списка"


def test_add_names():
    "add и names"
    menu = Menu()
    assert hasattr(menu, "_items"), "товары хранятся во внутреннем списке _items — создайте его в __init__"
    menu.add(Product("Латте", 220))
    menu.add(Product("Чай", 120))
    assert menu.names() == ["Латте", "Чай"], f"names() = {menu.names()!r}"


def test_rejects():
    "не товар — TypeError"
    menu = Menu()
    try:
        menu.add("кирпич")
    except TypeError:
        pass
    except Exception as e:
        assert False, f"menu.add(\"кирпич\") выбросил {type(e).__name__}, а нужен именно TypeError — значение неверного типа"
    else:
        assert False, "menu.add(\"кирпич\") не выбросил TypeError — проверьте isinstance(product, Product)"
    assert menu.names() == [], "после отказа меню должно остаться пустым"


def test_find():
    "find — товар или None"
    menu = Menu()
    tea = Product("Чай", 120)
    menu.add(tea)
    assert menu.find("Чай") is tea, "find(\"Чай\") должен вернуть сам товар"
    assert menu.find("Какао") is None, "для товара, которого нет, find возвращает None"
# ─── другое решение ───
class Menu:
    def __init__(self, products=()):
        self._items = []
        for p in products:
            self.add(p)

    def add(self, product):
        if isinstance(product, Product):
            self._items.append(product)
        else:
            raise TypeError(f"не товар: {product!r}")

    def names(self):
        return [p.name for p in self._items]

    def find(self, name):
        matches = [p for p in self._items if p.name == name]
        return matches[0] if matches else None
# ─── ошибка ───
class Menu(list):
    def __init__(self):
        super().__init__()
        self._items = self

    def add(self, product):
        if not isinstance(product, Product):
            raise TypeError("в меню можно добавить только товар")
        self.append(product)

    def names(self):
        return [p.name for p in self]

    def find(self, name):
        for p in self:
            if p.name == name:
                return p
        return None
# ─── ошибка ───
class Menu:
    def __init__(self):
        self._items = []

    def add(self, product):
        self._items.append(product)

    def names(self):
        return [p.name for p in self._items if isinstance(p, Product)]

    def find(self, name):
        for p in self._items:
            if p.name == name:
                return p
        return None

# %% deliveries
class Pickup:
    def cost(self, km):
        return 0


class Courier:
    def cost(self, km):
        return 150 + 30 * km


print(Pickup().cost(5), Courier().cost(5))

# %% delivery-order [exercise]
class DeliveryOrder:
    def __init__(self, cart, delivery):
        self.cart = cart
        self.delivery = delivery

    def total(self, km):
        return self.cart.subtotal + self.delivery.cost(km)


cart = Cart()
cart.add(Product("Латте", 220))
order = DeliveryOrder(cart, Courier())
by_courier = order.total(5)
order.delivery = Pickup()
by_pickup = order.total(5)
# ─── заготовка ───
class DeliveryOrder:
    def __init__(self, cart, delivery):
        ...

    def total(self, km):
        ...


cart = Cart()
cart.add(Product("Латте", 220))
order = ...
by_courier = ...
by_pickup = ...
# ─── проверка ───
class _Drone:
    "доставка, которой заказ заранее не знает"

    def cost(self, km):
        return 99


def test_class():
    "total — корзина плюс доставка"
    basket = Cart()
    basket.add(Product("Раф", 260))
    try:
        got = DeliveryOrder(basket, _Drone()).total(3)
    except (TypeError, AttributeError) as e:
        assert False, f"DeliveryOrder(корзина, доставка).total(3) падает: {e}"
    assert got == 359, f"раф 260 ₽ + доставка 99 ₽ = {got!r}, а нужно 359 — берите стоимость у self.delivery.cost(km)"


def test_values():
    "by_courier и by_pickup"
    assert isinstance(order, DeliveryOrder), f"order — это {type(order).__name__}, а нужен DeliveryOrder"
    assert by_courier == 520, f"by_courier = {by_courier!r}, а корзина 220 ₽ + курьер на 5 км 300 ₽ = 520"
    assert by_pickup == 220, f"by_pickup = {by_pickup!r}, а с самовывозом остаётся сумма корзины — 220"
    assert isinstance(order.delivery, Pickup), "в конце у заказа должна быть доставка Pickup — присвойте order.delivery"
# ─── другое решение ───
class DeliveryOrder:
    def __init__(self, cart, delivery):
        self.cart = cart
        self.delivery = delivery

    def total(self, km):
        delivery_cost = self.delivery.cost(km)
        return self.cart.subtotal + delivery_cost


cart = Cart()
cart.add(Product("Латте", 220))
order = DeliveryOrder(cart, Courier())
by_courier = order.total(5)
order.delivery = Pickup()
by_pickup = order.total(5)
# ─── ошибка ───
class DeliveryOrder:
    def __init__(self, cart, delivery):
        self.cart = cart
        self.delivery = delivery

    def total(self, km):
        return self.cart.subtotal + Courier().cost(km)


cart = Cart()
cart.add(Product("Латте", 220))
order = DeliveryOrder(cart, Courier())
by_courier = order.total(5)
order.delivery = Pickup()
by_pickup = order.total(5)
