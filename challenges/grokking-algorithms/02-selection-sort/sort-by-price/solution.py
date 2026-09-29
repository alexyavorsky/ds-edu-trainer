def cheapest_index(items: list[tuple[str, int]]) -> int:
    """Индекс самого дешёвого товара; при равенстве — первого."""
    best = 0
    for i in range(1, len(items)):
        if items[i][1] < items[best][1]:
            best = i
    return best


def sort_by_price(items: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Возвращает новый список товаров, отсортированный по цене (сортировка выбором)."""
    rest = list(items)
    result = []
    while rest:
        result.append(rest.pop(cheapest_index(rest)))
    return result
