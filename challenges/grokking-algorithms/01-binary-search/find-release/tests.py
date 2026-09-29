VERSIONS = [101, 105, 110, 120, 131, 140, 152]


def test_found():
    """Существующий релиз: 110 → 2"""
    got = find_release(VERSIONS, 110)
    assert got == 2, f"ожидалось 2, получено {got!r}"


def test_not_found_between():
    """Нет такого релиза (между существующими) → -1"""
    got = find_release(VERSIONS, 111)
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_not_found_outside():
    """Меньше минимального и больше максимального → -1"""
    for target in (1, 999):
        got = find_release(VERSIONS, target)
        assert got == -1, f"find_release(..., {target}): ожидалось -1, получено {got!r}"


def test_empty():
    """Пустой список → -1"""
    got = find_release([], 5)
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_single():
    """Один релиз: находится и не находится"""
    assert find_release([7], 7) == 0, f"find_release([7], 7): получено {find_release([7], 7)!r}"
    assert find_release([7], 8) == -1, f"find_release([7], 8): получено {find_release([7], 8)!r}"


def test_every_position():
    """Каждый релиз находится на своём месте, соседние значения — нет"""
    for i, v in enumerate(VERSIONS):
        got = find_release(VERSIONS, v)
        assert got == i, f"find_release(..., {v}): ожидалось {i}, получено {got!r}"
        got = find_release(VERSIONS, v + 1)
        assert got == -1, f"find_release(..., {v + 1}): ожидалось -1, получено {got!r}"
