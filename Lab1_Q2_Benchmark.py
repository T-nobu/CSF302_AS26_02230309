"""
Lab 1 - Question 2: Empirical Growth Rate Measurement
Bubble Sort vs Merge Sort
Student Number: 02230309
"""

import random
import time

from Lab1_Q2_BubbleSort import bubble_sort_309
from Lab1_Q2_MergeSort import merge_sort_309

INPUT_SIZES_309 = [100, 500, 1_000, 2_000, 4_000, 8_000]
TRIALS_309 = 3  # number of repeated runs averaged per size


def generate_array_309(n):
    """Generates a list of n random integers."""
    return [random.randint(0, n * 10) for _ in range(n)]


def average_time_309(sort_func_309, arrays_309):
    """Runs `sort_func_309` on each array and returns the average time in seconds."""
    start_309 = time.perf_counter()
    for arr_309 in arrays_309:
        sort_func_309(arr_309)
    end_309 = time.perf_counter()
    return (end_309 - start_309) / len(arrays_309)


def run_benchmark_309():
    print(f"{'N':>10} | {'Bubble Sort (s)':>20} | {'Merge Sort (s)':>20}")
    print("-" * 56)

    results_309 = []

    for n_309 in INPUT_SIZES_309:
        trial_arrays_309 = [generate_array_309(n_309) for _ in range(TRIALS_309)]

        bubble_time_309 = average_time_309(bubble_sort_309, trial_arrays_309)
        merge_time_309 = average_time_309(merge_sort_309, trial_arrays_309)

        results_309.append((n_309, bubble_time_309, merge_time_309))
        print(f"{n_309:>10} | {bubble_time_309:>20.8f} | {merge_time_309:>20.8f}")

    return results_309


if __name__ == "__main__":
    run_benchmark_309()
