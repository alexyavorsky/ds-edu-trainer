Рейсы заданы графом цен `flights[a][b]`. Путешественник готов сделать **не больше `max_flights` перелётов**. Напишите `cheapest_limited(flights, start, goal, max_flights)`: функция возвращает минимальную цену с этим ограничением или `None`, если уложиться нельзя.

## Пример

```python
flights = {
    "A": {"B": 100, "D": 500},
    "B": {"C": 100},
    "C": {"D": 100},
}
cheapest_limited(flights, "A", "D", 3)   # 300: A → B → C → D
cheapest_limited(flights, "A", "D", 2)   # 500: трём перелётам нельзя — летим напрямую
cheapest_limited(flights, "A", "C", 1)   # None
```

## Ограничения

- Цены неотрицательные, `max_flights >= 0`. Если `start == goal`, ответ `0`.
