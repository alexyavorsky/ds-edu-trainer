RACE = [61, 58, 70, 58, 64]


def test_first():
    """k = 1 — самый быстрый"""
    got = kth_fastest(RACE, 1)
    assert got == 58, f"ожидалось 58, получено {got!r}"


def test_duplicates():
    """Повторы считаются: k = 2 → 58, k = 3 → 61"""
    assert kth_fastest(RACE, 2) == 58, f"k=2: получено {kth_fastest(RACE, 2)!r}"
    assert kth_fastest(RACE, 3) == 61, f"k=3: получено {kth_fastest(RACE, 3)!r}"


def test_last():
    """k = n — самый медленный"""
    got = kth_fastest(RACE, 5)
    assert got == 70, f"ожидалось 70, получено {got!r}"


def test_single():
    """Один бегун"""
    got = kth_fastest([99], 1)
    assert got == 99, f"ожидалось 99, получено {got!r}"


def test_all_equal():
    """Все результаты одинаковые"""
    for k in range(1, 6):
        got = kth_fastest([7, 7, 7, 7, 7], k)
        assert got == 7, f"k={k}: ожидалось 7, получено {got!r}"


def test_every_k():
    """Каждое k совпадает с отсортированным списком"""
    data = [(i * 37) % 23 for i in range(40)]
    expected = sorted(data)
    for k in range(1, len(data) + 1):
        got = kth_fastest(data, k)
        assert got == expected[k - 1], f"k={k}: ожидалось {expected[k - 1]}, получено {got!r}"


def test_input_not_changed():
    """Исходный список не изменяется"""
    data = [5, 1, 4, 2]
    kth_fastest(data, 2)
    assert data == [5, 1, 4, 2], f"список изменился: {data!r}"


def test_large_sorted_input():
    """100 000 уже упорядоченных результатов: верный ответ, без переполнения стека и за отведённое время"""
    data = list(range(100_000))
    got = kth_fastest(data, 77_777)
    assert got == 77_776, f"ожидалось 77776, получено {got!r}"


test_large_sorted_input.timeout = 5
test_large_sorted_input.timeout_hint = "На упорядоченном входе опорный «первый элемент» даёт худший случай O(n²) — берите случайный"
