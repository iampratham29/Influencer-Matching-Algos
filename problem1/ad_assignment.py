# problem1/ad_assignment.py

import json
from typing import Dict, List, Tuple

from min_cost_max_flow import Edge, add_edge, min_cost_max_flow


def build_flow_graph(
    advertisers: List[str],
    impressions: List[str],
    budgets: Dict[str, int],
    edges: List[Tuple[str, str]],
    values: Dict[Tuple[str, str], float],
):
    """
    Build residual graph for ad assignment.

    Node indexing:
        0              : source
        1..m           : advertisers
        m+1..m+n       : impressions
        m+n+1          : sink
    """
    m = len(advertisers)
    n = len(impressions)
    source = 0
    sink = m + n + 1
    num_nodes = sink + 1

    graph: List[List[Edge]] = [[] for _ in range(num_nodes)]

    adv_to_idx = {a: 1 + i for i, a in enumerate(advertisers)}
    imp_to_idx = {i: 1 + m + j for j, i in enumerate(impressions)}

    # Source -> advertisers
    for a in advertisers:
        cap = int(budgets.get(a, 0))
        if cap > 0:
            add_edge(graph, source, adv_to_idx[a], cap, 0.0)

    # Advertisers -> impressions (eligible edges)
    for a, i in edges:
        a_idx = adv_to_idx[a]
        i_idx = imp_to_idx[i]
        val = float(values.get((a, i), 0.0))
        add_edge(graph, a_idx, i_idx, 1, -val)

    # Impressions -> sink
    for i in impressions:
        i_idx = imp_to_idx[i]
        add_edge(graph, i_idx, sink, 1, 0.0)

    return graph, source, sink, adv_to_idx, imp_to_idx


def load_instance_from_json(path: str):
    """
    Load Problem 1 instance from JSON.

    Format:
    {
      "advertisers": ["a0",...],
      "impressions": ["i0",...],
      "budgets": {"a0": 10, ...},
      "edges": [
        {"advertiser": "a0", "impression": "i3", "value": 7.5},
        ...
      ]
    }
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    advertisers = data["advertisers"]
    impressions = data["impressions"]
    budgets = {str(k): int(v) for k, v in data["budgets"].items()}

    edges: List[Tuple[str, str]] = []
    values: Dict[Tuple[str, str], float] = {}
    for e in data["edges"]:
        a = str(e["advertiser"])
        i = str(e["impression"])
        v = float(e["value"])
        edges.append((a, i))
        values[(a, i)] = v

    return advertisers, impressions, budgets, edges, values


def solve_ad_assignment(instance_path: str):
    """
    End-to-end solver: load instance, build graph, run MCMF,
    extract assignments and revenue.
    """
    advertisers, impressions, budgets, edges, values = load_instance_from_json(
        instance_path
    )
    graph, source, sink, adv_to_idx, imp_to_idx = build_flow_graph(
        advertisers, impressions, budgets, edges, values
    )

    total_flow, total_cost = min_cost_max_flow(graph, source, sink)
    total_revenue = -total_cost

    # Recover assignments from residual graph:
    idx_to_adv = {idx: a for a, idx in adv_to_idx.items()}
    idx_to_imp = {idx: i for i, idx in imp_to_idx.items()}

    assignments: List[Tuple[str, str, float]] = []

    for a, a_idx in adv_to_idx.items():
        for edge in graph[a_idx]:
            # If to is impression node, check reverse capacity
            if edge.to in idx_to_imp:
                imp_idx = edge.to
                imp = idx_to_imp[imp_idx]
                rev_edge = graph[imp_idx][edge.rev]
                # If reverse edge capacity > 0, then 1 unit of flow was used
                if rev_edge.cap > 0:
                    value = values.get((a, imp), 0.0)
                    assignments.append((a, imp, value))

    return {
        "total_flow": total_flow,
        "total_revenue": total_revenue,
        "assignments": assignments,
    }
