import math


def classify(train: list[tuple[list[float], str]], query: list[float], k: int) -> str:
    """Жанр по голосованию k ближайших соседей."""
    neighbors = sorted(train, key=lambda item: math.dist(item[0], query))[:k]
    votes: dict[str, int] = {}
    for _, label in neighbors:
        votes[label] = votes.get(label, 0) + 1
    top = max(votes.values())
    for _, label in neighbors:  # от ближнего к дальнему
        if votes[label] == top:
            return label
    raise AssertionError("недостижимо")
