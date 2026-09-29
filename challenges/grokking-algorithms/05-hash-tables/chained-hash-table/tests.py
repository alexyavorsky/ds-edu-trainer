def test_put_get():
    """put и get для нескольких ключей"""
    table = ChainedHashTable(4)
    table.put("яблоко", 120)
    table.put("молоко", 90)
    assert table.get("яблоко") == 120, f"яблоко: получено {table.get('яблоко')!r}"
    assert table.get("молоко") == 90, f"молоко: получено {table.get('молоко')!r}"


def test_update():
    """Повторный put обновляет значение, а не добавляет второй ключ"""
    table = ChainedHashTable(4)
    table.put("яблоко", 120)
    table.put("яблоко", 110)
    assert table.get("яблоко") == 110, f"получено {table.get('яблоко')!r}"
    assert len(table) == 1, f"len = {len(table)}, ожидалось 1"


def test_missing_default():
    """Отсутствующий ключ → default"""
    table = ChainedHashTable()
    assert table.get("хлеб") is None, "без default должно вернуться None"
    assert table.get("хлеб", 0) == 0, "с default=0 должно вернуться 0"


def test_zero_value():
    """Значение 0 хранится и возвращается (не путать с «нет ключа»)"""
    table = ChainedHashTable()
    table.put("соль", 0)
    assert table.get("соль", -1) == 0, f"получено {table.get('соль', -1)!r}"


def test_all_collide():
    """Одна корзина: все ключи в коллизии, но различаются"""
    table = ChainedHashTable(size=1)
    for i in range(20):
        table.put(f"k{i}", i)
    table.put("k7", 700)
    assert len(table) == 20, f"len = {len(table)}, ожидалось 20"
    assert all(table.get(f"k{i}") == (700 if i == 7 else i) for i in range(20)), "значения перепутались"


def test_keys_in_right_buckets():
    """Каждая пара лежит в корзине hash(key) % size"""
    table = ChainedHashTable(8)
    for i in range(30):
        table.put(f"товар-{i}", i)
    for index, bucket in enumerate(table.buckets):
        for key, _ in bucket:
            assert hash(key) % 8 == index, f"ключ {key!r} лежит в корзине {index}, а должен в {hash(key) % 8}"
    assert len(table) == 30, f"len = {len(table)}, ожидалось 30"


def test_many():
    """1000 ключей в таблице на 64 корзины"""
    table = ChainedHashTable(64)
    for i in range(1000):
        table.put(str(i), i * i)
    assert all(table.get(str(i)) == i * i for i in range(1000)), "не все значения найдены"
    assert table.get("1000") is None, "найден несуществующий ключ"
