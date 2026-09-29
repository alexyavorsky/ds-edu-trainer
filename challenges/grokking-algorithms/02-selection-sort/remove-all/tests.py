def _build(values: list[int]) -> Node | None:
    head = None
    for v in reversed(values):
        head = Node(v, head)
    return head


def _values(head: Node | None) -> list[int]:
    values = []
    while head is not None:
        values.append(head.value)
        assert len(values) <= 10_000, "в списке цикл"
        head = head.next
    return values


def _check(values: list[int], code: int) -> None:
    got = _values(remove_all(_build(values), code))
    expected = [v for v in values if v != code]
    assert got == expected, f"remove_all({values}, {code}): ожидалось {expected}, получено {got}"


def test_example():
    """Пример: 7 0 3 0 0 5 без нулей"""
    _check([7, 0, 3, 0, 0, 5], 0)


def test_head_run():
    """Удаляемые в начале подряд: 0 0 1"""
    _check([0, 0, 1], 0)


def test_single_head():
    """Удаляется только голова"""
    _check([4, 1, 2], 4)


def test_tail():
    """Удаляется хвост"""
    _check([1, 2, 9], 9)


def test_all_removed():
    """Удаляется всё → None"""
    got = remove_all(_build([3, 3, 3]), 3)
    assert got is None, f"ожидалось None, получено список {_values(got)}"


def test_nothing_to_remove():
    """Нечего удалять — список не меняется"""
    _check([1, 2, 3], 8)


def test_empty():
    """Пустой список → None"""
    got = remove_all(None, 1)
    assert got is None, f"ожидалось None, получено {got!r}"


def test_mixed_runs():
    """Серии удаляемых в разных местах"""
    _check([2, 2, 1, 2, 2, 2, 3, 2, 4, 2, 2], 2)
