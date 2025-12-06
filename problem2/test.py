# problem2/test.py

from influencer_selection import (
    greedy_influencer_selection,
    random_influencer_selection,
)


def test_greedy_small():
    users = [f"u{i}" for i in range(5)]
    influencers = ["inf0", "inf1", "inf2"]
    follower_sets = {
        "inf0": {"u0", "u1"},
        "inf1": {"u1", "u2", "u3"},
        "inf2": {"u3", "u4"},
    }
    k = 2
    selected, coverage = greedy_influencer_selection(
        users, influencers, follower_sets, k
    )
    assert len(selected) <= k
    assert coverage >= 3  # small sanity bound
    print("Problem2 greedy small test passed.")


if __name__ == "__main__":
    test_greedy_small()
    print("All Problem 2 tests passed.")
