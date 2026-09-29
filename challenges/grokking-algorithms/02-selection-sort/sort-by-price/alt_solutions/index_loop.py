def sort_by_price(items: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Возвращает новый список товаров, отсортированный по цене (сортировка выбором)."""
    rest = items[:]
    result = []
    while len(rest) > 0:
        best = 0
        for i in range(len(rest)):
            if rest[i][1] < rest[best][1]:
                best = i
        result.append(rest[best])
        del rest[best]
    return result
