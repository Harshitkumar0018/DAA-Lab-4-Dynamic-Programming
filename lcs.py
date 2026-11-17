"""Longest Common Subsequence: tabulation, reconstruction and naive recursion."""
import random


def lcs_table(a: str, b: str):
    """Return the complete DP table for strings a and b."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def lcs_length(a: str, b: str) -> int:
    return lcs_table(a, b)[-1][-1]


def lcs_string(a: str, b: str) -> str:
    """Reconstruct one longest common subsequence."""
    dp = lcs_table(a, b)
    i, j = len(a), len(b)
    result = []

    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return "".join(reversed(result))


def lcs_recursive(a: str, b: str):
    """Naive recursion without memoization. Returns (length, call_count)."""
    calls = 0

    def solve(i, j):
        nonlocal calls
        calls += 1
        if i == 0 or j == 0:
            return 0
        if a[i - 1] == b[j - 1]:
            return 1 + solve(i - 1, j - 1)
        return max(solve(i - 1, j), solve(i, j - 1))

    return solve(len(a), len(b)), calls


def make_strings(n, seed=23, alphabet="ACGT"):
    rng = random.Random(seed)
    return (
        "".join(rng.choice(alphabet) for _ in range(n)),
        "".join(rng.choice(alphabet) for _ in range(n)),
    )


if __name__ == "__main__":
    a, b = "AGGTAB", "GXTXAYB"
    dp = lcs_table(a, b)
    print("LONGEST COMMON SUBSEQUENCE")
    print(f"String A: {a}")
    print(f"String B: {b}")
    print(f"LCS length: {dp[-1][-1]}")
    print(f"One LCS: {lcs_string(a, b)}")
    print("DP Table:")
    for row in dp:
        print(" ".join(f"{value:2d}" for value in row))
    length, calls = lcs_recursive(a, b)
    print(f"Naive recursive length: {length}")
    print(f"Naive recursive calls: {calls}")
