# Complexity Analysis

## Big-O Notation Primer

Big-O notation describes the upper bound of an algorithm's growth rate:

- **O(1)** - Constant: Same time regardless of input size
- **O(log n)** - Logarithmic: Time grows slowly as input doubles
- **O(n)** - Linear: Time grows proportionally with input
- **O(n log n)** - Linearithmic: Common in efficient sorting
- **O(n²)** - Quadratic: Time grows with square of input
- **O(2ⁿ)** - Exponential: Time doubles with each additional input

## Complexity Summary

| Technique | Time | Space | Operations for F(50) |
|-----------|------|-------|---------------------|
| Naive Recursion | O(2ⁿ) | O(n) | ~20 billion |
| Memoized Recursion | O(n) | O(n) | ~50 |
| Dynamic Programming | O(n) | O(n) | ~50 |
| Matrix Exponentiation | O(log n) | O(log n) | ~18 |
| Binet's Formula | O(1)* | O(1) | ~5 |
| Generator-based | O(n) | O(1) | ~50 |
| NumPy Vectorized | O(log n) | O(1) | ~18 |
| Numba JIT | O(n) | O(1) | ~50 |
| Cython Optimized | O(n) | O(1) | ~50 |
| Iterative Optimized | O(n) | O(1) | ~50 |
| Fast Doubling | O(log n) | O(log n) | ~18 |
| Parallel Processing | O(n) | O(n) | ~50 |

*Binet's O(1) assumes bounded precision; true arbitrary precision requires O(n) for the result itself.

## Detailed Analysis

### 1. Naive Recursion - O(2ⁿ)

```
T(n) = T(n-1) + T(n-2) + O(1)
```

The recurrence tree has exponential nodes:
- Each call branches into 2 calls
- Tree depth is n
- Total calls ≈ φⁿ ≈ O(1.618ⁿ) ⊂ O(2ⁿ)

**Example**: F(50) requires ~20 billion recursive calls!

**Space**: O(n) for the call stack depth.

### 2. Memoized Recursion - O(n)

With memoization, each F(k) is computed once:
- n+1 unique subproblems
- O(1) work per subproblem
- Total: O(n)

**Space**: O(n) for cache + O(n) for call stack = O(n)

### 3. Dynamic Programming - O(n)

Single loop from 2 to n:
```python
for i in range(2, n+1):
    dp[i] = dp[i-1] + dp[i-2]  # O(1)
```

**Time**: n-1 iterations × O(1) = O(n)
**Space**: O(n) for the array

### 4. Matrix Exponentiation - O(log n)

Binary exponentiation of 2×2 matrix:
- O(log n) matrix multiplications
- Each multiplication: O(1) for constant-size matrix

**Time**: O(log n)
**Space**: O(log n) for recursion or O(1) iterative

**Note**: For very large Fibonacci numbers, integer multiplication dominates. If F(n) has d digits, multiplication is O(d²) naively.

### 5. Binet's Formula - O(1)*

```
F(n) = (φⁿ - ψⁿ) / √5
```

Constant number of operations: exponentiation, subtraction, division.

**Caveat**: Floating-point precision limits accuracy. With arbitrary precision, computing φⁿ for n-bit precision takes O(n) time.

**Time**: O(1) with fixed precision, O(M(d) log n) with d-digit precision
**Space**: O(1) or O(d) for precision

### 6. Generator-based - O(n)

```python
def fib_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

**Time**: O(n) to reach F(n)
**Space**: O(1) - only two variables stored

### 7. NumPy Vectorized - O(log n)

Uses `np.linalg.matrix_power` which implements binary exponentiation.

**Time**: O(log n) matrix multiplications
**Space**: O(1) for fixed-size matrices

### 8-9. Numba JIT / Cython - O(n)

Same algorithm as iterative, but compiled to machine code:

```
a, b = 0, 1
for i in range(2, n+1):
    a, b = b, a + b
```

**Time**: O(n) but with much smaller constants
**Space**: O(1)

### 10. Iterative Space-Optimized - O(n)

```python
a, b = 0, 1
for _ in range(2, n+1):
    a, b = b, a + b
return b
```

**Time**: O(n)
**Space**: O(1) - only two variables

### 11. Fast Doubling - O(log n)

Uses identities:
```
F(2n)   = F(n) × [2×F(n+1) - F(n)]
F(2n+1) = F(n)² + F(n+1)²
```

**Time**: O(log n) recursive calls
**Space**: O(log n) for recursion stack

### 12. Parallel Processing - O(n)

Single F(n) computation remains O(n) - Fibonacci is inherently sequential.

Batch of k values with p processors:
- **Time**: O(max(nᵢ) × k/p)
- **Space**: O(k) for results

## Practical Performance

Algorithm complexity doesn't tell the whole story. Real performance depends on:

1. **Constant factors**: Cache efficiency, branch prediction
2. **Integer size**: Python integers grow with value
3. **Interpreter overhead**: JIT (Numba) vs interpreted
4. **Memory access patterns**: Array vs scalar operations

### Expected Benchmark Results

| Complexity | Typical Count (1s) | Example |
|------------|-------------------|---------|
| O(2ⁿ) | 30-35 | Naive Recursion |
| O(n) interpreted | 10,000-50,000 | DP, Generator |
| O(n) JIT/compiled | 100,000-1,000,000 | Numba, Cython |
| O(log n) | Varies widely | Matrix, Fast Doubling |
| O(1) | Millions | Binet (fixed precision) |

### Why O(log n) Isn't Always Fastest

For our sequential benchmark (F(0), F(1), F(2), ...):

- **O(n) methods**: Each F(k) takes O(1) additional work from F(k-1)
- **O(log n) methods**: Each F(k) computed independently in O(log k)

Total for F(0) to F(n):
- O(n) methods: O(1) + O(1) + ... = O(n)
- O(log n) methods: O(1) + O(1) + O(2) + ... + O(log n) = O(n log n)

So for sequential computation, O(n) methods win!

O(log n) excels when computing **single large** F(n) values.

## Space-Time Tradeoffs

| Method | Time | Space | Use Case |
|--------|------|-------|----------|
| DP Array | O(n) | O(n) | Need all F(0)...F(n) |
| Iterative | O(n) | O(1) | Single F(n), memory limited |
| Memoized | O(n) | O(n) | Random access to F(k) |
| Matrix | O(log n) | O(1) | Single large F(n) |

## Integer Arithmetic Complexity

For very large Fibonacci numbers, arithmetic on big integers becomes significant:

| Operation | Naive | Karatsuba | FFT |
|-----------|-------|-----------|-----|
| Multiplication | O(d²) | O(d^1.58) | O(d log d) |
| Addition | O(d) | O(d) | O(d) |

Where d = number of digits ≈ 0.21n for F(n).

For n = 1,000,000, F(n) has ~210,000 digits. Big integer multiplication becomes the bottleneck!

## References

1. Cormen, T.H., et al. (2009). *Introduction to Algorithms*. Chapter 3: Growth of Functions.
2. Sedgewick, R., & Wayne, K. (2011). *Algorithms*. Chapter 1.4: Analysis of Algorithms.
3. Knuth, D.E. (1997). *The Art of Computer Programming, Vol. 2*. Chapter 4.3.3: Big Numbers.
