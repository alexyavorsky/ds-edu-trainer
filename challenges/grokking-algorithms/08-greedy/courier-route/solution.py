import math


def plan_route(points: list[tuple[float, float]]) -> list[int]:
    """Порядок обхода точек эвристикой «ближайший сосед», начиная с 0."""
    if not points:
        return []
    route = [0]
    unvisited = set(range(1, len(points)))
    while unvisited:
        here = points[route[-1]]
        nearest = min(unvisited, key=lambda i: math.dist(here, points[i]))
        route.append(nearest)
        unvisited.remove(nearest)
    return route
