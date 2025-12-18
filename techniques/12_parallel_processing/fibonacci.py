"""
Parallel Processing Fibonacci Implementation.

Demonstrates parallel computation using Python's multiprocessing.
While Fibonacci's sequential nature limits parallelization benefits,
this technique shows how to use parallel processing for batch computation.

Time Complexity: O(n) per computation
Space Complexity: O(n) for process pool overhead

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - Python multiprocessing documentation
      https://docs.python.org/3/library/multiprocessing.html
    - Amdahl's Law: Limits of parallelization
"""

import sys
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique


def _fib_single(n: int) -> int:
    """
    Standalone Fibonacci function for use in parallel workers.

    Must be defined at module level for pickling.
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


class ParallelProcessing(FibonacciTechnique):
    """
    Parallel/concurrent Fibonacci computation.

    This technique demonstrates parallel processing concepts, though
    Fibonacci's inherently sequential nature (F(n) depends on F(n-1)
    and F(n-2)) limits the benefits of parallelization.

    The main use case is computing multiple independent Fibonacci
    numbers in parallel, not parallelizing a single computation.

    Educational value:
    - Demonstrates multiprocessing in Python
    - Shows Amdahl's Law limitations
    - Illustrates GIL bypass with processes
    - Batch computation patterns
    """

    def __init__(self, max_workers: Optional[int] = None):
        """
        Initialize with optional worker count.

        Args:
            max_workers: Number of parallel workers (default: CPU count)
        """
        super().__init__()
        self.max_workers = max_workers

    @property
    def name(self) -> str:
        return "Parallel Processing"

    @property
    def description(self) -> str:
        return "Multiprocessing for batch Fibonacci computation"

    @property
    def time_complexity(self) -> str:
        return "O(n)"

    @property
    def space_complexity(self) -> str:
        return "O(n)"

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using single-threaded iteration.

        For a single value, parallel overhead isn't worthwhile.
        This method uses the standard iterative approach.

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")

        return _fib_single(n)

    def calculate_batch_parallel(self, indices: list[int]) -> list[int]:
        """
        Calculate multiple Fibonacci numbers in parallel.

        This is where parallelization shines - computing independent
        Fibonacci numbers simultaneously across multiple CPU cores.

        Args:
            indices: List of Fibonacci indices to compute

        Returns:
            List of Fibonacci numbers in corresponding order
        """
        if not indices:
            return []

        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(_fib_single, indices))

        return results

    def calculate_batch_threaded(self, indices: list[int]) -> list[int]:
        """
        Calculate multiple Fibonacci numbers using threads.

        Note: Due to Python's GIL, threads don't provide true
        parallelism for CPU-bound tasks. This is included for
        educational comparison.

        Args:
            indices: List of Fibonacci indices to compute

        Returns:
            List of Fibonacci numbers in corresponding order
        """
        if not indices:
            return []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            results = list(executor.map(_fib_single, indices))

        return results

    def supports_large_n(self) -> bool:
        return True
