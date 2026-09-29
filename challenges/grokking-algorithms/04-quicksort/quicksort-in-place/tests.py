def _sorted_copy(data: list[int]) -> list[int]:
    items = list(data)
    quicksort_in_place(items)
    return items


def test_example():
    """Пример: [5, 2, 9, 1, 5, 6]"""
    got = _sorted_copy([5, 2, 9, 1, 5, 6])
    assert got == [1, 2, 5, 5, 6, 9], f"получено {got!r}"


def test_partition():
    """partition: опорный на своём месте, слева меньшие, справа не меньшие"""
    items = [7, 2, 9, 4, 5]
    p = partition(items, 0, 4)
    assert items[p] == 5, f"на позиции {p} стоит {items[p]}, а должен опорный 5; список {items}"
    assert all(x < 5 for x in items[:p]) and all(x >= 5 for x in items[p + 1:]), f"неверное разбиение: {items}"


def test_partition_subrange():
    """partition трогает только отрезок [low, high]"""
    items = [100, 3, 1, 2, -100]
    p = partition(items, 1, 3)
    assert items[0] == 100 and items[4] == -100, f"изменены элементы вне отрезка: {items}"
    assert items[p] == 2 and sorted(items[1:4]) == [1, 2, 3], f"неверное разбиение: {items}, p = {p}"


def test_empty_and_single():
    """Пустой список и один элемент"""
    assert _sorted_copy([]) == [], "пустой список"
    assert _sorted_copy([4]) == [4], "один элемент"


def test_two():
    """Два элемента в обоих порядках"""
    assert _sorted_copy([2, 1]) == [1, 2], f"получено {_sorted_copy([2, 1])!r}"
    assert _sorted_copy([1, 2]) == [1, 2], f"получено {_sorted_copy([1, 2])!r}"


def test_sorted_and_duplicates():
    """Упорядоченный вход и одинаковые элементы"""
    assert _sorted_copy([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5], f"получено {_sorted_copy([1, 2, 3, 4, 5])!r}"
    assert _sorted_copy([3, 3, 3]) == [3, 3, 3], f"получено {_sorted_copy([3, 3, 3])!r}"


def test_in_place():
    """Сортирует тот же объект и ничего не возвращает"""
    items = [3, 1, 2]
    result = quicksort_in_place(items)
    assert result is None, "функция должна менять список, а не возвращать новый"
    assert items == [1, 2, 3], f"получено {items!r}"


def test_bigger():
    """300 чисел с повторами"""
    data = [(i * 89) % 53 for i in range(300)]
    got = _sorted_copy(data)
    assert got == sorted(data), f"начало: {got[:6]}"
