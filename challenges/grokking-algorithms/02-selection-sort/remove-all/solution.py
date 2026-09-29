class Node:
    """Узел односвязного списка."""

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next


def remove_all(head: Node | None, code: int) -> Node | None:
    """Удаляет все узлы со значением code, возвращает новую голову."""
    while head is not None and head.value == code:
        head = head.next
    cur = head
    while cur is not None and cur.next is not None:
        if cur.next.value == code:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head
