def letters(text: str) -> str:
    """Строка без пробелов в нижнем регистре."""
    return text.replace(" ", "").lower()


def is_anagram(a: str, b: str) -> bool:
    """True, если a и b состоят из одних и тех же букв (без учёта регистра и пробелов)."""
    counts: dict[str, int] = {}
    for ch in letters(a):
        # TODO: увеличьте счётчик буквы ch
        pass
    for ch in letters(b):
        # TODO: уменьшите счётчик; если буквы нет или счётчик ушёл в минус — верните False
        pass
    # TODO: все ли счётчики вернулись к нулю?
    return True
