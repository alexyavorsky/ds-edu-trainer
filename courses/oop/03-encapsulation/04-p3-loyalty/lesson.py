# Урок oop-p3-loyalty. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% card [exercise]
class LoyaltyCard:
    def __init__(self, owner):
        self.owner = owner
        self._points = 0
        self._total = 0

    @property
    def points(self):
        return self._points

    @property
    def total(self):
        return self._total

    def earn(self, amount):
        if amount <= 0:
            raise ValueError("сумма покупки должна быть больше нуля")
        self._total += amount
        earned = amount * 5 // 100
        self._points += earned
        return earned
# ─── заготовка ───
class LoyaltyCard:
    def __init__(self, owner):
        ...

    @property
    def points(self):
        ...

    @property
    def total(self):
        ...

    def earn(self, amount):
        ...
# ─── проверка ───
def _card():
    try:
        return LoyaltyCard("Анна")
    except TypeError as e:
        assert False, f"LoyaltyCard(\"Анна\") не создаётся: {e}"


def test_new():
    "новая карта: владелец, 0 баллов, 0 ₽ покупок"
    for name in ["points", "total"]:
        assert isinstance(LoyaltyCard.__dict__.get(name), property), f"{name} должен быть свойством — с декоратором @property"
    card = _card()
    assert getattr(card, "owner", None) == "Анна", "владелец хранится в атрибуте owner"
    assert card.points == 0 and card.total == 0, f"у новой карты points = {card.points!r}, total = {card.total!r}, а нужно 0 и 0"


def test_read_only():
    "points и total нельзя записать снаружи"
    for name in ["points", "total"]:
        prop = LoyaltyCard.__dict__.get(name)
        assert isinstance(prop, property), f"{name} должен быть свойством"
        assert prop.fset is None, f"у свойства {name} есть сеттер — баллы и сумма меняются только через earn"


def test_earn():
    "earn начисляет 5 % с округлением вниз"
    card = _card()
    got = card.earn(1250)
    assert got is not None, "earn ничего не возвращает — верните число начисленных баллов"
    assert got != 62.5, "баллы — целые: округлите вниз целочисленным делением //"
    assert got == 62, f"earn(1250) вернул {got!r}, а 5 % от 1250 с округлением вниз — 62"
    card.earn(399)
    assert card.points == 62 + 19, f"после покупок на 1250 и 399 ₽ баллов {card.points}, а нужно 81"
    assert card.total == 1649, f"после покупок на 1250 и 399 ₽ total = {card.total}, а нужно 1649"


def test_earn_invalid():
    "сумма 0 и меньше — ValueError, карта не меняется"
    card = _card()
    card.earn(1000)
    for bad in [0, -500]:
        try:
            card.earn(bad)
        except ValueError:
            pass
        else:
            assert False, f"earn({bad}) не выбросил ValueError"
        assert (card.points, card.total) == (50, 1000), f"после earn({bad}) points = {card.points}, total = {card.total} — карта не должна меняться"
# ─── другое решение ───
class LoyaltyCard:
    RATE = 5

    def __init__(self, owner):
        self.owner = owner
        self._points = 0
        self._total = 0

    @property
    def points(self):
        return self._points

    @property
    def total(self):
        return self._total

    def earn(self, amount):
        if not amount > 0:
            raise ValueError("сумма покупки должна быть больше нуля")
        earned = int(amount * self.RATE / 100)
        self._total = self._total + amount
        self._points = self._points + earned
        return earned
# ─── ошибка ───
class LoyaltyCard:
    def __init__(self, owner):
        self.owner = owner
        self._points = 0
        self._total = 0

    @property
    def points(self):
        return self._points

    @property
    def total(self):
        return self._total

    def earn(self, amount):
        if amount <= 0:
            raise ValueError("сумма покупки должна быть больше нуля")
        self._total += amount
        earned = amount * 5 / 100
        self._points += earned
        return earned
