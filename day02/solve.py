"""Day 2: Gift Shop - Find invalid IDs (digits repeated twice)."""

from collections.abc import Iterator
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run_parts, parse_lines


def parse(lines: list[str]) -> Iterator[tuple[int, int]]:
    """Parse input into (start, end) ranges.
    Args:
        lines: Raw input lines containing comma-separated ranges.
    Yields:
        Tuples of (start, end) for each range."""

    def parse_line(line: str) -> Iterator[tuple[int, int]]:
        for part in line.split(","):
            part = part.strip()
            if part:
                start, end = part.split("-")
                yield int(start), int(end)

    return parse_lines(lines, parse_line)


def is_invalid(n: int) -> bool:
    """Check if ID is invalid (made of same sequence repeated twice).
    Args:
        n: Product ID to check.
    Returns:
        True if ID consists of same sequence repeated exactly twice."""
    s = str(n)
    length = len(s)
    if length % 2 != 0:
        return False
    half = length // 2
    return s[:half] == s[half:]


def is_invalid_v2(n: int) -> bool:
    """Check if ID is invalid (made of same sequence repeated at least twice).
    Args:
        n: Product ID to check.
    Returns:
        True if ID consists of same sequence repeated at least twice."""
    s = str(n)
    length = len(s)
    # Try all possible repeat lengths (1 to length//2)
    for rep_len in range(1, length // 2 + 1):
        if length % rep_len == 0:
            pattern = s[:rep_len]
            if pattern * (length // rep_len) == s:
                return True
    return False


def sum_invalid_ids(lines: list[str], is_invalid_func) -> int:
    """Sum all invalid IDs in the given ranges.
    Args:
        lines: Raw input lines containing ranges.
        is_invalid_func: Function to check if ID is invalid.
    Returns:
        Sum of all invalid IDs."""
    total = 0

    for start, end in parse(lines):
        for n in range(start, end + 1):
            if is_invalid_func(n):
                total += n

    return total


if __name__ == "__main__":
    run_parts(
        lambda lines: sum_invalid_ids(lines, is_invalid),
        lambda lines: sum_invalid_ids(lines, is_invalid_v2),
    )
