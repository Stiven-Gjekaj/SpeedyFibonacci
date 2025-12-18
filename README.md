# SpeedyFibonacci

**An Educational Benchmark Suite for Fibonacci Calculation Techniques in Python**

Compare 12 different algorithms for computing Fibonacci numbers, measuring how many each can calculate in one second. This project demonstrates algorithmic complexity, optimization techniques, and Python performance engineering.

## Quick Start

```bash
# Clone or navigate to the project
cd SpeedyFibonacci

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the benchmark
python scripts/run_benchmark.py
```

## What This Project Does

Each technique runs for **exactly 1 second**, computing Fibonacci numbers F(0), F(1), F(2), ... until time runs out. The benchmark measures:

- **Count**: Total Fibonacci numbers calculated
- **Max N**: Highest index reached (e.g., F(50000))
- **Correctness**: Results validated against known values

This reveals the dramatic difference between O(2^n), O(n), and O(log n) algorithms!

## Implemented Techniques

| # | Technique | Time | Space | Description |
|---|-----------|------|-------|-------------|
| 1 | Naive Recursion | O(2^n) | O(n) | Classic recursive - slow but educational |
| 2 | Memoized Recursion | O(n) | O(n) | Top-down DP with caching |
| 3 | Dynamic Programming | O(n) | O(n) | Bottom-up iterative with array |
| 4 | Matrix Exponentiation | O(log n) | O(log n) | [[1,1],[1,0]]^n identity |
| 5 | Binet's Formula | O(1)* | O(1) | Closed-form with golden ratio |
| 6 | Generator-based | O(n) | O(1) | Python generator pattern |
| 7 | NumPy Vectorized | O(log n) | O(1) | NumPy matrix operations |
| 8 | Numba JIT | O(n) | O(1) | LLVM-compiled Python |
| 9 | Cython Optimized | O(n) | O(1) | C-extension compilation |
| 10 | Iterative Space-Optimized | O(n) | O(1) | Two-variable iteration |
| 11 | Fast Doubling | O(log n) | O(log n) | F(2n) identity method |
| 12 | Parallel Processing | O(n) | O(n) | Multiprocessing demo |

*Binet's formula is O(1) theoretically but precision-limited for large n.

## Sample Output

```
╔═══════════════════════════════════════════════════════════════╗
║   SpeedyFibonacci Benchmark Results                           ║
╚═══════════════════════════════════════════════════════════════╝

┌──────┬─────────────────────────────┬───────────────────┬─────────┐
│ Rank │ Technique                   │ Numbers Calculated│ Max N   │
├──────┼─────────────────────────────┼───────────────────┼─────────┤
│ 1    │ Numba JIT                   │ 847,293           │ 847,292 │
│ 2    │ Iterative Space-Optimized   │ 623,481           │ 623,480 │
│ 3    │ Generator-based             │ 589,234           │ 589,233 │
│ ...  │ ...                         │ ...               │ ...     │
│ 12   │ Naive Recursion             │ 35                │ 34      │
└──────┴─────────────────────────────┴───────────────────┴─────────┘

Fastest: Numba JIT (847,293 numbers)
Highest N: Fast Doubling (reached n=1,234,567)
```

## Project Structure

```
SpeedyFibonacci/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore patterns
│
├── techniques/              # 12 Fibonacci implementations
│   ├── 01_naive_recursion/
│   │   ├── fibonacci.py     # Implementation
│   │   └── README.md        # Algorithm documentation
│   ├── 02_memoized_recursion/
│   ├── ... (10 more)
│   └── 12_parallel_processing/
│
├── benchmarking/            # Benchmark infrastructure
│   ├── benchmark_runner.py  # Main orchestrator
│   ├── technique_loader.py  # Dynamic discovery
│   └── timer.py             # Precision timing
│
├── output/                  # Result presentation
│   ├── console_formatter.py # Terminal tables
│   ├── csv_exporter.py      # CSV export
│   └── visualizer.py        # Matplotlib plots
│
├── scripts/                 # Entry points
│   ├── run_benchmark.py     # Main benchmark runner
│   ├── setup_cython.py      # Cython compilation
│   └── clean.py             # Cleanup utility
│
├── results/                 # Generated output
├── tests/                   # Unit tests
└── docs/                    # Additional documentation
```

## Usage

### Run All Benchmarks

```bash
python scripts/run_benchmark.py
```

### Options

```bash
# Run for 5 seconds per technique
python scripts/run_benchmark.py --duration 5

# Skip visualizations (faster)
python scripts/run_benchmark.py --no-plots

# Run specific technique(s)
python scripts/run_benchmark.py --technique "Naive Recursion"

# List all available techniques
python scripts/run_benchmark.py --list

# Minimal output
python scripts/run_benchmark.py --quiet
```

### Compile Cython (Optional)

For maximum Cython performance:

```bash
python scripts/setup_cython.py build_ext --inplace
```

## Output

The benchmark generates:

1. **Console Table**: Colored, ranked comparison
2. **CSV Files**: `results/benchmark_results_*.csv`
3. **Visualizations**: `results/*_comparison.png`

## Educational Value

This project teaches:

- **Algorithm Complexity**: See O(2^n) vs O(n) vs O(log n) in action
- **Dynamic Programming**: Top-down (memoization) vs bottom-up (tabulation)
- **Python Optimization**: NumPy, Numba, Cython techniques
- **Mathematical Connections**: Golden ratio, matrix identities
- **Benchmarking Methodology**: Fair comparison, timing precision
- **Software Design**: Abstract interfaces, modular architecture

## Requirements

- Python 3.11 or higher
- Dependencies in `requirements.txt`:
  - numpy
  - numba
  - Cython
  - matplotlib
  - tabulate
  - pandas
  - rich

## Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v
```

## Academic References

Each technique README includes citations. Key references:

1. Cormen, T.H., et al. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
2. Knuth, D.E. (1997). *The Art of Computer Programming, Vol. 1*. Addison-Wesley.
3. Nayuki. "Fast Fibonacci algorithms". https://www.nayuki.io/page/fast-fibonacci-algorithms

See [docs/CITATIONS.md](docs/CITATIONS.md) for complete bibliography.

## Contributing

1. Add new technique in `techniques/XX_name/`
2. Inherit from `FibonacciTechnique`
3. Write README with complexity analysis
4. Add tests in `tests/`

## License

MIT License - Free for educational and commercial use.

## Acknowledgments

- The algorithms implemented here represent decades of mathematical and computer science research
- Thanks to the Python scientific computing ecosystem (NumPy, Numba, Cython)
- Inspired by the elegance of the Fibonacci sequence and its deep connections to mathematics
