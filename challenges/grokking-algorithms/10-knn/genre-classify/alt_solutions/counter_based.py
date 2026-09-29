import math
from collections import Counter


def classify(train: list[tuple[list[float], str]], query: list[float], k: int) -> str:
    """Жанр по голосованию k ближайших соседей."""
    order = sorted(range(len(train)), key=lambda i: (math.dist(train[i][0], query), i))
    labels = [train[i][1] for i in order[:k]]
    votes = Counter(labels)
    top = max(votes.values())
    leaders = {label for label, n in votes.items() if n == top}
    for label in labels:  # от ближнего к дальнему
        if label in leaders:
            return label
    return labels[0]
