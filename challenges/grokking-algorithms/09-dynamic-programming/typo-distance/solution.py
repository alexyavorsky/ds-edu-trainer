def edit_distance(a: str, b: str) -> int:
    """Минимальное число вставок, удалений и замен, превращающих a в b."""
    n, m = len(a), len(b)
    table = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        table[i][0] = i  # удалить все i символов
    for j in range(m + 1):
        table[0][j] = j  # вставить все j символов
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = 1 + min(table[i - 1][j], table[i][j - 1], table[i - 1][j - 1])
    return table[n][m]
