"""Day 7: Laboratories - Traverse tachyon manifold grid."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run


def parse(f) -> tuple[tuple[str, ...], int, int, int]:
    """Parse grid and compute dimensions.
    Args:
        f: File handle.
    Returns:
        Tuple of (grid, start_col, rows, cols)."""
    grid = tuple(line.rstrip() for line in f)
    start_col = grid[0].index('S')
    return grid, start_col, len(grid), len(grid[0])


def count_visited(parsed) -> int:
    """Count ^ cells visited during traversal.
    Args:
        parsed: Tuple of (grid, start_col, rows, cols).
    Returns:
        Number of ^ cells visited."""
    grid, start_col, rows, cols = parsed
    visited = set()
    count = 0

    def traverse(row: int, col: int):
        nonlocal count
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return
        if (row, col) in visited:
            return
        visited.add((row, col))
        char = grid[row][col]
        if char == '^':
            count += 1
            traverse(row + 1, col - 1)
            traverse(row + 1, col + 1)
        elif char in '.S':
            traverse(row + 1, col)

    traverse(1, start_col)
    return count


def count_paths(parsed) -> int:
    """Count total timelines (paths) through the manifold.
    Args:
        parsed: Tuple of (grid, start_col, rows, cols).
    Returns:
        Number of distinct paths to bottom."""
    grid, start_col, rows, cols = parsed
    memo = {}

    def recurse(row: int, col: int) -> int:
        if row >= rows or col < 0 or col >= cols:
            return 0
        if row == rows - 1:
            return 1
        if (row, col) in memo:
            return memo[(row, col)]
        char = grid[row][col]
        if char == '^':
            result = recurse(row + 1, col - 1) + recurse(row + 1, col + 1)
        elif char in '.S':
            result = recurse(row + 1, col)
        else:
            result = 0
        memo[(row, col)] = result
        return result

    return recurse(0, start_col)


if __name__ == "__main__":
    run(__file__, parse, count_visited, count_paths)
