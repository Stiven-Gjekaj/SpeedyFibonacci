"""
Matrix Exponentiation Fibonacci Implementation.

Uses the matrix identity [[1,1],[1,0]]^n = [[F(n+1),F(n)],[F(n),F(n-1)]]
combined with fast exponentiation (binary exponentiation) to achieve O(log n).

Time Complexity: O(log n) - using fast matrix exponentiation
Space Complexity: O(log n) - recursion depth for exponentiation

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - Gries, D., & Levin, G. (1980). "Computing Fibonacci Numbers (and
      Similarly Defined Functions) in Log Time". IPL 11(2).
    - CLRS Chapter 31.6: Matrix Exponentiation
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique


class MatrixExponentiation(FibonacciTechnique):
    """
    Matrix exponentiation Fibonacci using the identity:

    [[1, 1], [1, 0]]^n = [[F(n+1), F(n)], [F(n), F(n-1)]]

    Combined with binary exponentiation (exponentiation by squaring),
    this achieves O(log n) time complexity.

    This is one of the fastest methods for computing individual large
    Fibonacci numbers and demonstrates an important technique in
    computational mathematics.
    """

    @property
    def name(self) -> str:
        return "Matrix Exponentiation"

    @property
    def description(self) -> str:
        return "O(log n) using [[1,1],[1,0]]^n matrix identity"

    @property
    def time_complexity(self) -> str:
        return "O(log n)"

    @property
    def space_complexity(self) -> str:
        return "O(log n)"

    def _matrix_mult(
        self,
        A: list[list[int]],
        B: list[list[int]]
    ) -> list[list[int]]:
        """
        Multiply two 2x2 matrices.

        Args:
            A: First 2x2 matrix
            B: Second 2x2 matrix

        Returns:
            Product matrix A * B
        """
        return [
            [
                A[0][0] * B[0][0] + A[0][1] * B[1][0],
                A[0][0] * B[0][1] + A[0][1] * B[1][1]
            ],
            [
                A[1][0] * B[0][0] + A[1][1] * B[1][0],
                A[1][0] * B[0][1] + A[1][1] * B[1][1]
            ]
        ]

    def _matrix_pow(self, M: list[list[int]], n: int) -> list[list[int]]:
        """
        Compute M^n using binary exponentiation.

        Uses the property:
        - M^n = (M^(n/2))^2 if n is even
        - M^n = M * M^(n-1) if n is odd

        Args:
            M: 2x2 matrix
            n: Exponent

        Returns:
            M raised to power n
        """
        # Identity matrix
        result = [[1, 0], [0, 1]]

        while n > 0:
            if n % 2 == 1:
                result = self._matrix_mult(result, M)
            M = self._matrix_mult(M, M)
            n //= 2

        return result

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using matrix exponentiation.

        Uses: [[1,1],[1,0]]^n = [[F(n+1),F(n)],[F(n),F(n-1)]]

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n <= 1:
            return n

        # The Fibonacci matrix
        F = [[1, 1], [1, 0]]

        # Compute F^(n-1) to get F(n) at position [0][0]
        result = self._matrix_pow(F, n - 1)

        return result[0][0]

    def supports_large_n(self) -> bool:
        return True