# ─── ошибка ───
class LoyaltyCard:
    def __init__(self, owner):
        self.owner = owner
        self._points = 0
        self._total = 0

    @property
    def points(self):
        return self._points

    @property
    def total(self):
        return self._total

    def earn(self, amount):
        self._total += amount
        if amount <= 0:
            raise ValueError("сумма покупки должна быть больше нуля")
        earned = amount * 5 // 100
        self._points += earned
        return earned

# %% level [exercise]
class LoyaltyCard:
    def __init__(self, owner):
        self.owner = owner
        self._points = 0
        self._total = 0

    @property
    def points(self):
        return self._points

    @property
    def total(self):
        return self._total

    @property
    def level(self):
        if self._total < 5000:
            return "базовый"
        if self._total < 20000:
            return "серебряный"
        return "золотой"

    def earn(self, amount):
        if amount <= 0:
            raise ValueError("сумма покупки должна быть больше нуля")
        self._total += amount
        earned = amount * 5 // 100
        self._points += earned
        return earned

    def spend(self, points):
        if points <= 0:
            raise ValueError("списать можно только положительное число баллов")
        if points > self._points:
            raise ValueError("недостаточно баллов")
        self._points -= points
# ─── заготовка ───
class LoyaltyCard:
    # скопируйте сюда __init__, points, total и earn из шага 1

    @property
    def level(self):
        ...

    def spend(self, points):
        ...
# ─── проверка ───
def _card(total):
    "карта с покупкой на total ₽ (если total > 0)"
    try:
        card = LoyaltyCard("Анна")
    except TypeError:
        assert False, "LoyaltyCard(\"Анна\") не создаётся — скопируйте __init__ из шага 1"
    for name in ["earn", "points", "total"]:
        assert hasattr(LoyaltyCard, name), f"в классе нет {name} — скопируйте класс из шага 1 целиком"
    if total:
        card.earn(total)
    assert card.total == total and card.points == total * 5 // 100, "earn, points или total работают не так, как в шаге 1 — в скопированном классе ошибка из шага 1"
    return card


def test_level():
    "уровни по сумме покупок"
    assert isinstance(LoyaltyCard.__dict__.get("level"), property), "level должен быть свойством — с @property"
    for total, expected in [(0, "базовый"), (4999, "базовый"), (5000, "серебряный"), (19999, "серебряный"), (20000, "золотой")]:
        got = _card(total).level
        assert got == expected, f"при покупках на {total} ₽ уровень {got!r}, а нужно {expected!r}"


def test_spend():
    "spend списывает баллы"
    card = _card(4000)
    got = card.spend(150)
    assert card.points == 50, f"было 200 баллов, списали 150 — осталось {card.points}, а нужно 50"


def _error(card, points):
    try:
        card.spend(points)
    except ValueError as e:
        return str(e)
    return None


def test_spend_too_much():
    "больше, чем есть, — ValueError «недостаточно баллов»"
    card = _card(4000)
    text = _error(card, 500)
    assert text is not None, "spend(500) при 200 баллах не выбросил ValueError"
    assert text == "недостаточно баллов", f"сообщение {text!r}, а нужно \"недостаточно баллов\""
    assert card.points == 200, f"после неудачного списания баллов {card.points} — баланс не должен меняться"


def test_spend_not_positive():
    "0 и меньше — ValueError"
    card = _card(4000)
    for bad in [0, -50]:
        text = _error(card, bad)
        assert text is not None, f"spend({bad}) не выбросил ValueError"
        assert text == "списать можно только положительное число баллов", f"для spend({bad}) сообщение {text!r}"
        assert card.points == 200, f"после spend({bad}) баллов {card.points} — баланс не должен меняться"
