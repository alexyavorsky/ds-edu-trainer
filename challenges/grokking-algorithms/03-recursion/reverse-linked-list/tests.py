def _build(values: list[int]) -> Node | None:
    head = None
    for v in reversed(values):
        head = Node(v, head)
    return head


def _to_list(head: Node | None, limit: int = 10_000) -> list[int]:
    values = []
    while head is not None:
        values.append(head.value)
        assert len(values) <= limit, f"в списке цикл: {values[:6]}… — какой-то next указывает назад"
        head = head.next
    return values


def _nodes(head: Node | None) -> list[Node]:
    nodes = []
    while head is not None and len(nodes) <= 10_000:
        nodes.append(head)
        head = head.next
    return nodes


def test_three():
    """1 → 2 → 3 превращается в 3 → 2 → 1"""
    got = _to_list(reverse(_build([1, 2, 3])))
    assert got == [3, 2, 1], f"получено {got}"


def test_empty():
    """Пустой список → None"""
    got = reverse(None)
    assert got is None, f"ожидалось None, получено {got!r}"


def test_single():
    """Один узел возвращается как есть"""
    node = Node(42)
    got = reverse(node)
    assert got is node and node.next is None, "ожидался тот же узел с next = None"


def test_two():
    """Два узла: 1 → 2 превращается в 2 → 1"""
    got = _to_list(reverse(_build([1, 2])))
    assert got == [2, 1], f"получено {got}"


def test_duplicates():
    """Повторяющиеся значения: 5 → 5 → 7 → 5"""
    got = _to_list(reverse(_build([5, 5, 7, 5])))
    assert got == [5, 7, 5, 5], f"получено {got}"


def test_old_head_becomes_tail():
    """Бывшая голова становится хвостом: её next — None"""
    head = _build([1, 2, 3, 4])
    reverse(head)
    assert head.next is None, f"у бывшей головы next = узел {head.next.value}, а должен быть None"


def test_same_nodes():
    """Новые узлы не создаются — переставляются старые"""
    head = _build([1, 2, 3, 4, 5])
    before = _nodes(head)
    after = _nodes(reverse(head))
    assert [id(n) for n in after] == [id(n) for n in reversed(before)], "узлы должны быть теми же объектами"


def test_long():
    """Список из 500 узлов"""
    values = list(range(500))
    got = _to_list(reverse(_build(values)))
    assert got == values[::-1], f"получено {got[:5]}…"
