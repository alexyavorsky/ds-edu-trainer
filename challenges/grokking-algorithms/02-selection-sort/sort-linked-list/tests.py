def _build(values: list[int]) -> Node | None:
    head = None
    for v in reversed(values):
        head = Node(v, head)
    return head


def _nodes(head: Node | None) -> list[Node]:
    nodes = []
    while head is not None:
        nodes.append(head)
        assert len(nodes) <= 10_000, "в списке цикл — у какого-то узла не обнулён next"
        head = head.next
    return nodes


def _check(values: list[int]) -> None:
    head = _build(values)
    original = _nodes(head)
    result = _nodes(sort_nodes(head))
    got = [n.value for n in result]
    expected = sorted(values)
    assert got == expected, f"{values}: получено {got}, ожидалось {expected}"
    assert len(result) == len(original), f"узлов было {len(original)}, стало {len(result)}"
    ids = {id(n) for n in original}
    assert all(id(n) in ids for n in result), "в результате есть новые узлы — нужно переставлять старые"
    # равные значения — в исходном порядке
    position = {id(n): i for i, n in enumerate(original)}
    for a, b in zip(result, result[1:]):
        if a.value == b.value:
            assert position[id(a)] < position[id(b)], f"равные значения {a.value} поменялись местами"


def test_example():
    """Пример: 4 → 1 → 3 → 1"""
    _check([4, 1, 3, 1])


def test_empty():
    """Пустой список → None"""
    got = sort_nodes(None)
    assert got is None, f"ожидалось None, получено {got!r}"


def test_single():
    """Один узел"""
    _check([9])


def test_sorted_and_reverse():
    """Уже отсортированный и обратный порядок"""
    _check([1, 2, 3, 4, 5])
    _check([5, 4, 3, 2, 1])


def test_min_in_the_middle_and_end():
    """Минимум в середине и в хвосте"""
    _check([5, 6, 0, 7, 8])
    _check([5, 6, 7, 8, 0])


def test_duplicates_stable():
    """Много равных значений — порядок равных сохраняется"""
    _check([2, 1, 2, 1, 2, 1, 0, 2])


def test_all_equal():
    """Все значения одинаковые"""
    _check([3, 3, 3, 3])


def test_longer():
    """200 узлов"""
    _check([(i * 71) % 97 for i in range(200)])
