import itertools
import math


def _length(points, route):
    loop = route + route[:1]
    return sum(math.dist(points[a], points[b]) for a, b in zip(loop, loop[1:]))


def _check_greedy(points):
    route = plan_route(points)
    assert isinstance(route, list), f"ожидался список индексов, получено {route!r}"
    assert sorted(route) == list(range(len(points))), f"каждая точка должна встретиться ровно один раз: {route}"
    assert route[0] == 0, f"маршрут должен начинаться со склада (0): {route}"
    visited = {0}
    for a, b in zip(route, route[1:]):
        rest = [i for i in range(len(points)) if i not in visited]
        best = min(math.dist(points[a], points[i]) for i in rest)
        assert math.isclose(math.dist(points[a], points[b]), best), (
            f"из точки {a} поехали в {b}, но есть ближе (расстояние {best:.2f}): {route}"
        )
        visited.add(b)
    return route


def test_example():
    """Пример из условия"""
    got = _check_greedy([(0, 0), (10, 0), (1, 1), (9, 1)])
    assert got == [0, 2, 3, 1], f"получено {got}"


def test_empty_and_single():
    """Нет точек и только склад"""
    assert plan_route([]) == [], f"пусто: {plan_route([])!r}"
    assert plan_route([(3, 4)]) == [0], f"только склад: {plan_route([(3, 4)])!r}"


def test_line():
    """Точки на прямой по обе стороны от склада"""
    _check_greedy([(0, 0), (5, 0), (-1, 0), (2, 0), (-7, 0)])


def test_ties_allowed():
    """Равноудалённые точки — годится любая из ближайших"""
    _check_greedy([(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)])


def test_close_to_optimal():
    """На 7 точках маршрут не длиннее оптимального больше чем в 1.5 раза"""
    points = [(0, 0), (2, 7), (6, 1), (8, 8), (3, 3), (9, 3), (1, 5)]
    route = _check_greedy(points)
    optimum = min(_length(points, [0, *p]) for p in itertools.permutations(range(1, len(points))))
    ratio = _length(points, route) / optimum
    assert ratio <= 1.5, f"маршрут длиннее оптимального в {ratio:.2f} раза"


def test_many_points():
    """1000 точек: маршрут обходит все точки по правилу ближайшего соседа за отведённое время"""
    points = [((i * 7919) % 1000, (i * 104729) % 1000) for i in range(1000)]
    route = plan_route(points)
    assert sorted(route) == list(range(1000)) and route[0] == 0, "маршрут должен обойти все точки, начиная с 0"
    for a, b in list(zip(route, route[1:]))[:5]:  # первые шаги — выборочная проверка правила
        rest = set(range(1000)) - set(route[: route.index(b)])
        best = min(math.dist(points[a], points[i]) for i in rest)
        assert math.isclose(math.dist(points[a], points[b]), best), f"из {a} поехали в {b}, но есть ближе"


test_many_points.timeout = 10
