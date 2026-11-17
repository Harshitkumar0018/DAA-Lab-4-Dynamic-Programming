"""0/1 Knapsack: full DP table, chosen items and one-row optimization."""
import random

# Each item is represented as (name, value, weight).
DEMO_ITEMS = [
    ("map", 10, 5),
    ("compass", 40, 4),
    ("water", 30, 6),
    ("tent", 50, 9),
    ("food", 35, 5),
    ("radio", 25, 3),
]
DEMO_CAPACITY = 15


def knapsack_dp(items, capacity):
    """Return (best_value, table, chosen_item_names)."""
    if capacity < 0:
        raise ValueError("Capacity must be zero or greater.")

    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        _, value, weight = items[i - 1]
        for room in range(capacity + 1):
            dp[i][room] = dp[i - 1][room]
            if weight <= room:
                dp[i][room] = max(
                    dp[i][room],
                    dp[i - 1][room - weight] + value
                )

    chosen = []
    room = capacity
    for i in range(n, 0, -1):
        if dp[i][room] != dp[i - 1][room]:
            chosen.append(items[i - 1][0])
            room -= items[i - 1][2]

    return dp[n][capacity], dp, list(reversed(chosen))


def knapsack_1d(items, capacity):
    """Space-optimized version using O(capacity) auxiliary space."""
    if capacity < 0:
        raise ValueError("Capacity must be zero or greater.")

    best = [0] * (capacity + 1)
    for _, value, weight in items:
        for room in range(capacity, weight - 1, -1):
            best[room] = max(best[room], best[room - weight] + value)
    return best[capacity]


def make_items(n, seed=29, max_value=100, max_weight=100):
    rng = random.Random(seed)
    return [
        (f"item{i:04d}", rng.randint(1, max_value), rng.randint(1, max_weight))
        for i in range(n)
    ]


if __name__ == "__main__":
    best, table, chosen = knapsack_dp(DEMO_ITEMS, DEMO_CAPACITY)
    print("0/1 KNAPSACK")
    print(f"Capacity: {DEMO_CAPACITY}")
    print(f"Items: {DEMO_ITEMS}")
    print(f"Maximum value: {best}")
    print(f"Selected items: {chosen}")
    print(f"One-row optimization check: {knapsack_1d(DEMO_ITEMS, DEMO_CAPACITY)}")
    print("DP Table:")
    for row in table:
        print(" ".join(f"{value:4d}" for value in row))
