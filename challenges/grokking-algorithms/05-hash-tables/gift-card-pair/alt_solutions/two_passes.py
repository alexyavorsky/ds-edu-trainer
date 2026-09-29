def pair_for_card(prices: list[int], total: int) -> tuple[int, int] | None:
    """Индексы (i, j), i < j, с prices[i] + prices[j] == total, или None."""
    last_index = {}
    for i, price in enumerate(prices):  # первый проход: цена → последний индекс
        last_index[price] = i
    for i, price in enumerate(prices):  # второй проход: ищем пару правее
        j = last_index.get(total - price)
        if j is not None and j > i:
            return i, j
    return None
