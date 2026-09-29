def _is_subsequence(s, text):
    it = iter(text)
    return all(ch in it for ch in s)


def _check(a, b, best):
    """best — длина самой длинной общей подпоследовательности (заранее посчитана)."""
    got = lcs(a, b)
    assert isinstance(got, str), f"ожидалась строка, получено {got!r}"
    assert _is_subsequence(got, a), f"{got!r} — не подпоследовательность {a!r}"
    assert _is_subsequence(got, b), f"{got!r} — не подпоследовательность {b!r}"
    assert len(got) == best, f"{a!r}/{b!r}: длина {len(got)}, а можно {best}: {got!r}"


def test_identical():
    """Одинаковые строки → сама строка"""
    got = lcs("abc", "abc")
    assert got == "abc", f"ожидалось 'abc', получено {got!r}"


def test_example_russian():
    """рыбак и бирка"""
    _check("рыбак", "бирка", 2)


def test_classic():
    """abcbdab и bdcaba → длина 4"""
    _check("abcbdab", "bdcaba", 4)


def test_empty_and_disjoint():
    """Пустая строка и строки без общих символов → ''"""
    assert lcs("", "abc") == "", "с пустой строкой — ''"
    assert lcs("abc", "xyz") == "", "без общих символов — ''"


def test_one_inside_other():
    """Одна строка — подпоследовательность другой"""
    got = lcs("axbycz", "abc")
    assert got == "abc", f"ожидалось 'abc', получено {got!r}"


def test_many_pairs():
    """Разные пары строк"""
    pairs = [("programming", "gaming", 6), ("ACCGGTCGAG", "GTCGTTCGGA", 6), ("aaab", "abbb", 2), ("xyzxyz", "zyxzyx", 3)]
    for a, b, best in pairs:
        _check(a, b, best)
