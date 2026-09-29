def first_at_least(prices: list[int], budget: int) -> int:
    """Индекс первой цены >= budget в отсортированном списке или len(prices)."""
    return _search(prices, budget, 0, len(prices))


def _search(prices: list[int], budget: int, low: int, high: int) -> int:
    if low == high:
        return low
    mid = (low + high) // 2
    if prices[mid] >= budget:
        return _search(prices, budget, low, mid)
    return _search(prices, budget, mid + 1, high)
