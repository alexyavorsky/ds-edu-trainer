from functools import cache


def min_coins(amount: int, coins: list[int]) -> int:
    """Минимальное число монет на сумму amount или -1."""

    @cache
    def best(s: int) -> float:
        if s == 0:
            return 0
        return min((best(s - c) + 1 for c in coins if c <= s), default=float("inf"))

    result = best(amount)
    return -1 if result == float("inf") else int(result)
