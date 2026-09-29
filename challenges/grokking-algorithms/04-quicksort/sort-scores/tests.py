def test_example():
    """Пример: [4, 2, 5, 2, 3] → [2, 2, 3, 4, 5]"""
    got = sort_scores([4, 2, 5, 2, 3])
    assert got == [2, 2, 3, 4, 5], f"получено {got!r}"


def test_single():
    """Одна оценка → та же оценка"""
    got = sort_scores([5])
    assert got == [5], f"получено {got!r}"


def test_empty():
    """Пустой список → []"""
    got = sort_scores([])
    assert got == [], f"получено {got!r}"


def test_two():
    """Две оценки в обратном порядке"""
    got = sort_scores([5, 3])
    assert got == [3, 5], f"получено {got!r}"


def test_all_equal():
    """Все оценки одинаковые — ни одна не теряется"""
    got = sort_scores([4, 4, 4, 4])
    assert got == [4, 4, 4, 4], f"получено {got!r}"


def test_length_preserved():
    """Длина результата равна длине входа"""
    data = [3, 5, 2, 4, 5, 3, 2, 5]
    got = sort_scores(data)
    assert len(got) == len(data), f"было {len(data)} оценок, стало {len(got)}: {got!r}"
    assert got == sorted(data), f"получено {got!r}"
