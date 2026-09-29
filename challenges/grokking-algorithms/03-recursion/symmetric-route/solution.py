def is_symmetric(route: list[str]) -> bool:
    """Проверяет, читается ли маршрут одинаково с начала и с конца."""
    if len(route) <= 1:
        return True
    if route[0] != route[-1]:
        return False
    return is_symmetric(route[1:-1])
