"""
NumPy Vectorized Fibonacci Implementation.

Uses NumPy's matrix exponentiation for efficient Fibonacci calculation.
Leverages NumPy's C-level optimizations for matrix operations.

Time Complexity: O(log n) - matrix exponentiation
Space Complexity: O(1) - constant matrix size

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - NumPy Documentation: https://numpy.org/doc/stable/
    - Harris, C.R., et al. (2020). "Array programming with NumPy".
      Nature 585, 357-362.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class NumpyVectorized(FibonacciTechnique):
    """
    NumPy-based Fibonacci using matrix exponentiation.

    Uses NumPy's optimized matrix operations to compute Fibonacci numbers
    via the matrix identity [[1,1],[1,0]]^n.

    NumPy advantages:
    - C-level implementation of matrix operations
    - Optimized for numerical computing
    - Supports arbitrary precision with dtype=object
    """

    @property
    def name(self) -> str:
        return "NumPy Vectorized"

    @property
    def description(self) -> str:
        return "NumPy matrix exponentiation with C-level ops"

    @property
    def time_complexity(self) -> str:
        return "O(log n)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using NumPy matrix power.

        Uses np.linalg.matrix_power for efficient matrix exponentiation.

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n <= 1:
            return n

        if not NUMPY_AVAILABLE:
            raise RuntimeError("NumPy is not installed")

        # Use object dtype to support arbitrary precision integers
        F = np.array([[1, 1], [1, 0]], dtype=object)

        # Matrix exponentiation: F^(n-1)
        result = np.linalg.matrix_power(F, n - 1)

        return int(result[0, 0])

    def supports_large_n(self) -> bool:
        return True

    def setup(self) -> None:
        """Verify NumPy is available."""
        if not NUMPY_AVAILABLE:
            raise RuntimeError("NumPy is required for this technique")
