from collections import deque


def route(lines: dict[str, list[str]], start: str, goal: str) -> list[str] | None:
    """Кратчайший по числу перегонов путь от start до goal или None."""
    parent: dict[str, str | None] = {start: None}
    queue = deque([start])
    while queue:
        station = queue.popleft()
        if station == goal:
            path = []
            node: str | None = station
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]
        for nxt in lines.get(station, []):
            if nxt not in parent:
                parent[nxt] = station
                queue.append(nxt)
    return None
