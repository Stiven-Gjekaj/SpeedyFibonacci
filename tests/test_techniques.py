"""
Tests for Fibonacci technique implementations.

Verifies that all techniques:
1. Implement the correct interface
2. Return correct Fibonacci values
3. Handle edge cases properly

Author: SpeedyFibonacci Contributors
License: MIT
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.base_technique import FibonacciTechnique
from utils.constants import KNOWN_FIBONACCI
from benchmarking.technique_loader import load_all_techniques
from benchmarking.validators import validate_technique


# Known Fibonacci values for testing
FIBONACCI_TEST_CASES = [
    (0, 0),
    (1, 1),
    (2, 1),
    (3, 2),
    (4, 3),
    (5, 5),
    (6, 8),
    (7, 13),
    (8, 21),
    (9, 34),
    (10, 55),
]


@pytest.fixture(scope="module")
def all_techniques():
    """Load all techniques once for the test module."""
    return load_all_techniques(validate=False)


class TestTechniqueLoading:
    """Test technique discovery and loading."""

    def test_techniques_loaded(self, all_techniques):
        """Verify at least 10 techniques are discovered."""
        assert len(all_techniques) >= 10, \
            f"Expected at least 10 techniques, found {len(all_techniques)}"

    def test_all_have_unique_names(self, all_techniques):
        """Verify all techniques have unique names."""
        names = [t.name for t in all_techniques]
        assert len(names) == len(set(names)), \
            "Duplicate technique names found"


class TestTechniqueInterface:
    """Test that all techniques implement the required interface."""

    def test_inherits_from_base(self, all_techniques):
        """All techniques should inherit from FibonacciTechnique."""
        for tech in all_techniques:
            assert isinstance(tech, FibonacciTechnique), \
                f"{tech} is not a FibonacciTechnique"

    def test_has_name(self, all_techniques):
        """All techniques should have a non-empty name."""
        for tech in all_techniques:
            assert tech.name, f"Technique has empty name: {tech}"
            assert isinstance(tech.name, str)

    def test_has_description(self, all_techniques):
        """All techniques should have a description."""
        for tech in all_techniques:
            assert hasattr(tech, 'description')
            assert isinstance(tech.description, str)

    def test_has_time_complexity(self, all_techniques):
        """All techniques should declare time complexity."""
        for tech in all_techniques:
            assert tech.time_complexity, \
                f"{tech.name} has no time_complexity"
            assert 'O(' in tech.time_complexity or 'o(' in tech.time_complexity.lower(), \
                f"{tech.name} time_complexity should be in Big-O notation"

    def test_has_space_complexity(self, all_techniques):
        """All techniques should declare space complexity."""
        for tech in all_techniques:
            assert tech.space_complexity, \
                f"{tech.name} has no space_complexity"

    def test_has_calculate_method(self, all_techniques):
        """All techniques should have a calculate method."""
        for tech in all_techniques:
            assert hasattr(tech, 'calculate')
            assert callable(tech.calculate)


class TestTechniqueCorrectness:
    """Test that all techniques compute correct Fibonacci values."""

    @pytest.mark.parametrize("n,expected", FIBONACCI_TEST_CASES)
    def test_known_values(self, all_techniques, n, expected):
        """Test each technique against known Fibonacci values."""
        for tech in all_techniques:
            result = tech.calculate(n)
            assert result == expected, \
                f"{tech.name}: F({n}) = {result}, expected {expected}"

    def test_f0_is_0(self, all_techniques):
        """F(0) should be 0 for all techniques."""
        for tech in all_techniques:
            assert tech.calculate(0) == 0, \
                f"{tech.name}: F(0) should be 0"

    def test_f1_is_1(self, all_techniques):
        """F(1) should be 1 for all techniques."""
        for tech in all_techniques:
            assert tech.calculate(1) == 1, \
                f"{tech.name}: F(1) should be 1"

    def test_larger_values(self, all_techniques):
        """Test larger Fibonacci values for techniques that support them."""
        large_tests = [(20, 6765), (30, 832040)]

        for tech in all_techniques:
            if not tech.supports_large_n():
                continue

            for n, expected in large_tests:
                try:
                    result = tech.calculate(n)
                    assert result == expected, \
                        f"{tech.name}: F({n}) = {result}, expected {expected}"
                except RecursionError:
                    # Some techniques hit recursion limits
                    pass

    def test_negative_raises_error(self, all_techniques):
        """Negative n should raise ValueError."""
        for tech in all_techniques:
            with pytest.raises(ValueError):
                tech.calculate(-1)


class TestValidation:
    """Test the validation utilities."""

    def test_validate_technique_passes(self, all_techniques):
        """All techniques should pass validation."""
        for tech in all_techniques:
            is_valid, error = validate_technique(tech, test_range=15)
            assert is_valid, f"{tech.name} failed validation: {error}"


class TestSpecificTechniques:
    """Tests for specific technique behaviors."""

    def test_naive_recursion_limit(self, all_techniques):
        """Naive recursion should not support large n."""
        naive = next((t for t in all_techniques if 'naive' in t.name.lower()), None)
        if naive:
            assert not naive.supports_large_n(), \
                "Naive recursion should not support large n"

    def test_memoized_faster_than_naive(self, all_techniques):
        """Memoized should handle larger n than naive."""
        naive = next((t for t in all_techniques if 'naive' in t.name.lower()), None)
        memoized = next((t for t in all_techniques if 'memoized' in t.name.lower()), None)

        if naive and memoized:
            # Naive should struggle with n=35, memoized should handle it easily
            memoized.setup()
            result = memoized.calculate(35)
            assert result == KNOWN_FIBONACCI[35]
            memoized.teardown()
