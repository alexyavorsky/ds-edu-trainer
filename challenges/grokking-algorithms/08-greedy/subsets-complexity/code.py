from itertools import combinations


def best_load(weights: list[int], limit: int) -> int:
    best = 0
    for size in range(len(weights) + 1):
        for subset in combinations(weights, size):
            total = sum(subset)
            if best < total <= limit:
                best = total
    return best
