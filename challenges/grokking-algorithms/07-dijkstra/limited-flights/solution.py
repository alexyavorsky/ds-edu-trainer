import heapq


def cheapest_limited(flights: dict[str, dict[str, int]], start: str, goal: str, max_flights: int) -> int | None:
    """Минимальная цена из start в goal не больше чем за max_flights перелётов или None."""
    best = {(start, 0): 0}
    done: set[tuple[str, int]] = set()
    heap = [(0, start, 0)]  # (цена, город, сделано перелётов)
    while heap:
        cost, city, used = heapq.heappop(heap)
        if (city, used) in done:
            continue
        if city == goal:
            return cost
        done.add((city, used))
        if used == max_flights:
            continue
        for nxt, price in flights.get(city, {}).items():
            state = (nxt, used + 1)
            if cost + price < best.get(state, cost + price + 1):
                best[state] = cost + price
                heapq.heappush(heap, (cost + price, nxt, used + 1))
    return None
