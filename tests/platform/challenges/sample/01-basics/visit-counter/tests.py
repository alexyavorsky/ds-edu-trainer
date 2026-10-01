def test_start():
    """Новый счётчик показывает 0"""
    assert VisitCounter().value == 0


def test_increment():
    """increment() три раза — value == 3"""
    c = VisitCounter()
    for _ in range(3):
        c.increment()
    assert c.value == 3


def test_independent():
    """Два счётчика не мешают друг другу"""
    a, b = VisitCounter(), VisitCounter()
    a.increment()
    assert (a.value, b.value) == (1, 0)


def test_sample_day():
    """События sample_visits(): к вечеру 3 посетителя"""
    c = VisitCounter()
    for event in sample_visits():
        if event == "in":
            c.increment()
        else:
            c.reset()
    assert c.value == 3
