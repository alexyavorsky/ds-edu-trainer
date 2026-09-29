def flatten(items: list) -> list[int]:
    """Возвращает все числа из вложенного списка в исходном порядке."""
    if not items:
        return []
    return expand(items[0]) + flatten(items[1:])


def expand(item) -> list[int]:
    return flatten(item) if isinstance(item, list) else [item]
