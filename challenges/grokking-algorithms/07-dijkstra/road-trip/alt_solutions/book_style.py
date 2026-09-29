import math


def travel_time(roads: list[tuple[str, str, int]], start: str, goal: str) -> int | None:
    """Минимальное время из start в goal по двусторонним дорогам или None."""
    graph: dict[str, dict[str, int]] = {start: {}, goal: {}}
    for a, b, minutes in roads:
        for x, y in ((a, b), (b, a)):
            graph.setdefault(x, {})
            if y not in graph[x] or minutes < graph[x][y]:
                graph[x][y] = minutes
    costs = {city: math.inf for city in graph}
    costs[start] = 0
    processed = set()
    while True:
        node = None
        for city in graph:
            if city not in processed and costs[city] < math.inf and (node is None or costs[city] < costs[node]):
                node = city
        if node is None:
            break
        processed.add(node)
        for nxt, minutes in graph[node].items():
            costs[nxt] = min(costs.get(nxt, math.inf), costs[node] + minutes)
    return None if costs[goal] == math.inf else costs[goal]
