# Iterative Space-Optimized

## Overview

The space-optimized iterative approach is the most practical pure Python solution for computing Fibonacci numbers. It achieves O(n) time with O(1) space by observing that only the last two values are needed at any point.

## Algorithm Description

The key insight is that F(n) only depends on F(n-1) and F(n-2), so we don't need to store the entire sequence.

```python
def fibonacci(n):
    if n <= 1:
        return n

    a, b = 0, 1  # F(0), F(1)

    for i in range(2, n + 1):
        a, b = b, a + b  # Elegant Python tuple swap

    return b
```

### Step-by-Step Execution for F(6)

| Iteration | Before | After | Represents |
|-----------|--------|-------|------------|
| Start | a=0, b=1 | - | F(0), F(1) |
| i=2 | a=0, b=1 | a=1, b=1 | F(1), F(2) |
| i=3 | a=1, b=1 | a=1, b=2 | F(2), F(3) |
| i=4 | a=1, b=2 | a=2, b=3 | F(3), F(4) |
| i=5 | a=2, b=3 | a=3, b=5 | F(4), F(5) |
| i=6 | a=3, b=5 | a=5, b=8 | F(5), F(6) |

Result: F(6) = 8 ✓

### Pseudocode

```
FUNCTION fibonacci(n):
    IF n <= 1:
        RETURN n

    a = 0  // F(i-2)
    b = 1  // F(i-1)

    FOR i FROM 2 TO n:
        temp = a + b
        a = b
        b = temp

    RETURN b
```

## Complexity Analysis

### Time Complexity: O(n)

- Single loop from 2 to n
- Each iteration: O(1) operations
  - One addition
  - Two assignments (via tuple swap)
- Total: O(n)

### Space Complexity: O(1)

- Only two variables (a, b) regardless of n
- No array, no recursion stack
- Constant auxiliary space

**Note**: The result F(n) itself grows exponentially (F(n) has about 0.21n digits), so the space to store the result is O(n). But the algorithm's auxiliary space is O(1).

## Performance Characteristics

| n | Time (approx) | Memory |
|---|--------------|--------|
| 100 | < 1ms | O(1) |
| 1,000 | < 1ms | O(1) |
| 10,000 | ~5ms | O(1) |
| 100,000 | ~500ms | O(1) |
| 1,000,000 | ~1 min | O(1) |

**In our 1-second benchmark**: This is typically one of the fastest pure Python methods due to its simplicity and low overhead.

## Python's Tuple Swap

The line `a, b = b, a + b` is particularly elegant:

### How It Works

```python
# Python evaluates the right side first
# Then assigns to the left side simultaneously
a, b = b, a + b

# Equivalent to:
temp = a + b
a = b
b = temp
```

### Why It's Safe

Python evaluates the entire right-hand side before any assignments:
1. Evaluate `b` → get value of b
2. Evaluate `a + b` → get sum
3. Assign to `a` → b's old value
4. Assign to `b` → the sum

No temporary variable needed in the source code (Python handles it internally).

## Implementation Variants

### Classic with temp variable
```python
def fib_classic(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for i in range(2, n + 1):
        temp = a + b
        a = b
        b = temp
    return b
```

### Using tuple unpacking
```python
def fib_tuple(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

### Using walrus operator (Python 3.8+)
```python
def fib_walrus(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, (b := a + b)  # Less readable, not recommended
    return b
```

### Inline version (code golf)
```python
fib = lambda n: (lambda a,b,n: b if n<2 else fib(n-1)+fib(n-2))(0,1,n)
# Don't do this! Just for fun.
```

## Comparison with Other O(n) Methods

| Method | Space | Overhead | Best For |
|--------|-------|----------|----------|
| Space-Optimized | O(1) | Minimal | Single F(n) |
| DP Array | O(n) | Array allocation | All F(0)...F(n) |
| Generator | O(1) | Generator protocol | Streaming |
| Memoized | O(n) | Cache management | Repeated queries |

## When to Use

**Use this technique when:**
- Computing a single Fibonacci number
- Memory is constrained
- Simplicity is valued
- Teaching basic algorithms
- Most practical applications

**Don't use when:**
- Need all F(0)...F(n) (use DP array)
- Need repeated random access (use memoization)
- n is extremely large (use O(log n) methods)

## Optimizations

### Loop unrolling (minor improvement)
```python
def fib_unrolled(n):
    if n <= 1:
        return n
    a, b = 0, 1

    # Process two iterations at a time
    for _ in range((n - 1) // 2):
        a = a + b
        b = a + b

    # Handle odd n
    if n % 2 == 0:
        return a + b
    return b
```

### Local variable optimization
```python
def fib_local(n):
    # Accessing local variables is faster than global
    if n <= 1:
        return n

    _range = range  # Local reference
    a, b = 0, 1

    for _ in _range(2, n + 1):
        a, b = b, a + b

    return b
```

## References

1. Sedgewick, R., & Wayne, K. (2011). *Algorithms* (4th ed.). Addison-Wesley. Section 1.1.

2. Cormen, T.H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.

3. Lutz, M. (2013). *Learning Python* (5th ed.). O'Reilly Media. [Python tuple unpacking]

4. Python Documentation. "More on Defining Functions". https://docs.python.org/3/tutorial/controlflow.html

## Example

```python
from techniques.10_iterative_space_optimized.fibonacci import IterativeSpaceOptimized

technique = IterativeSpaceOptimized()

# Calculate individual values
print(technique.calculate(10))   # 55
print(technique.calculate(50))   # 12586269025
print(technique.calculate(100))  # 354224848179261915075

# Large values work fine (Python handles big integers)
result = technique.calculate(10000)
print(f"F(10000) has {len(str(result))} digits")

# Benchmark
import time
start = time.perf_counter()
for i in range(10000):
    technique.calculate(100)
elapsed = time.perf_counter() - start
print(f"10000 calls to F(100): {elapsed:.3f}s")
```
