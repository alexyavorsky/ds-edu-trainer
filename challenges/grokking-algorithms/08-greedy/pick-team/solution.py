def pick_team(needed: set[str], candidates: dict[str, set[str]]) -> list[str] | None:
    """Имена кандидатов, вместе покрывающих needed (жадно), или None."""
    uncovered = set(needed)
    team: list[str] = []
    while uncovered:
        best, best_cover = None, set()
        for name, skills in candidates.items():
            cover = uncovered & skills
            if len(cover) > len(best_cover):
                best, best_cover = name, cover
        if best is None:
            return None
        team.append(best)
        uncovered -= best_cover
    return team
