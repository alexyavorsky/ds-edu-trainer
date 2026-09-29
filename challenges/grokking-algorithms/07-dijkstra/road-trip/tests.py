ROADS = [
    ("Тула", "Москва", 150),
    ("Москва", "Тверь", 120),
    ("Тула", "Калуга", 90),
    ("Калуга", "Москва", 40),
    ("Тула", "Москва", 200),
]


def test_example():
    """Тула → Тверь = 250 через Калугу"""
    got = travel_time(ROADS, "Тула", "Тверь")
    assert got == 250, f"ожидалось 250, получено {got!r}"


def test_reverse_direction():
    """Дороги двусторонние: Тверь → Тула = 250"""
    got = travel_time(ROADS, "Тверь", "Тула")
    assert got == 250, f"ожидалось 250, получено {got!r}"


def test_parallel_roads():
    """Из двух дорог между городами берётся быстрая"""
    got = travel_time([("A", "B", 50), ("A", "B", 10), ("B", "A", 30)], "A", "B")
    assert got == 10, f"ожидалось 10, получено {got!r}"


def test_unreachable():
    """Нет пути → None"""
    got = travel_time([("A", "B", 1), ("C", "D", 1)], "A", "D")
    assert got is None, f"ожидалось None, получено {got!r}"


def test_same_city():
    """start == goal → 0, даже без дорог"""
    assert travel_time([], "X", "X") == 0, f"получено {travel_time([], 'X', 'X')!r}"


def test_zero_minutes():
    """Переезды по 0 минут"""
    roads = [("A", "B", 0), ("B", "C", 0), ("A", "C", 5)]
    got = travel_time(roads, "A", "C")
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_grid():
    """Решётка 40×40: в правый нижний угол"""
    roads = []
    for r in range(40):
        for c in range(40):
            if r + 1 < 40:
                roads.append((f"{r},{c}", f"{r + 1},{c}", 1 + (r * c) % 3))
            if c + 1 < 40:
                roads.append((f"{r},{c}", f"{r},{c + 1}", 1 + (r + c) % 2))
    got = travel_time(roads, "0,0", "39,39")
    assert got == 91, f"ожидалось 91, получено {got!r}"
