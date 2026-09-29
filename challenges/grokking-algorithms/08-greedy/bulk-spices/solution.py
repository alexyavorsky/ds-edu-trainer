def max_value(spices: list[tuple[str, int, int]], capacity: int) -> float:
    """Максимальная ценность, если специи можно брать частями."""
    order = sorted(spices, key=lambda s: s[2] / s[1], reverse=True)
    total = 0.0
    room = capacity
    for name, weight, value in order:
        if room <= 0:
            break
        take = min(weight, room)
        total += value * take / weight
        room -= take
    return total
