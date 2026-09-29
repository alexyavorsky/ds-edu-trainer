def test_same():
    """Одинаковые слова → 0"""
    got = edit_distance("кошка", "кошка")
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_one_substitution():
    """Одна замена: кошка → мошка = 1"""
    got = edit_distance("кошка", "мошка")
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_insert_and_delete():
    """Вставка и удаление: кот → крот = 1, крот → кот = 1"""
    got = edit_distance("кот", "крот")
    assert got == 1, f"кот → крот: ожидалось 1, получено {got!r}"
    got = edit_distance("крот", "кот")
    assert got == 1, f"крот → кот: ожидалось 1, получено {got!r}"


def test_empty():
    """Пустые строки: '' → abc = 3, abc → '' = 3, '' → '' = 0"""
    for a, b, expected in [("", "abc", 3), ("abc", "", 3), ("", "", 0)]:
        got = edit_distance(a, b)
        assert got == expected, f"edit_distance({a!r}, {b!r}): ожидалось {expected}, получено {got!r}"


def test_single_chars():
    """Строки из одного символа: a → a = 0, a → b = 1"""
    assert edit_distance("a", "a") == 0, f"a → a: получено {edit_distance('a', 'a')!r}"
    assert edit_distance("a", "b") == 1, f"a → b: получено {edit_distance('a', 'b')!r}"


def test_classic():
    """kitten → sitting = 3, алгоритм → логарифм = 4, sunday → saturday = 3"""
    for a, b, expected in [("kitten", "sitting", 3), ("алгоритм", "логарифм", 4), ("sunday", "saturday", 3)]:
        got = edit_distance(a, b)
        assert got == expected, f"{a} → {b}: ожидалось {expected}, получено {got!r}"


def test_repeated_letters():
    """Повторяющиеся буквы: aaaa → aa = 2, abab → baba = 2"""
    for a, b, expected in [("aaaa", "aa", 2), ("abab", "baba", 2)]:
        got = edit_distance(a, b)
        assert got == expected, f"{a} → {b}: ожидалось {expected}, получено {got!r}"


def test_symmetric():
    """Расстояние симметрично"""
    for a, b in [("sunday", "saturday"), ("abc", "cab"), ("aaaa", "b")]:
        forward, backward = edit_distance(a, b), edit_distance(b, a)
        assert forward == backward, f"{a!r} → {b!r} = {forward!r}, а обратно = {backward!r}"


def test_long_strings():
    """Строки по 150 символов: верные ответы за отведённое время"""
    a = "".join(chr(ord("a") + (i * 7) % 26) for i in range(150))
    b = "".join(chr(ord("a") + (i * 11) % 26) for i in range(150))
    c = "".join(chr(ord("a") + (i * i + 3 * i) % 26) for i in range(150))
    for x, y, expected in [(a, b, 138), (a, c, 133), (a, a[:75], 75)]:
        got = edit_distance(x, y)
        assert got == expected, f"строки длины {len(x)} и {len(y)}: ожидалось {expected}, получено {got!r}"


test_long_strings.timeout = 10
test_long_strings.timeout_hint = "Если это рекурсия, добавьте запоминание: без него одни и те же подзадачи считаются заново"
