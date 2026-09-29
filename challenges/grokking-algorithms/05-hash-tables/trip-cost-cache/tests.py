PRICES = {"Казань": 3000, "Сочи": 5000, "Омск": 4200, "Тверь": 900}


def _server():
    """Возвращает fetch_price со счётчиком запросов по городам."""
    calls: dict[str, int] = {}

    def fetch_price(city: str) -> int:
        calls[city] = calls.get(city, 0) + 1
        return PRICES[city]

    return fetch_price, calls


def test_example_total():
    """Пример: Казань, Сочи, Казань → 11000"""
    fetch, _ = _server()
    got = trip_cost(["Казань", "Сочи", "Казань"], fetch)
    assert got == 11000, f"ожидалось 11000, получено {got!r}"


def test_example_calls():
    """Пример: Казань запрошена один раз, хотя встречается дважды"""
    fetch, calls = _server()
    trip_cost(["Казань", "Сочи", "Казань"], fetch)
    assert calls == {"Казань": 1, "Сочи": 1}, f"запросы к серверу: {calls}"


def test_empty():
    """Пустой маршрут → 0, без запросов"""
    fetch, calls = _server()
    got = trip_cost([], fetch)
    assert got == 0 and not calls, f"итог {got!r}, запросы {calls}"


def test_single_city_many_times():
    """Один город пять раз подряд — один запрос"""
    fetch, calls = _server()
    got = trip_cost(["Тверь"] * 5, fetch)
    assert got == 4500, f"ожидалось 4500, получено {got!r}"
    assert calls == {"Тверь": 1}, f"запросы к серверу: {calls}"


def test_all_different():
    """Все города разные — по одному запросу на город"""
    fetch, calls = _server()
    got = trip_cost(list(PRICES), fetch)
    assert got == sum(PRICES.values()), f"ожидалось {sum(PRICES.values())}, получено {got!r}"
    assert all(n == 1 for n in calls.values()) and len(calls) == 4, f"запросы к серверу: {calls}"


def test_long_route():
    """Длинный маршрут с повторами"""
    route = ["Омск", "Сочи", "Омск", "Тверь", "Сочи", "Омск", "Казань", "Тверь"]
    fetch, calls = _server()
    got = trip_cost(route, fetch)
    expected = sum(PRICES[c] for c in route)
    assert got == expected, f"ожидалось {expected}, получено {got!r}"
    assert sum(calls.values()) == 4, f"сделано {sum(calls.values())} запросов, нужно 4: {calls}"
