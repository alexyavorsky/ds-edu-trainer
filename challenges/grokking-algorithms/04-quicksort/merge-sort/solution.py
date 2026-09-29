def merge(left: list[int], right: list[int]) -> list[int]:
    """Сливает два отсортированных списка в один отсортированный."""
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(items: list[int]) -> list[int]:
    """Возвращает новый отсортированный список (сортировка слиянием)."""
    if len(items) < 2:
        return list(items)
    mid = len(items) // 2
    return merge(merge_sort(items[:mid]), merge_sort(items[mid:]))
