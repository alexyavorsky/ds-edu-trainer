# Урок oop-inheritance. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% inherit
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.price})"

    def label(self):
        return f"{self.name} — {self.price} ₽"


class Snack(Product):
    pass


cookie = Snack("Овсяное печенье", 90)
print(cookie.label())
print(cookie)

# %% override
class Tea(Product):
    def brew_minutes(self):  # новый метод
        return 4

    def label(self):  # своя версия метода базового класса
        return f"{self.name} — {self.price} ₽, заваривать {self.brew_minutes()} мин"


print(Tea("Улун", 180).label())
print(Product("Улун", 180).label())

# %% seasonal [exercise]
class SeasonalProduct(Product):
    def label(self):
        return f"{self.name} — {self.price} ₽ (сезонное)"
# ─── заготовка ───
class SeasonalProduct:  # укажите базовый класс
    def label(self):
        ...
# ─── проверка ───
def test_subclass():
    "SeasonalProduct — подкласс Product"
    assert isinstance(SeasonalProduct, type), "SeasonalProduct должен быть классом"
    assert issubclass(SeasonalProduct, Product), "SeasonalProduct не наследует от Product — укажите базовый класс в скобках: class SeasonalProduct(Product):"


def test_label():
    "label — с пометкой «сезонное»"
    assert issubclass(SeasonalProduct, Product), "сначала укажите базовый класс Product"
    try:
        item = SeasonalProduct("Тыквенный латте", 290)
    except TypeError as e:
        assert False, f"SeasonalProduct(\"Тыквенный латте\", 290) не создаётся: {e}. Свой __init__ не нужен — он наследуется"
    got = item.label()
    assert got == "Тыквенный латте — 290 ₽ (сезонное)", f"label() вернул {got!r}, а нужно \"Тыквенный латте — 290 ₽ (сезонное)\""


def test_base_unchanged():
    "у обычного товара label прежний"
    got = Product("Латте", 220).label()
    assert got == "Латте — 220 ₽", f"у Product label() стал {got!r} — меняйте метод только в подклассе"
# ─── другое решение ───
class SeasonalProduct(Product):
    MARK = "(сезонное)"

    def label(self):
        return self.name + " — " + str(self.price) + " ₽ " + self.MARK
# ─── ошибка ───
class SeasonalProduct:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def label(self):
        return f"{self.name} — {self.price} ₽ (сезонное)"
# ─── ошибка ───
class SeasonalProduct(Product):
    def label(self):
        return f"{self.name} (сезонное)"

# %% pastry [exercise]
class Pastry(Product):
    def combo_price(self, drink):
        return round((self.price + drink.price) * 90 / 100)
# ─── заготовка ───
class Pastry(Product):
    def combo_price(self, drink):
        ...
# ─── проверка ───
def test_combo():
    "комплект со скидкой 10 %"
    croissant = Pastry("Круассан", 140)
    got = croissant.combo_price(Product("Латте", 220))
    assert got is not None, "combo_price ничего не возвращает — нужен return"
    assert got != 360, "360 — сумма без скидки, а комплект дешевле на 10 %"
    assert got != 36, "36 — это сама скидка, а нужна цена комплекта"
    assert got == 324, f"круассан + латте = {got!r}, а со скидкой 10 % нужно 324"


def test_round():
    "цена округляется до целых"
    got = Pastry("Маффин", 133).combo_price(Product("Чай", 120))
    assert got == 228, f"маффин за 133 + чай за 120 = {got!r}, а нужно 228 (227.7 после скидки, округлите)"


def test_inherits():
    "Pastry — товар с label"
    assert issubclass(Pastry, Product), "Pastry должен наследовать от Product"
    assert Pastry("Круассан", 140).label() == "Круассан — 140 ₽", "label у выпечки должен остаться от Product"
# ─── другое решение ───
class Pastry(Product):
    COMBO_DISCOUNT = 10

    def combo_price(self, drink):
        total = self.price + drink.price
        return round(total - total * self.COMBO_DISCOUNT / 100)
# ─── ошибка ───
class Pastry(Product):
    def combo_price(self, drink):
        return round((self.price + drink.price) * 10 / 100)
# ─── ошибка ───
class Pastry(Product):
    def combo_price(self, drink):
        return (self.price + drink.price) * 90 / 100

# %% isinstance
croissant = Pastry("Круассан", 140)
print(isinstance(croissant, Pastry), isinstance(croissant, Product))
print(isinstance(Product("Чай", 120), Pastry))
print(issubclass(Pastry, Product), issubclass(SeasonalProduct, Pastry))
print(issubclass(bool, int))

# %% wrong-order
def shelf_of(item):
    if isinstance(item, Product):  # ошибка: базовый класс первым
        return "общая полка"
    elif isinstance(item, Pastry):
        return "витрина с выпечкой"
    return "?"


for item in [Product("Чай", 120), Pastry("Круассан", 140)]:
    print(item.name, "→", shelf_of(item))

# %% kind [exercise]
def kind_of(item):
    if isinstance(item, SeasonalProduct):
        return "сезонное"
    if isinstance(item, Pastry):
        return "выпечка"
    return "товар"
# ─── заготовка ───
def kind_of(item):
    ...
# ─── проверка ───
def test_kinds():
    "сезонное, выпечка и обычный товар"
    got = [kind_of(SeasonalProduct("Глинтвейн", 300)), kind_of(Pastry("Круассан", 140)), kind_of(Product("Чай", 120))]
    assert got != ["товар", "товар", "товар"], "для всех вернулось «товар» — проверка isinstance(item, Product) стоит раньше проверок подклассов"
    assert got == ["сезонное", "выпечка", "товар"], f"kind_of вернула {got}, а нужно ['сезонное', 'выпечка', 'товар']"
# ─── другое решение ───
def kind_of(item):
    kinds = [(SeasonalProduct, "сезонное"), (Pastry, "выпечка"), (Product, "товар")]
    for cls, name in kinds:
        if isinstance(item, cls):
            return name
# ─── ошибка ───
def kind_of(item):
    if isinstance(item, Product):
        return "товар"
    if isinstance(item, SeasonalProduct):
        return "сезонное"
    if isinstance(item, Pastry):
        return "выпечка"

# %% subclass-quiz [quiz]
print(issubclass(Product, Pastry))
