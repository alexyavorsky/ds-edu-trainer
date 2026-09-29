import math


def _checker(first_bad: int):
    """Возвращает is_bad со счётчиком вызовов."""
    calls = []

    def is_bad(k: int) -> bool:
        calls.append(k)
        if len(calls) > 400:
            raise AssertionError("уже больше 400 вызовов is_bad — похоже на перебор сборок подряд")
        return k >= first_bad

    return is_bad, calls


def _limit(n: int) -> int:
    """Бинарному поиску хватает ⌈log₂ n⌉ + 1 вызовов; допускаем втрое больше."""
    return 3 * (math.ceil(math.log2(n)) + 1)


def test_example():
    """Сломаны 4..7 → 4"""
    is_bad, _ = _checker(4)
    got = first_bad_build(7, is_bad)
    assert got == 4, f"ожидалось 4, получено {got!r}"


def test_all_good():
    """Все сборки исправны → -1"""
    is_bad, _ = _checker(10**20)
    got = first_bad_build(50, is_bad)
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_all_bad():
    """Сломана уже первая сборка → 1"""
    is_bad, _ = _checker(1)
    got = first_bad_build(50, is_bad)
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_last_bad():
    """Сломана только последняя сборка"""
    is_bad, _ = _checker(50)
    got = first_bad_build(50, is_bad)
    assert got == 50, f"ожидалось 50, получено {got!r}"


def test_single_build():
    """Одна сборка: сломана и исправна"""
    is_bad, _ = _checker(1)
    assert first_bad_build(1, is_bad) == 1, "единственная сборка сломана — ожидалось 1"
    is_bad, _ = _checker(2)
    assert first_bad_build(1, is_bad) == -1, "единственная сборка исправна — ожидалось -1"


def test_every_answer_small():
    """n = 20: правильный ответ для любой первой сломанной сборки"""
    for first in range(1, 22):
        is_bad, _ = _checker(first)
        got = first_bad_build(20, is_bad)
        expected = first if first <= 20 else -1
        assert got == expected, f"первая сломанная {first}: ожидалось {expected}, получено {got!r}"


def test_range_respected():
    """is_bad вызывается только для номеров от 1 до n — и когда сломана первая, и когда все исправны"""
    for first in (1, 2, 100, 10**20):
        is_bad, calls = _checker(first)
        first_bad_build(100, is_bad)
        wrong = [k for k in calls if not 1 <= k <= 100]
        assert not wrong, f"первая сломанная {first}: is_bad вызвана для несуществующих сборок {wrong[:5]}"


def test_few_calls():
    """n = 10¹²: верные ответы и не больше 123 вызовов is_bad"""
    n = 10**12
    for first in (1, 777_777_777_777, n, n + 1):
        is_bad, calls = _checker(first)
        got = first_bad_build(n, is_bad)
        expected = first if first <= n else -1
        assert got == expected, f"первая сломанная {first}: ожидалось {expected}, получено {got!r}"
        assert len(calls) <= _limit(n), (
            f"первая сломанная {first}: сделано {len(calls)} вызовов is_bad при лимите {_limit(n)} "
            "(бинарному поиску хватает ~41) — похоже на перебор или лишние проверки на каждом шаге"
        )
