"""
Lab 1 - Question 1: Empirical Growth Rate Measurement
Linear Search vs Binary Search
Student Number: 02230309
"""

import random
import time

from Lab1_Q1_LinearSearch import linear_search_309
from Lab1_Q1_BinarySearch import binary_search_309

INPUT_SIZES_309 = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
TRIALS_309 = 5  # number of repeated searches averaged per size


def generate_dataset_309(n):
    """Generates a list of n random integers."""
    return [random.randint(0, n * 10) for _ in range(n)]


def average_time_309(search_func_309, arr, targets_309):
    """
    Runs `search_func_309` once per value in `targets_309`
    and returns the average execution time in seconds.
    """
    start_309 = time.perf_counter()
    for value_309 in targets_309:
        search_func_309(arr, value_309)
    end_309 = time.perf_counter()
    return (end_309 - start_309) / len(targets_309)


def run_benchmark_309():
    print(f"{'N':>10} | {'Linear Search (s)':>20} | {'Binary Search (s)':>20}")
    print("-" * 56)

    results_309 = []

    for n_309 in INPUT_SIZES_309:
        dataset_309 = generate_dataset_309(n_309)
        sorted_dataset_309 = sorted(dataset_309)

        # Mix of present and absent targets, some picked from real data
        targets_309 = [random.choice(dataset_309) for _ in range(TRIALS_309)]

        linear_time_309 = average_time_309(linear_search_309, dataset_309, targets_309)
        binary_time_309 = average_time_309(binary_search_309, sorted_dataset_309, targets_309)

        results_309.append((n_309, linear_time_309, binary_time_309))
        print(f"{n_309:>10} | {linear_time_309:>20.8f} | {binary_time_309:>20.8f}")

    return results_309


if __name__ == "__main__":
    run_benchmark_309()
