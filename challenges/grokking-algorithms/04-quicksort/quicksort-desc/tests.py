def test_example():
    """Пример: [30, 75, 10, 75, 50] → [75, 75, 50, 30, 10]"""
    got = quicksort_desc([30, 75, 10, 75, 50])
    assert got == [75, 75, 50, 30, 10], f"получено {got!r}"


def test_empty():
    """Пустой список → []"""
    got = quicksort_desc([])
    assert got == [], f"получено {got!r}"


def test_single():
    """Один элемент"""
    got = quicksort_desc([42])
    assert got == [42], f"получено {got!r}"


def test_already_desc_and_asc():
    """Уже по убыванию и по возрастанию"""
    assert quicksort_desc([5, 4, 3, 2, 1]) == [5, 4, 3, 2, 1], f"получено {quicksort_desc([5, 4, 3, 2, 1])!r}"
    assert quicksort_desc([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1], f"получено {quicksort_desc([1, 2, 3, 4, 5])!r}"


def test_duplicates_and_negative():
    """Дубликаты и отрицательные числа"""
    got = quicksort_desc([0, -3, 7, -3, 7, 0])
    assert got == [7, 7, 0, 0, -3, -3], f"получено {got!r}"


def test_input_not_changed():
    """Исходный список не изменяется"""
    data = [3, 1, 2]
    quicksort_desc(data)
    assert data == [3, 1, 2], f"список изменился: {data!r}"


def test_bigger():
    """300 значений"""
    data = [(i * 53) % 101 for i in range(300)]
    got = quicksort_desc(data)
    assert got == sorted(data, reverse=True), f"начало: {got[:6]}"
