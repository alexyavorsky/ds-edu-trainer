def test_example():
    """CDEFGAB и CEGBD → 4"""
    got = common_motif_length("CDEFGAB", "CEGBD")
    assert got == 4, f"ожидалось 4, получено {got!r}"


def test_repeats():
    """AAAA и AA → 2"""
    got = common_motif_length("AAAA", "AA")
    assert got == 2, f"ожидалось 2, получено {got!r}"


def test_nothing_common():
    """Нет общих нот → 0"""
    got = common_motif_length("CDE", "FGA")
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_empty():
    """Пустая мелодия → 0"""
    assert common_motif_length("", "CDE") == 0, "пустая a"
    assert common_motif_length("CDE", "") == 0, "пустая b"
    assert common_motif_length("", "") == 0, "обе пустые"


def test_identical():
    """Одинаковые мелодии → длина мелодии"""
    got = common_motif_length("GABCD", "GABCD")
    assert got == 5, f"ожидалось 5, получено {got!r}"


def test_not_contiguous():
    """Подпоследовательность не обязана идти подряд"""
    got = common_motif_length("CXDXE", "CDE")
    assert got == 3, f"ожидалось 3, получено {got!r}"


def test_symmetric():
    """Порядок аргументов не важен"""
    a, b = "ABCBDAB", "BDCABA"
    assert common_motif_length(a, b) == common_motif_length(b, a) == 4, "ожидалось 4 в обе стороны"
