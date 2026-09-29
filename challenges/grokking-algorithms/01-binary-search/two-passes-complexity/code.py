def price_range(prices: list[int]) -> int:
    lowest = prices[0]
    for p in prices:
        if p < lowest:
            lowest = p
    highest = prices[0]
    for p in prices:
        if p > highest:
            highest = p
    return highest - lowest
