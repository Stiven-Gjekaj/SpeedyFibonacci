"""
Numba JIT-compiled Fibonacci Implementation.

Uses Numba's Just-In-Time compilation to generate optimized machine code
from Python. This can achieve near-C performance for numerical operations.

Time Complexity: O(n)
Space Complexity: O(1)

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - Lam, S.K., Pitrou, A., & Seibert, S. (2015). "Numba: A LLVM-based
      Python JIT Compiler". LLVM-HPC2015.
    - Numba Documentation: https://numba.pydata.org/
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique

try:
    from numba import jit
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False


if NUMBA_AVAILABLE:
    @jit(nopython=True, cache=True)
    def _fib_numba(n: int) -> int:
        """
        JIT-compiled Fibonacci function.

        This function is compiled to machine code by Numba on first call.
        Subsequent calls use the cached compiled version.

        Note: Returns int64, so limited to F(92) max due to overflow.
        """
        if n <= 1:
            return n

        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b

        return b
else:
    def _fib_numba(n: int) -> int:
        """Fallback pure Python implementation when Numba unavailable."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


class NumbaJIT(FibonacciTechnique):
    """
    Numba JIT-compiled iterative Fibonacci.

    Numba compiles Python code to optimized machine code using LLVM.
    This achieves near-C performance while writing pure Python.

    Key features:
    - First call triggers compilation (small overhead)
    - Subsequent calls run compiled code directly
    - nopython=True forces pure compilation (no Python fallback)
    - cache=True saves compiled code to disk

    Limitations:
    - Uses fixed-size integers (int64), overflow at F(93)
    - Numba doesn't support Python's arbitrary precision integers
    - First call has compilation overhead
    """

    def __init__(self):
        super().__init__()
        self._warmed_up = False

    @property
    def name(self) -> str:
        return "Numba JIT"

    @property
    def description(self) -> str:
        return "LLVM JIT-compiled iterative (near-C speed)"

    @property
    def time_complexity(self) -> str:
        return "O(n)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using JIT-compiled code.

        Args:
            n: The Fibonacci index (0-indexed, max 92 for int64)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")

        # Numba uses int64, max F(92) before overflow
        if n > 92:
            # Fallback to Python for large n
            return self._python_fallback(n)

        return _fib_numba(n)

    def _python_fallback(self, n: int) -> int:
        """Pure Python fallback for n > 92."""
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

    def setup(self) -> None:
        """Warm up JIT compilation before benchmarking."""
        if NUMBA_AVAILABLE and not self._warmed_up:
            # Trigger compilation
            _fib_numba(10)
            self._warmed_up = True

    def supports_large_n(self) -> bool:
        """Limited by int64 overflow in JIT code."""
        return True  # Falls back to Python for large n

    def get_max_recommended_n(self) -> int:
        """int64 overflows at F(93)."""
        return 92
