from collections import deque


def maze_steps(maze: list[str]) -> int:
    """Минимальное число шагов от S до E или -1."""
    rows, cols = len(maze), len(maze[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if maze[r][c] == "S")
    dist = {start: 0}
    queue = deque([start])
    while queue:
        r, c = queue.popleft()
        if maze[r][c] == "E":
            return dist[(r, c)]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            # TODO: если (nr, nc) внутри поля, не стена и ещё не посещена —
            #       запишите расстояние и поставьте клетку в очередь
            pass
    return -1
