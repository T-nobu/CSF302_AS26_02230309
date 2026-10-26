"""
karatsuba.py
Q2: Karatsuba's Algorithm for Large Integer Multiplication

Integers are represented as digit lists (most-significant digit first),
NOT as native Python big integers -- all arithmetic (add, subtract,
multiply) is done manually on the digit arrays so the implementation
works the same way regardless of how large the numbers get.

Implements:
    - multiply_digit_lists(x, y): grade-school O(n^2) multiplication
    - karatsuba_multiply(x_str, y_str): O(n^log2(3)) ~= O(n^1.585)
      divide-and-conquer multiplication (3 recursive multiplications
      per split instead of 4)

Operands are padded to equal length and to the next power of 2 before
the recursive split, as required. The script verifies Karatsuba matches
the traditional method for digit lengths 8, 16, ..., 1024, times both,
and plots a runtime comparison graph (karatsuba_perf.png).
"""

import random
import time
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Digit-list <-> string helpers
# ---------------------------------------------------------------------------
def to_digit_list(number_str):
    """MSD-first digit list, e.g. '4021' -> [4, 0, 2, 1]."""
    return [int(ch) for ch in number_str]


def digits_to_str(digits):
    s = "".join(map(str, digits)).lstrip("0")
    return s if s else "0"


def pad_to_length(digits, length):
    return [0] * (length - len(digits)) + digits if length > len(digits) else digits


def next_power_of_2(n):
    p = 1
    while p < n:
        p *= 2
    return p


def strip_leading_zeros(digits):
    i = 0
    while i < len(digits) - 1 and digits[i] == 0:
        i += 1
    return digits[i:]


# ---------------------------------------------------------------------------
# Manual digit-array arithmetic (no native big-int multiplication used)
# ---------------------------------------------------------------------------
def add_digit_lists(x, y):
    n = max(len(x), len(y))
    x = pad_to_length(x, n)
    y = pad_to_length(y, n)
    result = [0] * (n + 1)
    carry = 0
    for i in range(n - 1, -1, -1):
        s = x[i] + y[i] + carry
        result[i + 1] = s % 10
        carry = s // 10
    result[0] = carry
    return strip_leading_zeros(result)


def sub_digit_lists(x, y):
    """Returns x - y. Assumes x >= y (true for every call Karatsuba makes)."""
    n = max(len(x), len(y))
    x = pad_to_length(x, n)
    y = pad_to_length(y, n)
    result = [0] * n
    borrow = 0
    for i in range(n - 1, -1, -1):
        diff = x[i] - y[i] - borrow
        if diff < 0:
            diff += 10
            borrow = 1
        else:
            borrow = 0
        result[i] = diff
    return strip_leading_zeros(result)


def shift_digits(digits, k):
    """Multiply by 10^k, i.e. append k zeros (unless the value is 0)."""
    if digits == [0]:
        return [0]
    return digits + [0] * k


def multiply_digit_lists(x, y):
    """
    Traditional grade-school multiplication, O(n^2), done manually via
    a MSD-first double loop with carry propagation (no native big-int
    multiplication is used).
    """
    x_rev = x[::-1]
    y_rev = y[::-1]
    result = [0] * (len(x) + len(y))
    for i in range(len(x_rev)):
        carry = 0
        for j in range(len(y_rev)):
            prod = x_rev[i] * y_rev[j] + result[i + j] + carry
            result[i + j] = prod % 10
            carry = prod // 10
        result[i + len(y_rev)] += carry
    result.reverse()
    return strip_leading_zeros(result)


# ---------------------------------------------------------------------------
# Karatsuba's algorithm -- 3 multiplications instead of 4 per split
# ---------------------------------------------------------------------------
def karatsuba(x, y):
    """x and y must be MSD-first digit lists of the SAME length."""
    n = len(x)

    if n == 1:
        return multiply_digit_lists(x, y)

    low_len = n // 2
    high_len = n - low_len

    x_high, x_low = x[:high_len], x[high_len:]
    y_high, y_low = y[:high_len], y[high_len:]

    # Only 3 recursive multiplications (z2, z0, and the "middle" product)
    # instead of the 4 a naive divide-and-conquer would need.
    z2 = karatsuba(x_high, y_high)                     # high * high
    z0 = karatsuba(x_low, y_low)                        # low * low

    sum_x = add_digit_lists(x_high, x_low)
    sum_y = add_digit_lists(y_high, y_low)
    common_len = max(len(sum_x), len(sum_y))
    sum_x = pad_to_length(sum_x, common_len)
    sum_y = pad_to_length(sum_y, common_len)
    z1_full = karatsuba(sum_x, sum_y)                    # (xh+xl)*(yh+yl)

    # z1 = (xh+xl)(yh+yl) - z2 - z0 = xh*yl + xl*yh
    z1 = sub_digit_lists(sub_digit_lists(z1_full, z2), z0)

    result = add_digit_lists(
        add_digit_lists(shift_digits(z2, 2 * low_len), shift_digits(z1, low_len)),
        z0,
    )
    return strip_leading_zeros(result)


