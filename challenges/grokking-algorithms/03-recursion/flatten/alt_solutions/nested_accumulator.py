def flatten(items: list) -> list[int]:
    """Возвращает все числа из вложенного списка в исходном порядке."""
    result: list[int] = []

    def walk(part: list) -> None:
        for item in part:
            if isinstance(item, list):
                walk(item)
            else:
                result.append(item)

    walk(items)
    return result
