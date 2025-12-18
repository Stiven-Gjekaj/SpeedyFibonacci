"""
Main benchmark orchestrator for Fibonacci techniques.

This module provides the BenchmarkRunner class that coordinates running
all Fibonacci techniques for a specified duration and collecting results.

Author: SpeedyFibonacci Contributors
License: MIT
"""

import sys
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.base_technique import FibonacciTechnique
from utils.constants import DEFAULT_DURATION
from benchmarking.technique_loader import load_all_techniques
from benchmarking.timer import PrecisionTimer
from benchmarking.validators import validate_result


@dataclass
class BenchmarkResult:
    """
    Result from benchmarking a single technique.

    Attributes:
        technique_name: Name of the technique
        description: Brief description of the technique
        count: Number of Fibonacci numbers calculated
        max_n: Maximum value of n reached
        duration: Actual benchmark duration in seconds
        time_complexity: Big-O time complexity
        space_complexity: Big-O space complexity
        error: Error message if benchmark failed
        timestamp: When the benchmark was run
    """
    technique_name: str
    description: str
    count: int
    max_n: int
    duration: float
    time_complexity: str
    space_complexity: str
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def success(self) -> bool:
        """Whether the benchmark completed without errors."""
        return self.error is None

    @property
    def rate(self) -> float:
        """Calculations per second."""
        return self.count / self.duration if self.duration > 0 else 0.0


@dataclass
class BenchmarkSummary:
    """
    Summary of all benchmark results.

    Attributes:
        results: List of individual benchmark results
        total_duration: Total time to run all benchmarks
        timestamp: When benchmarks were started
    """
    results: list[BenchmarkResult]
    total_duration: float
    timestamp: datetime = field(default_factory=datetime.now)

    def get_sorted_by_count(self, descending: bool = True) -> list[BenchmarkResult]:
        """Get results sorted by count (numbers calculated)."""
        return sorted(self.results, key=lambda r: r.count, reverse=descending)

    def get_sorted_by_max_n(self, descending: bool = True) -> list[BenchmarkResult]:
        """Get results sorted by maximum n reached."""
        return sorted(self.results, key=lambda r: r.max_n, reverse=descending)

    def get_fastest(self) -> Optional[BenchmarkResult]:
        """Get the technique that calculated the most numbers."""
        if not self.results:
            return None
        return max(self.results, key=lambda r: r.count)

    def get_highest_n(self) -> Optional[BenchmarkResult]:
        """Get the technique that reached the highest n."""
        if not self.results:
            return None
        return max(self.results, key=lambda r: r.max_n)


class BenchmarkRunner:
    """
    Orchestrates benchmark execution across all Fibonacci techniques.

    Example:
        runner = BenchmarkRunner(duration=1.0)
        summary = runner.run_all()

        for result in summary.get_sorted_by_count():
            print(f"{result.technique_name}: {result.count} numbers")
    """

    def __init__(
        self,
        duration: float = DEFAULT_DURATION,
        validate: bool = True,
        verbose: bool = True
    ):
        """
        Initialize the benchmark runner.

        Args:
            duration: Duration to run each technique (seconds)
            validate: Whether to validate results against known values
            verbose: Whether to print progress messages
        """
        self.duration = duration
        self.validate = validate
        self.verbose = verbose
        self.timer = PrecisionTimer(duration=duration)

    def run_all(
        self,
        techniques: Optional[list[FibonacciTechnique]] = None
    ) -> BenchmarkSummary:
        """
        Run benchmarks for all techniques.

        Args:
            techniques: List of techniques to benchmark (default: load all)

        Returns:
            BenchmarkSummary containing all results
        """
        import time
        start_time = time.perf_counter()

        if techniques is None:
            if self.verbose:
                print("Loading techniques...")
            techniques = load_all_techniques(validate=True)

        if self.verbose:
            print(f"Found {len(techniques)} techniques to benchmark")
            print(f"Running each technique for {self.duration} second(s)...\n")

        results = []
        for i, technique in enumerate(techniques, 1):
            if self.verbose:
                print(f"[{i}/{len(techniques)}] Benchmarking: {technique.name}...", end=" ", flush=True)

            result = self.run_single(technique)
            results.append(result)

            if self.verbose:
                if result.success:
                    print(f"{result.count:,} numbers (max n={result.max_n:,})")
                else:
                    print(f"ERROR: {result.error}")

        total_duration = time.perf_counter() - start_time

        if self.verbose:
            print(f"\nCompleted all benchmarks in {total_duration:.2f} seconds")

        return BenchmarkSummary(
            results=results,
            total_duration=total_duration
        )

    def run_single(self, technique: FibonacciTechnique) -> BenchmarkResult:
        """
        Run benchmark for a single technique.

        Args:
            technique: The technique to benchmark

        Returns:
            BenchmarkResult with timing and count data
        """
        # Setup phase
        try:
            technique.setup()
        except Exception as e:
            return BenchmarkResult(
                technique_name=technique.name,
                description=technique.description,
                count=0,
                max_n=0,
                duration=0.0,
                time_complexity=technique.time_complexity,
                space_complexity=technique.space_complexity,
                error=f"Setup failed: {e}"
            )

        # Validation function if enabled
        validate_func = validate_result if self.validate else None

        # Run the benchmark
        timing_result = self.timer.run_for_duration(
            func=technique.calculate,
            start_n=0,
            validate_func=validate_func
        )

        # Teardown phase
        try:
            technique.teardown()
        except Exception:
            pass  # Ignore teardown errors

        return BenchmarkResult(
            technique_name=technique.name,
            description=technique.description,
            count=timing_result.count,
            max_n=timing_result.max_n,
            duration=timing_result.actual_duration,
            time_complexity=technique.time_complexity,
            space_complexity=technique.space_complexity,
            error=timing_result.error
        )

    def run_technique_by_name(self, name: str) -> Optional[BenchmarkResult]:
        """
        Run benchmark for a specific technique by name.

        Args:
            name: The technique name (case-insensitive)

        Returns:
            BenchmarkResult, or None if technique not found
        """
        from benchmarking.technique_loader import get_technique_by_name

        technique = get_technique_by_name(name)
        if technique is None:
            return None

        return self.run_single(technique)
