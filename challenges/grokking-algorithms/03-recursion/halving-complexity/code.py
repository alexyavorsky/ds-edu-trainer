def halvings(n: int) -> int:
    if n <= 1:
        return 0
    return 1 + halvings(n // 2)
