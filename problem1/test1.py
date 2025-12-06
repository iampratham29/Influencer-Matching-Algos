# problem1/test1.py

from min_cost_max_flow import Edge, add_edge, min_cost_max_flow
from ad_assignment import solve_ad_assignment
from generate_data import generate_instance, save_instance


def test_min_cost_flow_simple():
    # Tiny sanity check for min-cost max-flow
    # s=0, a=1, b=2, t=3
    s, a, b, t = 0, 1, 2, 3
    graph = [[] for _ in range(4)]

    # s->a cap 2 cost 0; s->b cap 1 cost 0
    add_edge(graph, s, a, 2, 0.0)
    add_edge(graph, s, b, 1, 0.0)
    # a->t cap 2 cost 1; b->t cap 1 cost 2
    add_edge(graph, a, t, 2, 1.0)
    add_edge(graph, b, t, 1, 2.0)

    flow, cost = min_cost_max_flow(graph, s, t)
    assert flow == 3, "Flow should be 3"
    assert abs(cost - 4.0) < 1e-6, "Cost should be 4"


def test_ad_assignment_small():
    # Generate a small instance and just check code runs
    inst = generate_instance(
        num_advertisers=3,
        num_impressions=5,
        p_eligible=0.5,
        seed=1,
    )
    save_instance(inst, "tmp_instance.json")
    res = solve_ad_assignment("tmp_instance.json")
    assert res["total_flow"] >= 0
    print("Problem1 small test passed.")


if __name__ == "__main__":
    test_min_cost_flow_simple()
    test_ad_assignment_small()
    print("All Problem 1 tests passed.")
