def study_order(prereqs: dict[str, list[str]]) -> list[str] | None:
    """Порядок курсов, в котором пререквизиты идут раньше, или None при цикле."""
    courses = set(prereqs)
    for needs in prereqs.values():
        courses.update(needs)
    waiting = {c: 0 for c in courses}
    unlocks: dict[str, list[str]] = {c: [] for c in courses}
    for course, needs in prereqs.items():
        for need in needs:
            waiting[course] += 1
            unlocks[need].append(course)
    ready = sorted(c for c in courses if waiting[c] == 0)  # стек вместо очереди — порядок другой, но тоже верный
    order = []
    while ready:
        course = ready.pop()
        order.append(course)
        for nxt in unlocks[course]:
            waiting[nxt] -= 1
            if waiting[nxt] == 0:
                ready.append(nxt)
    return order if len(order) == len(courses) else None
