# problem1/run_problem1.py

import csv
import time
from pathlib import Path

import matplotlib.pyplot as plt

from generate_data import generate_instance, save_instance
from ad_assignment import solve_ad_assignment


def main():
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "output" / "problem1"
    output_dir.mkdir(parents=True, exist_ok=True)

    results_csv = output_dir / "results_problem1.csv"

    num_advertisers_list = [10, 20]
    num_impressions_list = [100, 200, 500]
    p_eligible_list = [0.1, 0.2, 0.3]

    with open(results_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "num_advertisers",
                "num_impressions",
                "p_eligible",
                "total_flow",
                "total_revenue",
                "runtime_seconds",
            ]
        )

        for m in num_advertisers_list:
            for n in num_impressions_list:
                for p in p_eligible_list:
                    instance = generate_instance(
                        num_advertisers=m,
                        num_impressions=n,
                        p_eligible=p,
                        seed=42,
                    )
                    inst_path = output_dir / f"inst_m{m}_n{n}_p{str(p).replace('.','_')}.json"
                    save_instance(instance, str(inst_path))

                    start = time.perf_counter()
                    res = solve_ad_assignment(str(inst_path))
                    end = time.perf_counter()
                    runtime = end - start

                    writer.writerow(
                        [
                            m,
                            n,
                            p,
                            res["total_flow"],
                            res["total_revenue"],
                            runtime,
                        ]
                    )
                    print(
                        f"[Problem1] m={m}, n={n}, p={p} -> "
                        f"flow={res['total_flow']}, "
                        f"revenue={res['total_revenue']:.2f}, "
                        f"time={runtime:.4f}s"
                    )

    # Load results and make plots
    rows = []
    with open(results_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["num_advertisers"] = int(row["num_advertisers"])
            row["num_impressions"] = int(row["num_impressions"])
            row["p_eligible"] = float(row["p_eligible"])
            row["total_flow"] = int(row["total_flow"])
            row["total_revenue"] = float(row["total_revenue"])
            row["runtime_seconds"] = float(row["runtime_seconds"])
            rows.append(row)

    # Plot: runtime vs impressions (for p=0.2, m=10)
    plt.figure()
    subset = [
        r for r in rows
        if r["num_advertisers"] == 10 and abs(r["p_eligible"] - 0.2) < 1e-9
    ]
    subset.sort(key=lambda r: r["num_impressions"])
    x = [r["num_impressions"] for r in subset]
    y = [r["runtime_seconds"] for r in subset]
    plt.plot(x, y, marker="o")
    plt.xlabel("Number of impressions (n)")
    plt.ylabel("Runtime (seconds)")
    plt.title("Problem 1: Runtime vs Impressions (m=10, p=0.2)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "runtime_vs_impressions.png")

    # Plot: runtime vs density (for n=200, m=10)
    plt.figure()
    subset = [
        r for r in rows
        if r["num_advertisers"] == 10 and r["num_impressions"] == 200
    ]
    subset.sort(key=lambda r: r["p_eligible"])
    x = [r["p_eligible"] for r in subset]
    y = [r["runtime_seconds"] for r in subset]
    plt.plot(x, y, marker="o")
    plt.xlabel("Eligibility probability p")
    plt.ylabel("Runtime (seconds)")
    plt.title("Problem 1: Runtime vs Edge Density (m=10, n=200)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "runtime_vs_density.png")

    # Plot: revenue vs total_flow (scatter)
    plt.figure()
    x = [r["total_flow"] for r in rows]
    y = [r["total_revenue"] for r in rows]
    plt.scatter(x, y)
    plt.xlabel("Total Flow (Assigned Impressions)")
    plt.ylabel("Total Revenue")
    plt.title("Problem 1: Revenue vs Flow")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_dir / "revenue_vs_flow.png")

    print(f"[Problem1] Results and plots saved in {output_dir}")


if __name__ == "__main__":
    main()
