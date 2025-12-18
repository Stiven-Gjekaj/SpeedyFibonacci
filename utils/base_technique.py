"""
Abstract base class for all Fibonacci calculation techniques.

This module defines the interface that all Fibonacci implementations must follow
to ensure consistent benchmarking and comparison across different algorithms.

Author: SpeedyFibonacci Contributors
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Optional


class FibonacciTechnique(ABC):
    """
    Abstract base class for Fibonacci calculation techniques.

    All Fibonacci implementations must inherit from this class and implement
    the required abstract methods and properties. This ensures a consistent
    interface for benchmarking and comparison.

    Example Usage:
        class MyTechnique(FibonacciTechnique):
            @property
            def name(self) -> str:
                return "My Technique"

            @property
            def description(self) -> str:
                return "Description of the technique"

            @property
            def time_complexity(self) -> str:
                return "O(n)"

            @property
            def space_complexity(self) -> str:
                return "O(1)"

            def calculate(self, n: int) -> int:
                # Implementation here
                pass
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Return the display name of this technique.

        Returns:
            str: Human-readable name (e.g., "Naive Recursion")
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Return a brief description of this technique.

        Returns:
            str: One-line description of the algorithm
        """
        pass

    @property
    @abstractmethod
    def time_complexity(self) -> str:
        """
        Return the Big-O time complexity.

        Returns:
            str: Time complexity notation (e.g., "O(n)", "O(2^n)")
        """
        pass

    @property
    @abstractmethod
    def space_complexity(self) -> str:
        """
        Return the Big-O space complexity.

        Returns:
            str: Space complexity notation (e.g., "O(1)", "O(n)")
        """
        pass

    @abstractmethod
    def calculate(self, n: int) -> int:
        """
        Calculate the nth Fibonacci number.

        The Fibonacci sequence is defined as:
            F(0) = 0
            F(1) = 1
            F(n) = F(n-1) + F(n-2) for n > 1

        Args:
            n: The index in the Fibonacci sequence (0-indexed)

        Returns:
            int: The nth Fibonacci number

        Raises:
            ValueError: If n is negative
        """
        pass

    def setup(self) -> None:
        """
        Optional setup method called before benchmarking.

        Override this method to perform any initialization needed
        before the benchmark runs (e.g., clearing caches, warming up JIT).
        """
        pass

    def teardown(self) -> None:
        """
        Optional teardown method called after benchmarking.

        Override this method to perform any cleanup needed
        after the benchmark completes (e.g., releasing resources).
        """
        pass

    def supports_large_n(self) -> bool:
        """
        Indicate whether this technique can handle large values of n.

        Some techniques (like naive recursion) have exponential time
        complexity and cannot practically compute large Fibonacci numbers.

        Returns:
            bool: True if the technique can handle n > 1000, False otherwise
        """
        return True

    def get_max_recommended_n(self) -> Optional[int]:
        """
        Return the maximum recommended value of n for this technique.

        Returns:
            Optional[int]: Maximum n value, or None if no limit
        """
        return None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __str__(self) -> str:
        return self.name
