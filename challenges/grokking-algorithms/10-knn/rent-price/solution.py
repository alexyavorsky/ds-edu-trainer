import math


def predict_rent(train: list[tuple[list[float], float]], query: list[float], k: int) -> float:
    """Средняя цена k ближайших квартир."""
    neighbors = sorted(train, key=lambda item: math.dist(item[0], query))[:k]
    return sum(price for _, price in neighbors) / len(neighbors)
