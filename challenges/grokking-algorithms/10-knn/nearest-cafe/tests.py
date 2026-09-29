def test_example():
    """Пример: ближайшая — [1, 2]"""
    got = nearest([[0, 0], [5, 5], [1, 2]], [2, 2])
    assert got == 2, f"ожидалось 2, получено {got!r}"


def test_tie_smaller_index():
    """Ничья → меньший индекс"""
    got = nearest([[1, 0], [-1, 0]], [0, 0])
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_differences_do_not_cancel():
    """Разности разного знака не компенсируют друг друга"""
    got = nearest([[5, -5], [1, 1]], [0, 0])
    assert got == 1, f"ожидалось 1 ([1, 1] ближе, чем [5, -5]), получено {got!r}"


def test_empty():
    """Нет кафе → -1"""
    got = nearest([], [0, 0])
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_single():
    """Одно кафе → 0"""
    got = nearest([[100, 100]], [0, 0])
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_exact_match():
    """Точка совпадает с запросом"""
    got = nearest([[3, 3], [1, 1], [1, 1]], [1, 1])
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_three_dimensions():
    """Три координаты"""
    got = nearest([[0, 0, 9], [2, 2, 2], [0, 5, 0]], [1, 1, 1])
    assert got == 1, f"ожидалось 1, получено {got!r}"
