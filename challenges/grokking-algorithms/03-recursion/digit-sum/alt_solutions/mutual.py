def digit_sum(n: int) -> int:
    """Возвращает сумму цифр неотрицательного числа n (рекурсивно)."""
    if n == 0:
        return 0
    return last_digit_plus_rest(n)


def last_digit_plus_rest(n: int) -> int:
    rest, last = divmod(n, 10)
    return last + digit_sum(rest)
