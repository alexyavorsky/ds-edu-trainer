import math


def distance(a: list[float], b: list[float]) -> float:
    """Евклидово расстояние между векторами признаков одинаковой длины."""
    if len(a) != len(b):
        raise ValueError(f"разная длина векторов: {len(a)} и {len(b)}")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
