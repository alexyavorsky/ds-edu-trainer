def find_release(versions: list[int], target: int) -> int:
    """Возвращает индекс target в отсортированном списке versions или -1."""
    low = 0
    high = len(versions) - 1
    while low < high:
        mid = (low + high) // 2
        guess = versions[mid]
        if guess == target:
            return mid
        if guess < target:
            low = mid + 1
        else:
            high = mid - 1
    return low
