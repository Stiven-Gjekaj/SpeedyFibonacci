# NumPy Vectorized

## Overview

This technique leverages NumPy's highly optimized C-level implementations for matrix operations to compute Fibonacci numbers using matrix exponentiation. NumPy is the foundational package for scientific computing in Python.

## Algorithm Description

Uses the same matrix identity as the pure Python matrix exponentiation, but with NumPy's optimized implementation:

```
| 1  1 |^n
|      |    contains F(n+1), F(n), F(n-1)
| 1  0 |
```

```python
import numpy as np

def fibonacci(n):
    if n <= 1:
        return n
    F = np.array([[1, 1], [1, 0]], dtype=object)
    result = np.linalg.matrix_power(F, n - 1)
    return int(result[0, 0])
```

### Key NumPy Function

`np.linalg.matrix_power(M, n)` efficiently computes M^n using binary exponentiation internally.

## Complexity Analysis

### Time Complexity: O(log n)

- `np.linalg.matrix_power` uses binary exponentiation
- O(log n) 2×2 matrix multiplications
- Each matrix multiplication is O(1) for fixed size

### Space Complexity: O(1)

- Fixed-size 2×2 matrices
- No additional arrays needed

### NumPy Performance

NumPy's C-level implementation offers:
- Contiguous memory layout for cache efficiency
- BLAS/LAPACK optimizations (when available)
- Reduced Python interpreter overhead

## Performance Characteristics

| n | Time (approx) | Notes |
|---|--------------|-------|
| 100 | < 1ms | Fast |
| 1,000 | < 1ms | Still fast |
| 10,000 | ~1ms | Logarithmic |
| 100,000 | ~10ms | Large number arithmetic dominates |
| 1,000,000 | ~500ms | Very large integers |

**In our 1-second benchmark**: NumPy overhead may make it slower than simple iteration for small n, but it excels for larger values.

## Implementation Details

### Data Types

**Using native types (limited precision):**
```python
F = np.array([[1, 1], [1, 0]], dtype=np.int64)
# Overflow at F(93) = 12200160415121876738 (exceeds int64)
```

**Using object dtype (arbitrary precision):**
```python
F = np.array([[1, 1], [1, 0]], dtype=object)
# Supports Python's arbitrary precision integers
```

### Alternative NumPy Approaches

**Iterative with NumPy arrays:**
```python
def fib_numpy_iterative(n):
    fib = np.zeros(n + 1, dtype=object)
    fib[1] = 1
    for i in range(2, n + 1):
        fib[i] = fib[i-1] + fib[i-2]
    return fib[n]
```

**Eigenvalue method:**
```python
def fib_eigen(n):
    F = np.array([[1, 1], [1, 0]], dtype=float)
    eigenvalues, eigenvectors = np.linalg.eig(F)
    # Reconstruct using eigendecomposition
    # (Less practical due to precision issues)
```

### NumPy vs Pure Python

| Aspect | NumPy | Pure Python |
|--------|-------|-------------|
| Setup overhead | Higher | Lower |
| Small n | Slower | Faster |
| Large n | Faster | Slower |
| Dependencies | Requires NumPy | None |
| Memory layout | Contiguous C array | Python objects |

## When to Use

**Use this technique when:**
- Already using NumPy in your project
- Computing Fibonacci in numerical pipelines
- Need O(log n) complexity
- Working with batch operations

**Don't use when:**
- Minimizing dependencies
- Very small n (overhead not worth it)
- Memory is severely constrained

## NumPy Best Practices

### Import Conventions
```python
import numpy as np  # Standard convention
```

### Array Creation
```python
# For Fibonacci with large integers
F = np.array([[1, 1], [1, 0]], dtype=object)

# For numerical work with bounded values
F = np.array([[1, 1], [1, 0]], dtype=np.float64)
```

### Batch Operations
```python
# Compute multiple Fibonacci numbers efficiently
def fib_batch(indices):
    F = np.array([[1, 1], [1, 0]], dtype=object)
    results = []
    for n in indices:
        if n <= 1:
            results.append(n)
        else:
            M = np.linalg.matrix_power(F, n - 1)
            results.append(int(M[0, 0]))
    return results
```

## References

1. Harris, C.R., Millman, K.J., van der Walt, S.J., et al. (2020). "Array programming with NumPy". *Nature*, 585, 357-362.

2. NumPy Documentation. "Linear Algebra (numpy.linalg)". https://numpy.org/doc/stable/reference/routines.linalg.html

3. Van Der Walt, S., Colbert, S.C., & Varoquaux, G. (2011). "The NumPy Array: A Structure for Efficient Numerical Computation". *Computing in Science & Engineering*, 13(2), 22-30.

4. Oliphant, T.E. (2006). *A Guide to NumPy*. Trelgol Publishing.

## Example

```python
from techniques.07_numpy_vectorized.fibonacci import NumpyVectorized
import numpy as np

technique = NumpyVectorized()

# Calculate Fibonacci numbers
print(technique.calculate(10))   # 55
print(technique.calculate(50))   # 12586269025
print(technique.calculate(100))  # 354224848179261915075

# Direct NumPy usage
F = np.array([[1, 1], [1, 0]], dtype=object)
result = np.linalg.matrix_power(F, 99)
print(result[0, 0])  # F(100) = 354224848179261915075

# Verify against known values
for n in [10, 20, 30, 40, 50]:
    print(f"F({n}) = {technique.calculate(n)}")
```
