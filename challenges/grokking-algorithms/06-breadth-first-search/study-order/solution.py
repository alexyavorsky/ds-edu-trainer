from collections import deque


def study_order(prereqs: dict[str, list[str]]) -> list[str] | None:
    """Порядок курсов, в котором пререквизиты идут раньше, или None при цикле."""
    unlocks: dict[str, list[str]] = {}  # пререквизит → курсы, которые он открывает
    waiting: dict[str, int] = {}  # курс → сколько пререквизитов ещё не пройдено
    for course, needs in prereqs.items():
        waiting.setdefault(course, 0)
        for need in needs:
            waiting.setdefault(need, 0)
            waiting[course] += 1
            unlocks.setdefault(need, []).append(course)

    queue = deque(c for c, n in waiting.items() if n == 0)
    order = []
    while queue:
        course = queue.popleft()
        order.append(course)
        for nxt in unlocks.get(course, []):
            waiting[nxt] -= 1
            if waiting[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == len(waiting) else None
