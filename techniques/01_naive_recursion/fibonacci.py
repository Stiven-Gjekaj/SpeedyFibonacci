"""
Naive Recursive Fibonacci Implementation.

This is the classic textbook recursive implementation of Fibonacci.
While elegant and easy to understand, it has exponential time complexity
due to redundant calculations.

Time Complexity: O(2^n) - exponential
Space Complexity: O(n) - due to call stack depth

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - Cormen, T.H., Leiserson, C.E., Rivest, R.L., & Stein, C. (2009).
      Introduction to Algorithms (3rd ed.). MIT Press. Chapter 15.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique


class NaiveRecursion(FibonacciTechnique):
    """
    Classic recursive Fibonacci implementation.

    Uses the direct mathematical definition:
        F(0) = 0
        F(1) = 1
        F(n) = F(n-1) + F(n-2) for n > 1

    This approach is pedagogically valuable but practically inefficient
    due to exponential time complexity from redundant sub-problem calculations.

    The number of function calls grows as the Fibonacci sequence itself:
        T(n) = T(n-1) + T(n-2) + O(1)

    Which resolves to approximately O(φ^n) where φ ≈ 1.618 (golden ratio).
    """

    @property
    def name(self) -> str:
        return "Naive Recursion"

    @property
    def description(self) -> str:
        return "Classic recursive implementation without optimization"

    @property
    def time_complexity(self) -> str:
        return "O(2^n)"

    @property
    def space_complexity(self) -> str:
        return "O(n)"

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using naive recursion.

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n <= 1:
            return n
        return self.calculate(n - 1) + self.calculate(n - 2)

    def supports_large_n(self) -> bool:
        """Naive recursion cannot handle large n values."""
        return False

    def get_max_recommended_n(self) -> int:
        """Maximum recommended n is around 35 due to exponential time."""
        return 35
