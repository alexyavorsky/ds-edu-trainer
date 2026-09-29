import math

GRAPH = {"склад": {"A": 5, "B": 2}, "B": {"A": 1, "клиент": 9}, "A": {"клиент": 3}}


def test_example():
    """Пример: 6 минут через B и A"""
    got = fastest_route(GRAPH, "склад", "клиент")
    assert got == (6, ["склад", "B", "A", "клиент"]), f"получено {got!r}"


def test_intermediate():
    """До A быстрее через B: 3 минуты"""
    got = fastest_route(GRAPH, "склад", "A")
    assert got == (3, ["склад", "B", "A"]), f"получено {got!r}"


def test_unreachable():
    """Недостижимый узел → (inf, [])"""
    got = fastest_route(GRAPH, "клиент", "склад")
    assert got == (math.inf, []), f"получено {got!r}"


def test_same_node():
    """start == goal → (0, [start])"""
    got = fastest_route(GRAPH, "склад", "склад")
    assert got == (0, ["склад"]), f"получено {got!r}"


def test_long_cheap_path():
    """Длинный путь из дешёвых рёбер лучше одного дорогого"""
    graph = {"s": {"t": 10, "a": 3}, "a": {"b": 3}, "b": {"t": 3}}
    got = fastest_route(graph, "s", "t")
    assert got == (9, ["s", "a", "b", "t"]), f"получено {got!r}"


def test_path_matches_cost():
    """Сумма весов по возвращённому пути равна времени"""
    graph = {"a": {"b": 4, "c": 1}, "c": {"b": 2, "d": 8}, "b": {"d": 1}, "d": {}}
    cost, path = fastest_route(graph, "a", "d")
    assert cost == 4, f"ожидалось 4, получено {cost!r}"
    total = sum(graph[x][y] for x, y in zip(path, path[1:]))
    assert total == cost and path[0] == "a" and path[-1] == "d", f"путь {path} стоит {total}, а время {cost}"
