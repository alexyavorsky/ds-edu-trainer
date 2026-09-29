import math


def days_needed(chapters: list[int], speed: int) -> int:
    """Сколько дней уйдёт на книгу при скорости speed страниц в день."""
    total = 0
    for pages in chapters:
        total += math.ceil(pages / speed) if pages < 2**52 else -(-pages // speed)
    return total


def min_daily_pages(chapters: list[int], days: int) -> int:
    """Минимальная скорость (страниц в день), чтобы успеть за days дней."""
    low, high = 0, sum(chapters)  # low — точно мало, high — точно хватает (шире, чем нужно)
    while high - low > 1:
        mid = (low + high) // 2
        if days_needed(chapters, mid) <= days:
            high = mid
        else:
            low = mid
    return high
