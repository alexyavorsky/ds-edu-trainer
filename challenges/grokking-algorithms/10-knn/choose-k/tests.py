import math

DATA = [
    ([0, 0], "A"), ([0, 1], "A"), ([1, 0], "A"), ([1, 1], "A"),
    ([5, 5], "B"), ([5, 6], "B"), ([6, 5], "B"), ([6, 6], "B"),
    ([0.5, 0.5], "B"),  # шум внутри скопления A
]


def test_loo_k1():
    """k = 1: точность 4/9 — шумовая точка сбивает всех соседей из A"""
    got = loo_accuracy(DATA, 1)
    assert math.isclose(got, 4 / 9), f"ожидалось {4 / 9:.4f}, получено {got!r}"


def test_loo_k3():
    """k = 3: точность 8/9 — ошибается только сама шумовая точка"""
    got = loo_accuracy(DATA, 3)
    assert math.isclose(got, 8 / 9), f"ожидалось {8 / 9:.4f}, получено {got!r}"


def test_loo_not_100_for_k1():
    """k = 1 не должен давать 100%, если точка не видит сама себя"""
    data = [([0], "A"), ([1], "B"), ([2], "A"), ([3], "B")]
    got = loo_accuracy(data, 1)
    assert math.isclose(got, 0.0), f"ожидалось 0.0 (каждый сосед — другой метки), получено {got!r}"


def test_best_k_example():
    """Пример: best_k(DATA, [1, 3, 5]) → 3 (у k = 3 и k = 5 точность 8/9, берём меньшее)"""
    got = best_k(DATA, [1, 3, 5])
    assert got == 3, f"ожидалось 3, получено {got!r}"


def test_tie_smallest_k():
    """Равная точность → наименьшее k"""
    data = [([0], "A"), ([1], "A"), ([2], "A"), ([10], "B"), ([11], "B"), ([12], "B")]
    got = best_k(data, [1, 3])
    assert got == 1, f"ожидалось 1 (у k = 1 и k = 3 одинаковая точность), получено {got!r}"


def test_single_candidate():
    """Один кандидат — он и ответ"""
    got = best_k(DATA, [5])
    assert got == 5, f"ожидалось 5, получено {got!r}"


def test_unsorted_candidates():
    """Кандидаты в произвольном порядке"""
    data = [([0], "A"), ([1], "A"), ([2], "A"), ([10], "B"), ([11], "B"), ([12], "B")]
    got = best_k(data, [3, 1])
    assert got == 1, f"ожидалось 1, получено {got!r}"
