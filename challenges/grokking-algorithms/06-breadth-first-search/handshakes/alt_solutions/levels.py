def handshakes(graph: dict[str, list[str]], start: str, goal: str) -> int:
    """Минимальное число шагов от start до goal или -1."""
    level, visited, steps = [start], {start}, 0
    while level:
        if goal in level:
            return steps
        next_level = []
        for person in level:
            for friend in graph.get(person, []):
                if friend not in visited:
                    visited.add(friend)
                    next_level.append(friend)
        level, steps = next_level, steps + 1
    return -1
