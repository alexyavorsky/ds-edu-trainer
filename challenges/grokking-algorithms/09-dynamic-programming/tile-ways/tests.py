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
    """n = 300 — верный ответ за отведённое время"""
    expected = 359579325206583560961765665172189099052367214309267232255589801
    got = tile_ways(300)
    assert got == expected, f"неверный ответ для n = 300 (ожидалось число из {len(str(expected))} цифр)"


test_large.timeout = 5
test_large.timeout_hint = "Если это рекурсия, добавьте запоминание или заполняйте таблицу слева направо"
