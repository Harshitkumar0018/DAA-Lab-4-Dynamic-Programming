"""Create benchmark graphs and representative DP table heatmaps."""
import csv
import os
import matplotlib.pyplot as plt

OUT = "outputs"
os.makedirs(OUT, exist_ok=True)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def save_line_plot(rows, x_key, y_key, title, ylabel, filename, log=False):
    plt.figure(figsize=(8, 5))
    groups = {}
    for row in rows:
        groups.setdefault(row["Algorithm"], []).append(row)
    for name, group in groups.items():
        group.sort(key=lambda r: int(r[x_key]))
        x = [int(r[x_key]) for r in group]
        y = [float(r[y_key]) for r in group]
        plt.plot(x, y, marker="o", label=name)
    if log:
        plt.xscale("log")
        plt.yscale("log")
    plt.xlabel("Input size")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, which="both", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, filename), dpi=180)
    plt.close()


def main():
    path = os.path.join(OUT, "benchmark_results.csv")
    if not os.path.exists(path):
        raise SystemExit("Run python run_experiments.py first.")

    rows = read_csv(path)
    save_line_plot(rows, "Input_Size", "Time_Seconds",
                   "Execution Time vs Input Size", "Execution time (seconds)",
                   "runtime_comparison.png", log=True)
    save_line_plot(rows, "Input_Size", "Peak_Memory_KiB",
                   "Peak Memory vs Input Size", "Peak memory (KiB)",
                   "memory_comparison.png", log=True)

    rec_path = os.path.join(OUT, "recursive_vs_dp.csv")
    if os.path.exists(rec_path):
        rec = read_csv(rec_path)
        x = [int(r["String_Length"]) for r in rec]
        calls = [int(r["Recursive_Calls"]) for r in rec]
        cells = [int(r["DP_Interior_Cells"]) for r in rec]
        plt.figure(figsize=(8, 5))
        plt.plot(x, calls, marker="o", label="Naive recursive calls")
        plt.plot(x, cells, marker="o", label="DP interior cells")
        plt.yscale("log")
        plt.xlabel("String length")
        plt.ylabel("Number of calls / states (log scale)")
        plt.title("Naive Recursion vs Dynamic Programming")
        plt.grid(True, which="both", alpha=0.35)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(OUT, "recursion_vs_dp.png"), dpi=180)
        plt.close()

    # LCS table heatmap
    from lcs import lcs_table
    a, b = "AGGTAB", "GXTXAYB"
    table = lcs_table(a, b)
    plt.figure(figsize=(8, 5))
    plt.imshow(table, aspect="auto")
    plt.colorbar(label="LCS length")
    plt.xticks(range(len(b) + 1), ["∅"] + list(b))
    plt.yticks(range(len(a) + 1), ["∅"] + list(a))
    plt.xlabel("String B prefix")
    plt.ylabel("String A prefix")
    plt.title("LCS Dynamic Programming Table")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "lcs_dp_table.png"), dpi=180)
    plt.close()

    # Knapsack table heatmap
    from knapsack_dp import DEMO_ITEMS, DEMO_CAPACITY, knapsack_dp
    _, kn_table, _ = knapsack_dp(DEMO_ITEMS, DEMO_CAPACITY)
    plt.figure(figsize=(9, 5))
    plt.imshow(kn_table, aspect="auto")
    plt.colorbar(label="Best value")
    plt.xlabel("Capacity")
    plt.ylabel("Number of items considered")
    plt.title("0/1 Knapsack DP Table")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "knapsack_dp_table.png"), dpi=180)
    plt.close()

    # Matrix-chain cost table heatmap
    from matrix_chain import matrix_chain
    _, mc_table, _ = matrix_chain([40, 20, 30, 10, 30])
    plt.figure(figsize=(6, 5))
    plt.imshow(mc_table, aspect="auto")
    plt.colorbar(label="Minimum multiplication cost")
    plt.xlabel("Ending matrix index")
    plt.ylabel("Starting matrix index")
    plt.title("Matrix Chain Cost Table")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, "matrix_chain_dp_table.png"), dpi=180)
    plt.close()

    print("Created charts and DP table visualizations in the outputs folder.")


if __name__ == "__main__":
    main()
