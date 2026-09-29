import random


def kth_fastest(times: list[int], k: int) -> int:
    """Возвращает k-й по величине (k = 1 — минимальный) элемент списка."""
    part = times
    while True:
        pivot = part[random.randrange(len(part))]
        less = [t for t in part if t < pivot]
        equal_count = sum(1 for t in part if t == pivot)
        if k <= len(less):
            part = less
        elif k <= len(less) + equal_count:
            return pivot
        else:
            k -= len(less) + equal_count
            part = [t for t in part if t > pivot]
