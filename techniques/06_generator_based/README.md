# Generator-based

## Overview

The generator-based approach uses Python's generator pattern to produce Fibonacci numbers lazily. This is a memory-efficient, Pythonic way to work with sequences that demonstrates Python's powerful iteration protocol.

## Algorithm Description

A generator function uses `yield` instead of `return`, producing values one at a time and maintaining state between calls.

```python
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

To get F(n), we advance the generator n times:

```python
def fibonacci(n):
    gen = fibonacci_generator()
    for _ in range(n):
        next(gen)
    return next(gen)
```

### Pseudocode

```
GENERATOR fibonacci_sequence():
    a = 0
    b = 1
    LOOP FOREVER:
        YIELD a
        temp = a + b
        a = b
        b = temp

FUNCTION fibonacci(n):
    gen = fibonacci_sequence()
    FOR i FROM 0 TO n-1:
        ADVANCE gen
    RETURN NEXT VALUE FROM gen
```

## Complexity Analysis

### Time Complexity: O(n)

- Must iterate through n+1 values to reach F(n)
- Each iteration: O(1) addition and variable swap
- No way to "skip ahead" with basic generator

### Space Complexity: O(1)

- Generator stores only two variables (a, b)
- No array, no recursion stack
- Memory usage constant regardless of n

This is the same space efficiency as the iterative space-optimized version, packaged in generator form.

## Python Generator Mechanics

### How Generators Work

```python
def gen():
    print("Before first yield")
    yield 1
    print("Before second yield")
    yield 2

g = gen()
print(next(g))  # Prints "Before first yield", returns 1
print(next(g))  # Prints "Before second yield", returns 2
```

Generators:
1. Return an iterator object when called
2. Execute code until `yield`
3. Suspend, saving state
4. Resume from suspension on `next()`
5. Raise `StopIteration` when exhausted

### Generator Expressions

```python
# Generator expression for Fibonacci-like pattern
# (Not actually Fibonacci, just example syntax)
squares = (x**2 for x in range(10))
```

## Performance Characteristics

| n | Time (approx) | Memory |
|---|--------------|--------|
| 100 | < 1ms | O(1) |
| 1,000 | < 1ms | O(1) |
| 10,000 | ~5ms | O(1) |
| 100,000 | ~50ms | O(1) |

**In our 1-second benchmark**: Similar to iterative methods, but with slight generator overhead.

## Implementation Details

### Efficient Usage Patterns

**Getting F(n):**
```python
gen = fibonacci_generator()
for _ in range(n):
    next(gen)
result = next(gen)
```

**First N Fibonacci numbers:**
```python
from itertools import islice

gen = fibonacci_generator()
first_10 = list(islice(gen, 10))
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

**Fibonacci numbers below limit:**
```python
from itertools import takewhile

gen = fibonacci_generator()
below_100 = list(takewhile(lambda x: x < 100, gen))
# [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```

**Sum of first N:**
```python
from itertools import islice

total = sum(islice(fibonacci_generator(), 10))
```

### Generator vs Iterator Class

Generator function:
```python
def fib_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b
```

Equivalent iterator class:
```python
class FibIterator:
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result
```

The generator is more concise!

### Memory Advantage

Compare memory usage:

| Method | Memory for F(1000000) |
|--------|----------------------|
| DP Array | ~20 MB (array of big ints) |
| Generator | ~1 KB (two integers) |

## When to Use

**Use this technique when:**
- Streaming Fibonacci numbers
- Memory is constrained
- Working with itertools and functional patterns
- Need first N Fibonacci numbers
- Teaching Python generators

**Don't use when:**
- Need random access to F(n)
- Need single large F(n) quickly (use O(log n) methods)
- Reusing computed values (no caching)

## Pythonic Patterns

### With enumerate
```python
for i, fib in enumerate(islice(fibonacci_generator(), 10)):
    print(f"F({i}) = {fib}")
```

### With zip
```python
gen = fibonacci_generator()
pairs = list(zip(islice(gen, 10), islice(gen, 10)))
# Creates pairs of consecutive Fibonacci numbers
```

### As context manager
```python
# Generators can be used in various contexts
with open('fibs.txt', 'w') as f:
    for fib in islice(fibonacci_generator(), 100):
        f.write(f"{fib}\n")
```

## References

1. Python Documentation. "Generators". https://docs.python.org/3/tutorial/classes.html#generators

2. Beazley, D. (2009). *Python Essential Reference* (4th ed.). Addison-Wesley. Chapter 6.

3. Ramalho, L. (2015). *Fluent Python*. O'Reilly. Chapter 14: Iterables, Iterators, and Generators.

4. PEP 255 -- Simple Generators. https://peps.python.org/pep-0255/

## Example

```python
from techniques.06_generator_based.fibonacci import GeneratorBased
from itertools import islice

technique = GeneratorBased()

# Single value
print(technique.calculate(10))   # 55
print(technique.calculate(100))  # 354224848179261915075

# Using the generator directly
gen = technique.get_generator()
first_ten = [next(gen) for _ in range(10)]
print(first_ten)  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# Memory-efficient: iterate without storing
gen = technique.get_generator()
count = sum(1 for f in islice(gen, 1000) if f % 2 == 0)
print(f"Even Fibonacci numbers in first 1000: {count}")
```
