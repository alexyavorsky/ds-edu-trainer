import math


def find_lowest(costs: dict[str, float], processed: set[str]) -> str | None:
    lowest, lowest_node = math.inf, None
    for node, cost in costs.items():
        if cost < lowest and node not in processed:
            lowest, lowest_node = cost, node
    return lowest_node


def dijkstra(graph: dict[str, dict[str, int]], costs: dict[str, float]) -> dict[str, float]:
    processed: set[str] = set()
    node = find_lowest(costs, processed)
    while node is not None:
        for neighbor, weight in graph[node].items():
            if costs[node] + weight < costs[neighbor]:
                costs[neighbor] = costs[node] + weight
        processed.add(node)
        node = find_lowest(costs, processed)
    return costs
