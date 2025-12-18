"""
Generator-based Fibonacci Implementation.

Uses Python generators for memory-efficient Fibonacci sequence generation.
The generator yields values lazily, storing only the last two values.

Time Complexity: O(n) - must iterate to reach F(n)
Space Complexity: O(1) - only stores two values at any time

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - Python Documentation: Generators
      https://docs.python.org/3/tutorial/classes.html#generators
    - Beazley, D. (2009). "Python Essential Reference" (4th ed.). Chapter 6.
"""

import sys
import os
from typing import Generator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique


def fibonacci_generator() -> Generator[int, None, None]:
    """
    Generate the Fibonacci sequence indefinitely.

    Yields:
        The next Fibonacci number in sequence

    Example:
        gen = fibonacci_generator()
        print(next(gen))  # 0
        print(next(gen))  # 1
        print(next(gen))  # 1
        print(next(gen))  # 2
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


class GeneratorBased(FibonacciTechnique):
    """
    Generator-based Fibonacci implementation.

    Uses Python's generator pattern to produce Fibonacci numbers lazily.
    This is memory-efficient as it only stores two values regardless of n,
    and is Pythonic for sequence iteration.

    While the calculate(n) method must iterate to reach F(n), the generator
    itself is useful for:
    - Streaming Fibonacci numbers
    - Memory-constrained environments
    - Functional programming patterns
    - Taking first N Fibonacci numbers efficiently
    """

    @property
    def name(self) -> str:
        return "Generator-based"

    @property
    def description(self) -> str:
        return "Python generator with lazy evaluation"

    @property
    def time_complexity(self) -> str:
        return "O(n)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) by iterating through the generator.

        Creates a new generator and advances it n+1 times to get F(n).

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")

        gen = fibonacci_generator()

        # Advance generator to position n
        for _ in range(n):
            next(gen)

        return next(gen)

    def get_generator(self) -> Generator[int, None, None]:
        """
        Get a new Fibonacci generator.

        Returns:
            A generator yielding the Fibonacci sequence
        """
        return fibonacci_generator()

    def supports_large_n(self) -> bool:
        return True
