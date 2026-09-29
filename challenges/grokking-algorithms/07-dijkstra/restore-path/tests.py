PARENTS = {"B": "start", "A": "B", "fin": "A", "C": "start"}


def test_example():
    """Пример: start → B → A → fin"""
    got = restore_path(PARENTS, "start", "fin")
    assert got == ["start", "B", "A", "fin"], f"получено {got!r}"


def test_one_edge():
    """Путь из одного ребра"""
    got = restore_path(PARENTS, "start", "C")
    assert got == ["start", "C"], f"получено {got!r}"


def test_same():
    """goal == start → [start]"""
    got = restore_path(PARENTS, "start", "start")
    assert got == ["start"], f"получено {got!r}"


def test_unreachable():
    """goal нет в таблице → []"""
    got = restore_path(PARENTS, "start", "X")
    assert got == [], f"получено {got!r}"


def test_empty_table():
    """Пустая таблица"""
    assert restore_path({}, "s", "s") == ["s"], "до себя путь из одного узла"
    assert restore_path({}, "s", "t") == [], "без таблицы до t не добраться"


def test_long_chain():
    """Цепочка из 1000 узлов"""
    parents = {f"n{i}": f"n{i - 1}" for i in range(1, 1000)}
    got = restore_path(parents, "n0", "n999")
    assert got == [f"n{i}" for i in range(1000)], f"начало: {got[:3]}, конец: {got[-3:]}"
