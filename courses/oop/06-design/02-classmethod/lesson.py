# Урок oop-classmethod. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% from-line
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.price})"

    @classmethod
    def from_line(cls, line):
        name, price = line.split(";")
        return cls(name, int(price))


print(Product.from_line("Латте;220"))
print([Product.from_line(line) for line in ["Чай;120", "Раф;260"]])

# %% drink-line [exercise]
class Drink:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.price}, {self.volume})"

    @classmethod
    def from_line(cls, line):
        name, price, volume = line.split(";")
        return cls(name, int(price), int(volume))
# ─── заготовка ───
class Drink:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.price}, {self.volume})"

    @classmethod
    def from_line(cls, line):
        ...
# ─── проверка ───
def test_is_classmethod():
    "from_line — метод класса"
    assert isinstance(Drink.__dict__.get("from_line"), classmethod), "from_line должен быть методом класса — с декоратором @classmethod"


def test_parse():
    "Drink.from_line(\"Латте;220;300\")"
    try:
        latte = Drink.from_line("Латте;220;300")
    except TypeError as e:
        assert False, f"Drink.from_line(\"Латте;220;300\") падает: {e}. Первый параметр метода класса — cls, второй — line"
    assert isinstance(latte, Drink), f"from_line вернул {type(latte).__name__}, а нужен экземпляр Drink: cls(...)"
    assert latte.name == "Латте", f"name = {latte.name!r}"
    assert latte.price == 220 and latte.volume == 300, f"price и volume = {latte.price!r} и {latte.volume!r}, а нужны числа 220 и 300 — переведите их int()"


def test_subclass():
    "подкласс получает экземпляр подкласса"
    class SeasonalDrink(Drink):
        pass
    got = SeasonalDrink.from_line("Глинтвейн;300;250")
    assert type(got) is SeasonalDrink, f"SeasonalDrink.from_line вернул {type(got).__name__} — создавайте экземпляр через cls(...), а не Drink(...)"
# ─── другое решение ───
class Drink:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.price}, {self.volume})"

    @classmethod
    def from_line(cls, line):
        parts = line.split(";")
        return cls(parts[0], int(parts[1]), int(parts[2]))
# ─── ошибка ───
class Drink:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.price}, {self.volume})"

    @classmethod
    def from_line(cls, line):
        name, price, volume = line.split(";")
        return Drink(name, int(price), int(volume))
# ─── ошибка ───
class Drink:
    def __init__(self, name, price, volume):
        self.name = name
        self.price = price
        self.volume = volume

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.price}, {self.volume})"

    @classmethod
    def from_line(cls, line):
        name, price, volume = line.split(";")
        return cls(name, price, volume)

# %% cls
class SeasonalProduct(Product):
    pass


print(SeasonalProduct.from_line("Глинтвейн;300"))
print(type(SeasonalProduct.from_line("Глинтвейн;300")).__name__)

# %% customer-dict [exercise]
class Customer:
    def __init__(self, name, phone, points=0):
        self.name = name
        self.phone = phone
        self.points = points

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"], data.get("points", 0))
# ─── заготовка ───
class Customer:
    def __init__(self, name, phone, points=0):
        self.name = name
        self.phone = phone
        self.points = points

    @classmethod
    def from_dict(cls, data):
        ...
# ─── проверка ───
def test_basic():
    "имя и телефон из словаря, баллов 0"
    assert isinstance(Customer.__dict__.get("from_dict"), classmethod), "from_dict должен быть методом класса — с @classmethod"
    anna = Customer.from_dict({"name": "Анна", "phone": "+7 900 111-22-33"})
    assert isinstance(anna, Customer), f"from_dict вернул {type(anna).__name__}, а нужен экземпляр Customer"
    assert (anna.name, anna.phone) == ("Анна", "+7 900 111-22-33"), f"name и phone = {anna.name!r}, {anna.phone!r}"
    assert anna.points == 0, f"без ключа points баллов должно быть 0, а получилось {anna.points!r}"


