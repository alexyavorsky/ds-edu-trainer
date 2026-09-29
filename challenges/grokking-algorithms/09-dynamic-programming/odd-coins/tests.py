def test_greedy_trap():
    """6 монетами [1, 3, 4] → 2 (жадный даёт 3)"""
    got = min_coins(6, [1, 3, 4])
    assert got == 2, f"ожидалось 2, получено {got!r}"


def test_impossible():
    """7 из [2, 4] не набрать → -1"""
    got = min_coins(7, [2, 4])
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_zero():
    """Сумма 0 → 0 монет"""
    got = min_coins(0, [5])
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_single_coin_type():
    """Одна монета: 15 из [5] → 3, 16 из [5] → -1"""
    assert min_coins(15, [5]) == 3, f"получено {min_coins(15, [5])!r}"
    assert min_coins(16, [5]) == -1, f"получено {min_coins(16, [5])!r}"


def test_another_trap():
    """20 монетами [1, 10, 15] → 2 (жадно 15 + 5 × 1 = 6)"""
    got = min_coins(20, [1, 10, 15])
    assert got == 2, f"ожидалось 2, получено {got!r}"


def test_sums_up_to_40():
    """Суммы 0…40 монетами [3, 7, 11] — заранее посчитанные ответы"""
    expected = [
        0, -1, -1, 1, -1, -1, 2, 1, -1, 3, 2, 1, 4, 3, 2, 5, 4, 3, 2, 5, 4,
        3, 2, 5, 4, 3, 6, 5, 4, 3, 6, 5, 4, 3, 6, 5, 4, 7, 6, 5, 4,
    ]
    for amount, answer in enumerate(expected):
        got = min_coins(amount, [3, 7, 11])
        assert got == answer, f"min_coins({amount}, [3, 7, 11]): ожидалось {answer}, получено {got!r}"


def test_large():
    """Суммы до 26 монетами [1, 2, 3, 4, 6, 9] — за отведённое время"""
    for amount, answer in [(26, 4), (25, 4), (20, 3)]:
        got = min_coins(amount, [1, 2, 3, 4, 6, 9])
        assert got == answer, f"min_coins({amount}, ...): ожидалось {answer}, получено {got!r}"


test_large.timeout_hint = "Если это рекурсия, добавьте запоминание: без него одни и те же суммы считаются заново"
