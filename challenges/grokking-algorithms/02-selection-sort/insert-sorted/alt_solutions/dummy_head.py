class Node:
    """Узел односвязного списка."""

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next


def insert_sorted(head: Node | None, time: int) -> Node:
    """Вставляет time в отсортированный список и возвращает голову."""
    dummy = Node(0, head)  # фиктивная голова — вспомогательный узел, в ответ не попадает
    prev = dummy
    while prev.next is not None and prev.next.value <= time:
        prev = prev.next
    prev.next = Node(time, prev.next)
    return dummy.next
