# problem1/generate_data.py

import json
import random
from typing import List, Dict


def generate_instance(
    num_advertisers: int,
    num_impressions: int,
    p_eligible: float,
    seed: int = 42,
):
    """
    Generate synthetic Problem 1 instance.
    """
    random.seed(seed)

    advertisers: List[str] = [f"a{k}" for k in range(num_advertisers)]
    impressions: List[str] = [f"i{k}" for k in range(num_impressions)]

    budgets: Dict[str, int] = {
        a: random.randint(5, 20) for a in advertisers
    }

    edges = []
    for a in advertisers:
        for i in impressions:
            if random.random() < p_eligible:
                value = random.randint(1, 10)
                edges.append(
                    {"advertiser": a, "impression": i, "value": value}
                )

    instance = {
        "advertisers": advertisers,
        "impressions": impressions,
        "budgets": budgets,
        "edges": edges,
    }
    return instance


def save_instance(instance, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(instance, f, indent=2)


if __name__ == "__main__":
    inst = generate_instance(
        num_advertisers=10,
        num_impressions=100,
        p_eligible=0.2,
        seed=42,
    )
    save_instance(inst, "sample_instance.json")
    print("Sample Problem 1 instance saved to problem1/sample_instance.json")
