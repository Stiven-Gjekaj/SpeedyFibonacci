# Cython Optimized

## Overview

Cython is a programming language that makes writing C extensions for Python easy. It allows you to write Python-like code with optional static type declarations that compile to highly efficient C code. This technique demonstrates using Cython to achieve C-level performance for Fibonacci calculation.

## Algorithm Description

The algorithm is the standard iterative approach, but with Cython's static typing:

```cython
cpdef long long fib_cython(int n):
    cdef long long a, b, temp
    cdef int i

    if n <= 1:
        return n

    a, b = 0, 1
    for i in range(2, n + 1):
        temp = a + b
        a = b
        b = temp

    return b
```

### Key Cython Features Used

- `cpdef`: Function callable from Python and C
- `cdef`: C-level variable declarations
- `long long`: 64-bit integer type
- `int`: 32-bit integer type
- Static loop variable typing

## Complexity Analysis

### Time Complexity: O(n)

Same algorithm as pure Python, but:
- Direct C-level integer operations
- Compiled loop without interpreter overhead
- Variables stored in CPU registers

### Space Complexity: O(1)

- Three C variables (a, b, temp)
- No Python object overhead

### Speedup Factors

Cython achieves speedups through:
1. Elimination of Python's dynamic dispatch
2. Direct C-level integer operations
3. Compiled loop statements
4. Memory-efficient C types

Typical speedup: 10-100x over pure Python

## Compilation Process

### Step 1: Write .pyx file
```cython
# fibonacci_impl.pyx
cpdef long long fib_cython(int n):
    ...
```

### Step 2: Create setup.py
```python
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("fibonacci_impl.pyx")
)
```

### Step 3: Compile
```bash
python setup.py build_ext --inplace
```

This produces: `fibonacci_impl.cpython-311-x86_64-linux-gnu.so`

### Step 4: Import and use
```python
from fibonacci_impl import fib_cython
print(fib_cython(50))  # 12586269025
```

## Performance Characteristics

| n | Pure Python | Cython | Speedup |
|---|-------------|--------|---------|
| 100 | ~1μs | ~0.05μs | ~20x |
| 1,000 | ~10μs | ~0.5μs | ~20x |
| 10,000 | ~100μs | ~5μs | ~20x |
| 92 (max) | ~10μs | ~0.4μs | ~25x |

**In our 1-second benchmark**: Cython will be among the fastest, computing millions of values for small n.

## Implementation Details

### Type Declarations

```cython
# C types for maximum speed
cdef int i              # 32-bit integer
cdef long long value    # 64-bit integer
cdef double x           # 64-bit float

# Python objects (slower)
cdef object py_obj
cdef list my_list
```

### Compiler Directives

```cython
# cython: language_level=3
# cython: boundscheck=False    # Disable array bounds checking
# cython: wraparound=False     # Disable negative indexing
# cython: cdivision=True       # Use C division semantics
```

### Function Types

```cython
# def: Python function (slowest)
def py_func(n):
    pass

# cdef: C function (not callable from Python)
cdef long long c_func(int n):
    pass

# cpdef: Hybrid (callable from both)
cpdef long long hybrid_func(int n):
    pass
```

### Memory Views (for arrays)

```cython
def process_array(double[:] arr):
    cdef int i
    cdef double total = 0
    for i in range(arr.shape[0]):
        total += arr[i]
    return total
```

## Limitations

1. **Compilation required**: Must compile before use
2. **Platform-specific**: Compiled binaries are OS/CPU specific
3. **Integer overflow**: long long overflows at F(93)
4. **No arbitrary precision**: Uses fixed C types

### Overflow Handling

```python
if CYTHON_AVAILABLE and n <= 92:
    return fib_cython(n)  # Fast path
else:
    return python_fallback(n)  # Arbitrary precision
```

## When to Use

**Use this technique when:**
- Maximum single-threaded performance is needed
- Compilation is acceptable
- Distributing binary packages
- Already using Cython in project

**Don't use when:**
- Need arbitrary precision integers
- Can't compile (restricted environment)
- Cross-platform pure Python required
- Development iteration speed is priority

## Comparison with Alternatives

| Aspect | Cython | Numba | PyPy | Pure Python |
|--------|--------|-------|------|-------------|
| Compilation | AOT (.pyx → .so) | JIT | JIT | None |
| Startup time | Fast (pre-compiled) | Slow (first call) | Fast | Fast |
| Dependencies | Cython, C compiler | LLVM | None | None |
| Ease of use | Moderate | Easy | Easy | Easiest |
| Performance | Very fast | Very fast | Fast | Slow |

## Advanced Techniques

### Parallel Loops with OpenMP

```cython
from cython.parallel import prange

cpdef long long[:] fib_array_parallel(int max_n):
    cdef long long[:] result = np.zeros(max_n + 1, dtype=np.int64)
    cdef int i

    result[0] = 0
    result[1] = 1

    # Note: Fibonacci has dependencies, so not actually parallelizable
    for i in range(2, max_n + 1):
        result[i] = result[i-1] + result[i-2]

    return result
```

### Using NumPy with Cython

```cython
import numpy as np
cimport numpy as np

cpdef np.ndarray[np.int64_t, ndim=1] fib_numpy_cython(int max_n):
    cdef np.ndarray[np.int64_t, ndim=1] fib = np.zeros(max_n + 1, dtype=np.int64)
    cdef int i

    fib[1] = 1
    for i in range(2, max_n + 1):
        fib[i] = fib[i-1] + fib[i-2]

    return fib
```

## References

1. Behnel, S., Bradshaw, R., Citro, C., Dalcin, L., Seljebotn, D.S., & Smith, K. (2011). "Cython: The Best of Both Worlds". *Computing in Science & Engineering*, 13(2), 31-39.

2. Cython Documentation. https://cython.readthedocs.io/

3. Smith, K. (2015). *Cython: A Guide for Python Programmers*. O'Reilly Media.

4. Lanaro, G. (2017). *Python High Performance* (2nd ed.). Packt Publishing. Chapter 3.

## Example

```python
from techniques.09_cython_optimized.fibonacci import CythonOptimized

technique = CythonOptimized()

# Check if compiled
print(f"Cython compiled: {technique.is_compiled()}")

# Calculate Fibonacci numbers
print(technique.calculate(10))   # 55
print(technique.calculate(50))   # 12586269025
print(technique.calculate(92))   # 7540113804746346429 (max for long long)
print(technique.calculate(100))  # Falls back to Python for arbitrary precision

# Direct usage if compiled
if technique.is_compiled():
    from techniques.09_cython_optimized.fibonacci_impl import fib_cython

    import time
    start = time.perf_counter()
    for i in range(1000000):
        fib_cython(50)
    elapsed = time.perf_counter() - start
    print(f"1M calls in {elapsed:.3f}s")
```
