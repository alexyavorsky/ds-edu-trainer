# Урок oop-operators. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% add
class Weight:
    def __init__(self, grams):
        self.grams = grams

    def __repr__(self):
        return f"Weight({self.grams})"

    def __add__(self, other):
        if not isinstance(other, Weight):
            return NotImplemented
        return Weight(self.grams + other.grams)  # новый объект


a = Weight(250)
b = Weight(100)
print(a + b, a, b)
print(a + b + Weight(50))

# %% mutating
class BadWeight:
    def __init__(self, grams):
        self.grams = grams

    def __repr__(self):
        return f"BadWeight({self.grams})"

    def __add__(self, other):
        self.grams += other.grams  # ошибка: меняет левое слагаемое
        return self


bag = BadWeight(250)
total = bag + BadWeight(100)
print(total, bag, total is bag)

# %% sum-error [raises=TypeError]
sum([Weight(250), Weight(100)])

# %% money [exercise]
class Money:
    def __init__(self, rubles):
        self.rubles = rubles

    def __repr__(self):
        return f"Money({self.rubles})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.rubles == other.rubles

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.rubles + other.rubles)

    def __radd__(self, other):
        if other == 0:
            return self
        return self.__add__(other)
# ─── заготовка ───
class Money:
    def __init__(self, rubles):
        self.rubles = rubles

    def __repr__(self):
        return f"Money({self.rubles})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.rubles == other.rubles

    def __add__(self, other):
        ...

    def __radd__(self, other):
        ...
# ─── проверка ───
def test_add():
    "Money + Money — новый Money"
    a, b = Money(220), Money(140)
    got = a + b
    assert isinstance(got, Money), f"Money(220) + Money(140) дал {got!r}, а нужен экземпляр Money"
    assert got == Money(360), f"Money(220) + Money(140) = {got!r}, а нужно Money(360)"
    assert a.rubles == 220 and b.rubles == 140, "сложение изменило слагаемые — создавайте новый Money, а не меняйте self"
    assert got is not a, "сложение вернуло левое слагаемое — нужен новый объект"


def test_foreign():
    "чужой тип — NotImplemented"
    try:
        got = Money.__dict__["__add__"](Money(220), 5)
    except AttributeError:
        assert False, "сложение с числом падает — сначала проверьте тип: isinstance(other, Money)"
    assert got is NotImplemented, f"Money.__add__ с числом вернул {got!r}, а нужно NotImplemented"


def test_sum():
    "sum работает"
    try:
        got = sum([Money(220), Money(140), Money(90)])
    except TypeError as e:
        assert False, f"sum по списку Money падает: {e}. Нужен __radd__: 0 + Money — вернуть self"
    assert got == Money(450), f"sum = {got!r}, а нужно Money(450)"
# ─── другое решение ───
class Money:
    def __init__(self, rubles):
        self.rubles = rubles

    def __repr__(self):
        return f"Money({self.rubles})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.rubles == other.rubles

    def __add__(self, other):
        if isinstance(other, Money):
            return Money(self.rubles + other.rubles)
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, int) and other == 0:
            return Money(self.rubles)
        return NotImplemented
# ─── ошибка ───
class Money:
    def __init__(self, rubles):
        self.rubles = rubles

    def __repr__(self):
        return f"Money({self.rubles})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.rubles == other.rubles

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self.rubles += other.rubles
        return self

    def __radd__(self, other):
        if other == 0:
            return self
        return self.__add__(other)
# ─── ошибка ───
class Money:
    def __init__(self, rubles):
        self.rubles = rubles

    def __repr__(self):
        return f"Money({self.rubles})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.rubles == other.rubles

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return Money(self.rubles + other.rubles)

    def __radd__(self, other):
        return self.__add__(other)

# %% grams [exercise]
class Grams:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Grams({self.value})"

    def __eq__(self, other):
        if not isinstance(other, Grams):
            return NotImplemented
        return self.value == other.value

    def __mul__(self, number):
        if not isinstance(number, int):
            return NotImplemented
        return Grams(self.value * number)

    def __rmul__(self, number):
        return self.__mul__(number)
# ─── заготовка ───
class Grams:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Grams({self.value})"

    def __eq__(self, other):
        if not isinstance(other, Grams):
            return NotImplemented
        return self.value == other.value

    def __mul__(self, number):
        ...

    def __rmul__(self, number):
        ...
# ─── проверка ───
def test_mul():
    "Grams(18) * 3"
    portion = Grams(18)
    got = portion * 3
    assert got == Grams(54), f"Grams(18) * 3 = {got!r}, а нужно Grams(54)"
    assert portion.value == 18, "умножение изменило исходный вес — возвращайте новый Grams"


def test_rmul():
    "3 * Grams(18)"
    try:
        got = 3 * Grams(18)
    except TypeError as e:
        assert False, f"3 * Grams(18) падает: {e}. Нужен __rmul__"
    assert got == Grams(54), f"3 * Grams(18) = {got!r}, а нужно Grams(54)"


def test_foreign():
    "не int — NotImplemented"
    got = Grams.__dict__["__mul__"](Grams(18), "3")
    assert got is NotImplemented, f"Grams(18) * \"3\" вернул {got!r}, а для не-int нужно NotImplemented"
# ─── другое решение ───
class Grams:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Grams({self.value})"

    def __eq__(self, other):
        if not isinstance(other, Grams):
            return NotImplemented
        return self.value == other.value

    def __mul__(self, number):
        if isinstance(number, int):
            return Grams(number * self.value)
        return NotImplemented

    __rmul__ = __mul__
# ─── ошибка ───
class Grams:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Grams({self.value})"

    def __eq__(self, other):
        if not isinstance(other, Grams):
            return NotImplemented
        return self.value == other.value

    def __mul__(self, number):
        if not isinstance(number, int):
            return NotImplemented
        return Grams(self.value * number)
# ─── ошибка ───
class Grams:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Grams({self.value})"

    def __eq__(self, other):
        if not isinstance(other, Grams):
            return NotImplemented
        return self.value == other.value

    def __mul__(self, number):
        return self.value * number

    def __rmul__(self, number):
        return self.__mul__(number)

# %% rmul-quiz [quiz]
class OnlyMul:
    def __mul__(self, number):
        return number


try:
    3 * OnlyMul()
except TypeError:
    print("TypeError")

# %% shift [exercise]
checks = [Money(640), Money(1250), Money(380), Money(910)]
cups = 120
revenue = sum(checks)
beans = Grams(18) * cups
# ─── заготовка ───
checks = [Money(640), Money(1250), Money(380), Money(910)]
cups = 120
revenue = ...
beans = ...
# ─── проверка ───
def test_revenue():
    "revenue — Money с суммой чеков"
    assert isinstance(revenue, Money), f"revenue — это {type(revenue).__name__}, а нужен Money: sum(checks)"
    assert revenue == Money(3180), f"revenue = {revenue!r}, а сумма чеков — Money(3180)"


def test_beans():
    "beans — Grams на все чашки"
    assert isinstance(beans, Grams), f"beans — это {type(beans).__name__}, а нужен Grams: Grams(18) * cups"
    assert beans == Grams(2160), f"beans = {beans!r}, а на 120 чашек нужно Grams(2160)"
# ─── другое решение ───
checks = [Money(640), Money(1250), Money(380), Money(910)]
cups = 120
revenue = Money(0)
for check in checks:
    revenue = revenue + check
beans = cups * Grams(18)
# ─── ошибка ───
checks = [Money(640), Money(1250), Money(380), Money(910)]
cups = 120
revenue = sum(c.rubles for c in checks)
beans = Grams(18) * cups
