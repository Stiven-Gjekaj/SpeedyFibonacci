# Naive Recursion

## Overview

The naive recursive implementation is the most straightforward translation of the mathematical definition of the Fibonacci sequence into code. While elegant and easy to understand, it serves as an important pedagogical example of why algorithmic efficiency matters.

## Algorithm Description

The Fibonacci sequence is defined mathematically as:

```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2)  for n > 1
```

The naive recursive implementation directly mirrors this definition:

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### Pseudocode

```
FUNCTION fibonacci(n):
    IF n = 0:
        RETURN 0
    IF n = 1:
        RETURN 1
    RETURN fibonacci(n - 1) + fibonacci(n - 2)
```

## Complexity Analysis

### Time Complexity: O(2^n)

The time complexity is exponential because each call branches into two more calls. The recurrence relation for the number of operations T(n) is:

```
T(n) = T(n-1) + T(n-2) + O(1)
```

This is the same recurrence as the Fibonacci sequence itself! Solving this:

```
T(n) ≈ O(φ^n)
```

Where φ (phi) is the golden ratio ≈ 1.618. Since φ^n < 2^n, we often simplify to O(2^n).

**Call Tree Visualization for F(5):**

```
                    F(5)
                   /    \
               F(4)      F(3)
              /    \     /    \
           F(3)   F(2)  F(2)  F(1)
          /   \   /  \   /  \
       F(2) F(1) F(1) F(0) F(1) F(0)
       /  \
    F(1) F(0)
```

Notice how F(3) is calculated twice, F(2) three times, etc. This redundancy is the source of inefficiency.

### Space Complexity: O(n)

The space complexity is O(n) due to the maximum depth of the call stack. At any point, the deepest recursion will be n levels deep (when following the F(n-1) chain to F(0)).

## Mathematical Background

### The Golden Ratio Connection

The Fibonacci sequence has a deep connection to the golden ratio φ = (1 + √5) / 2 ≈ 1.618034.

The ratio of consecutive Fibonacci numbers approaches φ:

```
lim(n→∞) F(n+1)/F(n) = φ
```

This relationship is why the time complexity can be expressed as O(φ^n).

### Recurrence Relations

The Fibonacci recurrence F(n) = F(n-1) + F(n-2) is a linear homogeneous recurrence relation with constant coefficients. Its characteristic equation is:

```
x² = x + 1
x² - x - 1 = 0
```

Solving gives roots x = φ and x = ψ (where ψ = (1-√5)/2 ≈ -0.618), which leads to Binet's formula.

## Performance Characteristics

| n | Approximate Function Calls | Time (typical) |
|---|---------------------------|----------------|
| 10 | 177 | < 1ms |
| 20 | 21,891 | ~10ms |
| 30 | 2,692,537 | ~1s |
| 35 | 29,860,703 | ~10s |
| 40 | 331,160,281 | ~2min |
| 45 | 3,672,623,805 | ~20min |

**In our 1-second benchmark, this technique typically calculates F(0) through F(30-35).**

## Implementation Details

### Python-Specific Considerations

1. **Recursion Limit**: Python has a default recursion limit (~1000). While naive recursion won't reach this limit due to time constraints, deeper recursive techniques need to handle this.

2. **Function Call Overhead**: Python's function call overhead makes this even slower compared to compiled languages.

3. **No Tail Call Optimization**: Python doesn't optimize tail recursion, so the full call stack is maintained.

### Edge Cases

- F(0) = 0
- F(1) = 1
- Negative n: Should raise ValueError

## When to Use

**Use this technique for:**
- Educational purposes to understand recursion
- Demonstrating the importance of algorithm optimization
- Very small n (n < 25) where simplicity matters more than speed

**Don't use this technique for:**
- Any practical application requiring n > 30
- Performance-critical code
- Production systems

## References

1. Cormen, T.H., Leiserson, C.E., Rivest, R.L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. Chapter 15: Dynamic Programming.

2. Knuth, D.E. (1997). *The Art of Computer Programming, Volume 1: Fundamental Algorithms* (3rd ed.). Addison-Wesley. Section 1.2.8.

3. Graham, R.L., Knuth, D.E., & Patashnik, O. (1994). *Concrete Mathematics: A Foundation for Computer Science* (2nd ed.). Addison-Wesley. Chapter 6.

## Example

```python
from techniques.01_naive_recursion.fibonacci import NaiveRecursion

technique = NaiveRecursion()
print(technique.calculate(10))  # Output: 55
print(technique.calculate(20))  # Output: 6765

# Timing example
import time
start = time.time()
result = technique.calculate(35)
elapsed = time.time() - start
print(f"F(35) = {result}, took {elapsed:.2f}s")
```
