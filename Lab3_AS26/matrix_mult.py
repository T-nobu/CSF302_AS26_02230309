"""
matrix_mult.py
Q1: Matrix Multiplication -- Strassen's vs Traditional

Implements:
    - traditional_multiply(A, B): O(n^3) triple nested loop
    - strassen_multiply(A, B):    O(n^log2(7)) ~= O(n^2.807) divide and conquer
                                   (7 recursive multiplications per split)

Matrix sizes are restricted to powers of 2 (2, 4, 8, ..., 128) as required.
The script verifies both algorithms produce identical results, times each,
and plots a runtime comparison graph (matrix_perf.png).
"""

import random
import time
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Traditional O(n^3) multiplication
# ---------------------------------------------------------------------------
def traditional_multiply(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += A[i][k] * B[k][j]
            result[i][j] = total
    return result


# ---------------------------------------------------------------------------
# Matrix helper functions used by Strassen's algorithm
# ---------------------------------------------------------------------------
def add_matrix(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def sub_matrix(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def split_matrix(M):
    """Split an n x n matrix into four (n/2) x (n/2) quadrants."""
    n = len(M)
    mid = n // 2
    top_left = [row[:mid] for row in M[:mid]]
    top_right = [row[mid:] for row in M[:mid]]
    bottom_left = [row[:mid] for row in M[mid:]]
    bottom_right = [row[mid:] for row in M[mid:]]
    return top_left, top_right, bottom_left, bottom_right


def join_matrix(C11, C12, C21, C22):
    """Reassemble four quadrants into a single n x n matrix."""
    top = [r1 + r2 for r1, r2 in zip(C11, C12)]
    bottom = [r1 + r2 for r1, r2 in zip(C21, C22)]
    return top + bottom


# ---------------------------------------------------------------------------
# Strassen's algorithm -- 7 multiplications instead of 8 per split
# ---------------------------------------------------------------------------
def strassen_multiply(A, B):
    n = len(A)

    # Base case: 1x1 "matrix" multiplication is just scalar multiplication.
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    # The 7 Strassen products -- this is where the saving over the
    # traditional 8-multiplication quadrant approach comes from.
    M1 = strassen_multiply(add_matrix(A11, A22), add_matrix(B11, B22))
    M2 = strassen_multiply(add_matrix(A21, A22), B11)
    M3 = strassen_multiply(A11, sub_matrix(B12, B22))
    M4 = strassen_multiply(A22, sub_matrix(B21, B11))
    M5 = strassen_multiply(add_matrix(A11, A12), B22)
    M6 = strassen_multiply(sub_matrix(A21, A11), add_matrix(B11, B12))
    M7 = strassen_multiply(sub_matrix(A12, A22), add_matrix(B21, B22))

    C11 = add_matrix(sub_matrix(add_matrix(M1, M4), M5), M7)
    C12 = add_matrix(M3, M5)
    C21 = add_matrix(M2, M4)
    C22 = add_matrix(sub_matrix(add_matrix(M1, M3), M2), M6)

    return join_matrix(C11, C12, C21, C22)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
def random_matrix(n, low=-10, high=10):
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def matrices_equal(A, B):
    n = len(A)
    return all(A[i][j] == B[i][j] for i in range(n) for j in range(n))


def print_matrix(M, label=""):
    if label:
        print(label)
    for row in M:
        print(row)
    print()


# ---------------------------------------------------------------------------
# Correctness check + timing experiment
# ---------------------------------------------------------------------------
def run_experiment(sizes):
    traditional_times = []
    strassen_times = []

    print(f"{'n':>5} | {'traditional (s)':>16} | {'strassen (s)':>13} | match")
    print("-" * 55)

    for n in sizes:
        A = random_matrix(n)
        B = random_matrix(n)

        start = time.perf_counter()
        trad_result = traditional_multiply(A, B)
        trad_time = time.perf_counter() - start

        start = time.perf_counter()
        strassen_result = strassen_multiply(A, B)
        strassen_time = time.perf_counter() - start

        match = matrices_equal(trad_result, strassen_result)
        print(f"{n:>5} | {trad_time:>16.6f} | {strassen_time:>13.6f} | {match}")

        if not match:
            raise AssertionError(f"Mismatch between algorithms at n={n}")

        traditional_times.append(trad_time)
        strassen_times.append(strassen_time)

    return traditional_times, strassen_times


def plot_results(sizes, traditional_times, strassen_times):
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, traditional_times, marker="o", label="Traditional O(n^3)")
    plt.plot(sizes, strassen_times, marker="o", label="Strassen O(n^2.807)")
    plt.xlabel("Matrix size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Matrix Multiplication: Traditional vs Strassen's")
    plt.xscale("log", base=2)
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("matrix_perf.png")
    print("\nSaved plot to matrix_perf.png")


if __name__ == "__main__":
    # Demonstrate correctness on a small readable example first.
    demo_A = random_matrix(4)
    demo_B = random_matrix(4)
    print_matrix(demo_A, "Matrix A (4x4):")
    print_matrix(demo_B, "Matrix B (4x4):")
    print_matrix(traditional_multiply(demo_A, demo_B), "Traditional result:")
    print_matrix(strassen_multiply(demo_A, demo_B), "Strassen result:")

    # Full experiment across increasing powers of 2.
    sizes = [2, 4, 8, 16, 32, 64, 128]
    traditional_times, strassen_times = run_experiment(sizes)
    plot_results(sizes, traditional_times, strassen_times)

   