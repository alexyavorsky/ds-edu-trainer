import math


def nearest(points: list[list[float]], query: list[float]) -> int:
    """Индекс ближайшей точки (меньший при равенстве) или -1."""
    best, best_dist = -1, math.inf
    for i, point in enumerate(points):
        d = math.sqrt(sum((x - y) ** 2 for x, y in zip(point, query)))
        if d < best_dist:
            best, best_dist = i, d
    return best
