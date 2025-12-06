# problem2/generate_influencer_data.py

import json
import random
from typing import Dict, List


def generate_influencer_instance(
    num_users: int,
    num_influencers: int,
    p_follow: float,
    seed: int = 123,
):
    """
    Generate random influencer selection instance.

    Users: "u0",...
    Influencers: "inf0",...
    Each user follows influencer i with probability p_follow.
    """
    random.seed(seed)

    users: List[str] = [f"u{k}" for k in range(num_users)]
    influencers: List[str] = [f"inf{k}" for k in range(num_influencers)]

    followers: Dict[str, List[str]] = {inf: [] for inf in influencers}

    for u in users:
        for inf in influencers:
            if random.random() < p_follow:
                followers[inf].append(u)

    instance = {
        "users": users,
        "influencers": influencers,
        "followers": followers,
    }
    return instance


def save_influencer_instance(instance, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(instance, f, indent=2)


if __name__ == "__main__":
    inst = generate_influencer_instance(
        num_users=1000,
        num_influencers=50,
        p_follow=0.05,
        seed=123,
    )
    save_influencer_instance(inst, "sample_influencer_instance.json")
    print("Sample Problem 2 influencer instance saved to problem2/sample_influencer_instance.json")
