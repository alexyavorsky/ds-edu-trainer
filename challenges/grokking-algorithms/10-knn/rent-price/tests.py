import math

TRAIN = [
    ([40, 3, 10], 35_000),
    ([42, 5, 12], 37_000),
    ([80, 10, 5], 90_000),
    ([38, 2, 15], 30_000),
]


def _close(got, expected, label):
    assert isinstance(got, (int, float)), f"{label}: ожидалось число, получено {got!r}"
    assert math.isclose(got, expected, rel_tol=1e-9), f"{label}: ожидалось {expected}, получено {got!r}"


def test_example():
    """Пример: среднее двух соседей → 36000"""
    _close(predict_rent(TRAIN, [41, 4, 11], 2), 36_000.0, "k=2")


def test_k_one():
    """k = 1 — цена ближайшей квартиры"""
    _close(predict_rent(TRAIN, [79, 9, 6], 1), 90_000.0, "k=1")


def test_k_too_big():
    """k больше числа квартир — среднее всех"""
    _close(predict_rent(TRAIN, [50, 5, 10], 100), (35_000 + 37_000 + 90_000 + 30_000) / 4, "k=100")


def test_exact_match():
    """Запрос совпадает с квартирой, k = 1"""
    _close(predict_rent(TRAIN, [38, 2, 15], 1), 30_000.0, "совпадение")


def test_ties_keep_order():
    """Равные расстояния — берётся квартира, что раньше в train"""
    train = [([1], 100.0), ([-1], 300.0), ([5], 1000.0)]
    _close(predict_rent(train, [0], 1), 100.0, "ничья, k=1")
    _close(predict_rent(train, [0], 2), 200.0, "k=2")


def test_float_prices():
    """Дробные цены"""
    train = [([0, 0], 10.1), ([0, 1], 10.2), ([0, 2], 10.3)]
    _close(predict_rent(train, [0, 1], 3), 10.2, "три соседа")
