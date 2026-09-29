def test_merge_example():
    """merge: [1, 4, 9] + [2, 3, 10]"""
    got = merge([1, 4, 9], [2, 3, 10])
    assert got == [1, 2, 3, 4, 9, 10], f"получено {got!r}"


def test_merge_empty_sides():
    """merge: одна из половин пустая"""
    assert merge([], [1, 2]) == [1, 2], f"merge([], [1, 2]) → {merge([], [1, 2])!r}"
    assert merge([3], []) == [3], f"merge([3], []) → {merge([3], [])!r}"
    assert merge([], []) == [], f"merge([], []) → {merge([], [])!r}"


def test_merge_uneven():
    """merge: одна половина закончилась намного раньше"""
    got = merge([1, 2], [3, 4, 5, 6])
    assert got == [1, 2, 3, 4, 5, 6], f"получено {got!r}"


def test_merge_duplicates():
    """merge: равные элементы в обеих половинах"""
    got = merge([2, 2, 5], [2, 5, 5])
    assert got == [2, 2, 2, 5, 5, 5], f"получено {got!r}"


def test_sort_example():
    """merge_sort: [5, 2, 8, 2, 1]"""
    got = merge_sort([5, 2, 8, 2, 1])
    assert got == [1, 2, 2, 5, 8], f"получено {got!r}"


def test_sort_edges():
    """merge_sort: пустой список и один элемент"""
    assert merge_sort([]) == [], f"получено {merge_sort([])!r}"
    assert merge_sort([7]) == [7], f"получено {merge_sort([7])!r}"


def test_sort_bigger():
    """merge_sort: 500 чисел с повторами"""
    data = [(i * 97) % 61 - 30 for i in range(500)]
    got = merge_sort(data)
    assert got == sorted(data), f"начало: {got[:6]}"


def test_input_not_changed():
    """Исходный список не изменяется"""
    data = [3, 1, 2]
    merge_sort(data)
    assert data == [3, 1, 2], f"список изменился: {data!r}"
