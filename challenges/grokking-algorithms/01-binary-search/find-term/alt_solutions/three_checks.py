def find_term(terms: list[str], term: str) -> int | None:
    """Возвращает индекс term в отсортированном списке terms или None."""
    low = 0
    high = len(terms)  # полуинтервал [low, high)
    while low < high:
        mid = low + (high - low) // 2
        if terms[mid] < term:
            low = mid + 1
        elif terms[mid] > term:
            high = mid
        elif terms[mid] == term:
            return mid
    return None
