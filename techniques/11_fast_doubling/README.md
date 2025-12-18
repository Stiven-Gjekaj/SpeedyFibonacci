# Fast Doubling

## Overview

Fast doubling is an elegant O(log n) algorithm for computing Fibonacci numbers. It uses two mathematical identities that allow us to "jump" through the sequence, computing F(2n) from F(n) without computing all intermediate values.

## Algorithm Description

The algorithm is based on these identities (derivable from matrix exponentiation):

```
F(2n)   = F(n) × [2×F(n+1) - F(n)]
F(2n+1) = F(n)² + F(n+1)²
```

Given F(n) and F(n+1), we can compute F(2n) and F(2n+1) in O(1) time!

### Recursive Implementation

```python
def fib_pair(n):
    """Returns (F(n), F(n+1))"""
    if n == 0:
        return (0, 1)

    a, b = fib_pair(n // 2)

    c = a * (2 * b - a)      # F(2k)
    d = a * a + b * b        # F(2k+1)

    if n % 2 == 0:
        return (c, d)
    else:
        return (d, c + d)

def fibonacci(n):
    return fib_pair(n)[0]
```

### How It Works

For n = 13 (binary: 1101):

```
Start: F(0)=0, F(1)=1

Process bit 1 (MSB):
  Double: F(0),F(1) → F(0),F(1)
  Bit=1: advance to F(1),F(2) = (1, 1)

Process bit 1:
  Double: F(1),F(2) → F(2),F(3) = (1, 2)
  Bit=1: advance to F(3),F(4) = (2, 3)

Process bit 0:
  Double: F(3),F(4) → F(6),F(7) = (8, 13)
  Bit=0: stay at F(6),F(7) = (8, 13)

Process bit 1 (LSB):
  Double: F(6),F(7) → F(12),F(13) = (144, 233)
  Bit=1: advance to F(13),F(14) = (233, 377)

Result: F(13) = 233 ✓
```

## Complexity Analysis

### Time Complexity: O(log n)

- Recursion depth is log₂(n)
- Each level does O(1) arithmetic operations*
- Total: O(log n) levels

*For very large Fibonacci numbers, multiplication of k-digit numbers takes O(k log k) with FFT-based methods, making the true complexity O(log n × M(digits)).

### Space Complexity: O(log n)

- Recursion depth is O(log n)
- Each level stores O(1) variables

The iterative version achieves O(1) auxiliary space.

## Mathematical Background

### Derivation from Matrix Identity

The fast doubling identities come from the matrix formulation:

```
[F(n+1)  F(n)  ]   [1 1]^n
[F(n)    F(n-1)] = [1 0]
```

Squaring this matrix:
```
[1 1]^(2n)   [1 1]^n   [1 1]^n
[1 0]     =  [1 0]   × [1 0]

[F(2n+1) F(2n)]   [F(n+1) F(n)]   [F(n+1) F(n)]
[F(2n)   F(2n-1)] = [F(n)   F(n-1)] × [F(n)   F(n-1)]
```

Multiplying out:
- F(2n) = F(n+1)×F(n) + F(n)×F(n-1)
        = F(n)×[F(n+1) + F(n-1)]
        = F(n)×[F(n+1) + F(n+1) - F(n)]
        = F(n)×[2×F(n+1) - F(n)]

- F(2n+1) = F(n+1)² + F(n)²

### Related Identities

```
F(2n-1) = F(n)² + F(n-1)²
F(2n)   = F(n) × [F(n) + 2×F(n-1)]
        = F(n) × [2×F(n+1) - F(n)]
F(2n+1) = F(n+1)² + F(n)²

F(n+m)  = F(n)×F(m-1) + F(n+1)×F(m)
F(n-m)  = (-1)^m × [F(n)×F(m+1) - F(n+1)×F(m)]
```

## Performance Characteristics

