"""Interactive command-line menu for the Lab 4 DP algorithms."""
from lcs import lcs_table, lcs_string, lcs_recursive
from knapsack_dp import DEMO_ITEMS, DEMO_CAPACITY, knapsack_dp, knapsack_1d
from matrix_chain import matrix_chain, parenthesize


def run_lcs():
    a = input("First string [AGGTAB]: ").strip() or "AGGTAB"
    b = input("Second string [GXTXAYB]: ").strip() or "GXTXAYB"
    dp = lcs_table(a, b)
    print(f"LCS length: {dp[-1][-1]}")
    print(f"One LCS: {lcs_string(a, b)}")
    if max(len(a), len(b)) <= 20:
        _, calls = lcs_recursive(a, b)
        print(f"Naive recursive calls: {calls}")
    print("DP Table:")
    for row in dp:
        print(" ".join(f"{v:2d}" for v in row))


def run_knapsack():
    print(f"Demo items (name, value, weight): {DEMO_ITEMS}")
    raw = input(f"Capacity [{DEMO_CAPACITY}]: ").strip()
    try:
        capacity = int(raw) if raw else DEMO_CAPACITY
        best, dp, chosen = knapsack_dp(DEMO_ITEMS, capacity)
    except ValueError as exc:
        print(f"Invalid input: {exc}")
        return
    print(f"Maximum value: {best}")
    print(f"Selected items: {chosen}")
    print(f"One-row check: {knapsack_1d(DEMO_ITEMS, capacity)}")
    print("DP Table:")
    for row in dp:
        print(" ".join(f"{v:4d}" for v in row))


def run_matrix_chain():
    raw = input("Dimensions [40 20 30 10 30]: ").strip()
    try:
        dims = [int(x) for x in (raw or "40 20 30 10 30").split()]
        best, cost, split = matrix_chain(dims)
    except ValueError as exc:
        print(f"Invalid input: {exc}")
        return
    print(f"Minimum cost: {best}")
    print(f"Optimal order: {parenthesize(split, 0, len(dims) - 2)}")
    print("Cost Table:")
    for row in cost:
        print(" ".join(f"{v:8.0f}" for v in row))
    print("Split Table:")
    for row in split:
        print(" ".join(f"{v:2d}" for v in row))


def main():
    while True:
        print("\\n========== DAA LAB 4: DYNAMIC PROGRAMMING ==========")
        print("1. Longest Common Subsequence")
        print("2. 0/1 Knapsack")
        print("3. Matrix Chain Multiplication")
        print("4. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            run_lcs()
        elif choice == "2":
            run_knapsack()
        elif choice == "3":
            run_matrix_chain()
        elif choice == "4":
            print("Program closed.")
            break
        else:
            print("Please enter a valid choice from 1 to 4.")


if __name__ == "__main__":
    main()
