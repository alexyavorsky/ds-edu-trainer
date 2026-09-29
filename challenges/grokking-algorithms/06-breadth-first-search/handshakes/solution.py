from collections import deque


def handshakes(graph: dict[str, list[str]], start: str, goal: str) -> int:
    """Минимальное число шагов от start до goal или -1."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        person = queue.popleft()
        if person == goal:
            return dist[person]
        for friend in graph.get(person, []):
            if friend not in dist:
                dist[friend] = dist[person] + 1
                queue.append(friend)
    return -1
