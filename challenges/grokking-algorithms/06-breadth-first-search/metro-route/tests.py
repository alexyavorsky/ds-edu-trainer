LINES = {
    "Парк": ["Музей", "Вокзал"],
    "Музей": ["Театр"],
    "Вокзал": ["Рынок"],
    "Рынок": ["Театр", "Порт"],
}


def _check(lines, start, goal, expected):
    """expected — длина кратчайшего пути в перегонах (заранее посчитана) или None, если пути нет."""
    got = route(lines, start, goal)
    if expected is None:
        assert got is None, f"{start} → {goal}: пути нет, ожидалось None, получено {got!r}"
        return
    assert isinstance(got, list) and got, f"{start} → {goal}: ожидался список станций, получено {got!r}"
    assert got[0] == start and got[-1] == goal, f"путь должен начинаться в {start} и кончаться в {goal}: {got}"
    for a, b in zip(got, got[1:]):
        assert b in lines.get(a, []), f"между {a} и {b} нет перегона: {got}"
    assert len(got) - 1 == expected, f"перегонов {len(got) - 1}, а кратчайший путь — {expected}: {got}"


def test_example():
    """Парк → Театр через Музей (2 перегона)"""
    _check(LINES, "Парк", "Театр", 2)


def test_same_station():
    """start == goal → [start]"""
    got = route(LINES, "Парк", "Парк")
    assert got == ["Парк"], f"получено {got!r}"


def test_no_route():
    """Пути нет → None"""
    _check(LINES, "Порт", "Парк", None)


def test_longer_route():
    """Парк → Порт (3 перегона)"""
    _check(LINES, "Парк", "Порт", 3)


def test_unknown_start():
    """Станции нет среди ключей"""
    assert route({}, "А", "Б") is None, "в пустой схеме пути нет"


def test_cycle_and_several_shortest():
    """Циклы и несколько кратчайших путей"""
    lines = {"a": ["b", "c"], "b": ["d", "a"], "c": ["d"], "d": ["e", "a"], "e": []}
    _check(lines, "a", "e", 3)
    _check(lines, "d", "c", 2)


def test_grid():
    """Решётка 30×30: путь из угла в угол"""
    lines = {}
    for r in range(30):
        for c in range(30):
            nb = []
            if r + 1 < 30:
                nb.append(f"{r + 1},{c}")
            if c + 1 < 30:
                nb.append(f"{r},{c + 1}")
            lines[f"{r},{c}"] = nb
    _check(lines, "0,0", "29,29", 58)
