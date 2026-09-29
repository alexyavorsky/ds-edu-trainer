def restore_path(parents: dict[str, str], start: str, goal: str) -> list[str]:
    """Путь от start до goal по таблице родителей или [] если goal недостижим."""
    if goal != start and goal not in parents:
        return []
    path = [goal]
    while path[-1] != start:
        path.append(parents[path[-1]])
    return path[::-1]
