def distance(a: list[float], b: list[float]) -> float:
    """Евклидово расстояние между векторами признаков одинаковой длины."""
    if len(a) != len(b):
        raise ValueError("векторы разной длины")
    total = 0.0
    for i in range(len(a)):
        diff = a[i] - b[i]
        total += diff * diff
    return total ** 0.5
