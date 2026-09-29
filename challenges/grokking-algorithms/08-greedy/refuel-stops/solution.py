def refuel_stops(stations: list[int], distance: int, tank: int) -> int:
    """Минимальное число заправок до финиша или -1."""
    reach = tank  # докуда можно доехать без новой заправки
    stops = 0
    i = 0
    while reach < distance:
        farthest = None
        while i < len(stations) and stations[i] <= reach:
            farthest = stations[i]
            i += 1
        if farthest is None:
            return -1  # ни одной новой заправки в пределах досягаемости
        stops += 1
        reach = farthest + tank
    return stops
