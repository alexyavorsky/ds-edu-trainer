def days_needed(chapters: list[int], speed: int) -> int:
    """Сколько дней уйдёт на книгу при скорости speed страниц в день."""
    # TODO: сложите дни по всем главам (каждая глава читается отдельно)
    ...


def min_daily_pages(chapters: list[int], days: int) -> int:
    """Минимальная скорость (страниц в день), чтобы успеть за days дней."""
    low, high = 1, max(chapters)  # при скорости max(chapters) — ровно день на главу
    while low < high:
        mid = (low + high) // 2
        if ...:  # TODO: успеваем ли со скоростью mid?
            high = mid
        else:
            low = mid + 1
    return low
