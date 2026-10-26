"""
Lab 1 - Question 3: Empirical Growth Rate Measurement
Naive Trial Division vs Optimized Trial Division vs Sieve of Eratosthenes
Student Number: 02230309
"""

import time

from Lab1_Q3_NaiveTrialDivision import primes_up_to_naive_309
from Lab1_Q3_OptimizedTrialDivision import primes_up_to_optimized_309
from Lab1_Q3_SieveOfEratosthenes import sieve_of_eratosthenes_309

INPUT_SIZES_309 = [10_000, 50_000, 100_000, 500_000, 1_000_000]

# Naive trial division is O(n^2) overall and becomes extremely slow at large N.
# Set this to the largest N you are willing to wait for with the naive method.
# Lower this value if the naive run is taking too long on your machine.
NAIVE_MAX_N_309 = 100_000


def timed_run_309(func_309, *args_309):
    start_309 = time.perf_counter()
    func_309(*args_309)
    end_309 = time.perf_counter()
    return end_309 - start_309


def run_benchmark_309():
    print(f"{'N':>10} | {'Naive (s)':>15} | {'Optimized (s)':>15} | {'Sieve (s)':>15}")
    print("-" * 64)

    results_309 = []

    for n_309 in INPUT_SIZES_309:
        if n_309 <= NAIVE_MAX_N_309:
            naive_time_309 = timed_run_309(primes_up_to_naive_309, n_309)
            naive_display_309 = f"{naive_time_309:>15.6f}"
        else:
            naive_time_309 = None
            naive_display_309 = f"{'skipped':>15}"

        optimized_time_309 = timed_run_309(primes_up_to_optimized_309, n_309)
        sieve_time_309 = timed_run_309(sieve_of_eratosthenes_309, n_309)

        results_309.append((n_309, naive_time_309, optimized_time_309, sieve_time_309))
        print(f"{n_309:>10} | {naive_display_309} | {optimized_time_309:>15.6f} | {sieve_time_309:>15.6f}")

    if NAIVE_MAX_N_309 < INPUT_SIZES_309[-1]:
        print(f"\nNote: Naive trial division skipped for N > {NAIVE_MAX_N_309} "
              f"(O(n^2) makes it impractically slow). Adjust NAIVE_MAX_N_309 if needed.")

    return results_309


if __name__ == "__main__":
    run_benchmark_309()
