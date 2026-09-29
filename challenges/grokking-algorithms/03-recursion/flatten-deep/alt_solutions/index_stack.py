def flatten_deep(items: list) -> list[int]:
    """Возвращает все числа из вложенного списка любой глубины, без рекурсии."""
    result: list[int] = []
    stack = [(items, 0)]  # (список, индекс следующего элемента)
    while stack:
        current, i = stack.pop()
        while i < len(current):
            item = current[i]
            i += 1
            if isinstance(item, list):
                stack.append((current, i))  # вернёмся сюда позже
                current, i = item, 0
            else:
                result.append(item)
    return result
