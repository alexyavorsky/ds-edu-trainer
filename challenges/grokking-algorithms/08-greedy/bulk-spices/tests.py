import math

SPICES = [("шафран", 10, 600), ("перец", 50, 500), ("корица", 40, 160)]


def _close(got, expected, label):
    assert isinstance(got, (int, float)), f"{label}: ожидалось число, получено {got!r}"
    assert math.isclose(got, expected, rel_tol=1e-9), f"{label}: ожидалось {expected}, получено {got!r}"


def test_example_60():
    """Сумка на 60 г → 1100"""
    _close(max_value(SPICES, 60), 1100.0, "capacity=60")


def test_example_30():
    """Сумка на 30 г → 800 (часть перца)"""
    _close(max_value(SPICES, 30), 800.0, "capacity=30")


def test_everything_fits():
    """Всё помещается → сумма ценностей"""
    _close(max_value(SPICES, 1000), 1260.0, "capacity=1000")


def test_zero_capacity():
    """Сумка на 0 г → 0"""
    _close(max_value(SPICES, 0), 0.0, "capacity=0")


def test_empty_shop():
    """Специй нет → 0"""
    _close(max_value([], 50), 0.0, "пустая лавка")


def test_fraction_of_first():
    """Места меньше, чем самой ценной специи"""
    _close(max_value([("ваниль", 20, 1000), ("соль", 100, 10)], 5), 250.0, "5 г ванили")


def test_order_matters():
    """Специи даны не по ценности за грамм"""
    spices = [("a", 30, 60), ("b", 10, 50), ("c", 20, 60)]
    _close(max_value(spices, 25), 95.0, "b целиком + 15 г c")
