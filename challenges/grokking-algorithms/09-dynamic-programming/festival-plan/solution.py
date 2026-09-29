def plan_festival(shows: list[tuple[str, int, int]], hours: int) -> list[int]:
    """Индексы выступлений с максимальным рейтингом, помещающихся в hours."""
    n = len(shows)
    table = [[0] * (hours + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, time, rating = shows[i - 1]
        for t in range(hours + 1):
            table[i][t] = table[i - 1][t]
            if time <= t:
                table[i][t] = max(table[i][t], table[i - 1][t - time] + rating)
    chosen = []
    t = hours
    for i in range(n, 0, -1):
        if table[i][t] != table[i - 1][t]:  # выступление i − 1 вошло в оптимум
            chosen.append(i - 1)
            t -= shows[i - 1][1]
    return chosen[::-1]
