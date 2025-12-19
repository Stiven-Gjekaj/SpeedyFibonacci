<div align="center">

# 📊 Complexity Analysis

[![Big-O](https://img.shields.io/badge/Topic-Big--O_Notation-blue?style=flat-square)]()
[![Algorithms](https://img.shields.io/badge/Algorithms-12-orange?style=flat-square)]()

*Deep dive into the time and space complexity of each Fibonacci technique*

</div>

---

## 📖 Table of Contents

- [Big-O Notation Primer](#-big-o-notation-primer)
- [Complexity Summary](#-complexity-summary)
- [Detailed Analysis](#-detailed-analysis)
- [Practical Performance](#-practical-performance)
- [Space-Time Tradeoffs](#%EF%B8%8F-space-time-tradeoffs)

---

## 🎓 Big-O Notation Primer

Big-O notation describes the **upper bound** of an algorithm's growth rate:

```mermaid
graph LR
    subgraph Fastest["🟢 Fast"]
        A["O(1)<br/>Constant"]
        B["O(log n)<br/>Logarithmic"]
    end

    subgraph Medium["🟡 Medium"]
        C["O(n)<br/>Linear"]
        D["O(n log n)<br/>Linearithmic"]
    end

    subgraph Slow["🔴 Slow"]
        E["O(n²)<br/>Quadratic"]
        F["O(2ⁿ)<br/>Exponential"]
    end

    A --> B --> C --> D --> E --> F

    style Fastest fill:#27ae60,stroke:#1e8449,color:#fff
    style Medium fill:#f39c12,stroke:#d35400,color:#fff
    style Slow fill:#e74c3c,stroke:#c0392b,color:#fff
```

| Notation | Name | Example | Growth |
|:--------:|------|---------|--------|
| `O(1)` | Constant | Array access | Same time regardless of input |
| `O(log n)` | Logarithmic | Binary search | Time grows slowly as input doubles |
| `O(n)` | Linear | Simple loop | Time grows proportionally |
| `O(n log n)` | Linearithmic | Merge sort | Efficient sorting |
| `O(n²)` | Quadratic | Nested loops | Time grows with square of input |
| `O(2ⁿ)` | Exponential | Naive recursion | Time doubles with each addition |

---

## 📋 Complexity Summary

```mermaid
quadrantChart
    title Time vs Space Complexity
    x-axis Low Space --> High Space
    y-axis Slow Time --> Fast Time

    quadrant-1 Fast & Space-Heavy
    quadrant-2 Fast & Space-Efficient
    quadrant-3 Slow & Space-Efficient
    quadrant-4 Slow & Space-Heavy

    Binet: [0.1, 0.95]
    Iterative: [0.1, 0.7]
    Generator: [0.1, 0.7]
    Numba: [0.1, 0.75]
    Cython: [0.1, 0.75]
    Fast Doubling: [0.3, 0.85]
    Matrix: [0.3, 0.85]
    NumPy: [0.2, 0.85]
    Memoized: [0.6, 0.7]
    DP: [0.6, 0.7]
    Parallel: [0.7, 0.65]
    Naive: [0.4, 0.05]
```

| # | Technique | Time | Space | Operations for F(50) |
|:-:|-----------|:----:|:-----:|:--------------------:|
| 1 | 🐢 Naive Recursion | `O(2ⁿ)` | `O(n)` | ~20 billion |
| 2 | 💾 Memoized Recursion | `O(n)` | `O(n)` | ~50 |
| 3 | 📊 Dynamic Programming | `O(n)` | `O(n)` | ~50 |
| 4 | 🔢 Matrix Exponentiation | `O(log n)` | `O(log n)` | ~18 |
| 5 | 🌟 Binet's Formula | `O(1)*` | `O(1)` | ~5 |
| 6 | 🔄 Generator-based | `O(n)` | `O(1)` | ~50 |
| 7 | 🧊 NumPy Vectorized | `O(log n)` | `O(1)` | ~18 |
| 8 | ⚡ Numba JIT | `O(n)` | `O(1)` | ~50 |
| 9 | 🚀 Cython Optimized | `O(n)` | `O(1)` | ~50 |
| 10 | 💨 Iterative Optimized | `O(n)` | `O(1)` | ~50 |
| 11 | ⚡ Fast Doubling | `O(log n)` | `O(log n)` | ~18 |
| 12 | 🔀 Parallel Processing | `O(n)` | `O(n)` | ~50 |

> [!NOTE]
> *Binet's O(1) assumes bounded precision; true arbitrary precision requires O(n) for the result itself.

---

## 🔍 Detailed Analysis

### 1️⃣ Naive Recursion — O(2ⁿ)

```mermaid
graph TD
    A["F(5)"] --> B["F(4)"]
    A --> C["F(3)"]
    B --> D["F(3)"]
    B --> E["F(2)"]
    C --> F["F(2)"]
    C --> G["F(1)"]
    D --> H["F(2)"]
    D --> I["F(1)"]
    E --> J["F(1)"]
    E --> K["F(0)"]

    style A fill:#e74c3c,stroke:#c0392b,color:#fff
    style B fill:#e74c3c,stroke:#c0392b,color:#fff
    style C fill:#3498db,stroke:#2980b9,color:#fff
    style D fill:#3498db,stroke:#2980b9,color:#fff
```

**The recurrence tree has exponential nodes:**

| n | Function Calls | Approximate |
|---|----------------|-------------|
| 10 | 177 | ~10² |
| 20 | 21,891 | ~10⁴ |
| 30 | 2,692,537 | ~10⁶ |
| 40 | 331,160,281 | ~10⁸ |
| 50 | **~20 billion** | ~10¹⁰ |

> [!WARNING]
> Each call branches into 2 more calls, causing exponential growth!

---

### 2️⃣ Memoized Recursion — O(n)

```mermaid
flowchart LR
    subgraph Cache["💾 Cache"]
        C0["F(0)=0"]
        C1["F(1)=1"]
        C2["F(2)=1"]
        C3["F(3)=2"]
        C4["..."]
    end

    A["F(n)?"] --> B{In cache?}
    B -->|Yes| C["Return cached"]
    B -->|No| D["Compute & store"]
    D --> Cache

    style Cache fill:#27ae60,stroke:#1e8449,color:#fff
```

**With memoization, each F(k) is computed exactly once:**
- n+1 unique subproblems
- O(1) work per subproblem
- **Total: O(n)**

---

### 3️⃣ Dynamic Programming — O(n)

```python
# Single loop from 2 to n
for i in range(2, n+1):
    dp[i] = dp[i-1] + dp[i-2]  # O(1) per iteration
```

| Metric | Value |
|--------|-------|
| Time | n-1 iterations × O(1) = **O(n)** |
| Space | Array of size n+1 = **O(n)** |

---

### 4️⃣ Matrix Exponentiation — O(log n)

```mermaid
flowchart LR
    A["M^n"] --> B{"n even?"}
    B -->|Yes| C["(M^(n/2))²"]
    B -->|No| D["M × M^(n-1)"]
    C --> E["log n steps"]
    D --> E

    style E fill:#27ae60,stroke:#1e8449,color:#fff
```

**Binary exponentiation reduces multiplications:**

| n | Matrix Multiplications |
|---|------------------------|
| 100 | 7 |
| 1,000 | 10 |
| 1,000,000 | 20 |

---

### 5️⃣ Binet's Formula — O(1)*

```
F(n) = (φⁿ - ψⁿ) / √5
```

**Constant number of operations:** exponentiation, subtraction, division.

> [!CAUTION]
> **Caveat:** Floating-point precision limits accuracy. With arbitrary precision, computing φⁿ for n-bit precision takes O(n) time.

---

### 6️⃣-10️⃣ Iterative Methods — O(n)

All iterative methods share the same complexity:

```mermaid
flowchart LR
    A["a=0, b=1"] --> B["Loop n-1 times"]
    B --> C["a, b = b, a+b"]
    C --> D["Return b"]

    style B fill:#f39c12,stroke:#d35400,color:#fff
```

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Generator | O(n) | O(1) | Lazy evaluation |
| Iterative | O(n) | O(1) | Two variables |
| Numba JIT | O(n) | O(1) | LLVM compiled |
| Cython | O(n) | O(1) | C extension |

---

### 1️⃣1️⃣ Fast Doubling — O(log n)

Uses identities to "jump" through the sequence:

```
F(2n)   = F(n) × [2×F(n+1) - F(n)]
F(2n+1) = F(n)² + F(n+1)²
```

| Metric | Value |
|--------|-------|
| Recursion depth | log₂(n) |
| Operations per level | O(1) |
| **Total** | **O(log n)** |

---

### 1️⃣2️⃣ Parallel Processing — O(n)

```mermaid
flowchart TD
    A["Batch: F(n₁), F(n₂), ... F(nₖ)"] --> B["Split across p processes"]
    B --> C1["Process 1"]
    B --> C2["Process 2"]
    B --> C3["Process 3"]
    B --> C4["Process p"]
    C1 --> D["Combine Results"]
    C2 --> D
    C3 --> D
    C4 --> D

    style A fill:#9b59b6,stroke:#8e44ad,color:#fff
    style D fill:#27ae60,stroke:#1e8449,color:#fff
```

| Scenario | Time Complexity |
|----------|-----------------|
| Single F(n) | O(n) — no benefit |
| Batch of k values, p cores | O(max(nᵢ) × k/p) |

---

## 📈 Practical Performance

> [!IMPORTANT]
> Algorithm complexity doesn't tell the whole story. Real performance depends on constant factors, integer size, and interpreter overhead.

### Expected Benchmark Results

| Complexity Class | Typical Count (1s) | Example Techniques |
|------------------|-------------------:|-------------------|
| 🔴 O(2ⁿ) | 30-35 | Naive Recursion |
| 🟡 O(n) interpreted | 10,000-50,000 | DP, Generator |
| 🟢 O(n) compiled | 100,000-1,000,000 | Numba, Cython |
| 🔵 O(log n) | Varies | Matrix, Fast Doubling |
| ⭐ O(1) | Millions | Binet (fixed precision) |

### Why O(log n) Isn't Always Fastest

For our **sequential benchmark** (F(0), F(1), F(2), ...):

```mermaid
flowchart LR
    subgraph Linear["O(n) Methods"]
        A["Each F(k) = O(1) extra work"]
        B["Total: O(n)"]
    end

    subgraph Logarithmic["O(log n) Methods"]
        C["Each F(k) computed independently"]
        D["Total: O(n log n)"]
    end

    A --> B
    C --> D

    style Linear fill:#27ae60,stroke:#1e8449,color:#fff
    style Logarithmic fill:#f39c12,stroke:#d35400,color:#fff
```

> [!TIP]
> O(log n) excels when computing **single large** F(n) values, not sequential computation!

---

## ⚖️ Space-Time Tradeoffs

```mermaid
graph TD
    subgraph Tradeoffs["Space-Time Tradeoffs"]
        A["Need all F(0)...F(n)?"] -->|Yes| B["DP Array<br/>O(n) space"]
        A -->|No| C["Need random access?"]
        C -->|Yes| D["Memoization<br/>O(n) space"]
        C -->|No| E["Single large F(n)?"]
        E -->|Yes| F["Matrix/Fast Doubling<br/>O(log n)"]
        E -->|No| G["Iterative<br/>O(1) space"]
    end

    style B fill:#3498db,stroke:#2980b9,color:#fff
    style D fill:#9b59b6,stroke:#8e44ad,color:#fff
    style F fill:#27ae60,stroke:#1e8449,color:#fff
    style G fill:#f39c12,stroke:#d35400,color:#fff
```

| Use Case | Best Method | Time | Space |
|----------|-------------|------|-------|
| All F(0)...F(n) | DP Array | O(n) | O(n) |
| Single F(n), memory limited | Iterative | O(n) | O(1) |
| Random access to F(k) | Memoized | O(n) | O(n) |
| Single large F(n) | Matrix/Fast Doubling | O(log n) | O(log n) |

---

## 🔢 Integer Arithmetic Complexity

> [!NOTE]
> For very large Fibonacci numbers, arithmetic on big integers becomes significant.

| Operation | Naive | Karatsuba | FFT |
|-----------|:-----:|:---------:|:---:|
| Multiplication | O(d²) | O(d^1.58) | O(d log d) |
| Addition | O(d) | O(d) | O(d) |

Where **d = number of digits ≈ 0.21n** for F(n).

**Example:** For n = 1,000,000, F(n) has ~210,000 digits. Big integer multiplication becomes the bottleneck!

---

## 📚 References

1. **Cormen, T.H., et al.** (2009). *Introduction to Algorithms*. Chapter 3: Growth of Functions.
2. **Sedgewick, R., & Wayne, K.** (2011). *Algorithms*. Chapter 1.4: Analysis of Algorithms.
3. **Knuth, D.E.** (1997). *The Art of Computer Programming, Vol. 2*. Chapter 4.3.3: Big Numbers.

---

<div align="center">

[← Back to Main README](../README.md)

</div>
