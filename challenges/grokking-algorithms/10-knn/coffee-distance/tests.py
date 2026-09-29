import math


def _close(got, expected, label):
    assert isinstance(got, (int, float)), f"{label}: ожидалось число, получено {got!r}"
    assert math.isclose(got, expected, rel_tol=1e-9, abs_tol=1e-12), f"{label}: ожидалось {expected}, получено {got!r}"


def test_three_four_five():
    """Египетский треугольник: (3, 4) и (0, 0) → 5"""
    _close(distance([3, 4], [0, 0]), 5.0, "distance([3, 4], [0, 0])")


def test_same_point():
    """Одинаковые векторы → 0"""
    _close(distance([7, 2, 5], [7, 2, 5]), 0.0, "одинаковые векторы")


def test_one_feature():
    """Один признак — модуль разности"""
    _close(distance([2], [9]), 7.0, "distance([2], [9])")


def test_negative_and_float():
    """Отрицательные и дробные значения"""
    _close(distance([-1.5, 2.0], [1.5, -2.0]), 5.0, "distance([-1.5, 2], [1.5, -2])")


def test_symmetric():
    """distance(a, b) == distance(b, a)"""
    a, b = [1, 5, 2, 8], [4, 1, 7, 3]
    _close(distance(a, b), distance(b, a), "симметричность")
    _close(distance(a, b), math.sqrt(9 + 16 + 25 + 25), "значение")


def test_empty_vectors():
    """Пустые векторы → 0"""
    _close(distance([], []), 0.0, "distance([], [])")


def test_length_mismatch():
    """Разная длина → ValueError"""
    try:
        distance([1, 2], [1, 2, 3])
    except ValueError:
        return
    raise AssertionError("ожидалось исключение ValueError")
