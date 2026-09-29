def pair_for_card(prices: list[int], total: int) -> tuple[int, int] | None:
    """Индексы (i, j), i < j, с prices[i] + prices[j] == total, или None."""
    seen: dict[int, int] = {}  # цена → индекс уже просмотренного товара
    for j, price in enumerate(prices):
        i = seen.get(total - price)
        if i is not None:
            return i, j
        seen[price] = j
    return None
