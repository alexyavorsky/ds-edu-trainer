def first_repeat(scans: list[str]) -> str | None:
    """Код билета, повторный проход которого случился раньше всех, или None."""
    seen: set[str] = set()
    for code in scans:
        if code in seen:
            return code
        seen.add(code)
    return None
