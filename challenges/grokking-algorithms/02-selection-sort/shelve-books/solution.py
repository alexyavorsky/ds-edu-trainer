def shelve(books: list[int]) -> int:
    """Сортирует books на месте выбором и возвращает число обменов."""
    swaps = 0
    for i in range(len(books) - 1):
        smallest = i
        for j in range(i + 1, len(books)):
            if books[j] < books[smallest]:
                smallest = j
        if smallest != i:
            books[i], books[smallest] = books[smallest], books[i]
            swaps += 1
    return swaps
