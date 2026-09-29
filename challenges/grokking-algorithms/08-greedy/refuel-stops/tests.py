def test_example():
    """Пример: 2 заправки"""
    got = refuel_stops([100, 200, 350, 450], 600, 250)
    assert got == 2, f"ожидалось 2, получено {got!r}"


def test_tank_exactly_enough():
    """Бака хватает ровно до финиша → 0"""
    got = refuel_stops([100, 200], 300, 300)
    assert got == 0, f"ожидалось 0, получено {got!r}"


def test_impossible():
    """Разрыв между заправками больше бака → -1"""
    got = refuel_stops([100, 400], 600, 250)
    assert got == -1, f"ожидалось -1, получено {got!r}"


def test_station_at_reach_edge():
    """Заправка ровно на пределе запаса хода — до неё можно доехать"""
    got = refuel_stops([250], 500, 250)
    assert got == 1, f"ожидалось 1, получено {got!r}"


def test_no_stations():
    """Заправок нет"""
    assert refuel_stops([], 100, 150) == 0, "бака хватает — 0"
    assert refuel_stops([], 200, 150) == -1, "бака не хватает — -1"


def test_greedy_farthest():
    """Выбирается самая дальняя из достижимых заправок"""
    got = refuel_stops([10, 20, 30, 40, 50, 60, 70, 80, 90], 100, 50)
    assert got == 1, f"ожидалось 1 (заправка на 50), получено {got!r}"


def test_many_stops():
    """Заправки каждые 10 км, бак на 10 км"""
    got = refuel_stops(list(range(10, 100, 10)), 100, 10)
    assert got == 9, f"ожидалось 9, получено {got!r}"
