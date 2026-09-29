def test_example():
    """Пример из условия"""
    cache = PreviewCache(2)
    cache.put("a", "превью A")
    cache.put("b", "превью B")
    assert cache.get("a") == "превью A", "a должно быть в кэше"
    cache.put("c", "превью C")
    assert cache.get("b") is None, "b должно быть вытеснено"
    assert cache.get("a") == "превью A" and cache.get("c") == "превью C", "a и c должны остаться"


def test_missing():
    """Отсутствующий ключ → None"""
    cache = PreviewCache(3)
    assert cache.get("нет") is None, "ожидалось None"


def test_capacity_one():
    """Ёмкость 1: каждый новый ключ вытесняет прежний"""
    cache = PreviewCache(1)
    cache.put("a", "A")
    cache.put("b", "B")
    assert cache.get("a") is None and cache.get("b") == "B", "в кэше должен остаться только b"


def test_update_refreshes():
    """Обновление существующего ключа — тоже обращение и не вытесняет других"""
    cache = PreviewCache(2)
    cache.put("a", "A")
    cache.put("b", "B")
    cache.put("a", "A2")
    cache.put("c", "C")
    assert cache.get("a") == "A2", "a обновлено и использовано недавно — должно остаться"
    assert cache.get("b") is None, "b давно не использовалось — должно быть вытеснено"


def test_update_does_not_evict():
    """Обновление при полном кэше ничего не вытесняет"""
    cache = PreviewCache(2)
    cache.put("a", "A")
    cache.put("b", "B")
    cache.put("b", "B2")
    assert cache.get("a") == "A" and cache.get("b") == "B2", "оба ключа должны остаться"


def test_get_refreshes():
    """get тоже продлевает жизнь элемента"""
    cache = PreviewCache(3)
    for key in "abc":
        cache.put(key, key.upper())
    cache.get("a")
    cache.get("b")
    cache.put("d", "D")
    assert cache.get("c") is None, "c использовалось давнее всех — должно быть вытеснено"
    assert all(cache.get(k) == k.upper() for k in "abd"), "a, b, d должны остаться"


def test_get_missing_does_not_change_order():
    """Промах get не влияет на порядок вытеснения"""
    cache = PreviewCache(2)
    cache.put("a", "A")
    cache.put("b", "B")
    cache.get("zzz")
    cache.put("c", "C")
    assert cache.get("a") is None and cache.get("b") == "B", "вытеснено должно быть a"


def test_many_operations():
    """50 000 операций на кэше из 1000 элементов: верное содержимое и без зависания"""
    cache = PreviewCache(1000)
    for i in range(50_000):
        cache.put(str(i), f"p{i}")
        cache.get(str(i // 2))
    assert cache.get("49999") == "p49999", "последний элемент должен быть в кэше"
    assert cache.get("0") is None, "самые старые элементы должны быть вытеснены"
    assert cache.get("49000") == "p49000", "в кэше должны остаться последние 1000 добавленных превью"
    assert cache.get("48999") is None, "превью, добавленное 1001-м с конца, должно быть вытеснено"


test_many_operations.timeout = 5
