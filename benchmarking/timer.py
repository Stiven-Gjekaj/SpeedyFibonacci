"""
High-precision timing utilities for benchmarking.

This module provides a precision timer that can run a function
for a specified duration and track performance metrics.

Author: SpeedyFibonacci Contributors
License: MIT
"""

import time
from dataclasses import dataclass
from typing import Callable, Any, Optional


@dataclass
class TimingResult:
    """
    Results from a timed execution.

    Attributes:
        count: Number of successful calculations completed
        max_n: Maximum value of n reached
        actual_duration: Actual time elapsed in seconds
        error: Optional error message if execution was interrupted
    """
    count: int
    max_n: int
    actual_duration: float
    error: Optional[str] = None


class PrecisionTimer:
    """
    High-precision timer for benchmarking Fibonacci techniques.

    Uses time.perf_counter() for maximum precision timing.
    Runs a calculation function repeatedly for a specified duration.

    Example:
        timer = PrecisionTimer(duration=1.0)
        result = timer.run_for_duration(technique.calculate)
        print(f"Calculated {result.count} numbers, max n={result.max_n}")
    """

    def __init__(self, duration: float = 1.0):
        """
        Initialize the timer.

        Args:
            duration: Target duration in seconds (default: 1.0)
        """
        self.duration = duration

    def run_for_duration(
        self,
        func: Callable[[int], Any],
        start_n: int = 0,
        validate_func: Optional[Callable[[int, Any], bool]] = None
    ) -> TimingResult:
        """
        Run a function repeatedly for the specified duration.

        Calls func(n) with incrementing n values until the duration
        is reached or an error occurs.

        Args:
            func: Function that takes an integer n and returns F(n)
            start_n: Starting value for n (default: 0)
            validate_func: Optional validation function(n, result) -> bool

        Returns:
            TimingResult with count, max_n, duration, and any error
        """
        start_time = time.perf_counter()
        n = start_n
        count = 0
        error_msg = None

        try:
            while (time.perf_counter() - start_time) < self.duration:
                result = func(n)

                # Optional validation
                if validate_func is not None:
                    if not validate_func(n, result):
                        error_msg = f"Validation failed at n={n}"
                        break

                count += 1
                n += 1

        except RecursionError:
            error_msg = f"RecursionError at n={n}"
        except MemoryError:
            error_msg = f"MemoryError at n={n}"
        except OverflowError:
            error_msg = f"OverflowError at n={n}"
        except Exception as e:
            error_msg = f"{type(e).__name__} at n={n}: {str(e)}"

        actual_duration = time.perf_counter() - start_time
        max_n = n - 1 if count > 0 else 0

        return TimingResult(
            count=count,
            max_n=max_n,
            actual_duration=actual_duration,
            error=error_msg
        )

    def time_single_call(self, func: Callable[[], Any]) -> tuple[Any, float]:
        """
        Time a single function call.

        Args:
            func: Function to time (no arguments)

        Returns:
            Tuple of (result, elapsed_time_in_seconds)
        """
        start = time.perf_counter()
        result = func()
        elapsed = time.perf_counter() - start
        return result, elapsed
