def edit_distance(a: str, b: str) -> int:
    """Минимальное число вставок, удалений и замен, превращающих a в b."""
    memo: dict[tuple[int, int], int] = {}

    def dist(i: int, j: int) -> int:
        if (i, j) in memo:
            return memo[(i, j)]
        if i == 0 or j == 0:
            result = i + j
        elif a[i - 1] == b[j - 1]:
            result = dist(i - 1, j - 1)
        else:
            result = 1 + min(dist(i - 1, j), dist(i, j - 1), dist(i - 1, j - 1))
        memo[(i, j)] = result
        return result

    return dist(len(a), len(b))
