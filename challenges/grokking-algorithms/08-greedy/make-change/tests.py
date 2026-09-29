RUB = [1, 2, 5, 10, 50, 100]


def _check(amount: int, coins: list[int], best: int) -> None:
    """best — минимальное число монет (заранее посчитано)."""
    got = make_change(amount, coins)
    assert isinstance(got, list), f"ожидался список монет, получено {got!r}"
    assert all(c in coins for c in got), f"есть монеты не из набора {coins}: {got}"
    assert sum(got) == amount, f"сумма монет {sum(got)}, а нужно {amount}: {got}"
    assert len(got) == best, f"монет {len(got)}, а можно обойтись {best}: {got}"


def test_example():
    """68 = 50 + 10 + 5 + 2 + 1"""
    _check(68, [1, 2, 5, 10, 50], 5)


def test_zero():
    """Сумма 0 → []"""
    got = make_change(0, RUB)
    assert got == [], f"ожидалось [], получено {got!r}"


def test_exact_coin():
    """Сумма равна номиналу — одна монета"""
    _check(50, RUB, 1)


def test_only_ones():
    """Есть только монета 1"""
    _check(7, [1], 7)


def test_unsorted_coins():
    """Номиналы в произвольном порядке"""
    _check(99, [10, 1, 100, 5, 2, 50], 8)


def test_many_amounts():
    """Двадцать разных сумм — минимальное число монет"""
    expected = {
        1: 1, 3: 2, 4: 2, 7: 2, 8: 3, 9: 3, 13: 3, 19: 4, 24: 4, 38: 6,
        49: 7, 64: 4, 88: 7, 99: 8, 137: 6, 188: 8, 199: 9, 244: 8, 299: 10, 300: 3,
    }
    for amount, best in expected.items():
        _check(amount, RUB, best)


def test_big_amount():
    """Большая сумма"""
    got = make_change(1_000_003, RUB)
    assert sum(got) == 1_000_003 and len(got) == 10_002, f"монет {len(got)}, сумма {sum(got)}"
