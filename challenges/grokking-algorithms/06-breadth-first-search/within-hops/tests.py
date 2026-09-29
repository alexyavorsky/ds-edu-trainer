GRAPH = {"я": ["Оля", "Пётр"], "Оля": ["Рома"], "Рома": ["Сеня"]}


def test_example():
    """Пример: k = 2"""
    got = within_hops(GRAPH, "я", 2)
    assert got == {"Оля", "Пётр", "Рома"}, f"получено {got!r}"


def test_k_zero():
    """k = 0 — никого"""
    got = within_hops(GRAPH, "я", 0)
    assert got == set(), f"получено {got!r}"


def test_k_one():
    """k = 1 — только прямые знакомые"""
    got = within_hops(GRAPH, "я", 1)
    assert got == {"Оля", "Пётр"}, f"получено {got!r}"


def test_large_k():
    """Большое k — все достижимые"""
    got = within_hops(GRAPH, "я", 100)
    assert got == {"Оля", "Пётр", "Рома", "Сеня"}, f"получено {got!r}"


def test_start_excluded_in_cycle():
    """Сам start не входит в ответ, даже если до него есть цикл"""
    graph = {"a": ["b"], "b": ["a", "c"]}
    got = within_hops(graph, "a", 3)
    assert got == {"b", "c"}, f"получено {got!r}"


def test_short_path_wins():
    """Кратчайший путь учитывается, даже если длинная ветка просмотрена бы первой"""
    graph = {"s": ["a", "b"], "b": ["c"], "c": ["d"], "a": ["d"], "d": ["e"]}
    got = within_hops(graph, "s", 3)
    assert got == {"a", "b", "c", "d", "e"}, f"получено {got!r} — e достижим за 3 шага: s → a → d → e"


def test_isolated():
    """У start нет знакомых"""
    got = within_hops({}, "один", 5)
    assert got == set(), f"получено {got!r}"
