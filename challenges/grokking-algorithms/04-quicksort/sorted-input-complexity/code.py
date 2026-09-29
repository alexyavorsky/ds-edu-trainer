def quicksort(items: list[int]) -> list[int]:
    if len(items) < 2:
        return items
    mid = len(items) // 2
    pivot = items[mid]
    rest = items[:mid] + items[mid + 1:]
    less = [x for x in rest if x <= pivot]
    greater = [x for x in rest if x > pivot]
    return quicksort(less) + [pivot] + quicksort(greater)
