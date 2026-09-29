import math


def cheapest(flights: dict[str, dict[str, int]], start: str, goal: str) -> float:
    """Минимальная цена перелёта из start в goal или math.inf."""
    cities = set(flights) | {c for edges in flights.values() for c in edges} | {start, goal}
    costs = {c: math.inf for c in cities}
    costs[start] = 0
    processed: set[str] = set()
    while True:  # как в книге: каждый раз ищем самый дешёвый необработанный узел перебором
        candidates = [c for c in cities if c not in processed and costs[c] < math.inf]
        if not candidates:
            break
        node = min(candidates, key=lambda c: costs[c])
        processed.add(node)
        for nxt, price in flights.get(node, {}).items():
            costs[nxt] = min(costs[nxt], costs[node] + price)
    return costs[goal]
