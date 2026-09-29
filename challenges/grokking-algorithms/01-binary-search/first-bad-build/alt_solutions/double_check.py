from collections.abc import Callable


def first_bad_build(n: int, is_bad: Callable[[int], bool]) -> int:
    """Возвращает номер первой сломанной сборки из 1..n или -1."""
    low, high = 1, n
    while low <= high:
        mid = (low + high) // 2
        if is_bad(mid):
            if mid == 1 or not is_bad(mid - 1):  # второй вызов на шаге — неэкономно, но верно
                return mid
            high = mid - 1
        else:
            low = mid + 1
    return -1
