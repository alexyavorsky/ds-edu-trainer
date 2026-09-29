from functools import lru_cache


def edit_distance(a: str, b: str) -> int:
    """Минимальное число вставок, удалений и замен, превращающих a в b."""

    @lru_cache(maxsize=None)
    def dist(i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        if a[i - 1] == b[j - 1]:
            return dist(i - 1, j - 1)
        return 1 + min(dist(i - 1, j), dist(i, j - 1), dist(i - 1, j - 1))

    return dist(len(a), len(b))
