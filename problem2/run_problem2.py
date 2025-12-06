# problem2/run_problem2.py

import csv
import time
from pathlib import Path

import matplotlib.pyplot as plt

from generate_influencer_data import (
    generate_influencer_instance,
    save_influencer_instance,
)
from influencer_selection import (
    load_influencer_instance,
    greedy_influencer_selection,
    random_influencer_selection,
)


def main():
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "output" / "problem2"
    output_dir.mkdir(parents=True, exist_ok=True)

    results_csv = output_dir / "influencer_results_problem2.csv"

    num_users_list = [500, 1000, 2000]
    num_influencers_list = [50, 100]
    p_follow = 0.05
    k_values = [5, 10, 20]

    with open(results_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "num_users",
                "num_influencers",
                "p_follow",
                "k",
                "greedy_coverage",
                "random_coverage",
                "greedy_time",
                "random_time",
            ]
        )

        for n in num_users_list:
            for m in num_influencers_list:
                instance = generate_influencer_instance(
                    num_users=n,
                    num_influencers=m,
                    p_follow=p_follow,
                    seed=123,
                )
                inst_path = output_dir / f"inf_n{n}_m{m}.json"
                save_influencer_instance(instance, str(inst_path))

                users, influencers, follower_sets = load_influencer_instance(
                    str(inst_path)
                )

                for k in k_values:
                    start = time.perf_counter()
                    _, greedy_cov = greedy_influencer_selection(
                        users, influencers, follower_sets, k
                    )
                    greedy_time = time.perf_counter() - start

                    start = time.perf_counter()
                    _, random_cov = random_influencer_selection(
                        users, influencers, follower_sets, k, seed=42
                    )
                    random_time = time.perf_counter() - start

                    writer.writerow(
                        [
                            n,
                            m,
                            p_follow,
                            k,
                            greedy_cov,
                            random_cov,
                            greedy_time,
                            random_time,
                        ]
                    )

                    print(
                        f"[Problem2] n={n}, m={m}, k={k} -> "
                        f"greedy_cov={greedy_cov}, random_cov={random_cov}, "
                        f"greedy_time={greedy_time:.4f}s, random_time={random_time:.4f}s"
                    )

    # Load results and plot
    rows = []
    with open(results_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["num_users"] = int(row["num_users"])
            row["num_influencers"] = int(row["num_influencers"])
            row["p_follow"] = float(row["p_follow"])
            row["k"] = int(row["k"])
            row["greedy_coverage"] = int(row["greedy_coverage"])
            row["random_coverage"] = int(row["random_coverage"])
            row["greedy_time"] = float(row["greedy_time"])
            row["random_time"] = float(row["random_time"])
            rows.append(row)

    # Plot coverage vs k for one (n,m)
    target_n = 1000
    target_m = 100
    subset = [
        r for r in rows
        if r["num_users"] == target_n and r["num_influencers"] == target_m
    ]
    subset.sort(key=lambda r: r["k"])
    ks = [r["k"] for r in subset]
    greedy_cov = [r["greedy_coverage"] for r in subset]
    random_cov = [r["random_coverage"] for r in subset]

    plt.figure()
    plt.plot(ks, greedy_cov, marker="o", label="Greedy")
    plt.plot(ks, random_cov, marker="x", label="Random")
    plt.xlabel("Budget k (influencers)")
    plt.ylabel("Coverage (users reached)")
    plt.title(f"Problem 2: Coverage vs k (n={target_n}, m={target_m})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "influencer_coverage_vs_k.png")

    # Plot runtime vs n for fixed (m,k)
    target_m = 50
    target_k = 10
    subset = [
        r for r in rows
        if r["num_influencers"] == target_m and r["k"] == target_k
    ]
    subset.sort(key=lambda r: r["num_users"])
    ns = [r["num_users"] for r in subset]
    greedy_t = [r["greedy_time"] for r in subset]
    random_t = [r["random_time"] for r in subset]

    plt.figure()
    plt.plot(ns, greedy_t, marker="o", label="Greedy")
    plt.plot(ns, random_t, marker="x", label="Random")
    plt.xlabel("Number of users n")
    plt.ylabel("Runtime (seconds)")
    plt.title(f"Problem 2: Runtime vs n (m={target_m}, k={target_k})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "influencer_runtime_vs_n.png")

    print(f"[Problem2] Results and plots saved in {output_dir}")


if __name__ == "__main__":
    main()
