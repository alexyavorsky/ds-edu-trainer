def count_inversions(ranks: list[int]) -> int:
    """Число пар i < j, у которых ranks[i] > ranks[j]."""
    _, count = sort_and_count(ranks)
    return count


def sort_and_count(items: list[int]) -> tuple[list[int], int]:
    if len(items) <= 1:
        return items[:], 0
    half = len(items) // 2
    left, a = sort_and_count(items[:half])
    right, b = sort_and_count(items[half:])
    merged, c = merge_and_count(left, right)
    return merged, a + b + c


def merge_and_count(left: list[int], right: list[int]) -> tuple[list[int], int]:
    merged, count, i, j = [], 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j] or left[i] == right[j]:  # лишнее сравнение — неэкономно, но верно
            merged.append(left[i])
            i += 1
        elif left[i] > right[j]:
            merged.append(right[j])
            count += len(left) - i
            j += 1
    merged += left[i:] + right[j:]
    return merged, count
