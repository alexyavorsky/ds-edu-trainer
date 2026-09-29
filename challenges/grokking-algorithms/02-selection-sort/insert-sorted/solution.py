class Node:
    """Узел односвязного списка."""

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next


def insert_sorted(head: Node | None, time: int) -> Node:
    """Вставляет time в отсортированный список и возвращает голову."""
    node = Node(time)
    if head is None or time < head.value:  # вставка в начало
        node.next = head
        return node
    cur = head
    while cur.next is not None and cur.next.value <= time:
        cur = cur.next
    node.next = cur.next
    cur.next = node
    return head
