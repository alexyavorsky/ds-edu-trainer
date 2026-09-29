def test_sorted():
    """Полное согласие → 0"""
    got = count_inversions([1, 2, 3, 4])
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_example():
    """[2, 4, 1, 3, 5] → 3"""
    got = count_inversions([2, 4, 1, 3, 5])
    assert got == 3, f"ожидалось 3, получено {got!r}"


def test_reversed():
    """Обратный порядок: n(n − 1)/2 инверсий"""
    got = count_inversions(list(range(10, 0, -1)))
    assert got == 45, f"ожидалось 45, получено {got!r}"


def test_empty_and_single():
    """Пустой список и один элемент → 0"""
    assert count_inversions([]) == 0, f"[]: получено {count_inversions([])!r}"
    assert count_inversions([5]) == 0, f"[5]: получено {count_inversions([5])!r}"


def test_duplicates():
    """Равные значения не образуют инверсий"""
    assert count_inversions([2, 2, 2]) == 0, f"[2, 2, 2]: получено {count_inversions([2, 2, 2])!r}"
    got = count_inversions([3, 1, 3, 1])
    assert got == 3, f"[3, 1, 3, 1]: ожидалось 3, получено {got!r}"


def test_many_lists():
    """30 списков разной длины с повторами — заранее посчитанные ответы"""
    expected = [0, 1, 3, 3, 8, 6, 13, 22, 15, 23, 35, 29, 39, 54, 49, 64, 65, 79, 99, 85, 101, 125, 113, 132, 160, 150, 175, 179, 200, 231]
    for seed, answer in enumerate(expected):
        ranks = [(seed * 31 + i * 17) % 11 for i in range(seed + 2)]
        got = count_inversions(ranks)
        assert got == answer, f"{ranks}: ожидалось {answer}, получено {got!r}"


def test_input_not_changed():
    """Исходный список не изменяется"""
    data = [3, 1, 2]
    count_inversions(data)
    assert data == [3, 1, 2], f"список изменился: {data!r}"


class _Rank(int):
    """Число, которое считает сравнения."""

    compared = 0

    def __lt__(self, other):
        _Rank.compared += 1
        return int(self) < int(other)

    def __le__(self, other):
        _Rank.compared += 1
        return int(self) <= int(other)

    def __gt__(self, other):
        _Rank.compared += 1
        return int(self) > int(other)

    def __ge__(self, other):
        _Rank.compared += 1
        return int(self) >= int(other)


def test_n_log_n():
    """2000 элементов: верный ответ и не больше 100 000 сравнений"""
    n = 2000
    ranks = [_Rank((i * 7919) % n) for i in range(n)]
    expected = 1_010_601
    _Rank.compared = 0
    got = count_inversions(ranks)
    assert got == expected, f"ожидалось {expected}, получено {got!r}"
    assert _Rank.compared <= 100_000, (
        f"сделано {_Rank.compared} сравнений при лимите 100 000 (сортировке слиянием хватает ~20 000, "
        f"перебор пар делает ~{n * n // 2}) — похоже на перебор пар"
    )
