def find_departure(times: list[int], target: int) -> int:
    """Индекс target в циклически сдвинутом отсортированном списке или -1."""
    if not times:
        return -1
    # 1. бинарным поиском находим начало (самый ранний рейс)
    low, high = 0, len(times) - 1
    while low < high:
        mid = (low + high) // 2
        if times[mid] > times[high]:
            low = mid + 1
        else:
            high = mid
    start = low
    # 2. обычный бинарный поиск в «развёрнутом» списке через сдвиг индексов
    n = len(times)
    low, high = 0, n - 1
    while low <= high:
        mid = (low + high) // 2
        real = (mid + start) % n
        if times[real] == target:
            return real
        if times[real] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1
