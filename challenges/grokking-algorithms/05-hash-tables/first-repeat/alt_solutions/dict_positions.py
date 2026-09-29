def first_repeat(scans: list[str]) -> str | None:
    """Код билета, повторный проход которого случился раньше всех, или None."""
    first_seen: dict[str, int] = {}
    for i in range(len(scans)):
        code = scans[i]
        if code in first_seen:
            return code
        first_seen[code] = i
    return None
