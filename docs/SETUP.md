# Setup Guide

Detailed instructions for setting up SpeedyFibonacci on different platforms.

## Requirements

- **Python**: 3.11 or higher
- **Operating Systems**: Linux, macOS, Windows
- **Optional**: C compiler for Cython (gcc, clang, or MSVC)

## Quick Setup

```bash
# 1. Navigate to project directory
cd SpeedyFibonacci

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run benchmark
python scripts/run_benchmark.py
```

## Detailed Setup by Platform

### Linux (Ubuntu/Debian)

```bash
# Install Python 3.11+ if needed
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Install C compiler for Cython (optional)
sudo apt install build-essential

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Compile Cython (optional, for maximum performance)
pip install Cython
python scripts/setup_cython.py build_ext --inplace
```

### macOS

```bash
# Install Python via Homebrew (if needed)
brew install python@3.11

# Xcode command line tools (for Cython)
xcode-select --install

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Compile Cython (optional)
python scripts/setup_cython.py build_ext --inplace
```

### Windows

```powershell
# Using Python from python.org
# Download and install Python 3.11+ from https://www.python.org/downloads/

# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1
# OR (Command Prompt)
venv\Scripts\activate.bat

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# For Cython: Install Visual Studio Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Select "C++ build tools" workload

# Compile Cython (optional)
python scripts/setup_cython.py build_ext --inplace
```

## Virtual Environment Management

### Activation Commands

| Platform | Command |
|----------|---------|
| Linux/macOS | `source venv/bin/activate` |
| Windows (PowerShell) | `.\venv\Scripts\Activate.ps1` |
| Windows (cmd) | `venv\Scripts\activate.bat` |
| Windows (Git Bash) | `source venv/Scripts/activate` |

### Deactivation

```bash
deactivate
```

### Removing Environment

```bash
# Deactivate first
deactivate

# Remove venv directory
rm -rf venv        # Linux/macOS
rmdir /s /q venv   # Windows
```

## Dependency Details

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| numpy | ≥1.24.0 | NumPy vectorized technique |
| numba | ≥0.57.0 | JIT compilation |
| Cython | ≥3.0.0 | C extension compilation |
| matplotlib | ≥3.7.0 | Visualization plots |
| tabulate | ≥0.9.0 | Console table formatting |
| pandas | ≥2.0.0 | Data handling |
| rich | ≥13.0.0 | Colored console output |

### Development Dependencies

```bash
pip install -r requirements-dev.txt
```

| Package | Purpose |
|---------|---------|
| pytest | Unit testing |
| pytest-cov | Coverage reporting |
| black | Code formatting |
| mypy | Type checking |
| flake8 | Linting |

## Cython Compilation

### Why Compile Cython?

The Cython technique has a pure Python fallback, but compiling provides:
- 10-100x speedup over Python
- Near-C performance
- Demonstrates compiled extension benefits

### Compilation Steps

```bash
# Ensure Cython is installed
pip install Cython

# Run the setup script
python scripts/setup_cython.py build_ext --inplace

# Verify compilation
python -c "from techniques.09_cython_optimized.fibonacci_impl import fib_cython; print(fib_cython(10))"
# Should print: 55
```

### Compilation Output

Successfully compiled, you'll see:
```
techniques/09_cython_optimized/fibonacci_impl.cpython-311-x86_64-linux-gnu.so
```

(File extension varies by platform)

### Troubleshooting Compilation

**Error: "Unable to find vcvarsall.bat" (Windows)**
- Install Visual Studio Build Tools
- Or use mingw: `pip install mingw-w64`

**Error: "gcc not found" (Linux)**
```bash
sudo apt install build-essential
```

**Error: "clang not found" (macOS)**
```bash
xcode-select --install
```

## Numba Notes

Numba requires LLVM and may take time on first run:

1. **First call compilation**: ~1-2 seconds
2. **Subsequent calls**: Near-instant (cached)

If you see warnings about LLVM, ensure numba is properly installed:

```bash
pip install --upgrade numba
python -c "import numba; print(numba.__version__)"
```

## Verification

After setup, verify everything works:

```bash
# Run tests
pytest tests/ -v

# Run quick benchmark
python scripts/run_benchmark.py --duration 0.5

# List techniques
python scripts/run_benchmark.py --list
```

Expected output:
```
Available Fibonacci techniques:
----------------------------------------
 1. Naive Recursion
    Classic recursive implementation without optimization
    Time: O(2^n), Space: O(n)

 2. Memoized Recursion
    ...
```

## Common Issues

### "Module not found" errors

```bash
# Ensure you're in the project root
cd /path/to/SpeedyFibonacci

# Ensure virtual environment is active
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Matplotlib display issues (headless server)

```bash
# Use non-interactive backend
export MPLBACKEND=Agg
python scripts/run_benchmark.py
```

### Permission denied (scripts)

```bash
chmod +x scripts/*.py
```

### Python version mismatch

```bash
# Check version
python --version

# Should be 3.11 or higher
# If not, specify full path:
/usr/bin/python3.11 -m venv venv
```

## IDE Setup

### VS Code

1. Install Python extension
2. Select interpreter: `venv/bin/python`
3. Install recommended extensions when prompted

### PyCharm

1. Open project folder
2. Configure interpreter: `venv/bin/python`
3. Mark `techniques/`, `benchmarking/`, etc. as source roots

## Updating Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade numpy
```

## Cleanup

```bash
# Remove generated files
python scripts/clean.py --all

# Remove virtual environment
deactivate
rm -rf venv
```
