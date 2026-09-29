def test_example():
    """«Листопад» и «Спад толи» — анаграммы"""
    got = is_anagram("Листопад", "Спад толи")
    assert got is True, f"ожидалось True, получено {got!r}"


def test_simple_true():
    """«кот» и «ток»"""
    got = is_anagram("кот", "ток")
    assert got is True, f"ожидалось True, получено {got!r}"


def test_extra_letters():
    """Во второй строке лишние буквы → False"""
    got = is_anagram("кот", "коты")
    assert got is False, f"ожидалось False, получено {got!r}"


def test_missing_letters():
    """Во второй строке не хватает букв → False"""
    got = is_anagram("коты", "кот")
    assert got is False, f"ожидалось False, получено {got!r}"


def test_same_letters_different_counts():
    """Те же буквы, но в разном количестве → False"""
    got = is_anagram("aab", "abb")
    assert got is False, f"ожидалось False, получено {got!r}"


def test_empty():
    """Две пустые строки (или одни пробелы) — анаграммы"""
    assert is_anagram("", "") is True, "is_anagram('', '') должно быть True"
    assert is_anagram("  ", "") is True, "пробелы не учитываются"


def test_case_and_spaces():
    """Регистр и пробелы не важны"""
    got = is_anagram("Dormitory", "dirty room")
    assert got is True, f"ожидалось True, получено {got!r}"


def test_hyphen_counts():
    """Прочие символы учитываются: «кот» и «кто-то» — не анаграммы"""
    got = is_anagram("кот", "кто-то")
    assert got is False, f"ожидалось False, получено {got!r}"
