def color_map(neighbors: dict[str, set[str]]) -> dict[str, int]:
    """Жадная раскраска: соседние районы получают разные цвета 0, 1, 2, …"""
    colors: dict[str, int] = {}
    order = sorted(neighbors, key=lambda r: len(neighbors[r]), reverse=True)
    for region in order:
        # TODO: соберите цвета, уже занятые соседями region
        taken: set[int] = set()
        color = 0
        # TODO: подберите наименьший цвет, которого нет в taken
        colors[region] = color
    return colors
