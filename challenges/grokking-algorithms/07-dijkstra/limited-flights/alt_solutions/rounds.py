import math


def cheapest_limited(flights: dict[str, dict[str, int]], start: str, goal: str, max_flights: int) -> int | None:
    """Минимальная цена из start в goal не больше чем за max_flights перелётов или None."""
    best = {start: 0}  # лучшая цена, если сделать не больше r перелётов
    for _ in range(max_flights):  # раунд за раундом добавляем по одному перелёту
        updated = dict(best)
        for city, cost in best.items():
            for nxt, price in flights.get(city, {}).items():
                if cost + price < updated.get(nxt, math.inf):
                    updated[nxt] = cost + price
        best = updated
    return best.get(goal)
