"""
Dynamic technique discovery and loading.

This module automatically discovers and imports all Fibonacci technique
implementations from the techniques/ directory.

Author: SpeedyFibonacci Contributors
License: MIT
"""

import importlib
import os
import re
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.base_technique import FibonacciTechnique
from utils.constants import TECHNIQUE_PREFIX_PATTERN


def load_all_techniques(
    techniques_dir: Optional[Path] = None,
    validate: bool = True
) -> list[FibonacciTechnique]:
    """
    Discover and load all Fibonacci techniques from the techniques directory.

    Scans the techniques/ directory for subdirectories matching the pattern
    XX_name (e.g., 01_naive_recursion), imports the fibonacci module from
    each, and returns instantiated technique objects.

    Args:
        techniques_dir: Path to techniques directory (default: auto-detect)
        validate: Whether to validate technique interface (default: True)

    Returns:
        List of FibonacciTechnique instances, sorted by directory name

    Raises:
        FileNotFoundError: If techniques directory doesn't exist
    """
    if techniques_dir is None:
        # Auto-detect techniques directory relative to this file
        techniques_dir = Path(__file__).parent.parent / "techniques"

    if not techniques_dir.exists():
        raise FileNotFoundError(f"Techniques directory not found: {techniques_dir}")

    techniques = []
    pattern = re.compile(TECHNIQUE_PREFIX_PATTERN)

    # Get all numbered directories, sorted
    tech_dirs = sorted([
        d for d in techniques_dir.iterdir()
        if d.is_dir() and pattern.match(d.name)
    ])

    for tech_dir in tech_dirs:
        try:
            technique = load_technique_from_dir(tech_dir, validate=validate)
            if technique is not None:
                techniques.append(technique)
        except Exception as e:
            print(f"Warning: Failed to load technique from {tech_dir.name}: {e}")

    return techniques


def load_technique_from_dir(
    tech_dir: Path,
    validate: bool = True
) -> Optional[FibonacciTechnique]:
    """
    Load a single technique from a directory.

    Imports the fibonacci module from the directory and finds a class
    that inherits from FibonacciTechnique.

    Args:
        tech_dir: Path to the technique directory
        validate: Whether to validate the technique interface

    Returns:
        FibonacciTechnique instance, or None if loading failed
    """
    # Check for fibonacci.py
    fib_module_path = tech_dir / "fibonacci.py"
    if not fib_module_path.exists():
        return None

    # Import the module
    module_name = f"techniques.{tech_dir.name}.fibonacci"

    # Ensure parent package is importable
    techniques_init = tech_dir.parent / "__init__.py"
    if not techniques_init.exists():
        techniques_init.touch()

    tech_init = tech_dir / "__init__.py"
    if not tech_init.exists():
        tech_init.touch()

    try:
        # Add project root to path if not already there
        project_root = tech_dir.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        module = importlib.import_module(module_name)

        # Find the technique class
        technique_class = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and
                issubclass(attr, FibonacciTechnique) and
                attr is not FibonacciTechnique):
                technique_class = attr
                break

        if technique_class is None:
            print(f"Warning: No FibonacciTechnique subclass found in {tech_dir.name}")
            return None

        # Instantiate and optionally validate
        technique = technique_class()

        if validate:
            _validate_technique_interface(technique)

        return technique

    except ImportError as e:
        print(f"Warning: Import error for {tech_dir.name}: {e}")
        return None


def _validate_technique_interface(technique: FibonacciTechnique) -> None:
    """
    Validate that a technique properly implements the interface.

    Args:
        technique: The technique to validate

    Raises:
        TypeError: If required properties/methods are missing or wrong type
    """
    # Check required properties
    if not isinstance(technique.name, str) or not technique.name:
        raise TypeError(f"{technique}: name must be a non-empty string")

    if not isinstance(technique.description, str):
        raise TypeError(f"{technique}: description must be a string")

    if not isinstance(technique.time_complexity, str):
        raise TypeError(f"{technique}: time_complexity must be a string")

    if not isinstance(technique.space_complexity, str):
        raise TypeError(f"{technique}: space_complexity must be a string")

    # Test calculate method with small value
    try:
        result = technique.calculate(0)
        if result != 0:
            raise ValueError(f"{technique}: calculate(0) should return 0, got {result}")

        result = technique.calculate(1)
        if result != 1:
            raise ValueError(f"{technique}: calculate(1) should return 1, got {result}")

    except Exception as e:
        raise TypeError(f"{technique}: calculate() method failed: {e}")


def get_technique_by_name(name: str) -> Optional[FibonacciTechnique]:
    """
    Find and return a technique by its name.

    Args:
        name: The technique name (case-insensitive)

    Returns:
        The technique instance, or None if not found
    """
    techniques = load_all_techniques(validate=False)
    name_lower = name.lower()

    for tech in techniques:
        if tech.name.lower() == name_lower:
            return tech

    return None


def list_available_techniques() -> list[str]:
    """
    List the names of all available techniques.

    Returns:
        List of technique names
    """
    techniques = load_all_techniques(validate=False)
    return [tech.name for tech in techniques]
