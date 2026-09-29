SHOWS = [("рок", 3, 50), ("джаз", 2, 30), ("фолк", 2, 35), ("техно", 4, 60)]


def _check(shows, hours, got, best):
    """best — максимальный суммарный рейтинг (заранее посчитан)."""
    assert isinstance(got, list), f"ожидался список индексов, получено {got!r}"
    assert len(set(got)) == len(got) and all(0 <= i < len(shows) for i in got), f"неверные индексы: {got}"
    total_time = sum(shows[i][1] for i in got)
    assert total_time <= hours, f"выбрано на {total_time} ч, а есть только {hours}: {got}"
    rating = sum(shows[i][2] for i in got)
    assert rating == best, f"рейтинг {rating}, а можно набрать {best}: {got}"


def test_example():
    """Пример: рок + фолк = 85"""
    _check(SHOWS, 5, plan_festival(SHOWS, 5), 85)


def test_greedy_fails():
    """Жадный выбор по рейтингу не оптимален"""
    shows = [("A", 5, 60), ("B", 3, 40), ("C", 2, 30)]
    _check(shows, 5, plan_festival(shows, 5), 70)


def test_no_time():
    """0 часов → []"""
    got = plan_festival(SHOWS, 0)
    assert got == [], f"ожидалось [], получено {got!r}"


def test_nothing_fits():
    """Все выступления длиннее свободного времени → []"""
    got = plan_festival([("опера", 5, 100)], 4)
    assert got == [], f"ожидалось [], получено {got!r}"


def test_all_fit():
    """Хватает времени на всё"""
    got = plan_festival(SHOWS, 100)
    assert sorted(got) == [0, 1, 2, 3], f"получено {got!r}"


def test_ten_shows():
    """10 выступлений при разном запасе времени — заранее посчитанный оптимум"""
    shows = [(f"s{i}", (i * 7) % 5 + 1, (i * 13) % 17 + 3) for i in range(10)]
    for hours, best in [(0, 0), (3, 25), (7, 46), (12, 67), (20, 89)]:
        _check(shows, hours, plan_festival(shows, hours), best)


def test_large():
    """36 выступлений, 300 часов — оптимум за отведённое время"""
    shows = [(f"s{i}", (i * 37) % 40 + 1, (i * 53) % 97 + 1) for i in range(36)]
    _check(shows, 300, plan_festival(shows, 300), 1060)


test_large.timeout_hint = "Если это рекурсия, добавьте запоминание: без него перебираются все 2³⁶ наборов"
