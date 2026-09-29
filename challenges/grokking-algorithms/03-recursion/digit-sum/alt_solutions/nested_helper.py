def digit_sum(n: int) -> int:
    """Возвращает сумму цифр неотрицательного числа n (рекурсивно)."""

    def go(rest: int, acc: int) -> int:
        if rest == 0:
            return acc
        return go(rest // 10, acc + rest % 10)

    return go(n, 0)
