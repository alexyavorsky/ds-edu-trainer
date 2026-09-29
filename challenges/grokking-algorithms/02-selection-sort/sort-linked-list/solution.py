class Node:
    """Узел односвязного списка."""

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next


def sort_nodes(head: Node | None) -> Node | None:
    """Сортирует список выбором, переставляя узлы; возвращает новую голову."""
    result_head = result_tail = None
    while head is not None:
        # ищем первый минимальный узел и его предшественника
        best_prev, best = None, head
        prev, cur = head, head.next
        while cur is not None:
            if cur.value < best.value:
                best_prev, best = prev, cur
            prev, cur = cur, cur.next
        # вынимаем его из исходного списка
        if best_prev is None:
            head = best.next
        else:
            best_prev.next = best.next
        best.next = None
        # приписываем в конец результата
        if result_tail is None:
            result_head = result_tail = best
        else:
            result_tail.next = best
            result_tail = best
    return result_head
