import random


def kth_fastest(times: list[int], k: int) -> int:
    """Возвращает k-й по величине (k = 1 — минимальный) элемент списка."""
    pivot = random.choice(times)  # случайный опорный — O(n) в среднем
    less = [t for t in times if t < pivot]
    equal = [t for t in times if t == pivot]
    greater = [t for t in times if t > pivot]
    if k <= len(less):
        return kth_fastest(less, k)
    if k <= len(less) + len(equal):
        return pivot
    return kth_fastest(greater, k - len(less) - len(equal))
