import math


def test_load_factor_value():
    """load_factor: 3 элемента в 4 корзинах → 0.75 до роста"""
    table = GrowingHashTable()
    table.count = 3
    got = table.load_factor()
    assert math.isclose(got, 0.75), f"ожидалось 0.75, получено {got!r}"


def test_grows_at_right_moment():
    """Третья вставка (3/4 = 0.75 > 0.7) удваивает таблицу до 8 корзин"""
    table = GrowingHashTable()
    table.put(0, "a")
    table.put(1, "b")
    assert len(table.buckets) == 4, f"после 2 вставок корзин {len(table.buckets)}, ожидалось 4"
    table.put(2, "c")
    assert len(table.buckets) == 8, f"после 3 вставок корзин {len(table.buckets)}, ожидалось 8"


def test_load_factor_bounded():
    """После каждой вставки коэффициент заполнения не больше 0.7"""
    table = GrowingHashTable()
    for i in range(200):
        table.put(f"key{i}", i)
        assert table.load_factor() <= 0.7, f"после {i + 1} вставок коэффициент {table.load_factor():.2f}"


def test_get_after_resize():
    """Все ключи находятся после нескольких удвоений"""
    table = GrowingHashTable()
    for i in range(50):
        table.put(i, i * 10)
    missing = [i for i in range(50) if table.get(i) != i * 10]
    assert not missing, f"не находятся ключи: {missing[:8]}"


def test_keys_in_right_buckets():
    """После роста каждая пара лежит в корзине hash(key) % size"""
    table = GrowingHashTable()
    for i in range(20):
        table.put(f"k{i}", i)
    size = len(table.buckets)
    for index, bucket in enumerate(table.buckets):
        for key, _ in bucket:
            assert hash(key) % size == index, f"{key!r} в корзине {index}, а должен в {hash(key) % size}"


def test_update_does_not_grow():
    """Обновление существующего ключа не увеличивает count"""
    table = GrowingHashTable()
    table.put("x", 1)
    table.put("x", 2)
    assert table.count == 1 and table.get("x") == 2, f"count = {table.count}, x = {table.get('x')!r}"


def test_missing_key():
    """Отсутствующий ключ → default"""
    table = GrowingHashTable()
    table.put("a", 1)
    assert table.get("b") is None and table.get("b", 0) == 0, "для отсутствующего ключа — default"
