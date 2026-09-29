def plan_route(points: list[tuple[float, float]]) -> list[int]:
    """Порядок обхода точек эвристикой «ближайший сосед», начиная с 0."""
    if len(points) == 0:
        return []
    left = list(range(1, len(points)))
    route = [0]
    while left:
        x, y = points[route[-1]]
        best_pos = 0
        best_d2 = None
        for pos, i in enumerate(left):
            d2 = (points[i][0] - x) ** 2 + (points[i][1] - y) ** 2  # квадрат расстояния — сравнивать можно без корня
            if best_d2 is None or d2 < best_d2:
                best_pos, best_d2 = pos, d2
        route.append(left.pop(best_pos))
    return route
