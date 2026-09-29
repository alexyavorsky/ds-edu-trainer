import math

FLIGHTS = {
    "Москва": {"Стамбул": 9000, "Дубай": 15000},
    "Стамбул": {"Дубай": 4000, "Бангкок": 21000},
    "Дубай": {"Бангкок": 11000},
}


def test_example():
    """Москва → Бангкок = 24000 с двумя пересадками"""
    got = cheapest(FLIGHTS, "Москва", "Бангкок")
    assert got == 24000, f"ожидалось 24000, получено {got!r}"


def test_direct_is_not_cheapest():
    """Прямой рейс в Дубай дороже, чем через Стамбул"""
    got = cheapest(FLIGHTS, "Москва", "Дубай")
    assert got == 13000, f"ожидалось 13000, получено {got!r}"


def test_unreachable():
    """Недостижимый город → math.inf"""
    got = cheapest(FLIGHTS, "Бангкок", "Москва")
    assert got == math.inf, f"ожидалось inf, получено {got!r}"


def test_same_city():
    """start == goal → 0"""
    got = cheapest(FLIGHTS, "Стамбул", "Стамбул")
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_unknown_city():
    """Города нет в графе вовсе"""
    assert cheapest({}, "А", "Б") == math.inf, "в пустом графе перелёта нет"


def test_zero_price():
    """Бесплатный рейс (цена 0)"""
    flights = {"A": {"B": 0, "C": 5}, "B": {"C": 1}}
    got = cheapest(flights, "A", "C")
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_more_hops_cheaper():
    """Больше пересадок, но дешевле — побеждает дешёвый путь"""
    flights = {"s": {"t": 100, "a": 1}, "a": {"b": 1}, "b": {"c": 1}, "c": {"t": 1}}
    got = cheapest(flights, "s", "t")
    assert got == 4, f"ожидалось 4, получено {got!r}"


def test_cycle():
    """Циклы в графе"""
    flights = {"a": {"b": 2}, "b": {"a": 1, "c": 7}, "c": {"a": 1}}
    assert cheapest(flights, "a", "c") == 9, f"получено {cheapest(flights, 'a', 'c')!r}"
    assert cheapest(flights, "c", "b") == 3, f"получено {cheapest(flights, 'c', 'b')!r}"
