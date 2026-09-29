from collections import deque


def reachable(graph: dict[str, list[str]], start: str) -> list[str]:
    searched = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node in searched:
            continue
        searched.append(node)
        for neighbor in graph.get(node, []):
            queue.append(neighbor)
    return searched
