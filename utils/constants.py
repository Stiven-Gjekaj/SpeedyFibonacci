"""
Shared constants for SpeedyFibonacci project.

This module contains constants used across the project including
known Fibonacci values for validation and default configuration.

Author: SpeedyFibonacci Contributors
License: MIT
"""

# Default benchmark duration in seconds
DEFAULT_DURATION: float = 1.0

# Known Fibonacci numbers for result validation
# These values are pre-computed and verified for testing technique correctness
KNOWN_FIBONACCI: dict[int, int] = {
    0: 0,
    1: 1,
    2: 1,
    3: 2,
    4: 3,
    5: 5,
    6: 8,
    7: 13,
    8: 21,
    9: 34,
    10: 55,
    11: 89,
    12: 144,
    13: 233,
    14: 377,
    15: 610,
    16: 987,
    17: 1597,
    18: 2584,
    19: 4181,
    20: 6765,
    25: 75025,
    30: 832040,
    35: 9227465,
    40: 102334155,
    45: 1134903170,
    50: 12586269025,
    55: 139583862445,
    60: 1548008755920,
    70: 190392490709135,
    80: 23416728348467685,
    90: 2880067194370816120,
    100: 354224848179261915075,
    150: 9969216677189303386214405760200,
    200: 280571172992510140037611932413038677189525,
    300: 222232244629420445529739893461909967206666939096499764990979600,
    500: 139423224561697880139724382870407283950070256587697307264108962948325571622863290691557658876222521294125,
}

# Golden ratio (phi) - used in Binet's formula
PHI: float = (1 + 5 ** 0.5) / 2

# Conjugate of golden ratio (psi)
PSI: float = (1 - 5 ** 0.5) / 2

# Square root of 5 - used in Binet's formula
SQRT_5: float = 5 ** 0.5

# Matrix used for matrix exponentiation technique
# [[1, 1], [1, 0]]^n gives [[F(n+1), F(n)], [F(n), F(n-1)]]
FIBONACCI_MATRIX: list[list[int]] = [[1, 1], [1, 0]]

# Technique folder naming convention
TECHNIQUE_PREFIX_PATTERN: str = r"^\d{2}_"

# Output formatting
CONSOLE_TABLE_FORMAT: str = "rounded_grid"
CSV_DELIMITER: str = ","
RESULTS_DIR_NAME: str = "results"
