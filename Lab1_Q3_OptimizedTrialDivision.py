"""
Lab 1 - Question 3: Optimized Trial Division (checking up to sqrt(n))
Student Number: 02230309
"""

import math


def is_prime_optimized_309(n):
    """
    Checks if `n` is prime by testing divisors only up to sqrt(n).
    Time Complexity: O(sqrt(n)) per check
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    limit_309 = int(math.isqrt(n))
    for divisor_309 in range(3, limit_309 + 1, 2):
        if n % divisor_309 == 0:
            return False
    return True


def primes_up_to_optimized_309(limit_309):
    """Returns a list of all primes <= limit_309 using optimized trial division."""
    return [num_309 for num_309 in range(2, limit_309 + 1) if is_prime_optimized_309(num_309)]


if __name__ == "__main__":
    print("Primes up to 50:", primes_up_to_optimized_309(50))