def karatsuba_multiply(x_str, y_str):
    x = to_digit_list(x_str)
    y = to_digit_list(y_str)
    n = next_power_of_2(max(len(x), len(y)))
    x = pad_to_length(x, n)
    y = pad_to_length(y, n)
    return karatsuba(x, y)


def traditional_multiply(x_str, y_str):
    return multiply_digit_lists(to_digit_list(x_str), to_digit_list(y_str))


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------
def random_number_string(n_digits):
    first = str(random.randint(1, 9))
    rest = "".join(str(random.randint(0, 9)) for _ in range(n_digits - 1))
    return first + rest


# ---------------------------------------------------------------------------
# Correctness check + timing experiment
# ---------------------------------------------------------------------------
def run_experiment(digit_lengths):
    traditional_times = []
    karatsuba_times = []

    print(f"{'digits':>7} | {'traditional (s)':>16} | {'karatsuba (s)':>14} | match")
    print("-" * 58)

    for n in digit_lengths:
        x_str = random_number_string(n)
        y_str = random_number_string(n)

        start = time.perf_counter()
        trad_result = traditional_multiply(x_str, y_str)
        trad_time = time.perf_counter() - start

        start = time.perf_counter()
        kara_result = karatsuba_multiply(x_str, y_str)
        kara_time = time.perf_counter() - start

        match = digits_to_str(trad_result) == digits_to_str(kara_result)
        # Extra sanity check against Python's native int multiplication
        # (used only to VERIFY correctness, not as part of either algorithm).
        match = match and (digits_to_str(trad_result) == str(int(x_str) * int(y_str)))

        print(f"{n:>7} | {trad_time:>16.6f} | {kara_time:>14.6f} | {match}")

        if not match:
            raise AssertionError(f"Mismatch between algorithms at {n} digits")

        traditional_times.append(trad_time)
        karatsuba_times.append(kara_time)

    return traditional_times, karatsuba_times


def plot_results(digit_lengths, traditional_times, karatsuba_times):
    plt.figure(figsize=(8, 5))
    plt.plot(digit_lengths, traditional_times, marker="o", label="Traditional O(n^2)")
    plt.plot(digit_lengths, karatsuba_times, marker="o", label="Karatsuba O(n^1.585)")
    plt.xlabel("Number of digits (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Large Integer Multiplication: Traditional vs Karatsuba")
    plt.xscale("log", base=2)
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("karatsuba_perf.png")
    print("\nSaved plot to karatsuba_perf.png")


if __name__ == "__main__":
    # Demonstrate correctness on a small readable example first.
    demo_x, demo_y = "4021", "3059"
    print(f"x = {demo_x}, y = {demo_y}")
    print("Traditional:", digits_to_str(traditional_multiply(demo_x, demo_y)))
    print("Karatsuba:  ", digits_to_str(karatsuba_multiply(demo_x, demo_y)))
    print("Python check:", int(demo_x) * int(demo_y))
    print()

    # Full experiment across increasing digit lengths, up to 1024 digits.
    digit_lengths = [8, 16, 32, 64, 128, 256, 512, 1024]
    traditional_times, karatsuba_times = run_experiment(digit_lengths)
    plot_results(digit_lengths, traditional_times, karatsuba_times)

    # -----------------------------------------------------------------
    # Conclusion:
    # The traditional grade-school method performs n^2 single-digit
    # multiplications for two n-digit numbers, giving O(n^2). Karatsuba's
    # algorithm reduces the multiplication count per split from the
    # naive 4 (xh*yh, xh*yl, xl*yh, xl*yl) to 3, by computing the two
    # "cross" products together as a single product
    # (xh+xl)(yh+yl) - xh*yh - xl*yl. This gives the recurrence
    # T(n) = 3*T(n/2) + O(n), which solves to T(n) = O(n^log2(3))
    # = O(n^1.585).
    #
    # As with Strassen's algorithm, Karatsuba's recursive overhead
    # (extra additions/subtractions and list slicing at every level)
    # tends to make it slower than the simple O(n^2) method for small
    # digit lengths, but the saved plot (karatsuba_perf.png) should
    # show the traditional curve growing faster (worse) than
    # Karatsuba's as the digit length increases toward 1024,
    # illustrating the n^2 vs n^1.585 gap predicted by the theory.
    # -----------------------------------------------------------------
