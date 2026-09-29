def test_example():
    """Пример из условия"""
    got = distance_to_hub(["A", "B", "C", "D", "E"], [("A", "B"), ("B", "C"), ("C", "D")], {"A", "D"})
    expected = {"A": 0, "B": 1, "C": 1, "D": 0, "E": -1}
    assert got == expected, f"получено {got!r}"


def test_no_hubs():
    """Складов нет → везде -1"""
    got = distance_to_hub(["A", "B"], [("A", "B")], set())
    assert got == {"A": -1, "B": -1}, f"получено {got!r}"


def test_all_hubs():
    """Склад в каждом городе → везде 0"""
    got = distance_to_hub(["A", "B"], [("A", "B")], {"A", "B"})
    assert got == {"A": 0, "B": 0}, f"получено {got!r}"


def test_roads_two_way():
    """Дороги двусторонние: порядок в паре не важен"""
    got = distance_to_hub(["A", "B", "C"], [("B", "A"), ("C", "B")], {"A"})
    assert got == {"A": 0, "B": 1, "C": 2}, f"получено {got!r}"


def test_nearest_not_first():
    """Ближайший склад, а не первый попавшийся"""
    towns = [str(i) for i in range(7)]
    roads = [(str(i), str(i + 1)) for i in range(6)]
    got = distance_to_hub(towns, roads, {"0", "6"})
    expected = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 2, "5": 1, "6": 0}
    assert got == expected, f"получено {got!r}"


def test_cycle():
    """Кольцевая дорога"""
    towns = list("ABCDEF")
    roads = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "A")]
    got = distance_to_hub(towns, roads, {"A"})
    expected = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 2, "F": 1}
    assert got == expected, f"получено {got!r}"


def test_large_line():
    """Цепочка из 20 000 городов со складами по краям: верные расстояния за отведённое время"""
    n = 20_000
    towns = [f"t{i}" for i in range(n)]
    roads = [(f"t{i}", f"t{i + 1}") for i in range(n - 1)]
    got = distance_to_hub(towns, roads, {"t0", f"t{n - 1}"})
    for town, expected in [("t0", 0), ("t1", 1), ("t10000", 9_999), (f"t{n - 2}", 1)]:
        assert got[town] == expected, f"{town}: ожидалось {expected}, получено {got.get(town)!r}"


test_large_line.timeout = 5
test_large_line.timeout_hint = "Если поиск запускается от каждого города отдельно, это O(V · (V + E)) — нужен один общий поиск от всех складов"
