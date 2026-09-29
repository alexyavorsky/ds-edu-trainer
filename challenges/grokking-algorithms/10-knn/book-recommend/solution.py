import math


def similarity(a: dict[str, float], b: dict[str, float]) -> float:
    """Косинусное сходство по книгам, которые оценили оба."""
    common = a.keys() & b.keys()
    if not common:
        return 0.0
    dot = sum(a[x] * b[x] for x in common)
    norm_a = math.sqrt(sum(a[x] ** 2 for x in common))
    norm_b = math.sqrt(sum(b[x] ** 2 for x in common))
    return dot / (norm_a * norm_b)


def recommend(ratings: dict[str, dict[str, float]], user: str, k: int) -> list[str]:
    """Книги для user по оценкам k самых похожих читателей (косинусное сходство)."""
    if user not in ratings:
        return []
    mine = ratings[user]
    scored = [(similarity(mine, theirs), name) for name, theirs in ratings.items() if name != user]
    neighbors = [name for sim, name in sorted(scored, key=lambda x: (-x[0], x[1])) if sim > 0][:k]

    collected: dict[str, list[float]] = {}
    for name in neighbors:
        for book, score in ratings[name].items():
            if book not in mine:
                collected.setdefault(book, []).append(score)
    averages = {book: sum(s) / len(s) for book, s in collected.items()}
    return sorted(averages, key=lambda book: (-averages[book], book))
