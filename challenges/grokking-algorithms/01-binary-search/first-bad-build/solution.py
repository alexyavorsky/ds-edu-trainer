from collections.abc import Callable


def first_bad_build(n: int, is_bad: Callable[[int], bool]) -> int:
    """Возвращает номер первой сломанной сборки из 1..n или -1."""
    low, high = 1, n + 1  # n + 1 означает «сломанных нет»
    while low < high:
        mid = (low + high) // 2
        if is_bad(mid):
            high = mid  # mid может быть ответом
        else:
            low = mid + 1  # ответ строго правее
    return low if low <= n else -1
