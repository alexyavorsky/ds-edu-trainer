def tile_ways(n: int) -> int:
    """Число способов выложить дорожку длины n плитками длины 1 и 2."""
    before, current = 1, 1  # ways[k - 1], ways[k]
    for _ in range(n - 1):
        before, current = current, before + current
    return current if n >= 1 else 1
