def _code_facts(func):
    """Разбирает код решения (всё, что выше линии тестов) и смотрит на функции, достижимые из func.

    Возвращает (есть ли рекурсия, есть ли цикл, какие функции вызываются) или None,
    если исходник недоступен. Рекурсия засчитывается и во вложенной или вспомогательной
    функции, и взаимная (a вызывает b, b вызывает a).
    """
    import ast
    import inspect

    try:
        with open(inspect.getfile(func), encoding="utf-8") as f:
            tree = ast.parse(f.read().split("# ════ Тесты")[0])
    except (OSError, TypeError, SyntaxError):
        return None

    calls: dict[str, set[str]] = {}
    loops: dict[str, bool] = {}

    def visit(fn) -> None:
        own_calls, own_loop, stack = set(), False, list(fn.body)
        while stack:
            node = stack.pop()
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit(node)  # вложенная функция — отдельная вершина графа вызовов
                continue
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                own_calls.add(node.func.id)
            own_loop |= isinstance(node, (ast.For, ast.While, ast.comprehension))
            stack.extend(ast.iter_child_nodes(node))
        calls.setdefault(fn.name, set()).update(own_calls)
        loops[fn.name] = loops.get(fn.name, False) or own_loop

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visit(node)

    reachable, todo = set(), [func.__name__]
    while todo:
        name = todo.pop()
        if name in calls and name not in reachable:
            reachable.add(name)
            todo.extend(calls[name])

    def in_cycle(start: str) -> bool:
        seen, todo = set(), list(calls.get(start, ()))
        while todo:
            name = todo.pop()
            if name == start:
                return True
            if name in reachable and name not in seen:
                seen.add(name)
                todo.extend(calls[name])
        return False

    recursive = any(in_cycle(name) for name in reachable)
    has_loop = any(loops[name] for name in reachable)
    used = set().union(*(calls[name] for name in reachable)) if reachable else set()
    return recursive, has_loop, used


def test_example():
    """9875 → 29"""
    got = digit_sum(9875)
    assert got == 29, f"ожидалось 29, получено {got!r}"


def test_zero():
    """Ноль → 0"""
    got = digit_sum(0)
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_single_digit():
    """Одна цифра: 7 → 7"""
    got = digit_sum(7)
    assert got == 7, f"ожидалось 7, получено {got!r}"


def test_zeros_inside():
    """Нули внутри и в конце: 1000 → 1, 50203 → 10"""
    for n, expected in [(1000, 1), (50203, 10)]:
        got = digit_sum(n)
        assert got == expected, f"digit_sum({n}): ожидалось {expected}, получено {got!r}"


def test_repeated_digits():
    """Одинаковые цифры: 999999 → 54"""
    got = digit_sum(999999)
    assert got == 54, f"ожидалось 54, получено {got!r}"


def test_huge_number():
    """Сто девяток подряд → 900"""
    n = 10**100 - 1
    got = digit_sum(n)
    assert got == 900, f"ожидалось 900, получено {got!r}"


def test_is_recursive():
    """Решение рекурсивное (можно через вспомогательную функцию), без циклов и str()"""
    facts = _code_facts(digit_sum)
    if facts is None:
        return  # исходник недоступен (код вставлен в REPL) — проверку пропускаем
    recursive, has_loop, used = facts
    assert not has_loop, "в решении есть цикл — задачу нужно решить рекурсией"
    assert "str" not in used, "в решении используется str() — нужны только арифметика и рекурсия"
    assert recursive, "рекурсии нет: ни digit_sum, ни её вспомогательные функции не вызывают сами себя"
