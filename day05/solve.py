"""Day 5: Cafeteria - Check which ingredients are fresh."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run_parts


def _parse(lines: list[str]) -> tuple[list[tuple[int, int]], list[int]]:
    """Parse ranges and ingredient IDs from input.
    Args:
        lines: Raw input lines.
    Returns:
        Tuple of (ranges, ingredient_ids)."""
    ranges = []
    ids = []
    in_ids = False
    for line in lines:
        line = line.strip()
        if not line:
            in_ids = True
            continue
        if in_ids:
            ids.append(int(line))
        else:
            start, end = line.split("-")
            ranges.append((int(start), int(end)))
    return ranges, ids


def _is_fresh(n: int, ranges: list[tuple[int, int]]) -> bool:
    """Check if ingredient ID is fresh (in any range).
    Args:
        n: Ingredient ID.
        ranges: List of (start, end) ranges.
    Returns:
        True if ID falls in any range."""
    for start, end in ranges:
        if start <= n <= end:
            return True
    return False


def solve_part1(lines: list[str]) -> int:
    """Count fresh ingredient IDs.
    Args:
        lines: Raw input lines.
    Returns:
        Number of fresh ingredients."""
    ranges, ids = _parse(lines)
    return sum(1 for n in ids if _is_fresh(n, ranges))


def solve_part2(lines: list[str]) -> int:
    """Count total unique fresh IDs across all ranges.
    Args:
        lines: Raw input lines.
    Returns:
        Total unique fresh IDs."""
    ranges, _ = _parse(lines)
    ranges.sort()

    # Merge overlapping ranges
    merged = []
    for start, end in ranges:
        if merged and start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    return sum(end - start + 1 for start, end in merged)


if __name__ == "__main__":
    run_parts(solve_part1, solve_part2)
