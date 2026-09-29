def _check(shifts, optimum):
    got = min_checks(shifts)
    assert isinstance(got, list), f"ожидался список моментов, получено {got!r}"
    for start, end in shifts:
        assert any(start <= t <= end for t in got), f"в смену [{start}, {end}] не было обхода: {got}"
    assert len(got) == optimum, f"обходов {len(got)}, а можно обойтись {optimum}: {got}"


def test_example():
    """Пример: 2 обхода"""
    _check([(1, 4), (2, 6), (5, 8), (7, 9)], 2)


def test_touching_shifts():
    """Смены касаются границами — хватает одного обхода"""
    _check([(1, 3), (3, 5)], 1)


def test_nested_shift():
    """Короткая смена внутри длинной"""
    _check([(1, 10), (2, 3)], 1)


def test_empty():
    """Смен нет → []"""
    got = min_checks([])
    assert got == [], f"ожидалось [], получено {got!r}"


def test_disjoint():
    """Непересекающиеся смены — по обходу на каждую"""
    _check([(1, 2), (4, 5), (7, 8)], 3)


def test_point_shifts():
    """Смены длиной в один момент"""
    _check([(5, 5), (5, 5), (6, 6)], 2)


def test_bigger():
    """40 смен в перемешанном порядке — хватает 12 обходов"""
    shifts = [((i * 37) % 50, (i * 37) % 50 + (i % 7) + 1) for i in range(40)]
    _check(shifts, 12)
