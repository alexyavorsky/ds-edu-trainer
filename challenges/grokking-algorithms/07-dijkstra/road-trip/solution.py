import heapq


def travel_time(roads: list[tuple[str, str, int]], start: str, goal: str) -> int | None:
    """Минимальное время из start в goal по двусторонним дорогам или None."""
    graph: dict[str, dict[str, int]] = {}
    for a, b, minutes in roads:
        for x, y in ((a, b), (b, a)):
            edges = graph.setdefault(x, {})
            edges[y] = min(edges.get(y, minutes), minutes)

    best = {start: 0}
    done: set[str] = set()
    heap = [(0, start)]
    while heap:
        cost, city = heapq.heappop(heap)
        if city in done:
            continue
        if city == goal:
            return cost
        done.add(city)
        for nxt, minutes in graph.get(city, {}).items():
            if cost + minutes < best.get(nxt, cost + minutes + 1):
                best[nxt] = cost + minutes
                heapq.heappush(heap, (cost + minutes, nxt))
    return None
