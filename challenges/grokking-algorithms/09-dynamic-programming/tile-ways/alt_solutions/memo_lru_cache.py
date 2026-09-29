from functools import lru_cache


@lru_cache(maxsize=None)
def tile_ways(n: int) -> int:
    """Число способов выложить дорожку длины n плитками длины 1 и 2."""
    if n <= 1:
        return 1
    return tile_ways(n - 1) + tile_ways(n - 2)
