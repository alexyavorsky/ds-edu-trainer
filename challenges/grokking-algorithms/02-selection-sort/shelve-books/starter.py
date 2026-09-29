def shelve(books: list[int]) -> int:
    """Сортирует books на месте выбором и возвращает число обменов."""
    swaps = 0
    for i in range(len(books) - 1):
        smallest = i
        for j in range(i + 1, len(books)):
            # TODO: если books[j] меньше текущего минимума — запомните j
            pass
        if smallest != i:
            # TODO: поменяйте местами книги на местах i и smallest
            swaps += 1
    return swaps
