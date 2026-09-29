def merge(left: list[int], right: list[int]) -> list[int]:
    """Сливает два отсортированных списка в один отсортированный."""
    result: list[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        # TODO: возьмите меньший из left[i] и right[j], сдвиньте его указатель
        break
    # TODO: добавьте в result то, что осталось в left и в right
    return result


def merge_sort(items: list[int]) -> list[int]:
    """Возвращает новый отсортированный список (сортировка слиянием)."""
    if len(items) < 2:
        return list(items)
    mid = len(items) // 2
    # TODO: отсортируйте половины рекурсивно и слейте их
    return list(items)
