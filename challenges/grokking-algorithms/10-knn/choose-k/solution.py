import math


def classify(train: list[tuple[list[float], str]], query: list[float], k: int) -> str:
    """Голосование k ближайших; при ничьей — метка ближайшего из лидеров."""
    neighbors = sorted(train, key=lambda item: math.dist(item[0], query))[:k]
    votes: dict[str, int] = {}
    for _, label in neighbors:
        votes[label] = votes.get(label, 0) + 1
    top = max(votes.values())
    return next(label for _, label in neighbors if votes[label] == top)


def loo_accuracy(data: list[tuple[list[float], str]], k: int) -> float:
    """Точность «исключи по одному» для заданного k."""
    correct = 0
    for i, (features, label) in enumerate(data):
        others = data[:i] + data[i + 1:]
        if classify(others, features, k) == label:
            correct += 1
    return correct / len(data)


def best_k(data: list[tuple[list[float], str]], candidates: list[int]) -> int:
    """k с наибольшей точностью; при равенстве — наименьшее."""
    best, best_acc = candidates[0], -1.0
    for k in sorted(candidates):
        acc = loo_accuracy(data, k)
        if acc > best_acc:
            best, best_acc = k, acc
    return best
