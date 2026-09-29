def normalize(rows: list[list[float]]) -> list[list[float]]:
    """Min-max нормализация каждого столбца к отрезку [0, 1]."""
    if not rows:
        return []
    columns = len(rows[0])
    # TODO: минимум и максимум каждого столбца
    mins = [0.0] * columns
    maxs = [1.0] * columns
    result = []
    for row in rows:
        new_row = []
        for j, x in enumerate(row):
            # TODO: нормализованное значение (0.0, если столбец постоянный)
            new_row.append(x)
        result.append(new_row)
    return result