| n | Time (approx) | Recursion Depth |
|---|--------------|-----------------|
| 100 | < 1ms | 7 |
| 1,000 | < 1ms | 10 |
| 10,000 | ~1ms | 14 |
| 100,000 | ~10ms | 17 |
| 1,000,000 | ~100ms | 20 |
| 10,000,000 | ~1s | 24 |

**In our 1-second benchmark**: Fast doubling is excellent for computing large individual Fibonacci numbers but has overhead for computing many small sequential values.

## Implementation Details

### Recursive vs Iterative

**Recursive (cleaner):**
```python
def fib_recursive(n):
    if n == 0:
        return (0, 1)
    a, b = fib_recursive(n // 2)
    c = a * (2*b - a)
    d = a*a + b*b
    return (c, d) if n % 2 == 0 else (d, c+d)
```

**Iterative (no stack limit):**
```python
def fib_iterative(n):
    if n == 0:
        return 0
    a, b = 0, 1
    for i in range(n.bit_length() - 1, -1, -1):
        c = a * (2*b - a)
        d = a*a + b*b
        if (n >> i) & 1:
            a, b = d, c + d
        else:
            a, b = c, d
    return a
```

### Comparison with Matrix Exponentiation

| Aspect | Fast Doubling | Matrix Exponentiation |
|--------|--------------|----------------------|
| Operations per level | 3 mults, 2 adds | 8 mults, 4 adds |
| Space per level | 2 integers | 4 integers |
| Code complexity | Simpler | More complex |
| Same complexity | O(log n) | O(log n) |

Fast doubling is essentially an optimized version of matrix exponentiation!

## When to Use

**Use this technique when:**
- Computing individual large F(n)
- O(log n) complexity is needed
- Memory efficiency matters
- Teaching advanced Fibonacci methods

**Don't use when:**
- Computing many sequential Fibonacci numbers
- n is small (overhead not worth it)
- Simplicity is prioritized

## Advanced Topics

### Negative Indices

Fibonacci can be extended to negative indices:
```
F(-n) = (-1)^(n+1) × F(n)

F(-1) = 1, F(-2) = -1, F(-3) = 2, F(-4) = -3, ...
```

Fast doubling can be adapted for this.

### Modular Fibonacci

For F(n) mod m, fast doubling is ideal:
```python
def fib_mod(n, m):
    if n == 0:
        return (0, 1)
    a, b = fib_mod(n // 2, m)
    c = (a * ((2*b - a) % m)) % m
    d = (a*a + b*b) % m
    if n % 2 == 0:
        return (c, d)
    else:
        return (d, (c + d) % m)
```

### GCD with Fibonacci

A beautiful identity:
```
gcd(F(m), F(n)) = F(gcd(m, n))
```

Fast doubling enables efficient computation of F(gcd(m,n)).

## References

1. Nayuki. "Fast Fibonacci algorithms". https://www.nayuki.io/page/fast-fibonacci-algorithms [Excellent detailed explanation]

2. Takahashi, D. (2000). "A Fast Algorithm for Computing Large Fibonacci Numbers". *Information Processing Letters*, 75(6), 243-246.

3. OEIS A000045. "Fibonacci numbers". https://oeis.org/A000045

4. Knuth, D.E. (1997). *The Art of Computer Programming, Volume 1* (3rd ed.). Section 1.2.8.

## Example

```python
from techniques.11_fast_doubling.fibonacci import FastDoubling

technique = FastDoubling()

# Calculate individual values
print(technique.calculate(10))    # 55
print(technique.calculate(100))   # 354224848179261915075
print(technique.calculate(1000))  # 209-digit number

# Compare speeds for large n
import time

n = 100000

start = time.perf_counter()
result = technique.calculate(n)
elapsed = time.perf_counter() - start
print(f"F({n}) computed in {elapsed:.4f}s")
print(f"Result has {len(str(result))} digits")

# Iterative version (avoids recursion limit)
result2 = technique.calculate_iterative(n)
assert result == result2
```
