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


def _deep(depth: int) -> list:
    nested: list = [0]
    for i in range(1, depth):
        nested = [nested, i]
    return nested


def test_example():
    """[1, [2, [3, [4]]], 5] → [1, 2, 3, 4, 5]"""
    got = flatten_deep([1, [2, [3, [4]]], 5])
    assert got == [1, 2, 3, 4, 5], f"получено {got!r}"


def test_empty():
    """Пустой список → []"""
    got = flatten_deep([])
    assert got == [], f"получено {got!r}"


def test_only_empty_lists():
    """Только пустые списки → []"""
    got = flatten_deep([[], [[]], [[], [[]]]])
    assert got == [], f"получено {got!r}"


def test_order_and_duplicates():
    """Порядок и дубликаты сохраняются"""
    got = flatten_deep([[1, 1], [[2], 1], [], 3, [[[1]]]])
    assert got == [1, 1, 2, 1, 3, 1], f"получено {got!r}"


def test_deep_left():
    """Вложенность 100 000 уровней: [[[…[0], 1]…], 99999]"""
    got = flatten_deep(_deep(100_000))
    assert got == list(range(100_000)), f"неверный результат, начало: {got[:5] if got else got!r}"


def test_deep_right():
    """Вложенность 100 000 уровней в другую сторону: [0, [1, [2, …]]]"""
    nested: list = []
    for i in range(99_999, -1, -1):
        nested = [i, nested]
    got = flatten_deep(nested)
    assert got == list(range(100_000)), f"неверный результат, начало: {got[:5] if got else got!r}"


def test_input_not_changed():
    """Исходный список не изменяется"""
    data = [1, [2, [3]], []]
    flatten_deep(data)
    assert data == [1, [2, [3]], []], f"список изменился: {data!r}"


def test_no_recursion():
    """Без рекурсии — ни прямой, ни через вспомогательные функции"""
    facts = _code_facts(flatten_deep)
    if facts is None:
        return  # исходник недоступен (код вставлен в REPL) — проверку пропускаем
    recursive, _, _ = facts
    assert not recursive, "в решении есть рекурсия — на глубине 100 000 она упадёт, нужен явный стек"
