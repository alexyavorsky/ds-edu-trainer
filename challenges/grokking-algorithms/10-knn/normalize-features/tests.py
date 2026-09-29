import math


def _close_rows(got, expected):
    assert isinstance(got, list) and len(got) == len(expected), f"ожидалось {expected}, получено {got!r}"
    for r, (g, e) in enumerate(zip(got, expected)):
        assert len(g) == len(e), f"строка {r}: ожидалось {e}, получено {g!r}"
        for j, (x, y) in enumerate(zip(g, e)):
            assert math.isclose(x, y, abs_tol=1e-9), f"строка {r}, столбец {j}: ожидалось {y}, получено {x!r}"


def test_example():
    """Пример: площадь и цена → [0, 1]"""
    _close_rows(normalize([[50, 3000], [70, 5000], [60, 4000]]), [[0.0, 0.0], [1.0, 1.0], [0.5, 0.5]])


def test_constant_column():
    """Постоянный столбец → нули"""
    _close_rows(normalize([[1, 7], [3, 7], [2, 7]]), [[0.0, 0.0], [1.0, 0.0], [0.5, 0.0]])


def test_single_row():
    """Одна строка — все столбцы постоянные"""
    _close_rows(normalize([[5, -2, 9]]), [[0.0, 0.0, 0.0]])


def test_empty():
    """Пустой вход → []"""
    got = normalize([])
    assert got == [], f"ожидалось [], получено {got!r}"


def test_negative_values():
    """Отрицательные значения"""
    _close_rows(normalize([[-10], [0], [10], [5]]), [[0.0], [0.5], [1.0], [0.75]])


def test_columns_independent():
    """Столбцы нормализуются независимо"""
    _close_rows(normalize([[0, 100], [10, 0]]), [[0.0, 1.0], [1.0, 0.0]])


def test_input_not_changed():
    """Исходные данные не изменяются"""
    data = [[1, 2], [3, 4]]
    normalize(data)
    assert data == [[1, 2], [3, 4]], f"данные изменились: {data!r}"
