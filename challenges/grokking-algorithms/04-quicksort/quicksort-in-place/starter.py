def partition(items: list[int], low: int, high: int) -> int:
    """Разбивает items[low..high] вокруг items[high], возвращает позицию опорного."""
    pivot = items[high]
    i = low  # граница: items[low..i-1] < pivot
    for j in range(low, high):
        if items[j] < pivot:
            items[i], items[j] = items[j], items[i]
            i += 1
    return i


def quicksort_in_place(items: list[int], low: int = 0, high: int | None = None) -> None:
    """Сортирует items[low..high] на месте."""
    if high is None:
        high = len(items) - 1
    if low >= high:
        return
    p = partition(items, low, high)
    quicksort_in_place(items, low, p)
    quicksort_in_place(items, p + 1, high)
