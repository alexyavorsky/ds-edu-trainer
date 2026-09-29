from collections import deque


def distances(graph: dict[str, list[str]], start: str) -> dict[str, int]:
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for friend in graph.get(node, []):
            if friend not in dist:
                dist[friend] = dist[node] + 1
                queue.append(friend)
    return dist
