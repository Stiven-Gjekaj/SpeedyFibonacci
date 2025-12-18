#!/usr/bin/env python3
"""
Cython Compilation Setup Script

Compiles the Cython (.pyx) implementation of Fibonacci to a
C extension module for maximum performance.

Usage:
    python scripts/setup_cython.py build_ext --inplace

This will create a compiled .so (Linux/Mac) or .pyd (Windows) file
in the techniques/09_cython_optimized/ directory.

Author: SpeedyFibonacci Contributors
License: MIT
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from setuptools import setup, Extension
    from Cython.Build import cythonize
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False
    print("Error: Cython is required. Install with: pip install Cython")
    sys.exit(1)

try:
    import numpy as np
    NUMPY_INCLUDE = [np.get_include()]
except ImportError:
    NUMPY_INCLUDE = []


def main():
    """Build Cython extension."""

    # Define the extension
    cython_file = project_root / "techniques" / "09_cython_optimized" / "fibonacci_impl.pyx"

    if not cython_file.exists():
        print(f"Error: Cython source file not found: {cython_file}")
        sys.exit(1)

    extensions = [
        Extension(
            name="techniques.09_cython_optimized.fibonacci_impl",
            sources=[str(cython_file)],
            include_dirs=NUMPY_INCLUDE,
            extra_compile_args=["-O3", "-ffast-math"],  # Optimization flags
        )
    ]

    # Compile
    setup(
        name="fibonacci_cython",
        ext_modules=cythonize(
            extensions,
            compiler_directives={
                'language_level': "3",
                'boundscheck': False,
                'wraparound': False,
                'cdivision': True,
            }
        ),
        script_args=sys.argv[1:] if len(sys.argv) > 1 else ['build_ext', '--inplace'],
    )

    print("\nCython compilation complete!")
    print("The Cython-optimized Fibonacci technique is now available.")


if __name__ == "__main__":
    main()
