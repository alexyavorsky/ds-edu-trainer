def unique_guests(log: list[str]) -> list[str]:
    unique = []
    for name in log:
        if name not in unique:
            unique.append(name)
    return unique
