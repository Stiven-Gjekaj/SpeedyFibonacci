# Fibonacci Theory and Mathematics

## The Fibonacci Sequence

The Fibonacci sequence is defined by the recurrence relation:

```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2)  for n > 1
```

The first terms are: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, ...

## Historical Background

The sequence is named after **Leonardo of Pisa** (c. 1170–1250), known as Fibonacci, who introduced it to Western mathematics in his 1202 book *Liber Abaci*. He used it to model rabbit population growth.

However, the sequence was known much earlier:
- Indian mathematicians Pingala (200 BC) and Hemachandra (1150 AD) described it in the context of Sanskrit prosody
- The sequence appears in nature: sunflower spirals, pinecone scales, nautilus shells

## The Golden Ratio (φ)

The golden ratio is defined as:

```
φ = (1 + √5) / 2 ≈ 1.6180339887...
```

Its conjugate is:

```
ψ = (1 - √5) / 2 ≈ -0.6180339887...
```

### Key Properties

1. **φ² = φ + 1** (the golden ratio satisfies x² - x - 1 = 0)
2. **1/φ = φ - 1** (reciprocal relationship)
3. **φ + ψ = 1** and **φ × ψ = -1**
4. **Continued fraction**: φ = 1 + 1/(1 + 1/(1 + 1/...))

### Fibonacci-Golden Ratio Connection

```
lim(n→∞) F(n+1)/F(n) = φ
```

The ratio of consecutive Fibonacci numbers approaches the golden ratio!

| n | F(n) | F(n+1) | F(n+1)/F(n) |
|---|------|--------|-------------|
| 1 | 1 | 1 | 1.000 |
| 2 | 1 | 2 | 2.000 |
| 3 | 2 | 3 | 1.500 |
| 5 | 5 | 8 | 1.600 |
| 10 | 55 | 89 | 1.618... |
| 20 | 6765 | 10946 | 1.6180339... |

## Binet's Formula

Named after Jacques Philippe Marie Binet (published 1843), though known earlier:

```
F(n) = (φⁿ - ψⁿ) / √5
```

### Proof Sketch

The Fibonacci recurrence F(n) = F(n-1) + F(n-2) is a linear homogeneous recurrence.

**Step 1**: Find characteristic equation
```
x² = x + 1
x² - x - 1 = 0
```

**Step 2**: Solve for roots
```
x = (1 ± √5) / 2
φ = (1 + √5) / 2
ψ = (1 - √5) / 2
```

**Step 3**: General solution form
```
F(n) = Aφⁿ + Bψⁿ
```

**Step 4**: Apply initial conditions
```
F(0) = A + B = 0          → B = -A
F(1) = Aφ + Bψ = 1        → A(φ - ψ) = 1
                           → A = 1/√5
                           → B = -1/√5
```

**Step 5**: Final formula
```
F(n) = (φⁿ - ψⁿ) / √5
```

### Simplified Approximation

Since |ψ| < 1, we have |ψⁿ| → 0 as n → ∞:

```
F(n) ≈ φⁿ / √5  (rounded to nearest integer)
```

This gives an O(1) calculation (with precision caveats).

## Matrix Representation

The Fibonacci recurrence can be expressed as matrix multiplication:

```
| F(n+1) |   | 1  1 | | F(n)   |
|        | = |      | |        |
| F(n)   |   | 1  0 | | F(n-1) |
```

Therefore:

```
| F(n+1)  F(n)   |   | 1  1 |ⁿ
|                | = |      |
| F(n)    F(n-1) |   | 1  0 |
```

This enables O(log n) computation via matrix exponentiation!

### Proof

By induction:

**Base case (n=1)**:
```
| 1  1 |¹  | 1  1 |   | F(2)  F(1) |
|      | = |      | = |            |
| 1  0 |   | 1  0 |   | F(1)  F(0) |
```
✓ Check: F(2)=1, F(1)=1, F(0)=0

