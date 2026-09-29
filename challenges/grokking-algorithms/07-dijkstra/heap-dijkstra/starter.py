import heapq


def shortest_costs(graph: dict[str, dict[str, int]], start: str) -> dict[str, int]:
    """Минимальные стоимости от start до всех достижимых узлов."""
    costs = {start: 0}
    processed: set[str] = set()
    heap = [(0, start)]
    while heap:
        cost, node = heap.pop()
        if node in processed:
            continue
        processed.add(node)
        for neighbor, weight in graph.get(node, {}).items():
            new_cost = cost + weight
            if neighbor not in processed and new_cost < costs.get(neighbor, new_cost + 1):
                costs[neighbor] = new_cost
                processed.add(neighbor)
                heapq.heappush(heap, (new_cost, neighbor))
    return costs
