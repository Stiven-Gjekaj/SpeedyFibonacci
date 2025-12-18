# Matrix Exponentiation

## Overview

Matrix exponentiation is an elegant O(log n) method for computing Fibonacci numbers based on a beautiful mathematical identity connecting Fibonacci numbers to matrix powers. Combined with binary exponentiation (exponentiation by squaring), this achieves logarithmic time complexity.

## Algorithm Description

The key insight is this matrix identity:

```
| F(n+1)  F(n)   |       | 1  1 |^n
|                |   =   |      |
| F(n)    F(n-1) |       | 1  0 |
```

Or equivalently:
```
| 1  1 |^n   | F(n+1)  F(n)   |
|      |   = |                |
| 1  0 |     | F(n)    F(n-1) |
```

To compute F(n), we compute the matrix power [[1,1],[1,0]]^(n-1) and read F(n) from position [0][0].

### Binary Exponentiation

To compute M^n efficiently, we use binary exponentiation:
- M^n = (M^(n/2))^2 if n is even
- M^n = M × M^(n-1) if n is odd

This reduces the number of matrix multiplications from O(n) to O(log n).

```python
def matrix_pow(M, n):
    result = identity_matrix
    while n > 0:
        if n % 2 == 1:
            result = result * M
        M = M * M
        n //= 2
    return result
```

### Pseudocode

```
FUNCTION fibonacci(n):
    IF n <= 1:
        RETURN n

    F = [[1, 1], [1, 0]]
    result = matrix_power(F, n-1)
    RETURN result[0][0]

FUNCTION matrix_power(M, n):
    result = [[1, 0], [0, 1]]  // Identity matrix

    WHILE n > 0:
        IF n is odd:
            result = matrix_multiply(result, M)
        M = matrix_multiply(M, M)
        n = n / 2

    RETURN result
```

## Complexity Analysis

### Time Complexity: O(log n)

- Binary exponentiation requires O(log n) iterations
- Each iteration does one or two 2×2 matrix multiplications
- 2×2 matrix multiplication: O(1) with respect to n (but O(M(k)) for k-bit integers)
- Total: O(log n) matrix multiplications

**Note**: For very large Fibonacci numbers, integer multiplication becomes significant. If F(n) has d digits, multiplication is O(d²) naively or O(d log d) with FFT-based multiplication.

### Space Complexity: O(log n)

- Iterative version: O(1) for matrices, O(log n) for storing large integers
- Recursive version: O(log n) call stack

### Comparison with Other Methods

| Method | Time | Best For |
|--------|------|----------|
| Iterative | O(n) | Computing sequence |
| Matrix | O(log n) | Single large F(n) |
| Fast Doubling | O(log n) | Single large F(n) |

## Mathematical Background

### Proof of the Matrix Identity

The Fibonacci recurrence can be written as:
```
| F(n+1) |   | 1  1 | | F(n)   |
|        | = |      | |        |
| F(n)   |   | 1  0 | | F(n-1) |
```

Applying this recursively from base case:
```
| F(n+1) |   | 1  1 |^n | F(1) |   | 1  1 |^n | 1 |
|        | = |      |   |      | = |      |   |   |
| F(n)   |   | 1  0 |   | F(0) |   | 1  0 |   | 0 |
```

This proves that [[1,1],[1,0]]^n contains F(n+1), F(n), F(n), F(n-1).

### Eigenvalue Connection

The eigenvalues of [[1,1],[1,0]] are:
- λ₁ = φ = (1 + √5) / 2 (golden ratio)
- λ₂ = ψ = (1 - √5) / 2

This connects matrix exponentiation to Binet's formula and explains why both achieve O(log n).

### Why It Works

The matrix [[1,1],[1,0]] encodes the Fibonacci recurrence. Each multiplication advances the sequence by one step. Binary exponentiation lets us "skip ahead" by powers of 2.

## Performance Characteristics

| n | Time (approx) | Notes |
|---|--------------|-------|
| 1,000 | < 1ms | Fast |
| 10,000 | ~1ms | Still fast |
| 100,000 | ~10ms | log n advantage shows |
| 1,000,000 | ~100ms | Much faster than O(n) |
| 10,000,000 | ~1s | Practical limit |

**In our 1-second benchmark**: The overhead of Python matrix operations means this technique may not beat simple iteration for small n, but excels for computing individual large Fibonacci numbers.

## Implementation Details

### Python Implementation

```python
def matrix_mult(A, B):
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0],
         A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0],
         A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

def matrix_pow(M, n):
    result = [[1, 0], [0, 1]]  # Identity
    while n > 0:
        if n % 2 == 1:
            result = matrix_mult(result, M)
        M = matrix_mult(M, M)
        n //= 2
    return result

def fib(n):
    if n <= 1:
        return n
    F = [[1, 1], [1, 0]]
    return matrix_pow(F, n-1)[0][0]
```

### NumPy Optimization

For larger matrices or batch operations, NumPy is more efficient:

```python
import numpy as np

def fib_numpy(n):
    F = np.array([[1, 1], [1, 0]], dtype=object)
    result = np.linalg.matrix_power(F, n-1)
    return result[0, 0]
```

## When to Use

**Use this technique when:**
- Computing a single large F(n)
- n is very large (> 10,000)
- Teaching matrix methods and binary exponentiation
- Demonstrating O(log n) algorithm design

**Don't use when:**
- Computing many sequential Fibonacci numbers
- n is small (< 1000) - overhead not worth it
- Maximum simplicity is required

## References

1. Gries, D., & Levin, G. (1980). "Computing Fibonacci Numbers (and Similarly Defined Functions) in Log Time". *Information Processing Letters*, 11(2), 68-69.

2. Cormen, T.H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. Section 31.6.

3. Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley. Chapter on number-theoretic algorithms.

4. Wikipedia: "Matrix exponential" and "Exponentiation by squaring".

## Example

```python
from techniques.04_matrix_exponentiation.fibonacci import MatrixExponentiation

technique = MatrixExponentiation()

# Small values
print(technique.calculate(10))   # 55
print(technique.calculate(50))   # 12586269025

# Large values - this is where matrix method shines
print(technique.calculate(1000))   # 70-digit number, very fast

# Very large - still logarithmic time
import time
start = time.time()
result = technique.calculate(100000)
print(f"F(100000) has {len(str(result))} digits")
print(f"Computed in {time.time()-start:.3f}s")
```
