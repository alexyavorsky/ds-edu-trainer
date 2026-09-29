def quicksort_desc(scores: list[int]) -> list[int]:
    """Возвращает новый список, отсортированный по убыванию (быстрая сортировка)."""
    if len(scores) < 2:  # базовый случай
        return list(scores)
    pivot = scores[0]
    greater = [s for s in scores[1:] if s > pivot]
    not_greater = [s for s in scores[1:] if s <= pivot]
    return quicksort_desc(greater) + [pivot] + quicksort_desc(not_greater)
