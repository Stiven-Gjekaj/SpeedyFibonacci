"""
Memoized Recursive Fibonacci Implementation.

This technique applies memoization (caching) to the naive recursive approach,
eliminating redundant calculations and achieving linear time complexity.

Time Complexity: O(n) - each F(k) computed only once
Space Complexity: O(n) - cache storage + call stack

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - Cormen, T.H., et al. (2009). Introduction to Algorithms (3rd ed.).
      MIT Press. Chapter 15: Dynamic Programming.
    - Michie, D. (1968). "Memo Functions and Machine Learning". Nature.
"""

import sys
import os
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique


class MemoizedRecursion(FibonacciTechnique):
    """
    Memoized recursive Fibonacci using Python's lru_cache.

    Memoization stores the results of expensive function calls and returns
    the cached result when the same inputs occur again. This transforms
    the exponential naive recursion into a linear algorithm.

    The technique demonstrates the "top-down" approach to dynamic programming,
    where we start with the original problem and recursively break it down,
    caching results along the way.
    """

    def __init__(self):
        super().__init__()
        # Create a new cached function for each instance
        self._fib = lru_cache(maxsize=None)(self._fib_impl)

    @property
    def name(self) -> str:
        return "Memoized Recursion"

    @property
    def description(self) -> str:
        return "Recursion with LRU cache (top-down dynamic programming)"

    @property
    def time_complexity(self) -> str:
        return "O(n)"

    @property
    def space_complexity(self) -> str:
        return "O(n)"

    def _fib_impl(self, n: int) -> int:
        """Internal recursive implementation."""
        if n <= 1:
            return n
        return self._fib(n - 1) + self._fib(n - 2)

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using memoized recursion.

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        return self._fib(n)

    def setup(self) -> None:
        """Clear the cache before benchmarking for fair comparison."""
        self._fib.cache_clear()
        # Re-create the cached function
        self._fib = lru_cache(maxsize=None)(self._fib_impl)

    def teardown(self) -> None:
        """Clear the cache after benchmarking."""
        self._fib.cache_clear()

    def supports_large_n(self) -> bool:
        """Can handle moderately large n, limited by recursion depth."""
        return True

    def get_max_recommended_n(self) -> int:
        """Limited by Python's recursion limit."""
        return 900  # Slightly below default recursion limit