**Inductive step**: If true for n, show for n+1:
```
| 1  1 |ⁿ⁺¹   | 1  1 |ⁿ | 1  1 |
|      |    = |      |  |      |
| 1  0 |      | 1  0 |  | 1  0 |

            | F(n+1)  F(n)   | | 1  1 |
          = |                | |      |
            | F(n)    F(n-1) | | 1  0 |

            | F(n+1)+F(n)   F(n+1) |
          = |                      |
            | F(n)+F(n-1)   F(n)   |

            | F(n+2)  F(n+1) |
          = |                |  ✓
            | F(n+1)  F(n)   |
```

## Fast Doubling Identities

These identities allow computing F(2n) from F(n):

```
F(2n)   = F(n) × [2×F(n+1) - F(n)]
F(2n+1) = F(n)² + F(n+1)²
```

### Derivation from Matrix Identity

From the matrix representation, squaring gives:

```
| 1  1 |²ⁿ   | 1  1 |ⁿ   | 1  1 |ⁿ
|      |   = |      |  × |      |
| 1  0 |     | 1  0 |    | 1  0 |
```

Multiplying out the right side and comparing elements yields the identities.

### Additional Identities

```
F(n+m) = F(n)×F(m-1) + F(n+1)×F(m)
F(n-m) = (-1)^m × [F(n)×F(m+1) - F(n+1)×F(m)]
F(2n-1) = F(n)² + F(n-1)²

gcd(F(m), F(n)) = F(gcd(m, n))
```

## Generating Functions

The ordinary generating function for Fibonacci numbers:

```
G(x) = Σ(n=0 to ∞) F(n)×xⁿ = x / (1 - x - x²)
```

### Proof

```
G(x) = F(0) + F(1)x + F(2)x² + F(3)x³ + ...
     = 0 + x + x² + 2x³ + 3x⁴ + 5x⁵ + ...

xG(x) = x² + x³ + 2x⁴ + 3x⁵ + ...
x²G(x) = x³ + x⁴ + 2x⁵ + ...

G(x) - xG(x) - x²G(x) = x
G(x)(1 - x - x²) = x
G(x) = x / (1 - x - x²)
```

## Growth Rate

Fibonacci numbers grow exponentially:

```
F(n) ~ φⁿ / √5

log₁₀(F(n)) ≈ n × log₁₀(φ) ≈ 0.209n
```

So F(n) has approximately **0.209n decimal digits**.

| n | F(n) | Digits |
|---|------|--------|
| 10 | 55 | 2 |
| 100 | 354224848179261915075 | 21 |
| 1000 | (209 digits) | 209 |
| 10000 | (2090 digits) | 2090 |

## Fibonacci in Nature

- **Phyllotaxis**: Leaf arrangements often follow Fibonacci patterns
- **Flower petals**: Lilies (3), buttercups (5), delphiniums (8), marigolds (13)
- **Spiral patterns**: Sunflower seeds, pinecones, nautilus shells
- **Branching**: Tree branch patterns often approximate Fibonacci ratios

## Applications

1. **Computer Science**: Data structures, hash functions, algorithm analysis
2. **Financial Markets**: Fibonacci retracement levels in technical analysis
3. **Music**: Bartók and Debussy used Fibonacci in compositions
4. **Architecture**: Proportions in classical and modern buildings
5. **Biology**: Population models, DNA sequences

## References

1. Koshy, T. (2001). *Fibonacci and Lucas Numbers with Applications*. Wiley.
2. Vorobiev, N.N. (2002). *Fibonacci Numbers*. Birkhäuser.
3. Dunlap, R.A. (1997). *The Golden Ratio and Fibonacci Numbers*. World Scientific.
4. Knuth, D.E. (1997). *The Art of Computer Programming, Vol. 1*. Section 1.2.8.
5. Graham, R.L., Knuth, D.E., & Patashnik, O. (1994). *Concrete Mathematics*. Chapter 6.
