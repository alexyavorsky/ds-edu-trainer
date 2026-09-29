def sort_scores(scores: list[int]) -> list[int]:
    """Возвращает новый список оценок по возрастанию (быстрая сортировка)."""
    if len(scores) < 2:
        return list(scores)
    pivot = scores[0]
    less = [s for s in scores[1:] if s < pivot]
    greater = [s for s in scores[1:] if s >= pivot]
    return sort_scores(less) + [pivot] + sort_scores(greater)
