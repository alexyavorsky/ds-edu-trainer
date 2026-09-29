def find_term(terms: list[str], term: str) -> int | None:
    """Возвращает индекс term в отсортированном списке terms или None."""
    low, high = 0, len(terms) - 1
    while low <= high:
        mid = (low + high) // 2
        guess = terms[mid]
        if guess == term:
            return mid
        if guess < term:
            low = mid + 1  # искомое правее середины
        else:
            high = mid - 1  # искомое левее середины
    return None
