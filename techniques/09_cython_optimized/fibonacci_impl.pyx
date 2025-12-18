# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True
"""
Cython implementation of Fibonacci calculation.

This file (.pyx) contains Cython code that will be compiled to C.
Static typing with cdef allows direct C-level operations.

To compile:
    python scripts/setup_cython.py build_ext --inplace

Author: SpeedyFibonacci Contributors
License: MIT
"""


cpdef long long fib_cython(int n):
    """
    Calculate F(n) using optimized Cython code.

    Uses C-level long long integers and compiled C loop.

    Args:
        n: The Fibonacci index (0-indexed, max 92 for long long)

    Returns:
        The nth Fibonacci number as long long

    Note:
        Overflows for n > 92. Use Python fallback for larger n.
    """
    cdef long long a, b, temp
    cdef int i

    if n <= 1:
        return n

    a = 0
    b = 1

    for i in range(2, n + 1):
        temp = a + b
        a = b
        b = temp

    return b


cpdef long long fib_cython_unrolled(int n):
    """
    Loop-unrolled version for even faster execution.

    Unrolling reduces loop overhead by processing multiple iterations
    per loop cycle.
    """
    cdef long long a, b
    cdef int i, remainder

    if n <= 1:
        return n

    a = 0
    b = 1

    # Process 4 iterations at a time
    for i in range(2, n - 2, 4):
        a = a + b  # i
        b = a + b  # i+1
        a = a + b  # i+2
        b = a + b  # i+3

    # Handle remaining iterations
    remainder = (n - 2) % 4
    i = n - remainder

    while i <= n:
        a, b = b, a + b
        i += 1

    return b
