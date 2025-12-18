# Dynamic Programming (Bottom-Up)

## Overview

The bottom-up dynamic programming approach builds the Fibonacci sequence iteratively from the base cases up to the target value. This is also called "tabulation" and represents the classic DP paradigm of solving smaller subproblems first and using their solutions to build up to larger problems.

## Algorithm Description

Instead of starting with F(n) and recursing down (top-down), we start with F(0) and F(1) and iteratively compute each subsequent value.

```python
def fibonacci(n):
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1

    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]
```

### Pseudocode

```
FUNCTION fibonacci(n):
    IF n <= 1:
        RETURN n

    CREATE array dp[0..n]
    dp[0] = 0
    dp[1] = 1

    FOR i FROM 2 TO n:
        dp[i] = dp[i-1] + dp[i-2]

    RETURN dp[n]
```

## Complexity Analysis

### Time Complexity: O(n)

- Single loop from 2 to n
- Each iteration does O(1) work (one addition, one assignment)
- Total: O(n)

### Space Complexity: O(n)

- Array of size n+1 to store all Fibonacci values
- No recursion, so no call stack overhead

Note: This can be optimized to O(1) space (see technique 10_iterative_space_optimized).

## Mathematical Background

### Recurrence Relation

The algorithm directly implements the recurrence:
```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2)
```

### Optimal Substructure

The Fibonacci problem has optimal substructure: the optimal solution to F(n) is built from optimal solutions to F(n-1) and F(n-2).

### Tabulation vs Memoization

| Aspect | Bottom-Up (Tabulation) | Top-Down (Memoization) |
|--------|----------------------|----------------------|
| Direction | Small → Large | Large → Small |
| Recursion | No | Yes |
| Stack overflow | No risk | Possible |
| Computes | All subproblems | Only needed subproblems |
| Code complexity | Usually simpler | May be more intuitive |

## Performance Characteristics

| n | Time (approx) | Memory |
|---|--------------|--------|
| 100 | < 1ms | ~1 KB |
| 1,000 | < 1ms | ~8 KB |
| 10,000 | ~5ms | ~80 KB |
| 100,000 | ~500ms | ~2 MB |

**In our 1-second benchmark, this technique typically calculates thousands of Fibonacci numbers.**

## Implementation Details

### Python List Performance

Python lists are implemented as dynamic arrays:
- Append: O(1) amortized
- Index access: O(1)
- Pre-allocation with `[0] * n` is efficient

### Memory Considerations

For very large n, the O(n) space can become significant:
- Python integers grow with value (arbitrary precision)
- F(100000) has ~20,000 digits
- Consider space-optimized version for memory-constrained scenarios

### Alternative Implementations

**Using append:**
```python
dp = [0, 1]
for i in range(2, n + 1):
    dp.append(dp[-1] + dp[-2])
return dp[n]
```

**Pre-allocated (slightly faster):**
```python
dp = [0] * (n + 1)
dp[1] = 1
for i in range(2, n + 1):
    dp[i] = dp[i-1] + dp[i-2]
return dp[n]
```

## When to Use

**Use this technique when:**
- You need all Fibonacci values from 0 to n
- Memory is not a critical constraint
- You want simple, straightforward code
- Teaching dynamic programming concepts

**Don't use when:**
- Only need a single F(n) value (space-optimized is better)
- Memory is very constrained
- n is extremely large

## References

1. Bellman, R. (1957). *Dynamic Programming*. Princeton University Press. [Foundational DP work]

2. Cormen, T.H., Leiserson, C.E., Rivest, R.L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. Chapter 15: Dynamic Programming.

3. Kleinberg, J., & Tardos, E. (2005). *Algorithm Design*. Addison-Wesley. Chapter 6: Dynamic Programming.

## Example

```python
from techniques.03_dynamic_programming.fibonacci import DynamicProgramming

technique = DynamicProgramming()

# Calculate individual values
print(technique.calculate(10))   # 55
print(technique.calculate(50))   # 12586269025
print(technique.calculate(100))  # 354224848179261915075

# The internal array holds all values up to n
# This is efficient when you need multiple Fibonacci numbers
```
