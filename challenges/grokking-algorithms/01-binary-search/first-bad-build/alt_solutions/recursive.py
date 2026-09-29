from collections.abc import Callable


def first_bad_build(n: int, is_bad: Callable[[int], bool]) -> int:
    """Возвращает номер первой сломанной сборки из 1..n или -1."""
    if not is_bad(n):
        return -1
    return _search(1, n, is_bad)


def _search(low: int, high: int, is_bad: Callable[[int], bool]) -> int:
    """Первая плохая сборка на отрезке [low, high], если high точно плохая."""
    if low == high:
        return low
    mid = (low + high) // 2
    if is_bad(mid):
        return _search(low, mid, is_bad)
    return _search(mid + 1, high, is_bad)
