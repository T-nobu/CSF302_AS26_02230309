"""
Lab 1 - Question 3: Naive Prime Checking using Trial Division
Student Number: 02230309
"""


def is_prime_naive_309(n):
    """
    Checks if `n` is prime by testing every integer from 2 to n-1.
    Time Complexity: O(n) per check
    """
    if n < 2:
        return False
    for divisor_309 in range(2, n):
        if n % divisor_309 == 0:
            return False
    return True


def primes_up_to_naive_309(limit_309):
    """Returns a list of all primes <= limit_309 using naive trial division."""
    return [num_309 for num_309 in range(2, limit_309 + 1) if is_prime_naive_309(num_309)]


if __name__ == "__main__":
    print("Primes up to 50:", primes_up_to_naive_309(50))
