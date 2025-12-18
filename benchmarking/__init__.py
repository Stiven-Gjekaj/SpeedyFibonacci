"""
SpeedyFibonacci - Benchmarking infrastructure.

This package contains the benchmarking framework for measuring
Fibonacci calculation performance across different techniques.
"""

from .benchmark_runner import BenchmarkRunner, BenchmarkResult
from .technique_loader import load_all_techniques
from .timer import PrecisionTimer
from .validators import validate_result, validate_technique

__all__ = [
    "BenchmarkRunner",
    "BenchmarkResult",
    "load_all_techniques",
    "PrecisionTimer",
    "validate_result",
    "validate_technique",
]
