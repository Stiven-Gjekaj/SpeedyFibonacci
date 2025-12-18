"""
Cython Optimized Fibonacci Implementation.

This module provides both a pure Python fallback and support for a Cython
compiled version. The Cython implementation (in fibonacci_impl.pyx) must
be compiled before use.

Time Complexity: O(n)
Space Complexity: O(1)

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - Cython Documentation: https://cython.org/
    - Behnel, S., et al. (2011). "Cython: The Best of Both Worlds".
      Computing in Science & Engineering.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique

# Try to import compiled Cython module
try:
    from .fibonacci_impl import fib_cython
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False


def _fib_python(n: int) -> int:
    """Pure Python fallback implementation."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


class CythonOptimized(FibonacciTechnique):
    """
    Cython-compiled iterative Fibonacci.

    Cython is a programming language that makes writing C extensions
    for Python as easy as Python itself. It compiles Python-like code
    to C, which is then compiled to a shared library.

    This implementation uses static typing and C-level operations
    for maximum performance. When compiled:
    - Variables are C types (long long)
    - Loop is compiled to C
    - No Python interpreter overhead

    If Cython module is not compiled, falls back to pure Python.

    To compile the Cython module:
        python scripts/setup_cython.py build_ext --inplace
    """

    @property
    def name(self) -> str:
        return "Cython Optimized"

    @property
    def description(self) -> str:
        status = "compiled" if CYTHON_AVAILABLE else "fallback"
        return f"C-extension via Cython ({status})"

    @property
    def time_complexity(self) -> str:
        return "O(n)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using Cython-compiled code.

        Falls back to pure Python if Cython module not compiled.

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")

        if CYTHON_AVAILABLE:
            # Use compiled Cython for small n (long long limit)
            if n <= 92:
                return fib_cython(n)
            else:
                # Fall back to Python for arbitrary precision
                return _fib_python(n)
        else:
            return _fib_python(n)

    def is_compiled(self) -> bool:
        """Check if Cython module is compiled and available."""
        return CYTHON_AVAILABLE

    def supports_large_n(self) -> bool:
        return True  # Falls back to Python for large n

    def get_max_recommended_n(self) -> int:
        """Cython uses long long, overflow at F(93)."""
        return 92 if CYTHON_AVAILABLE else None
