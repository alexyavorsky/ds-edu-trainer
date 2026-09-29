def min_coins(amount: int, coins: list[int]) -> int:
    """Минимальное число монет на сумму amount или -1."""
    impossible = amount + 1  # больше монет не понадобится никогда
    best = [0] + [impossible] * amount
    for s in range(1, amount + 1):
        for c in coins:
            if c <= s and best[s - c] + 1 < best[s]:
                best[s] = best[s - c] + 1
    return best[amount] if best[amount] != impossible else -1
