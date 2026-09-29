def color_map(neighbors: dict[str, set[str]]) -> dict[str, int]:
    """Жадная раскраска: соседние районы получают разные цвета 0, 1, 2, …"""
    colors: dict[str, int] = {}
    order = sorted(neighbors, key=lambda r: len(neighbors[r]), reverse=True)
    for region in order:
        taken = {colors[n] for n in neighbors[region] if n in colors}
        color = 0
        while color in taken:
            color += 1
        colors[region] = color
    return colors
