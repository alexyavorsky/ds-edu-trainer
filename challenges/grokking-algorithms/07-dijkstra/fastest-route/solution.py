import math


def fastest_route(graph: dict[str, dict[str, int]], start: str, goal: str) -> tuple[float, list[str]]:
    """(минимальное время, путь) от start до goal или (math.inf, [])."""
    nodes = set(graph) | {n for edges in graph.values() for n in edges} | {start, goal}
    costs = {n: math.inf for n in nodes}
    costs[start] = 0
    parents: dict[str, str] = {}
    processed: set[str] = set()
    while True:
        node = min((n for n in nodes if n not in processed), key=lambda n: costs[n], default=None)
        if node is None or costs[node] == math.inf:
            break
        processed.add(node)
        for neighbor, minutes in graph.get(node, {}).items():
            new_cost = costs[node] + minutes
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parents[neighbor] = node
    if costs[goal] == math.inf:
        return math.inf, []
    path = [goal]
    while path[-1] != start:
        path.append(parents[path[-1]])
    return costs[goal], path[::-1]
