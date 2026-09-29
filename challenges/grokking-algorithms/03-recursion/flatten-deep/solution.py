def flatten_deep(items: list) -> list[int]:
    """Возвращает все числа из вложенного списка любой глубины, без рекурсии."""
    result: list[int] = []
    stack = [iter(items)]  # вершина стека — список, который читаем сейчас
    while stack:
        for item in stack[-1]:
            if isinstance(item, list):
                stack.append(iter(item))  # «спускаемся» во вложенный список
                break
            result.append(item)
        else:
            stack.pop()  # список дочитан — возвращаемся к внешнему
    return result
