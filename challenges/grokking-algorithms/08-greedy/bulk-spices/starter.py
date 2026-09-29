def max_value(spices: list[tuple[str, int, int]], capacity: int) -> float:
    """Максимальная ценность, если специи можно брать частями."""
    # TODO: упорядочьте специи по ценности за грамм — от самой ценной
    order = list(spices)
    total = 0.0
    room = capacity
    for name, weight, value in order:
        if room <= 0:
            break
        # TODO: возьмите специю целиком, если влезает, иначе — часть, заполняющую остаток места
        pass
    return total
