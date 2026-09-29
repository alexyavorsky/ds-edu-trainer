def frosty_days(temps: list[int], low: int, high: int) -> int:
    if low > high:
        return 0
    if low == high:
        return 1 if temps[low] < 0 else 0
    mid = (low + high) // 2
    return frosty_days(temps, low, mid) + frosty_days(temps, mid + 1, high)
