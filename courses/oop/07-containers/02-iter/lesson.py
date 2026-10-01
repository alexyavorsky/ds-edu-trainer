# Урок oop-iter. Ячейки по порядку урока (формат — docs/COURSES_PLAN.md).
# Вывод демонстраций пишет scripts/validate_courses.ts --update в output.json — руками не править.

# %% yield
def countdown(n):
    while n > 0:
        yield n  # выдать значение и замереть до следующего шага
        n -= 1


for x in countdown(3):
    print(x)
print(list(countdown(5)))

# %% iter
class Shift:
    def __init__(self, barista, hours):
        self.barista = barista
        self._hours = list(hours)

    def __iter__(self):
        return iter(self._hours)  # новый итератор по списку часов


morning = Shift("Анна", ["08:00", "09:00", "10:00"])
for hour in morning:
    print(morning.barista, hour)
print(list(morning), len(list(morning)))

# %% menu-iter [exercise]
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __iter__(self):
        for p in self._items:
            yield p
# ─── заготовка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __iter__(self):
        ...
# ─── проверка ───
def _menu():
    return Menu([Product("Латте", 220), Product("Чай", 120), Product("Раф", 260)])


def test_for():
    "for перебирает товары по порядку"
    try:
        names = [p.name for p in _menu()]
    except TypeError as e:
        if "list" in str(e):
            assert False, "__iter__ вернул список — список итерируемый, но не итератор: верните iter(self._items) или выдавайте товары через yield"
        assert False, f"меню не перебирается циклом: {e}. __iter__ должен выдавать товары через yield"
    except AttributeError:
        assert False, "цикл по меню выдал не товары, а весь список сразу — выдавайте товары по одному: yield p внутри цикла"
    assert names == ["Латте", "Чай", "Раф"], f"цикл по меню дал {names}"


def test_twice():
    "меню можно пройти дважды"
    menu = _menu()
    try:
        first, second = list(menu), list(menu)
    except TypeError:
        assert False, "меню не перебирается циклом — сначала исправьте __iter__ (проверка выше)"
    assert len(first) == 3, f"проход по меню выдал {len(first)} шт., а товаров 3 — выдавайте каждый товар через yield p, а не весь список"
    assert len(second) == 3, "второй проход по меню пуст — __iter__ должен каждый раз начинать заново"
    assert first == second
# ─── другое решение ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __iter__(self):
        return iter(self._items)
# ─── ошибка ───
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"


class Menu:
    def __init__(self, products):
        self._items = list(products)
        self._it = iter(self._items)

    def __iter__(self):
        return self._it

# %% cheaper [exercise]
class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __iter__(self):
        for p in self._items:
            yield p

    def cheaper_than(self, price):
        for p in self._items:
            if p.price < price:
                yield p
# ─── заготовка ───
class Menu:
    # скопируйте сюда __init__ и __iter__ из упражнения выше

    def cheaper_than(self, price):
        ...
# ─── проверка ───
def _menu():
    try:
        return Menu([Product("Латте", 220), Product("Чай", 120), Product("Какао", 190)])
    except TypeError:
        assert False, "Menu([...]) не создаётся — скопируйте __init__ из упражнения выше"


def test_copied():
    "__iter__ на месте"
    assert "__iter__" in Menu.__dict__, "в классе нет __iter__ — скопируйте класс из упражнения выше"
    assert [p.name for p in _menu()] == ["Латте", "Чай", "Какао"], "цикл по меню работает не так, как в упражнении выше"


def test_cheaper():
    "cheaper_than выдаёт дешёвые товары"
    got = _menu().cheaper_than(200)
    assert not isinstance(got, list), "cheaper_than вернул список, а нужен генератор — используйте yield"
    assert got is not None, "cheaper_than ничего не возвращает — выдавайте товары через yield"
    names = [p.name for p in got]
    assert names == ["Чай", "Какао"], f"дешевле 200 ₽ — {names}, а нужно ['Чай', 'Какао']"
    assert [p.name for p in _menu().cheaper_than(100)] == [], "дешевле 100 ₽ ничего нет"
    assert [p.name for p in _menu().cheaper_than(190)] == ["Чай"], "какао стоит ровно 190 ₽ — оно не дешевле 190, сравнение строгое: <"
# ─── другое решение ───
class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __iter__(self):
        return iter(self._items)

    def cheaper_than(self, price):
        for p in self:
            if p.price < price:
                yield p
# ─── ошибка ───
class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __iter__(self):
        for p in self._items:
            yield p

    def cheaper_than(self, price):
        return [p for p in self._items if p.price < price]
# ─── ошибка ───
class Menu:
    def __init__(self, products):
        self._items = list(products)

    def __iter__(self):
        for p in self._items:
            yield p

    def cheaper_than(self, price):
        for p in self._items:
            if p.price <= price:
                yield p

# %% iter-next
drinks = ["латте", "чай"]
it = iter(drinks)
print(next(it))
print(next(it))
try:
    next(it)
except StopIteration:
    print("StopIteration — элементы кончились")

# %% one-pass
it = iter(drinks)
print(list(it))
print(list(it))  # итератор уже пройден
print(list(drinks), list(drinks))  # список — сколько угодно раз

# %% playlist [exercise]
class Playlist:
    def __init__(self, songs):
        self._songs = list(songs)

    def __iter__(self):
        for song in self._songs:
            yield song
# ─── заготовка ───
class Playlist:
    def __init__(self, songs):
        self._it = iter(songs)

    def __iter__(self):
        return self._it
# ─── проверка ───
def test_twice():
    "плейлист проходится несколько раз"
    playlist = Playlist(["Джаз утром", "Босса-нова"])
    first = list(playlist)
    second = list(playlist)
    assert first == ["Джаз утром", "Босса-нова"], f"первый проход дал {first}"
    assert second == first, "второй проход по плейлисту пуст — __iter__ должен отдавать новый итератор каждый раз"


def test_source_list():
    "исходный список не нужен после создания"
    songs = ["Джаз утром"]
    playlist = Playlist(songs)
    songs.append("чужая песня")
    assert list(playlist) == ["Джаз утром"], "плейлист изменился вместе с чужим списком — храните копию: list(songs)"
# ─── другое решение ───
class Playlist:
    def __init__(self, songs):
        self._songs = list(songs)

    def __iter__(self):
        return iter(self._songs)
# ─── ошибка ───
class Playlist:
    def __init__(self, songs):
        self._songs = songs

    def __iter__(self):
        return iter(self._songs)

# %% generator-quiz [quiz]
cheap = Menu([Product("Латте", 220), Product("Чай", 120), Product("Какао", 190)]).cheaper_than(200)
list(cheap)
print(list(cheap))

# %% next-quiz [quiz]
it = iter(["латте"])
next(it)
try:
    next(it)
except StopIteration:
    print("исключение `StopIteration`")
