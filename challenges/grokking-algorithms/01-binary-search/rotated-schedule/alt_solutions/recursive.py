def find_departure(times: list[int], target: int) -> int:
    """Индекс target в циклически сдвинутом отсортированном списке или -1."""
    return _search(times, target, 0, len(times) - 1)


def _search(times: list[int], target: int, low: int, high: int) -> int:
    if low > high:
        return -1
    mid = (low + high) // 2
    if times[mid] == target:
        return mid
    if times[low] <= times[mid]:
        if times[low] <= target < times[mid]:
            return _search(times, target, low, mid - 1)
        return _search(times, target, mid + 1, high)
    if times[mid] < target <= times[high]:
        return _search(times, target, mid + 1, high)
    return _search(times, target, low, mid - 1)
