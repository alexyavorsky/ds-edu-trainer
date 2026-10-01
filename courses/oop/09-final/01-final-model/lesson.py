# Урок oop-final-model. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% errors [exercise]
class ShopError(Exception):
    pass


class UnknownProductError(ShopError):
    pass
# ─── заготовка ───
# объявите ShopError и UnknownProductError
# ─── проверка ───
def test_hierarchy():
    "ShopError → UnknownProductError"
    shop, unknown = globals().get("ShopError"), globals().get("UnknownProductError")
    assert isinstance(shop, type) and isinstance(unknown, type), "объявите оба класса: ShopError и UnknownProductError"
    assert issubclass(shop, Exception), "ShopError должен наследовать от Exception"
    assert issubclass(unknown, shop), "UnknownProductError должен наследовать от ShopError"
# ─── другое решение ───
class ShopError(Exception):
    """Ошибка кассы."""


class UnknownProductError(ShopError):
    """Товара нет в каталоге."""
# ─── ошибка ───
class ShopError(Exception):
    pass


class UnknownProductError(KeyError):
    pass

# %% product [exercise]
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Product:
    name: str
    price: int
    category: str

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError(f"цена должна быть больше нуля: {self.name}")

    def __str__(self):
        return f"{self.name} — {self.price} ₽"
# ─── заготовка ───
from dataclasses import dataclass, field


class Product:
    ...
# ─── проверка ───
from dataclasses import fields, is_dataclass


def test_fields():
    "frozen dataclass с тремя полями"
    assert is_dataclass(Product), "Product — не dataclass"
    assert [f.name for f in fields(Product)] == ["name", "price", "category"], f"поля: {[f.name for f in fields(Product)]}"
    latte = Product("Латте", 240, "кофе")
    try:
        latte.price = 1
    except AttributeError:
        pass
    else:
        assert False, "цену удалось изменить — нужен @dataclass(frozen=True)"
    assert len({latte, Product("Латте", 240, "кофе")}) == 1, "одинаковые товары должны быть равны и хешироваться одинаково"


def test_check_and_str():
    "цена > 0 и str"
    try:
        Product("Чай", 0, "чай")
    except ValueError:
        pass
    else:
        assert False, "Product(\"Чай\", 0, \"чай\") создался — нужен ValueError в __post_init__"
    assert str(Product("Латте", 240, "кофе")) == "Латте — 240 ₽", f"str = {str(Product('Латте', 240, 'кофе'))!r}"
# ─── другое решение ───
import dataclasses


@dataclasses.dataclass(frozen=True)
class Product:
    name: str
    price: int
    category: str = "кофе"

    def __post_init__(self):
        if not self.price > 0:
            raise ValueError("цена должна быть больше нуля")

    def __str__(self):
        return self.name + " — " + str(self.price) + " ₽"
# ─── ошибка ───
from dataclasses import dataclass, field


@dataclass
class Product:
    name: str
    price: int
    category: str

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError(f"цена должна быть больше нуля: {self.name}")

    def __str__(self):
        return f"{self.name} — {self.price} ₽"

# %% catalog [exercise]
class Catalog:
    def __init__(self, products):
        self._products = {p.name: p for p in products}

    def __len__(self):
        return len(self._products)

    def __contains__(self, name):
        return name in self._products

    def __getitem__(self, name):
        if name not in self._products:
            raise UnknownProductError(f"нет в каталоге: {name}")
        return self._products[name]

    def __iter__(self):
        for name in sorted(self._products):
            yield self._products[name]
# ─── заготовка ───
class Catalog:
    def __init__(self, products):
        ...

    def __len__(self):
        ...

    def __contains__(self, name):
        ...

    def __getitem__(self, name):
        ...

    def __iter__(self):
        ...
# ─── проверка ───
def _catalog():
    return Catalog([Product("Раф", 260, "кофе"), Product("Чай", 120, "чай"), Product("Латте", 240, "кофе")])


def test_len_in():
    "len и in"
    c = _catalog()
    assert len(c) == 3, f"len(catalog) = {len(c)}, а товаров 3"
    assert ("Латте" in c) is True and ("Какао" in c) is False, "in проверяет, есть ли товар с таким названием"


def test_getitem():
    "товар по названию и UnknownProductError"
    c = _catalog()
    got = c["Чай"]
    assert isinstance(got, Product) and got.name == "Чай", f"catalog[\"Чай\"] = {got!r}"
    try:
        c["Какао"]
    except UnknownProductError as e:
        assert str(e) == "нет в каталоге: Какао", f"сообщение {str(e)!r}"
    except KeyError:
        assert False, "выброшен KeyError, а нужен UnknownProductError — проверьте название до обращения к словарю"
    else:
        assert False, "catalog[\"Какао\"] не выбросил UnknownProductError"


def test_iter():
    "товары по алфавиту"
    names = [p.name for p in _catalog()]
    assert names == ["Латте", "Раф", "Чай"], f"цикл по каталогу дал {names}, а нужно по алфавиту"
