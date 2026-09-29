def count_known(queries: list[int], catalog: list[int]) -> int:
    found = 0
    for q in queries:
        low, high = 0, len(catalog) - 1
        while low <= high:
            mid = (low + high) // 2
            if catalog[mid] == q:
                found += 1
                break
            if catalog[mid] < q:
                low = mid + 1
            else:
                high = mid - 1
    return found
