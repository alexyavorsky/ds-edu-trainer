from collections import deque


def within_hops(graph: dict[str, list[str]], start: str, k: int) -> set[str]:
    """Все, до кого можно дойти не больше чем за k шагов (без start)."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        person = queue.popleft()
        if dist[person] == k:
            continue  # дальше пересылать нельзя
        for friend in graph.get(person, []):
            if friend not in dist:
                dist[friend] = dist[person] + 1
                queue.append(friend)
    return {p for p, d in dist.items() if 0 < d <= k}