# ─── другое решение ───
class LoyaltyCard:
    LEVELS = [(5000, "базовый"), (20000, "серебряный")]

    def __init__(self, owner):
        self.owner = owner
        self._points = 0
        self._total = 0

    @property
    def points(self):
        return self._points

    @property
    def total(self):
        return self._total

    @property
    def level(self):
        for limit, name in self.LEVELS:
            if self.total < limit:
                return name
        return "золотой"

    def earn(self, amount):
        if amount <= 0:
            raise ValueError("сумма покупки должна быть больше нуля")
        self._total += amount
        earned = amount * 5 // 100
        self._points += earned
        return earned

    def spend(self, points):
        if points <= 0:
            raise ValueError("списать можно только положительное число баллов")
        elif points > self.points:
            raise ValueError("недостаточно баллов")
        else:
            self._points = self._points - points
# ─── ошибка ───
class LoyaltyCard:
    def __init__(self, owner):
        self.owner = owner
        self._points = 0
        self._total = 0

    @property
    def points(self):
        return self._points

    @property
    def total(self):
        return self._total

    @property
    def level(self):
        if self._total <= 5000:
            return "базовый"
        if self._total <= 20000:
            return "серебряный"
        return "золотой"

    def earn(self, amount):
        if amount <= 0:
            raise ValueError("сумма покупки должна быть больше нуля")
        self._total += amount
        earned = amount * 5 // 100
        self._points += earned
        return earned

    def spend(self, points):
        if points <= 0:
            raise ValueError("списать можно только положительное число баллов")
        if points > self._points:
            raise ValueError("недостаточно баллов")
        self._points -= points
# ─── ошибка ───
class LoyaltyCard:
    def __init__(self, owner):
        self.owner = owner
        self._points = 0
        self._total = 0

    @property
    def points(self):
        return self._points

    @property
    def total(self):
        return self._total

    @property
    def level(self):
        if self._total < 5000:
            return "базовый"
        if self._total < 20000:
            return "серебряный"
        return "золотой"

    def earn(self, amount):
        if amount <= 0:
            raise ValueError("сумма покупки должна быть больше нуля")
        self._total += amount
        earned = amount * 5 // 100
        self._points += earned
        return earned

    def spend(self, points):
        self._points -= points
        if self._points < 0:
            raise ValueError("недостаточно баллов")

# %% history [exercise]
purchases = [1200, 3500, 800, 900]
anna = LoyaltyCard("Анна")
earned = [anna.earn(x) for x in purchases]
anna_points = anna.points
anna_level = anna.level
# ─── заготовка ───
purchases = [1200, 3500, 800, 900]
anna = ...
earned = ...
anna_points = ...
anna_level = ...
# ─── проверка ───
def test_card():
    "anna — карта Анны с её покупками"
    assert isinstance(anna, LoyaltyCard), f"anna — это {type(anna).__name__}, а нужна карта: LoyaltyCard(\"Анна\")"
    assert anna.owner == "Анна", f"владелец карты — {anna.owner!r}, а нужно \"Анна\""
    assert anna.total == 6400, f"сумма покупок на карте {anna.total}, а нужно 6400 — зарегистрируйте каждую покупку один раз"


def test_earned():
    "earned — баллы за каждую покупку"
    assert isinstance(earned, list), f"earned — это {type(earned).__name__}, а нужен список"
    assert earned == [60, 175, 40, 45], f"earned = {earned}, а нужно [60, 175, 40, 45]"


def test_summary():
    "anna_points и anna_level"
    assert anna_points == 320, f"anna_points = {anna_points!r}, а у Анны 320 баллов"
    assert anna_level == "серебряный", f"anna_level = {anna_level!r}, а при покупках на 6400 ₽ уровень серебряный"
# ─── другое решение ───
purchases = [1200, 3500, 800, 900]
anna = LoyaltyCard("Анна")
earned = []
for amount in purchases:
    earned.append(anna.earn(amount))
anna_points, anna_level = anna.points, anna.level
# ─── ошибка ───
purchases = [1200, 3500, 800, 900]
anna = LoyaltyCard("Анна")
earned = [anna.earn(x) for x in purchases]
anna.earn(sum(purchases))
anna_points = anna.points
anna_level = anna.level

# %% pay-points [exercise]
try:
    anna.spend(1000)
except ValueError as error:
    error_text = str(error)
