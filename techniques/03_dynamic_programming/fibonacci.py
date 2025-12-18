"""
Dynamic Programming (Bottom-Up) Fibonacci Implementation.

This technique builds the Fibonacci sequence iteratively from the base cases,
storing all intermediate results in an array. Classic bottom-up DP approach.

Time Complexity: O(n)
Space Complexity: O(n) - stores all values from F(0) to F(n)

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - Cormen, T.H., et al. (2009). Introduction to Algorithms (3rd ed.).
      MIT Press. Chapter 15: Dynamic Programming.
    - Bellman, R. (1957). Dynamic Programming. Princeton University Press.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique


class DynamicProgramming(FibonacciTechnique):
    """
    Bottom-up dynamic programming Fibonacci implementation.

    Builds a table of Fibonacci values from F(0) to F(n), then returns F(n).
    This is the "bottom-up" or "tabulation" approach to dynamic programming,
    contrasted with the "top-down" memoization approach.

    Advantages over memoization:
    - No recursion overhead
    - No stack overflow risk
    - Predictable memory usage
    - Generally faster due to better cache locality
    """

    @property
    def name(self) -> str:
        return "Dynamic Programming"

    @property
    def description(self) -> str:
        return "Bottom-up iterative with array (tabulation)"

    @property
    def time_complexity(self) -> str:
        return "O(n)"

    @property
    def space_complexity(self) -> str:
        return "O(n)"

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using bottom-up dynamic programming.

        Builds array [F(0), F(1), ..., F(n)] iteratively.

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n <= 1:
            return n

        # Initialize table with base cases
        dp = [0] * (n + 1)
        dp[0] = 0
        dp[1] = 1

        # Fill table bottom-up
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]

    def supports_large_n(self) -> bool:
        return True
