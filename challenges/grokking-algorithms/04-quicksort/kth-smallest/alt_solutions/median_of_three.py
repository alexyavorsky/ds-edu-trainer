def kth_fastest(times: list[int], k: int) -> int:
    """Возвращает k-й по величине (k = 1 — минимальный) элемент списка."""
    if len(times) == 1:
        return times[0]
    a, b, c = times[0], times[len(times) // 2], times[-1]
    pivot = a + b + c - min(a, b, c) - max(a, b, c)  # медиана трёх
    less = [t for t in times if t < pivot]
    equal = [t for t in times if t == pivot]
    if k <= len(less):
        return kth_fastest(less, k)
    if k <= len(less) + len(equal):
        return pivot
    return kth_fastest([t for t in times if t > pivot], k - len(less) - len(equal))
