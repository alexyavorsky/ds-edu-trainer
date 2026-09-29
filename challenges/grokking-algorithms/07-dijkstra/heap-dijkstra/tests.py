def test_example():
    """Пример: до b выгоднее через c"""
    graph = {"a": {"b": 7, "c": 2}, "c": {"b": 3}, "b": {"d": 1}}
    got = shortest_costs(graph, "a")
    assert got == {"a": 0, "c": 2, "b": 5, "d": 6}, f"получено {got!r}"


def test_alphabet_trap():
    """Имена узлов не влияют на порядок обработки"""
    graph = {"s": {"a": 10, "z": 1}, "z": {"a": 1}, "a": {"t": 1}}
    got = shortest_costs(graph, "s")
    assert got == {"s": 0, "z": 1, "a": 2, "t": 3}, f"получено {got!r}"


def test_late_improvement():
    """Стоимость узла улучшается после того, как его уже увидели"""
    graph = {"s": {"x": 5, "y": 1}, "y": {"w": 1}, "w": {"x": 1}}
    got = shortest_costs(graph, "s")
    assert got["x"] == 3, f"до x: ожидалось 3, получено {got.get('x')!r}"


def test_single_node():
    """Граф из одного узла"""
    got = shortest_costs({}, "only")
    assert got == {"only": 0}, f"получено {got!r}"


def test_unreachable_not_in_result():
    """Недостижимые узлы в ответ не попадают"""
    graph = {"a": {"b": 1}, "c": {"a": 1}}
    got = shortest_costs(graph, "a")
    assert got == {"a": 0, "b": 1}, f"получено {got!r}"


def test_bigger():
    """Решётка 15×15: заранее посчитанные стоимости до нескольких узлов"""
    graph = {}
    for r in range(15):
        for c in range(15):
            edges = {}
            if r + 1 < 15:
                edges[f"{r + 1}-{c}"] = (r * 7 + c * 3) % 9 + 1
            if c + 1 < 15:
                edges[f"{r}-{c + 1}"] = (r * 5 + c * 11) % 9 + 1
            graph[f"{r}-{c}"] = edges
    expected = {
        "0-1": 1, "1-0": 1, "3-7": 26, "7-3": 37, "7-7": 32, "10-2": 51,
        "2-12": 52, "14-0": 66, "0-14": 70, "11-13": 60, "13-11": 60, "14-14": 73,
    }
    got = shortest_costs(graph, "0-0")
    assert len(got) == 225, f"достижимы все 225 узлов, а в ответе {len(got)}"
    for node, cost in expected.items():
        assert got.get(node) == cost, f"до {node}: ожидалось {cost}, получено {got.get(node)!r}"
