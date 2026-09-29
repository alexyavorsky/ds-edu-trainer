def find_term(terms: list[str], term: str) -> int | None:
    """Возвращает индекс term в отсортированном списке terms или None."""
    low, high = 0, len(terms) - 1
    while low <= high:
        mid = (low + high) // 2
        if terms[mid] == term:
            return mid
        elif terms[mid] < term:
            low = mid + 1
        else:
            high = mid - 1
    return None
