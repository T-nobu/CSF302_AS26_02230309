import unittest

from Lab4_Q1_ModularExponentiation import (
    binary_modular_exponentiation,
    naive_modular_exponentiation,
)
from Lab4_Q2_MatrixExponentiation import (
    binary_matrix_exponentiation,
    count_directed_walks,
    fibonacci_mod,
    identity_matrix,
    multiply_matrices_mod,
    naive_matrix_exponentiation,
)


class ModularExponentiationTests(unittest.TestCase):
    def test_naive_and_binary_match(self):
        for base, exponent, modulus in [
            (2, 10, 1000),
            (-3, 17, 11),
            (123, 0, 97),
            (20, 100, 1),
        ]:
            with self.subTest(base=base, exponent=exponent, modulus=modulus):
                self.assertEqual(
                    naive_modular_exponentiation(base, exponent, modulus),
                    binary_modular_exponentiation(base, exponent, modulus),
                )

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            binary_modular_exponentiation(2, -1, 7)
        with self.assertRaises(ValueError):
            binary_modular_exponentiation(2, 1, 0)


class MatrixExponentiationTests(unittest.TestCase):
    def test_matrix_helpers_and_power_algorithms(self):
        self.assertEqual(identity_matrix(2), [[1, 0], [0, 1]])
        self.assertEqual(
            multiply_matrices_mod([[1, 2], [3, 4]], [[5, 6], [7, 8]], 10),
            [[9, 2], [3, 0]],
        )
        matrix = [[1, 2], [3, 4]]
        for exponent in (0, 1, 5):
            with self.subTest(exponent=exponent):
                self.assertEqual(
                    naive_matrix_exponentiation(matrix, exponent, 13),
                    binary_matrix_exponentiation(matrix, exponent, 13),
                )
        self.assertEqual(
            binary_matrix_exponentiation(matrix, 0, 1),
            [[0, 0], [0, 0]],
        )

    def test_fibonacci_and_graph_walks(self):
        self.assertEqual(fibonacci_mod(0, 7), 0)
        self.assertEqual(fibonacci_mod(10, 1000), 55)
        self.assertEqual(fibonacci_mod(10**18, 10**9 + 7), 209783453)
        adjacency = [[0, 1, 1], [0, 0, 1], [0, 0, 0]]
        self.assertEqual(count_directed_walks(adjacency, 0, 2, 2, 101), 1)
        self.assertEqual(count_directed_walks(adjacency, 0, 0, 0, 101), 1)

    def test_matrix_invalid_inputs(self):
        with self.assertRaises(ValueError):
            binary_matrix_exponentiation([[1, 2]], 2, 7)
        with self.assertRaises(ValueError):
            binary_matrix_exponentiation([[1]], -1, 7)
        with self.assertRaises(ValueError):
            count_directed_walks([[0]], 0, 1, 1, 7)


if __name__ == "__main__":
    unittest.main()
