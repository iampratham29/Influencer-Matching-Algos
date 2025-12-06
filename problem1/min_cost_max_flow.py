
from typing import List, Tuple, Optional


class Edge:
    """
    Directed edge in residual graph.

    Attributes:
        to: destination vertex index
        rev: index of reverse edge in adjacency list of 'to'
        cap: remaining capacity
        cost: cost per unit of flow
    """
    __slots__ = ("to", "rev", "cap", "cost")

    def __init__(self, to: int, rev: int, cap: int, cost: float) -> None:
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost


def add_edge(graph: List[List[Edge]], fr: int, to: int, cap: int, cost: float) -> None:
    """
    Add a directed edge (fr -> to) with capacity `cap` and cost `cost`,
    plus the corresponding reverse edge (to -> fr) with 0 capacity and -cost.
    """
    forward = Edge(to=to, rev=len(graph[to]), cap=cap, cost=cost)
    backward = Edge(to=fr, rev=len(graph[fr]), cap=0, cost=-cost)
    graph[fr].append(forward)
    graph[to].append(backward)


def bellman_ford(
    graph: List[List[Edge]],
    n: int,
    source: int,
    sink: int
) -> Tuple[List[Optional[float]], List[int], List[int]]:
    """
    Bellman-Ford shortest path for graphs that may contain negative costs.
    Assumes no negative cycles reachable from source.

    Returns:
        dist: list of distances (None if unreachable)
        prev_v: previous vertex on shortest path
        prev_e: index of edge used from prev_v to v
    """
    INF = float("inf")
    dist: List[Optional[float]] = [None] * n
    dist[source] = 0.0
    prev_v = [-1] * n
    prev_e = [-1] * n

    # Relax edges up to n-1 times
    for _ in range(n - 1):
        updated = False
        for v in range(n):
            if dist[v] is None:
                continue
            for ei, e in enumerate(graph[v]):
                if e.cap <= 0:
                    continue
                nd = dist[v] + e.cost
                if dist[e.to] is None or nd < dist[e.to]:
                    dist[e.to] = nd
                    prev_v[e.to] = v
                    prev_e[e.to] = ei
                    updated = True
        if not updated:
            break

    return dist, prev_v, prev_e


def min_cost_max_flow(
    graph: List[List[Edge]],
    source: int,
    sink: int
) -> Tuple[int, float]:
    """
    Compute min-cost max-flow using successive shortest augmenting paths
    and Bellman-Ford for shortest paths.

    Args:
        graph: residual graph as adjacency list of Edge lists
        source: source vertex index
        sink: sink vertex index

    Returns:
        (total_flow, total_cost)
    """
    n = len(graph)
    flow = 0
    cost = 0.0

    while True:
        dist, prev_v, prev_e = bellman_ford(graph, n, source, sink)

        # No more augmenting path
        if dist[sink] is None:
            break

        # Determine bottleneck capacity on the path
        d = float("inf")
        v = sink
        while v != source:
            e = graph[prev_v[v]][prev_e[v]]
            d = min(d, e.cap)
            v = prev_v[v]

        if d == float("inf") or d <= 0:
            break

        # Augment flow and update residual capacities
        v = sink
        while v != source:
            e = graph[prev_v[v]][prev_e[v]]
            e.cap -= d
            graph[v][e.rev].cap += d
            v = prev_v[v]

        flow += d
        cost += dist[sink] * d

    return int(flow), cost
