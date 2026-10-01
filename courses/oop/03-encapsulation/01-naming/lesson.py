# Урок oop-naming. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% gift-card
class GiftCard:
    def __init__(self, amount):
        self._balance = amount  # внутренний атрибут

    def balance(self):
        return self._balance

    def pay(self, amount):
        if amount > self._balance:
            return False  # денег не хватает — баланс не меняется
        self._balance -= amount
        return True


card = GiftCard(500)
print(card.pay(200), card.balance())
print(card.pay(400), card.balance())

# %% underscore
card._balance = -500  # так можно, но так не делают
print(card.balance())

# %% top-up [exercise]
class GiftCard:
    def __init__(self, amount):
        self._balance = amount

    def balance(self):
        return self._balance

    def pay(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def top_up(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
# ─── заготовка ───
class GiftCard:
    def __init__(self, amount):
        self._balance = amount

    def balance(self):
        return self._balance

    def pay(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def top_up(self, amount):
        ...
# ─── проверка ───
def test_positive():
    "top_up(300) прибавляет и возвращает True"
    card = GiftCard(500)
    got = card.top_up(300)
    assert got is True, f"top_up(300) вернул {got!r}, а нужно True"
    assert card.balance() == 800, f"после top_up(300) баланс {card.balance()}, а нужно 800"


def test_rejected():
    "ноль и отрицательные суммы не принимаются"
    card = GiftCard(500)
    for amount in [0, -200]:
        got = card.top_up(amount)
        assert got is False, f"top_up({amount}) вернул {got!r}, а такую сумму принимать нельзя — нужно False"
        assert card.balance() == 500, f"после top_up({amount}) баланс {card.balance()} — он не должен меняться"
# ─── другое решение ───
class GiftCard:
    def __init__(self, amount):
        self._balance = amount

    def balance(self):
        return self._balance

    def pay(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def top_up(self, amount):
        if amount <= 0:
            return False
        self._balance = self._balance + amount
        return True
# ─── ошибка ───
class GiftCard:
    def __init__(self, amount):
        self._balance = amount

    def balance(self):
        return self._balance

    def pay(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def top_up(self, amount):
        self._balance += amount
        return True
# ─── ошибка ───
class GiftCard:
    def __init__(self, amount):
        self._balance = amount

    def balance(self):
        return self._balance

    def pay(self, amount):
        if amount > self._balance:
            return False
        self._balance -= amount
        return True

    def top_up(self, amount):
        if amount >= 0:
            self._balance += amount
            return True
        return False

# %% purchases [exercise]
card = GiftCard(1000)
orders = [450, 300, 400, 150]
paid = [card.pay(x) for x in orders]
left = card.balance()
# ─── заготовка ───
card = GiftCard(1000)
orders = [450, 300, 400, 150]
paid = ...
left = ...
# ─── проверка ───
def test_paid():
    "paid — результаты оплат по порядку"
    assert isinstance(paid, list), f"paid — это {type(paid).__name__}, а нужен список результатов pay"
    assert paid != [True, True, True, True], "на третий заказ (400 ₽) денег уже не хватает — результаты нужно брать из pay"
    assert paid == [True, True, False, True], f"paid = {paid}, а нужно [True, True, False, True]: на 400 ₽ не хватило, а 150 ₽ прошли"


def test_left():
    "left — остаток на карте"
    assert left != 1000 - 450 - 300 - 400 - 150, "остаток посчитан вычитанием всех заказов, а третий не оплачен — возьмите card.balance()"
    assert left == 100, f"left = {left!r}, а на карте осталось 100 ₽"
# ─── другое решение ───
card = GiftCard(1000)
orders = [450, 300, 400, 150]
paid = []
for amount in orders:
    paid.append(card.pay(amount))
left = card.balance()
# ─── ошибка ───
card = GiftCard(1000)
orders = [450, 300, 400, 150]
paid = [card.pay(x) for x in orders]
left = 1000 - sum(orders)

# %% mangling
class Safe:
    def __init__(self, code):
        self.__code = code  # Python переименует в _Safe__code

    def opens_with(self, code):
        return code == self.__code  # внутри класса имя то же


safe = Safe("0000")
print(safe.__dict__)
print(safe.opens_with("0000"))
print(safe._Safe__code)

# %% mangling-error [raises=AttributeError]
safe.__code

# %% terminal [exercise]
class Terminal:
    def __init__(self, pin):
        self.__pin = pin

    def check(self, pin):
        return pin == self.__pin
# ─── заготовка ───
class Terminal:
    def __init__(self, pin):
        ...

    def check(self, pin):
        ...
# ─── проверка ───
def test_check():
    "check — True для верного кода, False для неверного"
    t = Terminal("1234")
    got = t.check("1234")
    assert got is not None, "check() ничего не возвращает — нужен return"
    assert got is True, f"check(\"1234\") вернул {got!r}, а код верный"
    assert t.check("0000") is False, "check(\"0000\") должен вернуть False — код неверный"


def test_mangled():
    "ПИН хранится в __pin"
    t = Terminal("1234")
    assert "_Terminal__pin" in t.__dict__, f"в экземпляре атрибуты {list(t.__dict__)}, а ПИН должен храниться в self.__pin — с двумя подчёркиваниями"
# ─── другое решение ───
class Terminal:
    def __init__(self, pin):
        self.__pin = str(pin)

    def check(self, pin):
        return str(pin) == self.__pin
# ─── ошибка ───
class Terminal:
    def __init__(self, pin):
        self._pin = pin

    def check(self, pin):
        return pin == self._pin
