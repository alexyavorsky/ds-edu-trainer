def min_checks(shifts: list[tuple[int, int]]) -> list[int]:
    """Минимальный набор моментов, чтобы в каждую смену был хотя бы один обход."""
    checks: list[int] = []
    for start, end in sorted(shifts, key=lambda s: s[0]):
        if not checks or checks[-1] <= start:
            checks.append(end)  # как можно позже, но в пределах этой смены
    return checks
