class Node:
    """Узел односвязного списка."""

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next


def sort_nodes(head: Node | None) -> Node | None:
    """Сортирует список выбором, переставляя узлы; возвращает новую голову."""
    source = Node(0, head)  # фиктивные головы упрощают удаление и вставку
    result = Node(0)
    tail = result
    while source.next is not None:
        before_min = source
        walker = source
        while walker.next is not None:
            if walker.next.value < before_min.next.value:
                before_min = walker
            walker = walker.next
        node = before_min.next
        before_min.next = node.next
        node.next = None
        tail.next = node
        tail = node
    return result.next
