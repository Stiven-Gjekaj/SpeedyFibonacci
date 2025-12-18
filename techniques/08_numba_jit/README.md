# Numba JIT

## Overview

Numba is a Just-In-Time (JIT) compiler that translates Python code to optimized machine code using LLVM. This technique demonstrates how to achieve near-C performance while writing pure Python, making it one of the fastest methods for numerical Fibonacci computation.

## Algorithm Description

The algorithm is the same simple iterative approach, but JIT-compiled:

```python
from numba import jit

@jit(nopython=True, cache=True)
def fibonacci(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for i in range(2, n + 1):
        a, b = b, a + b
    return b
```

The `@jit` decorator tells Numba to compile this function to machine code.

### Decorator Options

- `nopython=True`: Force compilation without Python interpreter fallback
- `cache=True`: Save compiled code to disk for faster subsequent imports
- `parallel=True`: Enable automatic parallelization (not useful for Fibonacci)
- `fastmath=True`: Allow faster but less precise floating-point operations

## Complexity Analysis

### Time Complexity: O(n)

Same as iterative Python, but with much smaller constant factors:
- No Python interpreter overhead
- Direct CPU instructions
- Optimized register usage
- CPU cache-friendly

### Space Complexity: O(1)

- Two variables (a, b) stored in CPU registers
- No dynamic memory allocation

### Performance Multiplier

Typical speedups over pure Python:
- Simple loops: 10-100x faster
- Numerical operations: 50-200x faster
- Close to hand-written C code

## Performance Characteristics

| n | Pure Python | Numba | Speedup |
|---|-------------|-------|---------|
| 100 | ~1μs | ~0.1μs | ~10x |
| 1,000 | ~10μs | ~0.5μs | ~20x |
| 10,000 | ~100μs | ~5μs | ~20x |
| 92 (max int64) | ~10μs | ~0.5μs | ~20x |

**Note**: For n > 92, Numba overflows. Our implementation falls back to Python.

**In our 1-second benchmark**: Numba will be among the fastest for computing many sequential Fibonacci numbers up to F(92).

## Implementation Details

### First Call Compilation

```python
@jit(nopython=True)
def fib(n):
    # ...

# First call triggers compilation (~100ms)
fib(10)

# Subsequent calls use compiled code (~1μs)
fib(10)
```

### Type Inference

Numba infers types from function arguments:

```python
@jit(nopython=True)
def fib(n):  # n inferred as int64
    a, b = 0, 1  # inferred as int64
    # ...
```

### Explicit Type Signatures

```python
from numba import jit, int64

@jit(int64(int64), nopython=True)
def fib(n):
    # Explicitly typed: returns int64, takes int64
    # ...
```

### Integer Overflow

Numba uses fixed-size integers (typically int64):
- F(92) = 7540113804746346429 (fits in int64)
- F(93) = 12200160415121876738 (overflows int64!)

Our implementation detects this and falls back to Python.

### Caching

With `cache=True`, compiled code is saved to disk:
```
__pycache__/fibonacci.cpython-311.nbc  # Cached compiled code
```

This eliminates compilation time on subsequent program runs.

## Limitations

1. **Integer size**: int64 max, no arbitrary precision
2. **Compilation time**: First call is slow
3. **Type constraints**: Must use Numba-supported types
4. **Feature limitations**: Can't use all Python features

### Unsupported in nopython mode:
- Arbitrary precision integers
- Most Python objects
- Dynamic typing
- Many standard library functions

## When to Use

**Use this technique when:**
- Maximum speed is required
- Computing many Fibonacci numbers sequentially
- n is bounded (≤ 92 for int64)
- Already using Numba in your project

**Don't use when:**
- Need arbitrary precision (large n)
- Startup time is critical (compilation overhead)
- Minimizing dependencies
- Teaching basic algorithms (adds complexity)

## Comparison with Other Compiled Approaches

| Approach | Compilation | Ease of Use | Speed | Portability |
|----------|-------------|-------------|-------|-------------|
| Numba | JIT | Easy (decorator) | Very fast | Good |
| Cython | AOT | Moderate | Fast | Requires compilation |
| PyPy | JIT (interpreter) | Transparent | Fast | Separate interpreter |
| C Extension | AOT | Difficult | Very fast | Requires C knowledge |

## Advanced Usage

### Parallel Fibonacci (educational only)

```python
from numba import jit, prange

@jit(nopython=True, parallel=True)
def fib_sequence(max_n):
    """Compute F(0) to F(max_n) in parallel."""
    result = np.zeros(max_n + 1, dtype=np.int64)
    result[1] = 1
    # Note: This doesn't parallelize well due to dependencies
    for i in prange(2, max_n + 1):
        result[i] = result[i-1] + result[i-2]
    return result
```

### CUDA GPU (for matrix operations)

```python
from numba import cuda

@cuda.jit
def matrix_mult_gpu(A, B, C):
    # GPU-accelerated matrix multiplication
    # (Useful for batch Fibonacci via matrix method)
    pass
```

## References

1. Lam, S.K., Pitrou, A., & Seibert, S. (2015). "Numba: A LLVM-based Python JIT Compiler". *Proceedings of the Second Workshop on the LLVM Compiler Infrastructure in HPC*.

2. Numba Documentation. https://numba.pydata.org/

3. LLVM Project. https://llvm.org/

4. Lattner, C., & Adve, V. (2004). "LLVM: A Compilation Framework for Lifelong Program Analysis & Transformation". *CGO '04*.

## Example

```python
from techniques.08_numba_jit.fibonacci import NumbaJIT

technique = NumbaJIT()

# Warm up (triggers compilation)
technique.setup()

# Fast compiled execution
print(technique.calculate(10))   # 55
print(technique.calculate(50))   # 12586269025
print(technique.calculate(92))   # 7540113804746346429 (max for int64)

# Falls back to Python for large n
print(technique.calculate(100))  # 354224848179261915075

# Benchmark comparison
import time

# Numba (after warmup)
start = time.perf_counter()
for i in range(100000):
    technique.calculate(50)
numba_time = time.perf_counter() - start
print(f"Numba: {numba_time:.3f}s for 100k calls")
```
