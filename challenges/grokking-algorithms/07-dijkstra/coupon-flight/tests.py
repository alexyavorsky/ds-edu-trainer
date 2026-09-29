FLIGHTS = {"A": {"B": 1000, "C": 300}, "C": {"B": 600}}


def test_example():
    """Пример: купон на прямой рейс → 500"""
    got = cheapest_with_coupon(FLIGHTS, "A", "B")
    assert got == 500, f"ожидалось 500, получено {got!r}"


def test_coupon_on_cheap_leg():
    """Купон выгоднее тратить на дорогой рейс маршрута"""
    flights = {"s": {"m": 100}, "m": {"t": 900}}
    got = cheapest_with_coupon(flights, "s", "t")
    assert got == 550, f"ожидалось 550, получено {got!r}"


def test_odd_price_rounding():
    """Нечётная цена округляется вниз: 7 // 2 = 3"""
    got = cheapest_with_coupon({"a": {"b": 7}}, "a", "b")
    assert got == 3, f"ожидалось 3, получено {got!r}"


def test_same_city():
    """start == goal → 0"""
    got = cheapest_with_coupon(FLIGHTS, "A", "A")
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_unreachable():
    """Недостижимо → None"""
    got = cheapest_with_coupon(FLIGHTS, "B", "A")
    assert got is None, f"ожидалось None, получено {got!r}"


def test_only_one_coupon():
    """Купон один: на двух дорогих рейсах скидка только на одном"""
    flights = {"a": {"b": 100}, "b": {"c": 100}}
    got = cheapest_with_coupon(flights, "a", "c")
    assert got == 150, f"ожидалось 150, получено {got!r}"


def test_small_graphs():
    """15 небольших графов: заранее посчитанные ответы"""
    expected = [
        [None, None, None, 24, None], [14, None, None, 23, 36], [None, 26, None, 82, None],
        [None, None, 38, 57, None], [None, None, None, 5, None], [40, None, None, 46, 17],
        [None, 7, None, 25, None], [None, None, 19, 74, None], [None, None, None, 31, None],
        [21, None, None, 44, 43], [None, 33, None, 103, None], [None, None, 45, 78, None],
        [None, None, None, 12, None], [2, None, None, 42, 24], [None, 14, None, 46, None],
    ]
    for seed, answers in enumerate(expected):
        flights: dict[str, dict[str, int]] = {}
        for i in range(6):
            for j in range(6):
                if i != j and (i * 7 + j * 3 + seed) % 4 == 0:
                    flights.setdefault("abcdef"[i], {})["abcdef"[j]] = (i * 37 + j * 11 + seed * 13) % 90 + 5
        for goal, answer in zip("bcdef", answers):
            got = cheapest_with_coupon(flights, "a", goal)
            assert got == answer, f"граф {seed}, a → {goal}: ожидалось {answer}, получено {got!r}"
