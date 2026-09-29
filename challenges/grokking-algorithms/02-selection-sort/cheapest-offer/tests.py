def test_example():
    """Пример: [350, 290, 410, 290] → 1"""
    got = cheapest([350, 290, 410, 290])
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_min_is_last():
    """Минимум в конце списка: [500, 400, 300] → 2"""
    got = cheapest([500, 400, 300])
    assert got == 2, f"ожидалось 2, получено {got!r}"


def test_min_is_first():
    """Минимум в начале списка"""
    got = cheapest([100, 400, 300])
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_empty():
    """Пустой список → -1"""
    got = cheapest([])
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_single():
    """Одно предложение → 0"""
    got = cheapest([999])
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_all_equal():
    """Все цены равны → 0"""
    got = cheapest([7, 7, 7, 7])
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_two_items():
    """Два предложения, дешевле второе"""
    got = cheapest([5, 3])
    assert got == 1, f"ожидалось 1, получено {got!r}"
