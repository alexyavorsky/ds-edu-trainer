После работы алгоритма Дейкстры остаётся таблица родителей: `parents[x]` — узел, из которого выгоднее всего прийти в `x`. Допишите `restore_path(parents, start, goal)`: функция восстанавливает путь от `start` до `goal` в виде списка узлов. Если `goal` недостижим (его нет в таблице и он не совпадает со `start`), она возвращает `[]`. Пропуски помечены `# TODO`.

## Пример

```python
parents = {"B": "start", "A": "B", "fin": "A"}
restore_path(parents, "start", "fin")    # ["start", "B", "A", "fin"]
restore_path(parents, "start", "start")  # ["start"]
restore_path(parents, "start", "X")      # []
```
