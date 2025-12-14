"""Day 4: Printing Department - Count accessible paper rolls."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run_parts, iter_lines

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def _count_neighbors(grid: list[str], r: int, c: int) -> int:
    """Count neighboring rolls around position (r, c).
    Args:
        grid: 2D grid of characters.
        r: Row index.
        c: Column index.
    Returns:
        Number of adjacent rolls (@)."""
    rows, cols = len(grid), len(grid[0])
    count = 0
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
            count += 1
    return count


def solve_part1(lines: list[str]) -> int:
    """Count rolls accessible (< 4 neighbors).
    Args:
        lines: Raw input lines.
    Returns:
        Number of accessible rolls."""
    grid = [line for line in iter_lines(lines)]
    accessible = 0
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == "@" and _count_neighbors(grid, r, c) < 4:
                accessible += 1
    return accessible


def solve_part2(lines: list[str]) -> int:
    """Count total rolls removable by repeatedly removing accessible ones.
    Args:
        lines: Raw input lines.
    Returns:
        Total rolls removed."""
    grid = [list(line) for line in iter_lines(lines)]
    rows, cols = len(grid), len(grid[0])
    total_removed = 0

    while True:
        to_remove = []
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "@" and _count_neighbors(grid, r, c) < 4:
                    to_remove.append((r, c))
        if not to_remove:
            break
        for r, c in to_remove:
            grid[r][c] = "."
        total_removed += len(to_remove)

    return total_removed


if __name__ == "__main__":
    run_parts(solve_part1, solve_part2)
