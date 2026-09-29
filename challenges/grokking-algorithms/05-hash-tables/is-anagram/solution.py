def letters(text: str) -> str:
    """Строка без пробелов в нижнем регистре."""
    return text.replace(" ", "").lower()


def is_anagram(a: str, b: str) -> bool:
    """True, если a и b состоят из одних и тех же букв (без учёта регистра и пробелов)."""
    counts: dict[str, int] = {}
    for ch in letters(a):
        counts[ch] = counts.get(ch, 0) + 1
    for ch in letters(b):
        counts[ch] = counts.get(ch, 0) - 1
        if counts[ch] < 0:
            return False
    return all(c == 0 for c in counts.values())
