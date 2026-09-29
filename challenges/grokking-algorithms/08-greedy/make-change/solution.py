def make_change(amount: int, coins: list[int]) -> list[int]:
    """Монеты на сумму amount, выбранные жадно (сначала крупные)."""
    result: list[int] = []
    for coin in sorted(coins, reverse=True):
        count, amount = divmod(amount, coin)
        result.extend([coin] * count)
    return result
