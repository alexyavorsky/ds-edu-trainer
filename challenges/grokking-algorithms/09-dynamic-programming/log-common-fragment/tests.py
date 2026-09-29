def test_example_logs():
    """Логи: общий фрагмент «: disk » длины 7"""
    got = common_fragment_length("error: disk full", "warning: disk quota")
    assert got == 7, f"ожидалось 7, получено {got!r}"


def test_rotation():
    """abcx и xabc → 3"""
    got = common_fragment_length("abcx", "xabc")
    assert got == 3, f"ожидалось 3, получено {got!r}"


def test_scattered_is_not_substring():
    """Общие буквы вразброс — это не подстрока: axbxc и abc → 1"""
    got = common_fragment_length("axbxc", "abc")
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_empty():
    """Пустая строка → 0"""
    assert common_fragment_length("", "abc") == 0, "пустая a"
    assert common_fragment_length("abc", "") == 0, "пустая b"


def test_nothing_common():
    """Нет общих символов → 0"""
    got = common_fragment_length("abc", "xyz")
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_identical():
    """Одинаковые строки → длина строки"""
    got = common_fragment_length("timeout", "timeout")
    assert got == 7, f"ожидалось 7, получено {got!r}"


def test_more_pairs():
    """Ещё четыре пары строк — заранее посчитанные ответы"""
    pairs = [("mississippi", "missouri", 4), ("banana", "ananas", 5), ("abcdef", "zcdemf", 3), ("aaaa", "aa", 2)]
    for a, b, expected in pairs:
        got = common_fragment_length(a, b)
        assert got == expected, f"{a!r} и {b!r}: ожидалось {expected}, получено {got!r}"
