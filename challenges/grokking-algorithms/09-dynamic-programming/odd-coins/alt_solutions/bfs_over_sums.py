from collections import deque


def min_coins(amount: int, coins: list[int]) -> int:
    """Минимальное число монет на сумму amount или -1."""
    steps = {0: 0}  # поиск в ширину по суммам: одна монета — одно ребро
    queue = deque([0])
    while queue:
        s = queue.popleft()
        if s == amount:
            return steps[s]
        for c in coins:
            if s + c <= amount and s + c not in steps:
                steps[s + c] = steps[s] + 1
                queue.append(s + c)
    return -1
