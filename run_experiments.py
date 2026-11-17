"""Benchmark DP algorithms and save timing, memory and state-count CSV files."""
import csv
import gc
import os
import statistics
import time
import tracemalloc

from lcs import lcs_table, make_strings
from knapsack_dp import knapsack_dp, make_items
from matrix_chain import matrix_chain, make_dims

OUT = "outputs"
os.makedirs(OUT, exist_ok=True)


def measure(func, repeats=5):
    times = []
    for _ in range(repeats):
        gc.collect()
        start = time.perf_counter()
        func()
        times.append(time.perf_counter() - start)

    memory_values = []
    for _ in range(3):
        gc.collect()
        tracemalloc.start()
        func()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory_values.append(peak / 1024)

    return statistics.median(times), statistics.median(memory_values)


def main():
    rows = []

    # LCS: m*n non-boundary DP states.
    for n in [50,  100, 200, 400, 800, 1200]:
        a, b = make_strings(n, seed=23)
        fn = lambda a=a, b=b: lcs_table(a, b)
        elapsed, memory = measure(fn)
        states = n * n
        rows.append(["LCS", n, elapsed, memory, states])
        print(f"LCS n={n:4d} time={elapsed:.6f}s memory={memory:.2f} KiB states={states}")

    # Knapsack: capacity is 2*n; states = n * capacity (non-boundary).
    for n in [50, 100, 200, 400, 800]:
        items = make_items(n, seed=29)
        capacity = 2 * n
        fn = lambda items=items, capacity=capacity: knapsack_dp(items, capacity)
        elapsed, memory = measure(fn)
        states = n * capacity
        rows.append(["0/1 Knapsack", n, elapsed, memory, states])
        print(f"Knapsack n={n:4d} time={elapsed:.6f}s memory={memory:.2f} KiB states={states}")

    # Matrix Chain: n(n+1)/2 intervals.
    for n in [10, 20, 40, 80, 120, 160]:
        dims = make_dims(n, seed=31)
        fn = lambda dims=dims: matrix_chain(dims)
        elapsed, memory = measure(fn)
        states = n * (n + 1) // 2
        rows.append(["Matrix Chain", n, elapsed, memory, states])
        print(f"Matrix Chain n={n:4d} time={elapsed:.6f}s memory={memory:.2f} KiB states={states}")

    path = os.path.join(OUT, "benchmark_results.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Input_Size", "Time_Seconds", "Peak_Memory_KiB", "Subproblems"])
        writer.writerows(rows)
    print(f"\\nSaved benchmark data to {path}")

    # Naive recursive LCS comparison; intentionally limited to small inputs.
    recursive_rows = []
    for n in [6, 8, 10, 12, 14, 16]:
        a, b = make_strings(n, seed=23)
        start = time.perf_counter()
        _, calls = __import__("lcs").lcs_recursive(a, b)
        recursive_time = time.perf_counter() - start
        dp_start = time.perf_counter()
        lcs_table(a, b)
        dp_time = time.perf_counter() - dp_start
        recursive_rows.append([n, recursive_time, calls, dp_time, n * n])
        print(f"LCS recursion n={n:2d} calls={calls:,} recursive={recursive_time:.6f}s DP={dp_time:.6f}s")

    rpath = os.path.join(OUT, "recursive_vs_dp.csv")
    with open(rpath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["String_Length", "Recursive_Time_Seconds", "Recursive_Calls",
                         "DP_Time_Seconds", "DP_Interior_Cells"])
        writer.writerows(recursive_rows)
    print(f"Saved recursion comparison to {rpath}")


if __name__ == "__main__":
    main()
