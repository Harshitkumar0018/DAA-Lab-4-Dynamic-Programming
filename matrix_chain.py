"""Matrix Chain Multiplication using interval Dynamic Programming."""
import random


def matrix_chain(dims):
    """
    dims contains n+1 dimensions for n matrices.
    Return (minimum_cost, cost_table, split_table).
    """
    if len(dims) < 2 or any(d <= 0 for d in dims):
        raise ValueError("Provide at least two positive dimensions.")

    n = len(dims) - 1
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float("inf")
            for k in range(i, j):
                candidate = (
                    cost[i][k]
                    + cost[k + 1][j]
                    + dims[i] * dims[k + 1] * dims[j + 1]
                )
                if candidate < cost[i][j]:
                    cost[i][j] = candidate
                    split[i][j] = k

    return cost[0][n - 1], cost, split


def parenthesize(split, i, j):
    if i == j:
        return f"M{i + 1}"
    k = split[i][j]
    return "(" + parenthesize(split, i, k) + " x " + parenthesize(split, k + 1, j) + ")"


def make_dims(n, seed=31, low=10, high=100):
    rng = random.Random(seed)
    return [rng.randint(low, high) for _ in range(n + 1)]


if __name__ == "__main__":
    dims = [40, 20, 30, 10, 30]
    best, cost, split = matrix_chain(dims)
    print("MATRIX CHAIN MULTIPLICATION")
    print(f"Dimensions: {dims}")
    print(f"Number of matrices: {len(dims) - 1}")
    print(f"Minimum multiplication cost: {best}")
    print(f"Optimal order: {parenthesize(split, 0, len(dims) - 2)}")
    print("Cost Table:")
    for row in cost:
        print(" ".join(f"{value:8.0f}" for value in row))
    print("Split Table (0-indexed k):")
    for row in split:
        print(" ".join(f"{value:2d}" for value in row))
