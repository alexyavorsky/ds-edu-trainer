def make_change(amount: int, coins: list[int]) -> list[int]:
    """Монеты на сумму amount, выбранные жадно (сначала крупные)."""
    result = []
    while amount > 0:
        coin = max(c for c in coins if c <= amount)  # самая крупная подходящая
        result.append(coin)
        amount -= coin
    return result
