def quicksort_desc(scores: list[int]) -> list[int]:
    """Возвращает новый список, отсортированный по убыванию (быстрая сортировка)."""
    if len(scores) <= 1:
        return scores[:]
    pivot = scores[len(scores) // 2]
    greater = [s for s in scores if s > pivot]
    equal = [s for s in scores if s == pivot]
    less = [s for s in scores if s < pivot]
    return quicksort_desc(greater) + equal + quicksort_desc(less)
