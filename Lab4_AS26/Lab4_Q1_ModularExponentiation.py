"""Naive and binary modular exponentiation with correctness checks and benchmarks."""

import argparse
import time


def _validate_power_inputs(base: int, exponent: int, modulus: int) -> None:
    if not isinstance(base, int) or isinstance(base, bool):
        raise TypeError("base must be an integer")
    if not isinstance(exponent, int) or isinstance(exponent, bool):
        raise TypeError("exponent must be an integer")
    if not isinstance(modulus, int) or isinstance(modulus, bool):
        raise TypeError("modulus must be an integer")
    if exponent < 0:
        raise ValueError("exponent must be non-negative")
    if modulus < 1:
        raise ValueError("modulus must be at least 1")


def naive_modular_exponentiation(base: int, exponent: int, modulus: int) -> int:
    """Calculate base**exponent % modulus using repeated multiplication."""
    _validate_power_inputs(base, exponent, modulus)
    result = 1 % modulus
    base %= modulus
    for _ in range(exponent):
        result = (result * base) % modulus
    return result


def binary_modular_exponentiation(base: int, exponent: int, modulus: int) -> int:
    """Calculate base**exponent % modulus using square-and-multiply."""
    _validate_power_inputs(base, exponent, modulus)
    result = 1 % modulus
    base %= modulus
    while exponent:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result


def compare_examples() -> None:
    cases = [
        (2, 10, 1000),
        (7, 100, 13),
        (-3, 17, 11),
        (123456, 0, 97),
        (10, 50, 1),
    ]
    print("base | exponent | modulus | naive | binary | match")
    print("-" * 58)
    for base, exponent, modulus in cases:
        naive = naive_modular_exponentiation(base, exponent, modulus)
        binary = binary_modular_exponentiation(base, exponent, modulus)
        print(
            f"{base:>4} | {exponent:>8} | {modulus:>7} | "
            f"{naive:>5} | {binary:>6} | {naive == binary}"
        )
        if naive != binary:
            raise AssertionError("modular exponentiation implementations disagree")


def benchmark() -> None:
    base, modulus = 7, 1_000_000_007
    exponents = [10**power for power in range(1, 7)]
    print("\nModular exponentiation benchmark")
    print("exponent | naive (s) | binary (s) | result match")
    print("-" * 51)
    for exponent in exponents:
        start = time.perf_counter()
        naive_result = naive_modular_exponentiation(base, exponent, modulus)
        naive_time = time.perf_counter() - start

        start = time.perf_counter()
        binary_result = binary_modular_exponentiation(base, exponent, modulus)
        binary_time = time.perf_counter() - start

        print(
            f"{exponent:>8} | {naive_time:>9.6f} | {binary_time:>10.6f} | "
            f"{naive_result == binary_result}"
        )
        if naive_result != binary_result:
            raise AssertionError(f"results disagree for exponent {exponent}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="also run the repeated-multiplication benchmark up to exponent 10^6",
    )
    args = parser.parse_args()

    compare_examples()
    if args.benchmark:
        benchmark()


if __name__ == "__main__":
    main()
