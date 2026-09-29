import heapq
import math


def cheapest_with_coupon(flights: dict[str, dict[str, int]], start: str, goal: str) -> int | None:
    """Минимальная цена с одним купоном на полцены или None."""
    best: dict[tuple[str, bool], int] = {(start, False): 0}
    done: set[tuple[str, bool]] = set()
    heap = [(0, start, False)]  # (цена, город, купон уже использован?)

    def relax(city: str, used: bool, cost: int) -> None:
        if cost < best.get((city, used), math.inf):
            best[(city, used)] = cost
            heapq.heappush(heap, (cost, city, used))

    while heap:
        cost, city, used = heapq.heappop(heap)
        if (city, used) in done:
            continue
        if city == goal:
            return cost
        done.add((city, used))
        for nxt, price in flights.get(city, {}).items():
            # TODO: лететь по полной цене — купон не тратится
            # TODO: если купон ещё есть — лететь за price // 2 и перейти в состояние «купон использован»
            pass
    return None
