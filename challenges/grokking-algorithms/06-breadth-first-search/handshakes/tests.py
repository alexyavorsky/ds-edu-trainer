GRAPH = {
    "Аня": ["Борис", "Вера"],
    "Борис": ["Гоша"],
    "Вера": ["Гоша", "Дина"],
    "Дина": ["Егор"],
}


def test_two_steps():
    """Аня → Гоша: 2 шага"""
    got = handshakes(GRAPH, "Аня", "Гоша")
    assert got == 2, f"ожидалось 2, получено {got!r}"


def test_three_steps():
    """Аня → Егор: 3 шага"""
    got = handshakes(GRAPH, "Аня", "Егор")
    assert got == 3, f"ожидалось 3, получено {got!r}"


def test_same_person():
    """start == goal → 0"""
    got = handshakes(GRAPH, "Вера", "Вера")
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_one_way():
    """Знакомство одностороннее: Гоша → Аня недостижимо"""
    got = handshakes(GRAPH, "Гоша", "Аня")
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_unknown_people():
    """Человека нет в графе как ключа"""
    assert handshakes({}, "Икс", "Игрек") == -1, "в пустом графе пути нет"
    assert handshakes({}, "Икс", "Икс") == 0, "до себя — 0 шагов"


def test_cycle():
    """Цикл в графе не приводит к зависанию"""
    graph = {"a": ["b"], "b": ["c"], "c": ["a", "d"]}
    assert handshakes(graph, "a", "d") == 3, f"получено {handshakes(graph, 'a', 'd')!r}"
    assert handshakes(graph, "a", "z") == -1, f"получено {handshakes(graph, 'a', 'z')!r}"


def test_shortest_not_first_found():
    """Кратчайший путь, даже если длинная ветка идёт первой в списке"""
    graph = {"s": ["a", "t"], "a": ["b"], "b": ["t"]}
    got = handshakes(graph, "s", "t")
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_queue_not_stack():
    """Кратчайший путь 2, хотя обход «вглубь» первой найдёт цепочку длины 3"""
    graph = {"s": ["a", "b"], "b": ["c"], "c": ["t"], "a": ["t"]}
    got = handshakes(graph, "s", "t")
    assert got == 2, f"ожидалось 2 (s → a → t), получено {got!r}"


def test_long_chain():
    """Цепочка из 5000 человек — без переполнения стека"""
    graph = {f"p{i}": [f"p{i + 1}"] for i in range(5000)}
    got = handshakes(graph, "p0", "p5000")
    assert got == 5000, f"ожидалось 5000, получено {got!r}"
