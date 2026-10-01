# Урок smp-first-class (образец платформы). Вывод демонстраций пишет scripts/validate_courses.ts --update.

# %% counter
class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def __repr__(self):
        return f"Counter(value={self.value})"


c = Counter()
c.increment()
c

# %% cup [exercise]
class Cup:
    def __init__(self, volume):
        self.volume = volume
# ─── заготовка ───
class Cup:
    def __init__(self, volume):
        ...
# ─── проверка ───
def test_volume():
    "Cup(300).volume == 300"
    assert hasattr(Cup(300), "volume"), "у чашки нет атрибута volume — сохраните объём в __init__: self.volume = volume"
    assert Cup(300).volume == 300, "объём не сохранился в атрибуте volume"
# ─── другое решение ───
class Cup:
    def __init__(self, volume: int) -> None:
        self.volume = int(volume)
# ─── ошибка ───
class Cup:
    def __init__(self, volume):
        self.size = volume

# %% cart [exercise]
class Cart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)

    def count(self):
        return len(self.items)
# ─── заготовка ───
class Cart:
    def __init__(self):
        self.items = []

    def add(self, item):
        ...

    def count(self):
        ...
# ─── проверка ───
def test_add():
    "два товара — count() == 2"
    cart = Cart()
    cart.add("латте")
    cart.add("чай")
    assert cart.count() == 2, f"count() вернул {cart.count()}"
# ─── другое решение ───
class Cart:
    def __init__(self):
        self.items = {}

    def add(self, item):
        self.items[len(self.items)] = item

    def count(self):
        return len(self.items)
# ─── ошибка ───
class Cart:
    def __init__(self):
        self.items = []

    def add(self, item):
        self.items = [item]

    def count(self):
        return len(self.items)

# %% price [exercise]
class Price:
    def __init__(self, amount):
        self.amount = amount

    @property
    def discounted(self):
        return round(self.amount * 0.9, 2)
# ─── заготовка ───
class Price:
    def __init__(self, amount):
        self.amount = amount

    @property
    def discounted(self):
        ...
# ─── проверка ───
def test_discounted():
    "Price(200).discounted == 180"
    assert isinstance(Price.__dict__.get("discounted"), property), "discounted должно быть свойством (@property), а не методом"
    assert Price(200).discounted == 180, f"получилось {Price(200).discounted}"
# ─── другое решение ───
class Price:
    def __init__(self, amount):
        self.amount = amount

    @property
    def discounted(self):
        return self.amount - self.amount / 10
# ─── ошибка ───
class Price:
    def __init__(self, amount):
        self.amount = amount

    def discounted(self):
        return self.amount * 0.9