# ─── другое решение ───
class Catalog:
    def __init__(self, products):
        self._products = {}
        for p in products:
            self._products[p.name] = p

    def __len__(self):
        return len(self._products)

    def __contains__(self, name):
        return name in self._products

    def __getitem__(self, name):
        try:
            return self._products[name]
        except KeyError:
            raise UnknownProductError("нет в каталоге: " + name) from None

    def __iter__(self):
        return iter(sorted(self._products.values(), key=lambda p: p.name))
# ─── ошибка ───
class Catalog:
    def __init__(self, products):
        self._products = {p.name: p for p in products}

    def __len__(self):
        return len(self._products)

    def __contains__(self, name):
        return name in self._products

    def __getitem__(self, name):
        return self._products[name]

    def __iter__(self):
        for name in sorted(self._products):
            yield self._products[name]
# ─── ошибка ───
class Catalog:
    def __init__(self, products):
        self._products = {p.name: p for p in products}

    def __len__(self):
        return len(self._products)

    def __contains__(self, name):
        return name in self._products

    def __getitem__(self, name):
        if name not in self._products:
            raise UnknownProductError(f"нет в каталоге: {name}")
        return self._products[name]

    def __iter__(self):
        for product in self._products.values():
            yield product

# %% load [exercise]
def load_catalog(lines):
    products = []
    for line in lines:
        name, price, category = line.split(";")
        products.append(Product(name, int(price), category))
    return Catalog(products)


menu_lines = [
    "Эспрессо;150;кофе", "Капучино;220;кофе", "Латте;240;кофе", "Раф;260;кофе",
    "Чай;120;чай", "Какао;190;другое", "Круассан;140;выпечка", "Маффин;130;выпечка",
]
catalog = load_catalog(menu_lines)
# ─── заготовка ───
def load_catalog(lines):
    ...


menu_lines = [
    "Эспрессо;150;кофе", "Капучино;220;кофе", "Латте;240;кофе", "Раф;260;кофе",
    "Чай;120;чай", "Какао;190;другое", "Круассан;140;выпечка", "Маффин;130;выпечка",
]
catalog = ...
# ─── проверка ───
def test_function():
    "load_catalog собирает Catalog"
    got = load_catalog(["Чай;120;чай"])
    assert isinstance(got, Catalog), f"load_catalog вернула {type(got).__name__}, а нужен Catalog"
    tea = got["Чай"]
    assert tea == Product("Чай", 120, "чай"), f"из строки \"Чай;120;чай\" получилось {tea!r} — цену переведите int()"


def test_catalog():
    "catalog — меню кофейни"
    assert isinstance(catalog, Catalog), f"catalog — это {type(catalog).__name__}, а нужен Catalog: load_catalog(menu_lines)"
    assert len(catalog) == 8, f"в каталоге {len(catalog)} товаров, а строк меню 8"
    assert catalog["Маффин"].category == "выпечка", "категория маффина — выпечка"
# ─── другое решение ───
def load_catalog(lines):
    def parse(line):
        name, price, category = line.split(";")
        return Product(name, int(price), category)
    return Catalog([parse(line) for line in lines])


menu_lines = [
    "Эспрессо;150;кофе", "Капучино;220;кофе", "Латте;240;кофе", "Раф;260;кофе",
    "Чай;120;чай", "Какао;190;другое", "Круассан;140;выпечка", "Маффин;130;выпечка",
]
catalog = load_catalog(menu_lines)
# ─── ошибка ───
def load_catalog(lines):
    products = []
    for line in lines:
        name, price, category = line.split(";")
        products.append(Product(name, int(price), category))
    return products


menu_lines = [
    "Эспрессо;150;кофе", "Капучино;220;кофе", "Латте;240;кофе", "Раф;260;кофе",
    "Чай;120;чай", "Какао;190;другое", "Круассан;140;выпечка", "Маффин;130;выпечка",
]
catalog = load_catalog(menu_lines)

# %% look
for product in catalog:
    print(f"{product} ({product.category})")

# %% line
from dataclasses import dataclass


@dataclass
class Line:
    product: Product
    qty: int

    @property
    def cost(self):
        return self.product.price * self.qty


print(Line(catalog["Латте"], 2), Line(catalog["Латте"], 2).cost)

# %% cart [exercise]
class Cart:
    def __init__(self, catalog):
        self.catalog = catalog
        self._lines = []

    def add(self, name, qty=1):
        product = self.catalog[name]
        for line in self._lines:
            if line.product == product:
                line.qty += qty
                return
        self._lines.append(Line(product, qty))

    def __len__(self):
        return len(self._lines)

    def __iter__(self):
        for line in self._lines:
            yield line

    @property
    def subtotal(self):
        return sum(line.cost for line in self._lines)
# ─── заготовка ───
class Cart:
    def __init__(self, catalog):
        ...

    def add(self, name, qty=1):
        ...

    def __len__(self):
        ...

    def __iter__(self):
        ...

    @property
    def subtotal(self):
        ...
