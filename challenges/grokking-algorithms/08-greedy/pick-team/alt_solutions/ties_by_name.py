def pick_team(needed: set[str], candidates: dict[str, set[str]]) -> list[str] | None:
    """Имена кандидатов, вместе покрывающих needed (жадно), или None."""
    left = set(needed)
    team = []
    while left:
        # при равном вкладе берём кандидата с меньшим именем — другой порядок, тоже жадный
        name = max(sorted(candidates), key=lambda n: len(candidates[n] & left))
        if not candidates[name] & left:
            return None
        team.append(name)
        left -= candidates[name]
    return team
