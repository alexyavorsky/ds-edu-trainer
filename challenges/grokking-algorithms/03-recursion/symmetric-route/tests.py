def test_empty():
    """Пустой маршрут симметричен"""
    got = is_symmetric([])
    assert got is True, f"ожидалось True, получено {got!r}"


def test_single_stop():
    """Одна остановка — симметричен"""
    got = is_symmetric(["Вокзал"])
    assert got is True, f"ожидалось True, получено {got!r}"


def test_odd_symmetric():
    """Нечётная длина: Депо → Рынок → Депо"""
    got = is_symmetric(["Депо", "Рынок", "Депо"])
    assert got is True, f"ожидалось True, получено {got!r}"


def test_even_symmetric():
    """Чётная длина: Парк → Мост → Мост → Парк"""
    got = is_symmetric(["Парк", "Мост", "Мост", "Парк"])
    assert got is True, f"ожидалось True, получено {got!r}"


def test_five_symmetric():
    """Пять остановок: A → B → C → B → A"""
    got = is_symmetric(["A", "B", "C", "B", "A"])
    assert got is True, f"ожидалось True, получено {got!r}"


def test_two_different():
    """Две разные остановки — не симметричен"""
    got = is_symmetric(["Парк", "Мост"])
    assert got is False, f"ожидалось False, получено {got!r}"


def test_mismatch_in_middle():
    """Отличие в глубине: A B C D B A — не симметричен"""
    got = is_symmetric(["A", "B", "C", "D", "B", "A"])
    assert got is False, f"ожидалось False, получено {got!r}"


def test_long_symmetric():
    """Длинный симметричный маршрут из 7 остановок"""
    route = ["A", "B", "C", "D", "C", "B", "A"]
    got = is_symmetric(route)
    assert got is True, f"ожидалось True, получено {got!r}"


def test_input_not_changed():
    """Исходный список не изменяется"""
    route = ["A", "B", "A"]
    is_symmetric(route)
    assert route == ["A", "B", "A"], f"список изменился: {route!r}"