# ─── проверка ───
def _cart():
    return Cart(Catalog([Product("Латте", 240, "кофе"), Product("Круассан", 140, "выпечка")]))


def test_add():
    "add и subtotal"
    cart = _cart()
    assert len(cart) == 0 and cart.subtotal == 0, "новая корзина пустая, subtotal = 0"
    cart.add("Латте", 2)
    cart.add("Круассан")
    assert len(cart) == 2, f"в корзине {len(cart)} строк, а нужно 2"
    assert cart.subtotal == 620, f"subtotal = {cart.subtotal!r}, а два латте и круассан стоят 620"


def test_merge():
    "тот же товар — одна строка"
    cart = _cart()
    cart.add("Латте", 2)
    cart.add("Латте")
    lines = list(cart)
    assert len(lines) == 1, f"после двух add(\"Латте\") в корзине {len(lines)} строки — увеличьте количество существующей строки"
    assert lines[0].qty == 3, f"у латте qty = {lines[0].qty}, а нужно 3"


def test_unknown():
    "неизвестный товар — UnknownProductError"
    cart = _cart()
    try:
        cart.add("Глинтвейн")
    except UnknownProductError:
        pass
    else:
        assert False, "cart.add(\"Глинтвейн\") не выбросил UnknownProductError — товар берётся из каталога: self.catalog[name]"
    assert len(cart) == 0, "после ошибки корзина не должна меняться"
# ─── другое решение ───
class Cart:
    def __init__(self, catalog):
        self.catalog = catalog
        self._lines = {}

    def add(self, name, qty=1):
        product = self.catalog[name]
        if name in self._lines:
            self._lines[name].qty += qty
        else:
            self._lines[name] = Line(product, qty)

    def __len__(self):
        return len(self._lines)

    def __iter__(self):
        return iter(list(self._lines.values()))

    @property
    def subtotal(self):
        return sum(line.cost for line in self)
# ─── ошибка ───
class Cart:
    def __init__(self, catalog):
        self.catalog = catalog
        self._lines = []

    def add(self, name, qty=1):
        self._lines.append(Line(self.catalog[name], qty))

    def __len__(self):
        return len(self._lines)

    def __iter__(self):
        for line in self._lines:
            yield line

    @property
    def subtotal(self):
        return sum(line.cost for line in self._lines)

# %% orders [exercise]
requests = [
    [("Латте", 2), ("Круассан", 2), ("Латте", 1)],
    [("Капучино", 1), ("Глинтвейн", 1), ("Чай", 2), ("Маффин", 1)],
    [("Раф", 1), ("Какао", 1)],
]
subtotals = []
unknown = []
for request in requests:
    cart = Cart(catalog)
    for name, qty in request:
        try:
            cart.add(name, qty)
        except UnknownProductError:
            unknown.append(name)
    subtotals.append(cart.subtotal)
# ─── заготовка ───
requests = [
    [("Латте", 2), ("Круассан", 2), ("Латте", 1)],
    [("Капучино", 1), ("Глинтвейн", 1), ("Чай", 2), ("Маффин", 1)],
    [("Раф", 1), ("Какао", 1)],
]
subtotals = ...
unknown = ...
# ─── проверка ───
def test_subtotals():
    "суммы корзин"
    assert isinstance(subtotals, list), f"subtotals — это {type(subtotals).__name__}, а нужен список сумм"
    assert len(subtotals) == 3, f"в subtotals {len(subtotals)} сумм, а покупателей 3 — пропускайте позицию, а не весь заказ"
    assert subtotals == [1000, 590, 450], f"subtotals = {subtotals}, а нужно [1000, 590, 450]"


def test_unknown():
    "unknown — чего нет в каталоге"
    assert unknown == ["Глинтвейн"], f"unknown = {unknown}"
# ─── другое решение ───
requests = [
    [("Латте", 2), ("Круассан", 2), ("Латте", 1)],
    [("Капучино", 1), ("Глинтвейн", 1), ("Чай", 2), ("Маффин", 1)],
    [("Раф", 1), ("Какао", 1)],
]
subtotals, unknown = [], []
for request in requests:
    cart = Cart(catalog)
    for name, qty in request:
        if name in catalog:
            cart.add(name, qty)
        else:
            unknown.append(name)
    subtotals.append(cart.subtotal)
# ─── ошибка ───
requests = [
    [("Латте", 2), ("Круассан", 2), ("Латте", 1)],
    [("Капучино", 1), ("Глинтвейн", 1), ("Чай", 2), ("Маффин", 1)],
    [("Раф", 1), ("Какао", 1)],
]
subtotals = []
unknown = []
for request in requests:
    cart = Cart(catalog)
    try:
        for name, qty in request:
            cart.add(name, qty)
    except UnknownProductError:
        unknown.append(name)
    subtotals.append(cart.subtotal)

# %% summary
print(f"в каталоге {len(catalog)} товаров")
for i, total in enumerate(subtotals, 1):
    print(f"корзина {i}: {total} ₽")
print("нет в каталоге:", ", ".join(unknown))
