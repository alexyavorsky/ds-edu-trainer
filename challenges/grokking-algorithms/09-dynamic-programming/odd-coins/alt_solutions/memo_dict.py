def min_coins(amount: int, coins: list[int]) -> int:
    """Минимальное число монет на сумму amount или -1."""
    memo: dict[int, float] = {0: 0}

    def best(s: int) -> float:
        if s not in memo:
            options = [best(s - c) + 1 for c in coins if c <= s]
            memo[s] = min(options, default=float("inf"))
        return memo[s]

    result = best(amount)
    return -1 if result == float("inf") else int(result)
