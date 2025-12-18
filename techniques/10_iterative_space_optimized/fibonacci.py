"""
Iterative Space-Optimized Fibonacci Implementation.

The most efficient pure Python iterative approach, using only O(1) space
by tracking just the last two Fibonacci numbers.

Time Complexity: O(n)
Space Complexity: O(1) - only two variables regardless of n

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - This is the standard textbook iterative solution.
    - Sedgewick, R. (2011). Algorithms (4th ed.). Addison-Wesley.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique


class IterativeSpaceOptimized(FibonacciTechnique):
    """
    Space-optimized iterative Fibonacci.

    Uses the observation that to compute F(n), we only need F(n-1) and F(n-2).
    Therefore, we can use just two variables instead of storing the entire
    sequence, achieving O(1) space complexity.

    This is often the best choice for practical applications:
    - Simple to understand and implement
    - No recursion overhead
    - Minimal memory usage
    - Fast for moderate n values

    The elegant Python tuple swap `a, b = b, a + b` makes this
    particularly clean.
    """

    @property
    def name(self) -> str:
        return "Iterative Space-Optimized"

    @property
    def description(self) -> str:
        return "O(1) space iterative using two variables"

    @property
    def time_complexity(self) -> str:
        return "O(n)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using space-optimized iteration.

        Uses only two variables to track the sequence.

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n <= 1:
            return n

        a, b = 0, 1

        for _ in range(2, n + 1):
            a, b = b, a + b

        return b

    def supports_large_n(self) -> bool:
        return True
