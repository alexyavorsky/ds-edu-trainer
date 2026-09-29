FLIGHTS = {
    "A": {"B": 100, "D": 500},
    "B": {"C": 100},
    "C": {"D": 100},
}


def test_enough_flights():
    """Хватает перелётов → дешёвый путь 300"""
    got = cheapest_limited(FLIGHTS, "A", "D", 3)
    assert got == 300, f"ожидалось 300, получено {got!r}"


def test_limit_forces_direct():
    """Лимит 2 → прямой рейс за 500"""
    got = cheapest_limited(FLIGHTS, "A", "D", 2)
    assert got == 500, f"ожидалось 500, получено {got!r}"


def test_impossible():
    """До C не долететь за 1 перелёт → None"""
    got = cheapest_limited(FLIGHTS, "A", "C", 1)
    assert got is None, f"ожидалось None, получено {got!r}"


def test_zero_flights():
    """Лимит 0: только если start == goal"""
    assert cheapest_limited(FLIGHTS, "A", "A", 0) == 0, "start == goal → 0"
    assert cheapest_limited(FLIGHTS, "A", "B", 0) is None, "без перелётов в B не попасть"


def test_unreachable():
    """Недостижимо при любом лимите → None"""
    got = cheapest_limited(FLIGHTS, "D", "A", 10)
    assert got is None, f"ожидалось None, получено {got!r}"


def test_cheap_path_to_middle_is_too_long():
    """Дешёвый путь до промежуточного города съедает лимит — нужен другой"""
    flights = {
        "s": {"a": 1, "m": 10},
        "a": {"b": 1},
        "b": {"m": 1},
        "m": {"t": 1},
    }
    assert cheapest_limited(flights, "s", "t", 4) == 4, f"лимит 4: получено {cheapest_limited(flights, 's', 't', 4)!r}"
    assert cheapest_limited(flights, "s", "t", 3) == 11, f"лимит 3: получено {cheapest_limited(flights, 's', 't', 3)!r}"
    assert cheapest_limited(flights, "s", "t", 1) is None, "за 1 перелёт в t не попасть"


def test_cycle():
    """Цикл не мешает"""
    flights = {"a": {"b": 1}, "b": {"a": 1, "c": 5}}
    got = cheapest_limited(flights, "a", "c", 5)
    assert got == 6, f"ожидалось 6, получено {got!r}"
