# Binet's Formula

## Overview

Binet's formula provides a closed-form expression for computing Fibonacci numbers directly using the golden ratio, without iteration or recursion. This elegant mathematical formula demonstrates the deep connection between the Fibonacci sequence and the golden ratio.

## Algorithm Description

Binet's formula states:

```
        φⁿ - ψⁿ
F(n) = ─────────
          √5
```

Where:
- φ (phi) = (1 + √5) / 2 ≈ 1.6180339887... (golden ratio)
- ψ (psi) = (1 - √5) / 2 ≈ -0.6180339887... (conjugate of phi)
- √5 ≈ 2.2360679775...

### Simplified Form

Since |ψ| < 1, the term ψⁿ becomes negligible for large n:

```
F(n) ≈ φⁿ / √5  (rounded to nearest integer)
```

This gives an even simpler approximation!

### Implementation

```python
from decimal import Decimal, getcontext
getcontext().prec = 100  # High precision

sqrt5 = Decimal(5).sqrt()
phi = (1 + sqrt5) / 2
psi = (1 - sqrt5) / 2

def fibonacci(n):
    if n <= 1:
        return n
    result = (phi**n - psi**n) / sqrt5
    return int(result.to_integral_value())
```

## Complexity Analysis

### Time Complexity: O(1)*

Theoretically O(1) - a direct calculation with no loops or recursion.

*Caveat: Exponentiation of large numbers and high-precision arithmetic have their own complexity. For k-bit precision and exponent n:
- Naive exponentiation: O(n × M(k)) where M(k) is multiplication cost
- Binary exponentiation: O(log n × M(k))

For practical purposes with bounded precision, it's effectively O(1).

### Space Complexity: O(1)

Only stores a constant number of values regardless of n.

## Mathematical Background

### Proof of Binet's Formula

The Fibonacci recurrence F(n) = F(n-1) + F(n-2) is a linear homogeneous recurrence relation with constant coefficients.

**Step 1**: Write the characteristic equation
```
x² = x + 1
x² - x - 1 = 0
```

**Step 2**: Solve using quadratic formula
```
x = (1 ± √5) / 2
```
This gives φ = (1+√5)/2 and ψ = (1-√5)/2.

**Step 3**: General solution form
```
F(n) = Aφⁿ + Bψⁿ
```

**Step 4**: Use initial conditions F(0)=0, F(1)=1
```
F(0) = A + B = 0         → B = -A
F(1) = Aφ + Bψ = 1       → A(φ - ψ) = 1
                         → A = 1/√5, B = -1/√5
```

**Step 5**: Final formula
```
F(n) = (φⁿ - ψⁿ) / √5
```

### The Golden Ratio

The golden ratio φ appears throughout nature, art, and mathematics:
- Ratio of consecutive Fibonacci numbers approaches φ
- φ² = φ + 1
- 1/φ = φ - 1
- φ = 1 + 1/(1 + 1/(1 + 1/...)) (continued fraction)

### Why ψⁿ Vanishes

Since |ψ| = |(1-√5)/2| ≈ 0.618 < 1:
- ψ¹ ≈ -0.618
- ψ⁵ ≈ -0.090
- ψ¹⁰ ≈ 0.008
- ψ²⁰ ≈ 0.00007

For practical computation, F(n) ≈ round(φⁿ/√5) works for all n.

## Performance Characteristics

| n | Precision Needed | Float64 Accurate? |
|---|-----------------|-------------------|
| 10 | Low | Yes |
| 50 | Medium | Yes |
| 70 | High | Borderline |
| 100 | Very High | No (use Decimal) |
| 1000 | Extreme | Decimal with high prec |

**In our 1-second benchmark**: Binet's formula is extremely fast due to O(1) nature, but precision concerns mean we use Decimal arithmetic which adds overhead.

## Implementation Details

### Floating Point Version (Fast but Limited)

```python
import math

PHI = (1 + math.sqrt(5)) / 2
SQRT5 = math.sqrt(5)

def fib_float(n):
    return round(PHI**n / SQRT5)
```

This works for n ≤ 70 approximately.

### Decimal Version (Accurate)

```python
from decimal import Decimal, getcontext
getcontext().prec = 500  # Adjust as needed

sqrt5 = Decimal(5).sqrt()
phi = (Decimal(1) + sqrt5) / 2

def fib_decimal(n):
    result = phi**n / sqrt5
    return int(result.to_integral_value())
```

### Precision Requirements

To accurately compute F(n), you need roughly:
- log₁₀(F(n)) ≈ n × log₁₀(φ) ≈ 0.209n decimal digits
- F(100) has ~21 digits
- F(1000) has ~209 digits
- F(10000) has ~2090 digits

Set `getcontext().prec` accordingly.

## When to Use

**Use this technique when:**
- Computing a single Fibonacci number
- Demonstrating mathematical elegance
- Teaching the golden ratio connection
- Need O(1) complexity (with fixed precision)

**Don't use when:**
- Computing many sequential Fibonacci numbers
- Extremely large n (matrix or fast doubling better)
- Exact precision is critical without careful setup

## Historical Note

Although called "Binet's Formula," it was known to:
- Abraham de Moivre (1718)
- Daniel Bernoulli (1728)
- Leonhard Euler (1765)
- Jacques Philippe Marie Binet (1843) - published explicit form

## References

1. Binet, J.P.M. (1843). "Mémoire sur l'intégration des équations linéaires aux différences finies, d'un ordre quelconque, à coefficients variables". *Comptes Rendus de l'Académie des Sciences*, Paris.

2. Koshy, T. (2001). *Fibonacci and Lucas Numbers with Applications*. Wiley-Interscience.

3. Vorobiev, N.N. (2002). *Fibonacci Numbers*. Birkhäuser.

4. Dunlap, R.A. (1997). *The Golden Ratio and Fibonacci Numbers*. World Scientific.

## Example

```python
from techniques.05_binets_formula.fibonacci import BinetsFormula

technique = BinetsFormula()

# Fast direct calculation
print(technique.calculate(10))   # 55
print(technique.calculate(50))   # 12586269025
print(technique.calculate(100))  # 354224848179261915075

# Verify the golden ratio approximation
phi = 1.6180339887498949
sqrt5 = 2.23606797749979
print(f"F(10) ≈ {round(phi**10 / sqrt5)}")  # 55
```
