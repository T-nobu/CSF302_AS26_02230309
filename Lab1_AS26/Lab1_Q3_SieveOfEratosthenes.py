"""
Lab 1 - Question 3: Sieve of Eratosthenes
Student Number: 02230309
"""


def sieve_of_eratosthenes_309(limit_309):
    """
    Returns a list of all primes <= limit_309 using the Sieve of Eratosthenes.
    Time Complexity: O(n log log n)
    """
    if limit_309 < 2:
        return []

    is_prime_flags_309 = [True] * (limit_309 + 1)
    is_prime_flags_309[0] = is_prime_flags_309[1] = False

    for num_309 in range(2, int(limit_309 ** 0.5) + 1):
        if is_prime_flags_309[num_309]:
            for multiple_309 in range(num_309 * num_309, limit_309 + 1, num_309):
                is_prime_flags_309[multiple_309] = False

    return [i_309 for i_309, flag_309 in enumerate(is_prime_flags_309) if flag_309]


if __name__ == "__main__":
    print("Primes up to 50:", sieve_of_eratosthenes_309(50))
