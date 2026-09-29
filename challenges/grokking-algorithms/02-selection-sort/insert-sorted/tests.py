def _build(values: list[int]) -> Node | None:
    head = None
    for v in reversed(values):
        head = Node(v, head)
    return head


def _nodes(head: Node | None) -> list[Node]:
    nodes = []
    while head is not None:
        nodes.append(head)
        assert len(nodes) <= 10_000, "в списке цикл"
        head = head.next
    return nodes


def _values(head: Node | None) -> list[int]:
    return [n.value for n in _nodes(head)]


def test_middle():
    """Вставка в середину: 5 12 30 + 20"""
    got = _values(insert_sorted(_build([5, 12, 30]), 20))
    assert got == [5, 12, 20, 30], f"получено {got}"


def test_head():
    """Вставка в начало меняет голову"""
    got = _values(insert_sorted(_build([5, 12, 30]), 1))
    assert got == [1, 5, 12, 30], f"получено {got}"


def test_tail():
    """Вставка в конец"""
    got = _values(insert_sorted(_build([5, 12, 30]), 45))
    assert got == [5, 12, 30, 45], f"получено {got}"


def test_empty():
    """Пустой список → один узел"""
    head = insert_sorted(None, 7)
    assert _values(head) == [7], f"получено {_values(head)}"


def test_equal_goes_after():
    """Заказ с тем же временем встаёт после существующих"""
    head = _build([5, 12, 12, 30])
    old = _nodes(head)
    head = insert_sorted(head, 12)
    nodes = _nodes(head)
    assert [n.value for n in nodes] == [5, 12, 12, 12, 30], f"получено {[n.value for n in nodes]}"
    assert nodes[1] is old[1] and nodes[2] is old[2], "новый узел должен встать после уже существующих 12"


def test_equal_to_head():
    """Время совпадает со временем головы — голова не меняется"""
    head = _build([5, 9])
    new_head = insert_sorted(head, 5)
    assert new_head is head, "голова должна остаться прежней"
    assert _values(new_head) == [5, 5, 9], f"получено {_values(new_head)}"


def test_nodes_reused():
    """Старые узлы не пересоздаются, добавлен ровно один новый"""
    head = _build([1, 3, 5, 7])
    old = _nodes(head)
    nodes = _nodes(insert_sorted(head, 4))
    assert len(nodes) == 5, f"узлов стало {len(nodes)}, ожидалось 5"
    kept = [n for n in nodes if any(n is o for o in old)]
    assert len(kept) == 4, "часть старых узлов была заменена новыми"


def test_many_inserts():
    """Серия вставок даёт отсортированный список"""
    head = None
    data = [8, 3, 9, 1, 3, 7, 0, 9, 4]
    for t in data:
        head = insert_sorted(head, t)
    got = _values(head)
    expected = [0, 1, 3, 3, 4, 7, 8, 9, 9]
    assert got == expected, f"получено {got}"
