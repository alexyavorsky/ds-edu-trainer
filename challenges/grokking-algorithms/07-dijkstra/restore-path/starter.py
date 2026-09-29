def restore_path(parents: dict[str, str], start: str, goal: str) -> list[str]:
    """Путь от start до goal по таблице родителей или [] если goal недостижим."""
    if goal != start and goal not in parents:
        return []
    path = [goal]
    # TODO: пока не дошли до start, добавляйте в path родителя последнего узла
    # TODO: верните путь в порядке от start к goal
    return path
