def _check(neighbors, max_colors=None):
    got = color_map(neighbors)
    assert isinstance(got, dict) and set(got) == set(neighbors), f"нужно раскрасить все районы: {got!r}"
    for region, near in neighbors.items():
        for n in near:
            assert got[region] != got[n], f"соседи {region} и {n} одного цвета {got[region]}"
    used = set(got.values())
    assert used == set(range(len(used))), f"цвета должны идти подряд с 0: {sorted(used)}"
    limit = max((len(v) for v in neighbors.values()), default=0) + 1
    assert len(used) <= limit, f"цветов {len(used)}, а жадному хватает максимум {limit}"
    if max_colors is not None:
        assert len(used) <= max_colors, f"цветов {len(used)}, а здесь хватает {max_colors}"
    return got


def _undirected(edges):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    return graph


def test_example():
    """Пример из условия: 3 цвета"""
    _check(
        {"Центр": {"Север", "Юг", "Запад"}, "Север": {"Центр", "Запад"}, "Юг": {"Центр"}, "Запад": {"Центр", "Север"}},
        max_colors=3,
    )


def test_no_neighbors():
    """Районы без соседей — все цвета 0"""
    got = _check({"a": set(), "b": set()})
    assert got == {"a": 0, "b": 0}, f"получено {got!r}"


def test_empty():
    """Пустая карта"""
    got = color_map({})
    assert got == {}, f"получено {got!r}"


def test_triangle():
    """Три района, все соседи друг другу — 3 цвета"""
    _check(_undirected([("a", "b"), ("b", "c"), ("c", "a")]), max_colors=3)


def test_star():
    """«Звезда»: центр и 10 лучей — 2 цвета"""
    _check(_undirected([("hub", f"r{i}") for i in range(10)]), max_colors=2)


def test_even_cycle():
    """Кольцо из 8 районов"""
    _check(_undirected([(f"c{i}", f"c{(i + 1) % 8}") for i in range(8)]), max_colors=3)


def test_grid():
    """Решётка 10×10 районов"""
    edges = []
    for r in range(10):
        for c in range(10):
            if r + 1 < 10:
                edges.append((f"{r},{c}", f"{r + 1},{c}"))
            if c + 1 < 10:
                edges.append((f"{r},{c}", f"{r},{c + 1}"))
    _check(_undirected(edges))
