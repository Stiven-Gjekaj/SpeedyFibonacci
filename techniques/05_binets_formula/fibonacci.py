"""
Binet's Formula Fibonacci Implementation.

Uses the closed-form mathematical formula involving the golden ratio
to calculate Fibonacci numbers directly without iteration or recursion.

Time Complexity: O(1) - direct calculation (ignoring precision issues)
Space Complexity: O(1) - constant space

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - Binet, J.P.M. (1843). "Mémoire sur l'intégration des équations
      linéaires aux différences finies". Comptes Rendus.
    - Koshy, T. (2001). "Fibonacci and Lucas Numbers with Applications".
      Wiley-Interscience.
"""

import sys
import os
from decimal import Decimal, getcontext

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.base_technique import FibonacciTechnique


# Set high precision for accurate calculations
getcontext().prec = 1000


class BinetsFormula(FibonacciTechnique):
    """
    Binet's Formula implementation using the golden ratio.

    The formula is:
        F(n) = (φ^n - ψ^n) / √5

    Where:
        φ (phi) = (1 + √5) / 2 ≈ 1.618034 (golden ratio)
        ψ (psi) = (1 - √5) / 2 ≈ -0.618034 (conjugate)

    This gives an O(1) direct calculation, but floating-point precision
    limits accuracy for large n. We use Python's Decimal for better
    precision, but extremely large n may still have errors.

    Named after Jacques Philippe Marie Binet who published it in 1843,
    though it was known earlier to Euler, Daniel Bernoulli, and de Moivre.
    """

    def __init__(self):
        super().__init__()
        # Pre-compute constants with high precision
        self._sqrt5 = Decimal(5).sqrt()
        self._phi = (Decimal(1) + self._sqrt5) / Decimal(2)
        self._psi = (Decimal(1) - self._sqrt5) / Decimal(2)

    @property
    def name(self) -> str:
        return "Binet's Formula"

    @property
    def description(self) -> str:
        return "Closed-form formula using golden ratio φ"

    @property
    def time_complexity(self) -> str:
        return "O(1)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    def calculate(self, n: int) -> int:
        """
        Calculate F(n) using Binet's formula.

        F(n) = (φ^n - ψ^n) / √5

        Args:
            n: The Fibonacci index (0-indexed)

        Returns:
            The nth Fibonacci number
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if n <= 1:
            return n

        # Calculate using high-precision Decimal
        phi_n = self._phi ** n
        psi_n = self._psi ** n

        result = (phi_n - psi_n) / self._sqrt5

        # Round to nearest integer
        return int(result.to_integral_value())

    def supports_large_n(self) -> bool:
        """Limited by floating-point precision."""
        return True

    def get_max_recommended_n(self) -> int:
        """Precision degrades for very large n."""
        return 1000
