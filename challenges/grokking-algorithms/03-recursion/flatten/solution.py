def flatten(items: list) -> list[int]:
    """Возвращает все числа из вложенного списка в исходном порядке."""
    result: list[int] = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))  # рекурсивный случай: вложенный набор
        else:
            result.append(item)  # артикул — кладём как есть
    return result
