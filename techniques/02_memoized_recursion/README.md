# Memoized Recursion

## Overview

Memoization is an optimization technique that stores the results of expensive function calls and returns the cached result when the same inputs occur again. Applied to Fibonacci calculation, it transforms the exponential O(2^n) naive recursion into a linear O(n) algorithm.

This technique demonstrates "top-down" dynamic programming, where we start with the original problem and recursively break it down while caching intermediate results.

## Algorithm Description

The key insight is that in naive recursion, we calculate the same Fibonacci numbers many times. For example, F(5) requires F(3) twice, F(2) three times, etc.

With memoization, each F(k) is computed exactly once and then retrieved from cache for subsequent calls.

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### Pseudocode

```
INITIALIZE cache as empty dictionary

FUNCTION fibonacci(n):
    IF n IN cache:
        RETURN cache[n]

    IF n <= 1:
        result = n
    ELSE:
        result = fibonacci(n - 1) + fibonacci(n - 2)

    cache[n] = result
    RETURN result
```

## Complexity Analysis

### Time Complexity: O(n)

Each unique subproblem F(0), F(1), ..., F(n) is solved exactly once:
- First call to F(k): O(1) work + recursive calls
- Subsequent calls to F(k): O(1) cache lookup

Total: n+1 unique subproblems × O(1) work each = O(n)

### Space Complexity: O(n)

Two sources of space usage:
1. **Cache storage**: O(n) entries storing F(0) through F(n)
2. **Call stack**: O(n) maximum depth for first computation

Total: O(n)

### Comparison with Naive Recursion

| Metric | Naive | Memoized |
|--------|-------|----------|
| Time | O(2^n) | O(n) |
| Space | O(n) | O(n) |
| F(40) calls | 331M | 41 unique |

## Mathematical Background

### Overlapping Subproblems

The Fibonacci problem exhibits "overlapping subproblems" - a key characteristic that makes dynamic programming applicable. The same subproblems are encountered multiple times in different branches of the recursion tree.

**Subproblem DAG (Directed Acyclic Graph):**

Instead of the exponential tree, memoization converts the computation to a DAG with n+1 nodes:

```
F(5) → F(4) → F(3) → F(2) → F(1)
  ↓      ↓      ↓      ↓
F(3)   F(2)   F(1)   F(0)
```

### Top-Down vs Bottom-Up

Memoized recursion is the "top-down" approach to dynamic programming:
- Start with the main problem F(n)
- Recursively solve subproblems as needed
- Cache results to avoid recomputation

Compare with "bottom-up" (iterative DP):
- Start with base cases F(0), F(1)
- Build up to F(n) iteratively
- No recursion overhead

## Performance Characteristics

| n | Time (approx) | Cache Size |
|---|--------------|------------|
| 100 | < 1ms | 101 entries |
| 1,000 | < 10ms | 1,001 entries |
| 5,000 | ~50ms | 5,001 entries |
| 10,000 | ~100ms | 10,001 entries |

**Limitation**: Python's default recursion limit (~1000) restricts the maximum n. Increasing the limit is possible but risks stack overflow.

**In our 1-second benchmark, this technique typically calculates thousands of Fibonacci numbers.**

## Implementation Details

### Python's lru_cache

Python's `functools.lru_cache` provides a highly optimized memoization decorator:

```python
from functools import lru_cache

@lru_cache(maxsize=None)  # None = unlimited cache
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

Features:
- Thread-safe
- O(1) average lookup/insert
- Can limit cache size (LRU eviction)
- Cache statistics available via `.cache_info()`

### Manual Dictionary Cache

Alternative implementation without decorators:

```python
cache = {0: 0, 1: 1}

def fib(n):
    if n not in cache:
        cache[n] = fib(n-1) + fib(n-2)
    return cache[n]
```

### Handling Recursion Limit

For large n, increase Python's recursion limit:

```python
import sys
sys.setrecursionlimit(10000)
```

**Warning**: This risks stack overflow. For very large n, use iterative methods instead.

## When to Use

**Use this technique when:**
- You need the intuitive recursive structure
- n is moderate (< 1000 typically)
- Cache memory is not a concern
- You want to demonstrate dynamic programming concepts

**Don't use when:**
- n is very large (use iterative methods)
- Memory is constrained
- Maximum performance is required

## References

1. Michie, D. (1968). "Memo Functions and Machine Learning". *Nature*, 218, 19-22. [Original memoization paper]

2. Cormen, T.H., Leiserson, C.E., Rivest, R.L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. Chapter 15: Dynamic Programming.

3. Python Documentation. `functools.lru_cache`. https://docs.python.org/3/library/functools.html#functools.lru_cache

4. Bellman, R. (1957). *Dynamic Programming*. Princeton University Press.

## Example

```python
from techniques.02_memoized_recursion.fibonacci import MemoizedRecursion

technique = MemoizedRecursion()

# First calculation - builds cache
print(technique.calculate(100))  # 354224848179261915075

# Subsequent calculations - uses cache
print(technique.calculate(50))   # 12586269025 (instant)

# Cache info (internal)
print(technique._fib.cache_info())
# CacheInfo(hits=49, misses=101, maxsize=None, currsize=101)
```
