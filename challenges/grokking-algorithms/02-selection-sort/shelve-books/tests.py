def test_example():
    """Пример: [42, 19, 3, 7] → 3 обмена, [3, 7, 19, 42]"""
    books = [42, 19, 3, 7]
    swaps = shelve(books)
    assert books == [3, 7, 19, 42], f"полка: {books}"
    assert swaps == 3, f"обменов: ожидалось 3, получено {swaps!r}"


def test_sorted_no_swaps():
    """Уже упорядоченная полка — ноль обменов"""
    books = [1, 2, 3, 4]
    swaps = shelve(books)
    assert books == [1, 2, 3, 4], f"полка: {books}"
    assert swaps == 0, f"обменов: ожидалось 0, получено {swaps!r}"


def test_empty_and_single():
    """Пустая полка и полка с одной книгой"""
    for books in ([], [5]):
        before = list(books)
        swaps = shelve(books)
        assert books == before and swaps == 0, f"{before}: полка {books}, обменов {swaps!r}"


def test_reverse():
    """Обратный порядок: [5, 4, 3, 2, 1] → 2 обмена"""
    books = [5, 4, 3, 2, 1]
    swaps = shelve(books)
    assert books == [1, 2, 3, 4, 5], f"полка: {books}"
    assert swaps == 2, f"обменов: ожидалось 2, получено {swaps!r}"


def test_duplicates():
    """Повторяющиеся номера"""
    books = [3, 1, 3, 1, 2]
    swaps = shelve(books)
    assert books == [1, 1, 2, 3, 3], f"полка: {books}"
    assert swaps == 3, f"обменов: ожидалось 3, получено {swaps!r}"


def test_equal_takes_first():
    """При равных номерах берётся первая: [2, 1, 1] → 2 обмена"""
    books = [2, 1, 1]
    swaps = shelve(books)
    assert books == [1, 1, 2], f"полка: {books}"
    assert swaps == 2, f"обменов: ожидалось 2 (сначала меняем с первой единицей), получено {swaps!r}"


def test_in_place():
    """Сортировка на месте: тот же объект списка"""
    books = [2, 1]
    same = books
    shelve(books)
    assert same is books and books == [1, 2], f"полка: {books}"


def test_bigger():
    """50 книг в перемешанном порядке"""
    books = [(i * 37) % 50 for i in range(50)]
    shelve(books)
    assert books == list(range(50)), f"начало полки: {books[:8]}"
