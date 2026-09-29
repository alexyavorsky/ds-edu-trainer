def _check(prereqs: dict[str, list[str]]) -> None:
    got = study_order(prereqs)
    courses = set(prereqs) | {c for needs in prereqs.values() for c in needs}
    assert isinstance(got, list), f"ожидался список курсов, получено {got!r}"
    assert sorted(got) == sorted(courses), f"каждый курс должен встретиться ровно один раз: {got}"
    position = {c: i for i, c in enumerate(got)}
    for course, needs in prereqs.items():
        for need in needs:
            assert position[need] < position[course], f"«{need}» должен идти раньше «{course}»: {got}"


def test_example():
    """Пример из условия"""
    _check({"Алгоритмы": ["Python", "Дискретка"], "Python": [], "ML": ["Алгоритмы", "Статистика"]})


def test_cycle_two():
    """Цикл из двух курсов → None"""
    got = study_order({"A": ["B"], "B": ["A"]})
    assert got is None, f"ожидалось None, получено {got!r}"


def test_cycle_deep():
    """Цикл глубоко в плане → None"""
    got = study_order({"A": [], "B": ["A"], "C": ["B", "E"], "D": ["C"], "E": ["D"]})
    assert got is None, f"ожидалось None, получено {got!r}"


def test_self_loop():
    """Курс требует сам себя → None"""
    got = study_order({"A": ["A"]})
    assert got is None, f"ожидалось None, получено {got!r}"


def test_empty():
    """Пустой план → []"""
    got = study_order({})
    assert got == [], f"ожидалось [], получено {got!r}"


def test_independent():
    """Курсы без требований — любой порядок"""
    _check({"A": [], "B": [], "C": []})


def test_diamond_and_duplicates_in_values():
    """«Ромб» зависимостей: общий пререквизит у двух веток"""
    _check({"D": ["B", "C"], "B": ["A"], "C": ["A"]})


def test_long_chain():
    """Цепочка из 20 000 курсов — без переполнения стека"""
    prereqs = {f"c{i}": [f"c{i - 1}"] for i in range(1, 20_000)}
    _check(prereqs)
