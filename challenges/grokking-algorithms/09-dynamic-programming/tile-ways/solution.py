def tile_ways(n: int) -> int:
    """Число способов выложить дорожку длины n плитками длины 1 и 2."""
    ways = [1] + [0] * n  # ways[k] — число дорожек длины k
    for k in range(1, n + 1):
        ways[k] = ways[k - 1] + (ways[k - 2] if k >= 2 else 0)
    return ways[n]
