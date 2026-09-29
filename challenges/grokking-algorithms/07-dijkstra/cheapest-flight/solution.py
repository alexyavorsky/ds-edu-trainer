import heapq
import math


def cheapest(flights: dict[str, dict[str, int]], start: str, goal: str) -> float:
    """Минимальная цена перелёта из start в goal или math.inf."""
    costs = {start: 0}
    processed: set[str] = set()
    heap = [(0, start)]
    while heap:
        cost, city = heapq.heappop(heap)
        if city in processed:
            continue  # устаревшая запись: город уже обработан дешевле
        if city == goal:
            return cost
        processed.add(city)
        for nxt, price in flights.get(city, {}).items():
            new_cost = cost + price
            if new_cost < costs.get(nxt, math.inf):
                costs[nxt] = new_cost
                heapq.heappush(heap, (new_cost, nxt))
    return math.inf
