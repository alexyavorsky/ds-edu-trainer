def count_inversions(ranks: list[int]) -> int:
    """Число пар i < j, у которых ranks[i] > ranks[j]."""
    return _sort_count(ranks)[1]


def _sort_count(items: list[int]) -> tuple[list[int], int]:
    """Возвращает (отсортированный список, число инверсий в нём)."""
    if len(items) < 2:
        return list(items), 0
    mid = len(items) // 2
    left, a = _sort_count(items[:mid])
    right, b = _sort_count(items[mid:])
    merged: list[int] = []
    split = 0
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            split += len(left) - i  # right[j] меньше всех оставшихся слева
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, a + b + split
