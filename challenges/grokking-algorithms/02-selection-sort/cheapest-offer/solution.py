def cheapest(offers: list[int]) -> int:
    """Индекс минимальной цены (первый при равенстве) или -1 для пустого списка."""
    if not offers:
        return -1
    best = 0
    for i in range(1, len(offers)):
        if offers[i] < offers[best]:
            best = i
    return best
