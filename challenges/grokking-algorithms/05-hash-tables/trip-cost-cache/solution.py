from collections.abc import Callable


def trip_cost(route: list[str], fetch_price: Callable[[str], int]) -> int:
    """Сумма цен по маршруту; цена каждого города запрашивается один раз."""
    total = 0
    cache: dict[str, int] = {}
    for city in route:
        if city not in cache:
            cache[city] = fetch_price(city)
        total += cache[city]
    return total
