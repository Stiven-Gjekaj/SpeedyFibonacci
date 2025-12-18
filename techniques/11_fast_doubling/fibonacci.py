"""
Fast Doubling Fibonacci Implementation.

An elegant O(log n) algorithm based on these identities:
    F(2n) = F(n) * [2*F(n+1) - F(n)]
    F(2n+1) = F(n)^2 + F(n+1)^2

Time Complexity: O(log n)
Space Complexity: O(log n) - recursion depth

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - Nayuki: "Fast Fibonacci algorithms"
      https://www.nayuki.io/page/fast-fibonacci-algorithms
    - These identities derive from matrix exponentiation properties.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique


class FastDoubling(FibonacciTechnique):
    """
    Fast Doubling algorithm for Fibonacci numbers.

    Uses the identities:
        F(2n)   = F(n) * [2*F(n+1) - F(n)]
        F(2n+1) = F(n)^2 + F(n+1)^2

    This achieves O(log n) time by "doubling" towards the target n,
    similar to binary exponentiation but without matrix multiplication.

    The algorithm processes n bit-by-bit from most significant to least,
    making it very efficient for computing large individual Fibonacci numbers.
    """

    @property
    def name(self) -> str:
        return "Fast Doubling"

    @property
    def description(self) -> str:
        return "O(log n) using F(2n) and F(2n+1) identities"

    @property
    def time_complexity(self) -> str:
        return "O(log n)"

    @property
    def space_complexity(self) -> str:
        return "O(log n)"

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using fast doubling algorithm.

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")

        return self._fast_doubling(n)[0]

    def _fast_doubling(self, n: int) -> tuple[int, int]:
        """
        Internal recursive implementation returning (F(n), F(n+1)).

        Uses the identities:
            F(2n)   = F(n) * [2*F(n+1) - F(n)]
            F(2n+1) = F(n)^2 + F(n+1)^2

        Args:
            n: The Fibonacci index

        Returns:
            Tuple of (F(n), F(n+1))
        """
        if n == 0:
            return (0, 1)

        # Recursively compute F(n//2) and F(n//2 + 1)
        a, b = self._fast_doubling(n // 2)

        # F(2k) = F(k) * [2*F(k+1) - F(k)]
        c = a * (2 * b - a)

        # F(2k+1) = F(k)^2 + F(k+1)^2
        d = a * a + b * b

        if n % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)

    def calculate_iterative(self, n: int) -> int:
        """
        Iterative version of fast doubling (avoids recursion limit).

        Processes bits of n from most significant to least significant.
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            return 0

        # Find the position of the highest bit
        # We'll process bits from high to low
        a, b = 0, 1  # F(0), F(1)

        # Get the bit length of n
        highest_bit = n.bit_length() - 1

        for i in range(highest_bit, -1, -1):
            # Double: compute F(2k) and F(2k+1) from F(k) and F(k+1)
            c = a * (2 * b - a)      # F(2k)
            d = a * a + b * b        # F(2k+1)

            if (n >> i) & 1:
                # Bit is 1: we want F(2k+1), F(2k+2)
                a, b = d, c + d
            else:
                # Bit is 0: we want F(2k), F(2k+1)
                a, b = c, d

        return a

    def supports_large_n(self) -> bool:
        return True
