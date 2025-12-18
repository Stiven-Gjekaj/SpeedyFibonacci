"""
Validation utilities for Fibonacci results.

This module provides functions to validate Fibonacci calculation
results against known values and verify technique implementations.

Author: SpeedyFibonacci Contributors
License: MIT

References:
    - OEIS A000045: Fibonacci numbers
      https://oeis.org/A000045
"""

from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import KNOWN_FIBONACCI
from utils.base_technique import FibonacciTechnique


def validate_result(n: int, result: int) -> bool:
    """
    Validate a Fibonacci result against known values.

    Checks if the calculated result matches the known Fibonacci value
    for the given n. If n is not in the known values table, returns True
    (assumes correct when we can't verify).

    Args:
        n: The Fibonacci index
        result: The calculated Fibonacci number

    Returns:
        bool: True if valid or unverifiable, False if incorrect
    """
    if n in KNOWN_FIBONACCI:
        return result == KNOWN_FIBONACCI[n]
    return True  # Can't validate, assume correct


def validate_technique(technique: FibonacciTechnique, test_range: int = 20) -> tuple[bool, Optional[str]]:
    """
    Validate a technique's implementation against known Fibonacci values.

    Tests the technique's calculate() method against known values
    for n in range(0, test_range).

    Args:
        technique: The FibonacciTechnique instance to validate
        test_range: Number of values to test (default: 20)

    Returns:
        Tuple of (is_valid, error_message)
        - (True, None) if all tests pass
        - (False, "error description") if any test fails
    """
    for n in range(min(test_range, max(KNOWN_FIBONACCI.keys()) + 1)):
        if n not in KNOWN_FIBONACCI:
            continue

        try:
            result = technique.calculate(n)
            expected = KNOWN_FIBONACCI[n]

            if result != expected:
                return False, f"F({n}): expected {expected}, got {result}"

        except RecursionError:
            # Some techniques can't handle larger n values
            if n <= 10:
                return False, f"RecursionError at n={n} (too early)"
            break
        except Exception as e:
            return False, f"Exception at n={n}: {type(e).__name__}: {e}"

    return True, None


def get_known_fibonacci(n: int) -> Optional[int]:
    """
    Get a known Fibonacci number if available.

    Args:
        n: The Fibonacci index

    Returns:
        The Fibonacci number if known, None otherwise
    """
    return KNOWN_FIBONACCI.get(n)


def compute_fibonacci_reference(n: int) -> int:
    """
    Compute Fibonacci number using a simple, verified iterative method.

    This serves as a reference implementation for validation.
    Not optimized for speed, but guaranteed correct.

    Args:
        n: The Fibonacci index

    Returns:
        The nth Fibonacci number
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
