def find_term(terms: list[str], term: str) -> int | None:
    """Возвращает индекс term в отсортированном списке terms или None."""
    return _search(terms, term, 0, len(terms) - 1)


def _search(terms: list[str], term: str, low: int, high: int) -> int | None:
    if low > high:
        return None
    mid = (low + high) // 2
    if terms[mid] == term:
        return mid
    if terms[mid] > term:
        return _search(terms, term, low, mid - 1)
    return _search(terms, term, mid + 1, high)
