def predict_rent(train: list[tuple[list[float], float]], query: list[float], k: int) -> float:
    """Средняя цена k ближайших квартир."""
    def dist2(features: list[float]) -> float:
        return sum((x - y) ** 2 for x, y in zip(features, query))  # квадрат расстояния — порядок тот же

    left = list(range(len(train)))
    total, taken = 0.0, 0
    while left and taken < k:
        best = min(left, key=lambda i: (dist2(train[i][0]), i))
        total += train[best][1]
        taken += 1
        left.remove(best)
    return total / taken
