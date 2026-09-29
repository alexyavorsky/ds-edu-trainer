class Node:
    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next


def get(head: Node, index: int) -> int:
    node = head
    for _ in range(index):
        node = node.next
    return node.value


def total(head: Node, n: int) -> int:
    result = 0
    for i in range(n):
        result += get(head, i)
    return result
