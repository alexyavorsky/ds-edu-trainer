def normalize(rows: list[list[float]]) -> list[list[float]]:
    """Min-max нормализация каждого столбца к отрезку [0, 1]."""
    if not rows:
        return []
    columns = len(rows[0])
    mins = [min(row[j] for row in rows) for j in range(columns)]
    maxs = [max(row[j] for row in rows) for j in range(columns)]
    result = []
    for row in rows:
        new_row = []
        for j, x in enumerate(row):
            span = maxs[j] - mins[j]
            new_row.append((x - mins[j]) / span if span else 0.0)
        result.append(new_row)
    return result
