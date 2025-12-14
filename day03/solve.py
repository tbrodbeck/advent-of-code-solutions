"""Day 3: Lobby - Maximum joltage from battery banks."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run_parts, iter_lines


def _max_joltage(bank: str, k: int = 2) -> int:
    """Find max joltage by picking k digits in order.
    Args:
        bank: String of digit characters.
        k: Number of digits to pick.
    Returns:
        Maximum joltage from picking k digits."""
    digits = [int(c) for c in bank]
    n = len(digits)
    result = []
    start = 0
    for i in range(k):
        end = n - k + i + 1
        best_idx = start
        for j in range(start, end):
            if digits[j] > digits[best_idx]:
                best_idx = j
        result.append(digits[best_idx])
        start = best_idx + 1
    return int("".join(str(d) for d in result))


def solve(lines: list[str], k: int) -> int:
    """Sum of max joltage from each bank.
    Args:
        lines: Raw input lines.
        k: Number of digits to pick per bank.
    Returns:
        Total joltage."""
    return sum(_max_joltage(line, k) for line in iter_lines(lines))


if __name__ == "__main__":
    run_parts(lambda lines: solve(lines, 2), lambda lines: solve(lines, 12))