def test_points():
    "баллы из словаря, если есть"
    try:
        boris = Customer.from_dict({"name": "Борис", "phone": "+7 900 222-33-44", "points": 340})
    except KeyError as e:
        assert False, f"нет ключа {e} — берите необязательные значения через data.get(…)"
    assert boris.points == 340, f"баллы из словаря — 340, а получилось {boris.points!r}"
# ─── другое решение ───
class Customer:
    def __init__(self, name, phone, points=0):
        self.name = name
        self.phone = phone
        self.points = points

    @classmethod
    def from_dict(cls, data):
        customer = cls(data["name"], data["phone"])
        if "points" in data:
            customer.points = data["points"]
        return customer
# ─── ошибка ───
class Customer:
    def __init__(self, name, phone, points=0):
        self.name = name
        self.phone = phone
        self.points = points

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"])

# %% static
class PriceTag:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @staticmethod
    def parse_price(text):  # ни self, ни cls
        return int(text.replace("₽", "").strip())

    @classmethod
    def from_text(cls, name, text):
        return cls(name, cls.parse_price(text))


print(PriceTag.parse_price("220 ₽"))
print(PriceTag.from_text("Латте", "240 ₽").price)

# %% phone [exercise]
class Customer:
    def __init__(self, name, phone, points=0):
        self.name = name
        self.phone = phone
        self.points = points

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"], data.get("points", 0))

    @staticmethod
    def normalize_phone(phone):
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) != 11:
            raise ValueError("в номере телефона должно быть 11 цифр")
        return digits
# ─── заготовка ───
class Customer:
    # скопируйте сюда __init__ и from_dict из упражнения выше

    @staticmethod
    def normalize_phone(phone):
        ...
# ─── проверка ───
def test_copied():
    "from_dict на месте"
    assert isinstance(Customer.__dict__.get("from_dict"), classmethod), "в классе нет from_dict — скопируйте класс из упражнения выше"
    anna = Customer.from_dict({"name": "Анна", "phone": "1"})
    assert anna.points == 0, "from_dict работает не так, как в упражнении выше — проверьте скопированный код"


def test_static():
    "normalize_phone — статический метод"
    assert isinstance(Customer.__dict__.get("normalize_phone"), staticmethod), "normalize_phone должен быть статическим — с @staticmethod"


def _call(phone):
    try:
        return Customer.normalize_phone(phone)
    except TypeError:
        assert False, "normalize_phone не вызывается с одним аргументом — у статического метода нет self, уберите его из параметров"


def test_digits():
    "оставляет 11 цифр"
    got = _call("+7 (900) 111-22-33")
    assert got is not None, "normalize_phone ничего не возвращает — нужен return"
    assert got == "79001112233", f"normalize_phone(\"+7 (900) 111-22-33\") = {got!r}, а нужно \"79001112233\""


def test_invalid():
    "не 11 цифр — ValueError"
    for bad in ["123-45", "+7 900 111-22-33-44"]:
        try:
            _call(bad)
        except ValueError:
            continue
        assert False, f"normalize_phone({bad!r}) не выбросил ValueError — в номере не 11 цифр"
# ─── другое решение ───
class Customer:
    def __init__(self, name, phone, points=0):
        self.name = name
        self.phone = phone
        self.points = points

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"], data.get("points", 0))

    @staticmethod
    def normalize_phone(phone):
        digits = ""
        for ch in phone:
            if ch in "0123456789":
                digits += ch
        if len(digits) == 11:
            return digits
        raise ValueError("в номере телефона должно быть 11 цифр")
# ─── ошибка ───
class Customer:
    def __init__(self, name, phone, points=0):
        self.name = name
        self.phone = phone
        self.points = points

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"], data.get("points", 0))

    @staticmethod
    def normalize_phone(phone):
        return "".join(ch for ch in phone if ch.isdigit())
# ─── ошибка ───
class Customer:
    def __init__(self, name, phone, points=0):
        self.name = name
        self.phone = phone
        self.points = points

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"], data.get("points", 0))

    @staticmethod
    def normalize_phone(self, phone):
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) != 11:
            raise ValueError("в номере телефона должно быть 11 цифр")
        return digits
