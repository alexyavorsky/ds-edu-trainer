from functools import lru_cache


def plan_festival(shows: list[tuple[str, int, int]], hours: int) -> list[int]:
    """Индексы выступлений с максимальным рейтингом, помещающихся в hours."""

    @lru_cache(maxsize=None)
    def best(i: int, left: int) -> int:
        """Лучший рейтинг из выступлений i, i+1, … при left свободных часах."""
        if i == len(shows):
            return 0
        skip = best(i + 1, left)
        _, time, rating = shows[i]
        take = rating + best(i + 1, left - time) if time <= left else -1
        return max(skip, take)

    chosen, left = [], hours
    for i in range(len(shows)):
        if best(i, left) != best(i + 1, left):  # без i результат хуже — значит, i взято
            chosen.append(i)
            left -= shows[i][1]
    return chosen
