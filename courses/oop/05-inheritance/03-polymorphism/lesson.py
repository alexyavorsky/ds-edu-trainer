# Урок oop-polymorphism. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% delivery
class Pickup:
    name = "самовывоз"

    def cost(self, km):
        return 0


class Courier:
    name = "курьер"

    def cost(self, km):
        return 150 + 30 * km


class Partner:
    name = "служба доставки"

    def cost(self, km):
        return 290


for option in [Pickup(), Courier(), Partner()]:
    print(f"{option.name}: 3 км — {option.cost(3)} ₽, 10 км — {option.cost(10)} ₽")

# %% cheapest [exercise]
def cheapest(options, km):
    return min(options, key=lambda option: option.cost(km))
# ─── заготовка ───
def cheapest(options, km):
    ...
# ─── проверка ───
class _Taxi:
    "класс, которого функция заранее не знает"
    name = "такси"

    def cost(self, km):
        return 100 + 40 * km


def test_choice():
    "выбирает способ с наименьшей стоимостью"
    courier, partner = Courier(), Partner()
    got = cheapest([courier, partner], 3)
    assert got is not None, "функция ничего не возвращает — нужен return"
    assert not isinstance(got, (int, float)), f"функция вернула число {got!r}, а нужен сам способ доставки"
    assert got is courier, f"на 3 км дешевле курьер (240 ₽), а функция выбрала {getattr(got, 'name', got)}"
    assert cheapest([courier, partner], 10) is partner, "на 10 км дешевле служба доставки (290 ₽ против 450 ₽)"


def test_any_class():
    "работает с незнакомым классом"
    taxi, partner = _Taxi(), Partner()
    got = cheapest([partner, taxi], 2)
    assert got is taxi, "на 2 км такси (180 ₽) дешевле службы доставки — функция должна сравнивать cost(km) любых объектов, без проверок класса"
# ─── другое решение ───
def cheapest(options, km):
    best = options[0]
    for option in options:
        if option.cost(km) < best.cost(km):
            best = option
    return best
# ─── ошибка ───
def cheapest(options, km):
    return min(option.cost(km) for option in options)
# ─── ошибка ───
def cheapest(options, km):
    best = options[0]
    for option in options:
        if isinstance(option, (Courier, Partner)) and option.cost(km) < best.cost(km):
            best = option
    return best

# %% duck
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class GiftCertificate:  # не наследует от Product
    def __init__(self, amount):
        self.name = f"Сертификат на {amount} ₽"
        self.price = amount


def receipt(items):
    for item in items:
        print(f"{item.name:<24}{item.price:>6} ₽")


receipt([Product("Латте", 220), GiftCertificate(1000)])

# %% total [exercise]
def total(items):
    return sum(item.price for item in items)
# ─── заготовка ───
def total(items):
    ...
# ─── проверка ───
class _Service:
    "услуга — не товар, но с ценой"

    def __init__(self, price):
        self.price = price


def test_products():
    "сумма товаров"
    got = total([Product("Латте", 220), Product("Круассан", 140)])
    assert got is not None, "функция ничего не возвращает — нужен return"
    assert got == 360, f"total для латте и круассана = {got!r}, а нужно 360"


def test_anything():
    "сумма объектов разных классов"
    got = total([Product("Латте", 220), GiftCertificate(1000), _Service(300)])
    assert got != 220, "в сумму попал только товар — не проверяйте класс, у сертификата и услуги тоже есть price"
    assert got == 1520, f"total = {got!r}, а латте, сертификат и услуга стоят 1520"
    assert total([]) == 0, "сумма пустого списка — 0"
# ─── другое решение ───
def total(items):
    result = 0
    for item in items:
        result += item.price
    return result
# ─── ошибка ───
def total(items):
    return sum(item.price for item in items if isinstance(item, Product))

# %% channels
class SmsChannel:
    def __init__(self, phone):
        self.phone = phone

    def send(self, text):
        return f"смс на {self.phone}: {text}"


class EmailChannel:
    def __init__(self, address):
        self.address = address

    def send(self, text):
        return f"письмо на {self.address}: {text}"


def notify(channels, text):
    return [channel.send(text) for channel in channels]


sms = SmsChannel("+7 900 111-22-33")
email = EmailChannel("anna@example.com")
for line in notify([sms, email], "заказ №17 принят"):
    print(line)

# %% push [exercise]
class PushChannel:
    def __init__(self, user):
        self.user = user

    def send(self, text):
        return f"пуш для {self.user}: {text}"


sent = notify([sms, email, PushChannel("Анна")], "заказ готов")
# ─── заготовка ───
class PushChannel:
    def __init__(self, user):
        ...

    def send(self, text):
        ...


sent = ...
# ─── проверка ───
def test_channel():
    "PushChannel.send"
    try:
        push = PushChannel("Анна")
    except TypeError as e:
        assert False, f"PushChannel(\"Анна\") не создаётся: {e}"
    assert getattr(push, "user", None) == "Анна", "имя получателя хранится в атрибуте user"
    got = push.send("заказ готов")
    assert got == "пуш для Анна: заказ готов", f"send(\"заказ готов\") вернул {got!r}"


def test_sent():
    "sent — результат notify для трёх каналов"
    assert isinstance(sent, list), f"sent — это {type(sent).__name__}, а нужен список — результат notify(...)"
    assert len(sent) == 3, f"в sent {len(sent)} сообщений, а каналов три: sms, email и пуш"
    assert sent[2] == "пуш для Анна: заказ готов", f"третье сообщение: {sent[2]!r}"
    assert sent[0] == "смс на +7 900 111-22-33: заказ готов", "первым должен идти канал sms"
# ─── другое решение ───
class PushChannel:
    def __init__(self, user):
        self.user = user

    def send(self, text):
        return "пуш для " + self.user + ": " + text


channels = [sms, email]
channels.append(PushChannel("Анна"))
sent = notify(channels, "заказ готов")
# ─── ошибка ───
class PushChannel:
    def __init__(self, user):
        self.user = user

    def send(self, text):
        print(f"пуш для {self.user}: {text}")


sent = notify([sms, email, PushChannel("Анна")], "заказ готов")
# ─── ошибка ───
class PushChannel:
    def __init__(self, user):
        self.user = user

    def send(self, text):
        return f"пуш для {self.user}: {text}"


sent = notify([PushChannel("Анна")], "заказ готов")

# %% hasattr
for thing in [sms, Product("Чай", 120)]:
    print(type(thing).__name__, hasattr(thing, "send"))
