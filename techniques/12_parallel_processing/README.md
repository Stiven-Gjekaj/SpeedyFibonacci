# Parallel Processing

## Overview

This technique demonstrates parallel computation using Python's multiprocessing module. While Fibonacci's inherently sequential nature limits parallelization benefits for single computations, parallel processing excels at computing multiple independent Fibonacci numbers simultaneously.

## Algorithm Description

The core algorithm is the standard iterative approach, but executed across multiple processes:

```python
from concurrent.futures import ProcessPoolExecutor

def fib_single(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def fib_batch_parallel(indices):
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(fib_single, indices))
    return results
```

### Amdahl's Law

Amdahl's Law describes the theoretical speedup from parallelization:

```
Speedup = 1 / (S + P/N)
```

Where:
- S = Serial (non-parallelizable) fraction
- P = Parallelizable fraction (P = 1 - S)
- N = Number of processors

For computing a single F(n), almost everything is serial (S ≈ 1), so parallelization doesn't help.

For computing F(n₁), F(n₂), ..., F(nₖ) independently, P ≈ 1, so we get near-linear speedup!

## Complexity Analysis

### Single Computation

- **Time**: O(n) - same as iterative
- **Space**: O(1) auxiliary

### Batch Computation (k numbers, p processes)

- **Time**: O(max(n₁...nₖ) × k/p) - work divided among processes
- **Space**: O(k) for results + process overhead

### Speedup Characteristics

| Scenario | Speedup |
|----------|---------|
| Single F(n) | ~1x (no benefit) |
| k independent F(nᵢ), p cores | Up to px |
| F(0) to F(n) sequentially | ~1x (dependencies) |

## Performance Characteristics

### Single Value (No Parallelization Benefit)

| n | Sequential | Parallel Overhead |
|---|------------|-------------------|
| 100 | < 1ms | Process startup: ~50ms |
| 1,000 | ~1ms | Not worth it |
| 10,000 | ~10ms | Maybe worth it |

### Batch Computation (4 cores)

| Batch Size | Sequential | 4-Process Parallel | Speedup |
|------------|------------|-------------------|---------|
| 100 × F(1000) | ~100ms | ~30ms | ~3.3x |
| 1000 × F(1000) | ~1s | ~300ms | ~3.3x |
| 10000 × F(100) | ~500ms | ~150ms | ~3.3x |

**In our 1-second benchmark**: Parallel processing has significant overhead, so it's typically slower than simple iteration for sequential F(0), F(1), F(2), ... computation.

## Python Parallel Processing

### The GIL Problem

Python's Global Interpreter Lock (GIL) prevents true parallel execution of Python bytecode in threads. Solutions:

1. **Multiprocessing**: Separate processes, each with own GIL
2. **C Extensions**: Release GIL during computation
3. **Numba/Cython**: Compiled code can release GIL

### ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor

# Simple parallel map
with ProcessPoolExecutor(max_workers=4) as executor:
    results = executor.map(fib_single, range(100))

# Submit individual tasks
with ProcessPoolExecutor() as executor:
    futures = [executor.submit(fib_single, n) for n in range(100)]
    results = [f.result() for f in futures]
```

### ThreadPoolExecutor (for I/O)

```python
from concurrent.futures import ThreadPoolExecutor

# Useful for I/O-bound tasks, not CPU-bound like Fibonacci
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fib_single, range(100)))
```

### multiprocessing.Pool

```python
from multiprocessing import Pool

with Pool(processes=4) as pool:
    results = pool.map(fib_single, range(100))
```

## Implementation Considerations

### Pickling Functions

For multiprocessing, functions must be picklable (defined at module level):

```python
# Works - module-level function
def fib_single(n):
    ...

# Doesn't work - local function
def compute_batch():
    def fib_local(n):  # Can't pickle!
        ...
    with ProcessPoolExecutor() as ex:
        ex.map(fib_local, range(10))  # Error!
```

### Process Startup Overhead

Each process has startup cost (~50-100ms). For small tasks, this overhead dominates:

```python
# Bad: many small tasks
results = [executor.submit(fib, n) for n in range(1000)]

# Better: batch into chunks
def fib_chunk(chunk):
    return [fib(n) for n in chunk]

chunks = [range(i, i+100) for i in range(0, 1000, 100)]
results = executor.map(fib_chunk, chunks)
```

### Memory Sharing

Processes don't share memory. For large inputs/outputs:
- Use `multiprocessing.shared_memory`
- Use memory-mapped files
- Minimize data transfer

## When to Use

**Use parallel processing when:**
- Computing many independent Fibonacci numbers
- Tasks are CPU-intensive enough to justify overhead
- You have multiple CPU cores
- Teaching parallel computing concepts

**Don't use when:**
- Computing single Fibonacci numbers
- Computing sequential F(0)...F(n)
- Startup overhead exceeds computation time
- Memory is very limited

## Alternative Parallel Approaches

### NumPy (Implicit SIMD)

```python
import numpy as np

# NumPy can parallelize operations internally
def fib_numpy_batch(max_n):
    fib = np.zeros(max_n + 1, dtype=object)
    fib[1] = 1
    for i in range(2, max_n + 1):
        fib[i] = fib[i-1] + fib[i-2]
    return fib
```

### Numba Parallel

```python
from numba import jit, prange

@jit(nopython=True, parallel=True)
def fib_parallel(n_values):
    results = np.zeros(len(n_values), dtype=np.int64)
    for i in prange(len(n_values)):
        results[i] = fib_single(n_values[i])
    return results
```

### Dask (Large-Scale)

```python
import dask.array as da

# For truly massive parallel computation
# (overkill for Fibonacci)
```

## Educational Value

This technique teaches:

1. **Amdahl's Law**: Limits of parallelization
2. **Python GIL**: Why threads don't always help
3. **Process vs Thread**: When to use each
4. **Overhead Analysis**: When parallel isn't faster
5. **Batch Processing**: Effective parallelization patterns

## References

1. Python Documentation. "multiprocessing — Process-based parallelism". https://docs.python.org/3/library/multiprocessing.html

2. Python Documentation. "concurrent.futures — Launching parallel tasks". https://docs.python.org/3/library/concurrent.futures.html

3. Amdahl, G.M. (1967). "Validity of the single processor approach to achieving large scale computing capabilities". *AFIPS Conference Proceedings*.

4. Beazley, D. (2010). "Understanding the Python GIL". PyCon 2010. https://www.dabeaz.com/GIL/

## Example

```python
from techniques.12_parallel_processing.fibonacci import ParallelProcessing
import time

technique = ParallelProcessing(max_workers=4)

# Single value (uses iterative, no parallelization)
print(technique.calculate(100))  # 354224848179261915075

# Batch parallel - this is where it shines!
indices = list(range(0, 1000))

# Sequential baseline
start = time.perf_counter()
sequential_results = [technique.calculate(n) for n in indices]
seq_time = time.perf_counter() - start
print(f"Sequential: {seq_time:.3f}s")

# Parallel
start = time.perf_counter()
parallel_results = technique.calculate_batch_parallel(indices)
par_time = time.perf_counter() - start
print(f"Parallel:   {par_time:.3f}s")

print(f"Speedup: {seq_time/par_time:.2f}x")

# Verify results match
assert sequential_results == parallel_results
```
