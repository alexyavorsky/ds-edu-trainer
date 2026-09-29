def first_at_least(prices: list[int], budget: int) -> int:
    """Индекс первой цены >= budget в отсортированном списке или len(prices)."""
    low, high = 0, len(prices)  # ответ всегда в диапазоне [low, high]
    while low < high:
        mid = (low + high) // 2
        if ...:  # TODO: условие — цена prices[mid] может быть ответом?
            high = mid
        else:
            low = mid + 1
    return ...  # TODO: что вернуть, когда диапазон сузился до одной точки?
