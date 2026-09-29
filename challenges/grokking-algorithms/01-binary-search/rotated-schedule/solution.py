def find_departure(times: list[int], target: int) -> int:
    """Индекс target в циклически сдвинутом отсортированном списке или -1."""
    low, high = 0, len(times) - 1
    while low <= high:
        mid = (low + high) // 2
        middle = times[mid]
        if middle == target:
            return mid
        first, last = times[low], times[high]
        if first <= middle:  # левая половина [low, mid] отсортирована
            if first <= target < middle:
                high = mid - 1
            else:
                low = mid + 1
        else:  # правая половина [mid, high] отсортирована
            if middle < target <= last:
                low = mid + 1
            else:
                high = mid - 1
    return -1