anna.spend(100)
left = anna.points
# ─── заготовка ───
error_text = ...
left = ...
# ─── проверка ───
def test_error():
    "error_text — сообщение об ошибке"
    assert isinstance(error_text, str), f"error_text — это {type(error_text).__name__}, а нужен текст ошибки: str(error)"
    assert error_text == "недостаточно баллов", f"error_text = {error_text!r}, а spend(1000) должен сообщить «недостаточно баллов»"


def test_left():
    "left — остаток после списания 100"
    if left < 220 and (220 - left) % 100 == 0:
        assert False, f"left = {left}: списание 100 баллов повторилось — похоже, ячейка выполнена несколько раз. Нажмите «Выполнить все выше» и выполните ячейку один раз"
    assert left != 320, "остаток не изменился — после неудачной попытки спишите 100 баллов: anna.spend(100)"
    assert left == 220, f"left = {left!r}, а после списания 100 из 320 баллов осталось 220"
# ─── другое решение ───
error_text = None
try:
    anna.spend(1000)
except ValueError as e:
    error_text = e.args[0]
anna.spend(100)
left = anna.points
# ─── ошибка ───
try:
    anna.spend(1000)
except ValueError as error:
    error_text = str(error)
left = anna.points

# %% guard
try:
    anna.points = 1_000_000
except AttributeError as error:
    print("не вышло:", error)
print(anna.points)

# %% gold [exercise]
clients = {
    "Анна": [1200, 3500, 800, 900],
    "Борис": [15000, 7000],
    "Вера": [300, 450],
    "Глеб": [9000, 9000, 2500],
}
cards = {}
for name, amounts in clients.items():
    card = LoyaltyCard(name)
    for amount in amounts:
        card.earn(amount)
    cards[name] = card
gold = [name for name, card in cards.items() if card.level == "золотой"]
# ─── заготовка ───
clients = {
    "Анна": [1200, 3500, 800, 900],
    "Борис": [15000, 7000],
    "Вера": [300, 450],
    "Глеб": [9000, 9000, 2500],
}
cards = ...
gold = ...
# ─── проверка ───
def test_cards():
    "cards — карта на каждого клиента"
    assert isinstance(cards, dict), f"cards — это {type(cards).__name__}, а нужен словарь «имя → карта»"
    assert list(cards) == ["Анна", "Борис", "Вера", "Глеб"], f"ключи cards: {list(cards)}"
    assert all(isinstance(c, LoyaltyCard) for c in cards.values()), "значения cards — карты LoyaltyCard"
    totals = {name: card.total for name, card in cards.items()}
    assert totals == {"Анна": 6400, "Борис": 22000, "Вера": 750, "Глеб": 20500}, f"суммы покупок на картах: {totals} — зарегистрируйте все покупки каждого клиента"
    assert cards["Анна"] is not cards["Борис"], "у клиентов должны быть разные карты"


def test_gold():
    "gold — золотые клиенты"
    assert gold == ["Борис", "Глеб"], f"gold = {gold}, а золотой уровень — у Бориса и Глеба"
# ─── другое решение ───
clients = {
    "Анна": [1200, 3500, 800, 900],
    "Борис": [15000, 7000],
    "Вера": [300, 450],
    "Глеб": [9000, 9000, 2500],
}
cards = {name: LoyaltyCard(name) for name in clients}
for name in clients:
    for amount in clients[name]:
        cards[name].earn(amount)
gold = []
for name in cards:
    if cards[name].level == "золотой":
        gold.append(name)
# ─── ошибка ───
clients = {
    "Анна": [1200, 3500, 800, 900],
    "Борис": [15000, 7000],
    "Вера": [300, 450],
    "Глеб": [9000, 9000, 2500],
}
cards = {}
for name, amounts in clients.items():
    card = LoyaltyCard(name)
    card.earn(max(amounts))
    cards[name] = card
gold = [name for name, card in cards.items() if card.level == "золотой"]

# %% summary
for name, card in cards.items():
    print(f"{name}: {card.total} ₽, {card.points} баллов, уровень {card.level}")
