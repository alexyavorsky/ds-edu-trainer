class Node:
    """Узел односвязного списка."""

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next


def insert_sorted(head: Node | None, time: int) -> Node:
    """Вставляет time в отсортированный список и возвращает голову."""
    if head is None or time < head.value:
        return Node(time, head)
    head.next = insert_sorted(head.next, time)
    return head
