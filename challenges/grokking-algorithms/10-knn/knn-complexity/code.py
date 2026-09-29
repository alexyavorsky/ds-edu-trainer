import math
from collections import Counter


def classify(train: list[tuple[list[float], str]], query: list[float], k: int) -> str:
    distances = []
    for features, label in train:
        d = math.sqrt(sum((x - y) ** 2 for x, y in zip(features, query)))
        distances.append((d, label))
    distances.sort()
    votes = Counter(label for _, label in distances[:k])
    return votes.most_common(1)[0][0]
