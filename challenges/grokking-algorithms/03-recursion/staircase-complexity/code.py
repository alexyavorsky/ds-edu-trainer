def bricks(n: int) -> int:
    if n == 0:
        return 0
    step = 0
    for _ in range(n):  # укладываем ступень из n кирпичей по одному
        step += 1
    return step + bricks(n - 1)
