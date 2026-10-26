"""Square matrix modular exponentiation, Fibonacci, graph walks, and benchmarks."""

import argparse
import random
import time
from collections.abc import Sequence

Matrix = Sequence[Sequence[int]]


def _validate_modulus(modulus: int) -> None:
    if not isinstance(modulus, int) or isinstance(modulus, bool):
        raise TypeError("modulus must be an integer")
    if modulus < 1:
        raise ValueError("modulus must be at least 1")


def _validate_exponent(exponent: int) -> None:
    if not isinstance(exponent, int) or isinstance(exponent, bool):
        raise TypeError("exponent must be an integer")
    if exponent < 0:
        raise ValueError("exponent must be non-negative")


def _validate_dimension(dimension: int) -> None:
    if not isinstance(dimension, int) or isinstance(dimension, bool):
        raise TypeError("dimension must be an integer")
    if dimension < 1:
        raise ValueError("dimension must be positive")


def _validate_square_matrix(matrix: Matrix, name: str) -> int:
    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        raise ValueError(f"{name} must be a non-empty square matrix")
    if any(
        not isinstance(value, int) or isinstance(value, bool)
        for row in matrix
        for value in row
    ):
        raise TypeError(f"{name} entries must be integers")
    return size


def multiply_matrices_mod(left: Matrix, right: Matrix, modulus: int) -> list[list[int]]:
    """Multiply two equally sized square matrices modulo modulus."""
    _validate_modulus(modulus)
    size = _validate_square_matrix(left, "left")
    if _validate_square_matrix(right, "right") != size:
        raise ValueError("matrices must have the same dimensions")

    result = [[0] * size for _ in range(size)]
    for row in range(size):
        for column in range(size):
            total = 0
            for inner in range(size):
                total = (
                    total
                    + (left[row][inner] % modulus)
                    * (right[inner][column] % modulus)
                ) % modulus
            result[row][column] = total
    return result


def identity_matrix(dimension: int) -> list[list[int]]:
    """Generate the identity matrix of the requested positive dimension."""
    _validate_dimension(dimension)
    return [
        [1 if row == column else 0 for column in range(dimension)]
        for row in range(dimension)
    ]


def naive_matrix_exponentiation(
    matrix: Matrix, exponent: int, modulus: int
) -> list[list[int]]:
    """Calculate matrix**exponent modulo modulus using repeated multiplication."""
    _validate_modulus(modulus)
    _validate_exponent(exponent)
    size = _validate_square_matrix(matrix, "matrix")
    result = [
        [value % modulus for value in row] for row in identity_matrix(size)
    ]
    base = [[value % modulus for value in row] for row in matrix]
    for _ in range(exponent):
        result = multiply_matrices_mod(result, base, modulus)
    return result


def binary_matrix_exponentiation(
    matrix: Matrix, exponent: int, modulus: int
) -> list[list[int]]:
    """Calculate matrix**exponent modulo modulus using repeated squaring."""
    _validate_modulus(modulus)
    _validate_exponent(exponent)
    size = _validate_square_matrix(matrix, "matrix")
    result = [
        [value % modulus for value in row] for row in identity_matrix(size)
    ]
    base = [[value % modulus for value in row] for row in matrix]
    while exponent:
        if exponent & 1:
            result = multiply_matrices_mod(result, base, modulus)
        base = multiply_matrices_mod(base, base, modulus)
        exponent >>= 1
    return result


def fibonacci_mod(index: int, modulus: int) -> int:
    """Return F(index) modulo modulus using the Fibonacci Q-matrix."""
    _validate_exponent(index)
    _validate_modulus(modulus)
    q_matrix = [[1, 1], [1, 0]]
    return binary_matrix_exponentiation(q_matrix, index, modulus)[0][1]


def count_directed_walks(
    adjacency: Matrix, source: int, destination: int, edge_count: int, modulus: int
) -> int:
    """Count source-to-destination directed walks of exactly edge_count edges."""
    _validate_modulus(modulus)
    _validate_exponent(edge_count)
    size = _validate_square_matrix(adjacency, "adjacency")
    for label, vertex in (("source", source), ("destination", destination)):
        if not isinstance(vertex, int) or isinstance(vertex, bool):
            raise TypeError(f"{label} must be an integer vertex index")
        if not 0 <= vertex < size:
            raise ValueError(f"{label} must be between 0 and {size - 1}")
    powered = binary_matrix_exponentiation(adjacency, edge_count, modulus)
    return powered[source][destination]


def compare_examples() -> None:
    examples = [
        ([[1, 1], [1, 0]], 10, 1000),
        ([[1, 2], [3, 4]], 5, 13),
        ([[0, 1], [1, 1]], 0, 7),
    ]
    print("Matrix exponentiation comparisons")
    for matrix, exponent, modulus in examples:
        naive = naive_matrix_exponentiation(matrix, exponent, modulus)
        binary = binary_matrix_exponentiation(matrix, exponent, modulus)
        print(
            f"A={matrix}, n={exponent}, m={modulus}: "
            f"match={naive == binary}, result={binary}"
        )
        if naive != binary:
            raise AssertionError("matrix exponentiation implementations disagree")

    print(f"\nF(10^18) mod (10^9 + 7) = {fibonacci_mod(10**18, 10**9 + 7)}")

    graph = [
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
    ]
    walks = count_directed_walks(graph, 0, 3, 2, 1_000_000_007)
    print(f"Walks from vertex 0 to 3 using exactly 2 edges: {walks}")


def benchmark() -> None:
    dimensions = [2, 4, 8, 16, 32]
    exponents = [2**power for power in range(4, 13)]
    modulus = 1_000_000_007
    generator = random.Random(302)

    print("\nMatrix exponentiation benchmark (times in seconds)")
    print("dimension | exponent | naive (s) | binary (s) | match")
    print("-" * 66)
    for dimension in dimensions:
        matrix = [
            [generator.randrange(10) for _ in range(dimension)]
            for _ in range(dimension)
        ]
        for exponent in exponents:
            start = time.perf_counter()
            naive_result = naive_matrix_exponentiation(matrix, exponent, modulus)
            naive_time = time.perf_counter() - start

            start = time.perf_counter()
            binary_result = binary_matrix_exponentiation(matrix, exponent, modulus)
            binary_time = time.perf_counter() - start

            matches = naive_result == binary_result
            print(
                f"{dimension:>9} | {exponent:>8} | {naive_time:>9.6f} | "
                f"{binary_time:>10.6f} | {matches}"
            )
            if not matches:
                raise AssertionError(
                    f"results disagree for dimension={dimension}, exponent={exponent}"
                )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="run all 45 dimension/exponent benchmark combinations",
    )
    args = parser.parse_args()

    compare_examples()
    if args.benchmark:
        benchmark()


if __name__ == "__main__":
    main()
