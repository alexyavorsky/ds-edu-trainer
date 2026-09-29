from collections import deque


def distance_to_hub(towns: list[str], roads: list[tuple[str, str]], hubs: set[str]) -> dict[str, int]:
    """Для каждого города — число дорог до ближайшего склада (или -1)."""
    neighbors: dict[str, list[str]] = {town: [] for town in towns}
    for a, b in roads:
        neighbors[a].append(b)
        neighbors[b].append(a)

    dist: dict[str, int] = {}
    queue: deque[str] = deque()
    for hub in hubs:
        dist[hub] = 0
        queue.append(hub)

    while queue:
        town = queue.popleft()
        for nxt in neighbors[town]:
            if nxt not in dist:
                dist[nxt] = dist[town] + 1
                queue.append(nxt)

    return {town: dist.get(town, -1) for town in towns}
