def pair_for_card(prices: list[int], total: int) -> tuple[int, int] | None:
    """Индексы (i, j), i < j, с prices[i] + prices[j] == total, или None."""
    values = list(prices)  # один проход-копия, дальше работаем с копией
    order = sorted(range(len(values)), key=lambda i: values[i])
    left, right = 0, len(order) - 1
    while left < right:
        s = values[order[left]] + values[order[right]]
        if s == total:
            i, j = order[left], order[right]
            return (i, j) if i < j else (j, i)
        if s < total:
            left += 1
        else:
            right -= 1
    return None
