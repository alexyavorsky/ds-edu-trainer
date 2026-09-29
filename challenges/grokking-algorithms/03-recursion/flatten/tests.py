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
    """[1, [2, 3], [[4]], 5] → [1, 2, 3, 4, 5]"""
    got = flatten([1, [2, 3], [[4]], 5])
    assert got == [1, 2, 3, 4, 5], f"получено {got!r}"


def test_empty():
    """Пустой список → []"""
    got = flatten([])
    assert got == [], f"получено {got!r}"


def test_already_flat():
    """Плоский список не меняется"""
    got = flatten([4, 5, 6])
    assert got == [4, 5, 6], f"получено {got!r}"


def test_only_empty_lists():
    """Только пустые наборы → []"""
    got = flatten([[], [[]], [[[]]]])
    assert got == [], f"получено {got!r}"


def test_single_deep_item():
    """Один артикул глубоко внутри: [[[[7]]]] → [7]"""
    got = flatten([[[[7]]]])
    assert got == [7], f"получено {got!r}"


def test_duplicates():
    """Дубликаты сохраняются"""
    got = flatten([3, [3, [3]], 3])
    assert got == [3, 3, 3, 3], f"получено {got!r}"


def test_order_after_deep_branch():
    """Порядок сохраняется и после глубокой ветки"""
    got = flatten([1, [2, [3, [4, [5]]]], 6, [7]])
    assert got == [1, 2, 3, 4, 5, 6, 7], f"получено {got!r}"


def test_depth_100():
    """Глубина 100"""
    nested: list = [0]
    for i in range(1, 100):
        nested = [nested, i]
    got = flatten(nested)
    assert got == list(range(100)), f"получено {got!r:.80}"


def test_input_not_changed():
    """Исходный список не изменяется"""
    data = [1, [2, [3]]]
    flatten(data)
    assert data == [1, [2, [3]]], f"список изменился: {data!r}"


def test_is_recursive():
    """Решение рекурсивное (можно через вспомогательную функцию)"""
    facts = _code_facts(flatten)
    if facts is None:
        return  # исходник недоступен (код вставлен в REPL) — проверку пропускаем
    recursive, _, _ = facts
    assert recursive, "рекурсии нет: ни flatten, ни её вспомогательные функции не вызывают сами себя"
