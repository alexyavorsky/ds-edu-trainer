def test_small():
    """n = 1, 2, 3, 4 → 1, 2, 3, 5"""
    for n, expected in [(1, 1), (2, 2), (3, 3), (4, 5)]:
        got = tile_ways(n)
        assert got == expected, f"tile_ways({n}): ожидалось {expected}, получено {got!r}"


def test_zero():
    """n = 0 → 1 (пустая дорожка)"""
    got = tile_ways(0)
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_ten():
    """n = 10 → 89"""
    got = tile_ways(10)
    assert got == 89, f"ожидалось 89, получено {got!r}"


def test_first_sixteen():
    """n = 0…15 — заранее посчитанные ответы"""
    expected = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
    for n, answer in enumerate(expected):
        got = tile_ways(n)
        assert got == answer, f"tile_ways({n}): ожидалось {answer}, получено {got!r}"


def test_large():
    """n = 38, 39, 40 — верные ответы за отведённое время"""
    for n, expected in [(38, 63245986), (39, 102334155), (40, 165580141)]:
        got = tile_ways(n)
        assert got == expected, f"tile_ways({n}): ожидалось {expected}, получено {got!r}"


test_large.timeout_hint = "Если это рекурсия, добавьте запоминание или заполняйте таблицу слева направо"
