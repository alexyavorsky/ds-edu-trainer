from collections import deque


def route(lines: dict[str, list[str]], start: str, goal: str) -> list[str] | None:
    """Кратчайший по числу перегонов путь от start до goal или None."""
    queue = deque([[start]])  # в очереди — целые пути (памяти больше, но верно)
    visited = {start}
    while queue:
        path = queue.popleft()
        if path[-1] == goal:
            return path
        for nxt in lines.get(path[-1], []):
            if nxt not in visited:
                visited.add(nxt)
                queue.append(path + [nxt])
    return None
