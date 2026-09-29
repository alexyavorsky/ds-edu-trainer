def test_example():
    """Пример из условия"""
    items = [("чай", 300), ("мёд", 450), ("сахар", 90), ("кофе", 300)]
    expected = [("сахар", 90), ("чай", 300), ("кофе", 300), ("мёд", 450)]
    got = sort_by_price(items)
    assert got == expected, f"получено {got!r}"


def test_empty():
    """Пустая витрина → []"""
    got = sort_by_price([])
    assert got == [], f"получено {got!r}"


def test_single():
    """Один товар"""
    got = sort_by_price([("соль", 40)])
    assert got == [("соль", 40)], f"получено {got!r}"


def test_reverse_order():
    """Цены по убыванию"""
    items = [("a", 5), ("b", 4), ("c", 3), ("d", 2), ("e", 1)]
    got = sort_by_price(items)
    assert got == items[::-1], f"получено {got!r}"


def test_equal_prices_keep_order():
    """Одинаковые цены сохраняют исходный порядок"""
    items = [("x", 10), ("y", 5), ("z", 10), ("w", 5), ("v", 10)]
    expected = [("y", 5), ("w", 5), ("x", 10), ("z", 10), ("v", 10)]
    got = sort_by_price(items)
    assert got == expected, f"получено {got!r}"


def test_input_not_changed():
    """Исходный список не изменяется"""
    items = [("b", 2), ("a", 1)]
    sort_by_price(items)
    assert items == [("b", 2), ("a", 1)], f"список изменился: {items!r}"
