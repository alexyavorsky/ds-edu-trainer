def first_at_least(prices: list[int], budget: int) -> int:
    """Индекс первой цены >= budget в отсортированном списке или len(prices)."""
    low, high = 0, len(prices) - 1
    answer = len(prices)
    while low <= high:
        mid = (low + high) // 2
        if prices[mid] >= budget:
            answer = mid
            high = mid - 1
        elif prices[mid] < budget:  # лишнее чтение — неэкономно, но верно
            low = mid + 1
    return answer
