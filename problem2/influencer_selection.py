# problem2/influencer_selection.py

import json
import random
from typing import Dict, List, Set, Tuple


def load_influencer_instance(path: str):
    """
    Load influencer instance from JSON:
    {
      "users": [...],
      "influencers": [...],
      "followers": { "inf0": ["u1","u3",...], ... }
    }
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    users: List[str] = data["users"]
    influencers: List[str] = data["influencers"]
    followers_raw: Dict[str, List[str]] = data["followers"]

    follower_sets: Dict[str, Set[str]] = {
        inf: set(flist) for inf, flist in followers_raw.items()
    }

    return users, influencers, follower_sets


def greedy_influencer_selection(
    users: List[str],
    influencers: List[str],
    follower_sets: Dict[str, Set[str]],
    k: int,
):
    """
    Greedy maximum coverage:
    at each step pick influencer with maximum marginal gain.
    """
    selected: List[str] = []
    covered: Set[str] = set()
    remaining = set(influencers)

    for _ in range(k):
        best_inf = None
        best_gain = 0
        for inf in remaining:
            gain = len(follower_sets[inf] - covered)
            if gain > best_gain:
                best_gain = gain
                best_inf = inf

        if best_inf is None or best_gain == 0:
            break

        selected.append(best_inf)
        covered |= follower_sets[best_inf]
        remaining.remove(best_inf)

    return selected, len(covered)


def random_influencer_selection(
    users: List[str],
    influencers: List[str],
    follower_sets: Dict[str, Set[str]],
    k: int,
    seed: int = None,
):
    """
    Baseline: pick k influencers at random (without replacement).
    """
    rng = random.Random(seed)
    if k >= len(influencers):
        chosen = list(influencers)
    else:
        chosen = rng.sample(influencers, k)

    covered: Set[str] = set()
    for inf in chosen:
        covered |= follower_sets[inf]

    return chosen, len(covered)
