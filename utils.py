"""Shared utilities for Advent of Code solutions."""

import os
from collections.abc import Callable, Iterator


def iter_lines(lines: list[str]) -> Iterator[str]:
    """Iterate over non-empty stripped lines.
    Args:
        lines: Raw input lines.
    Yields:
        Each non-empty line, stripped."""
    for line in lines:
        line = line.strip()
        if line:
            yield line


def parse_lines(lines: list[str], parse_line_func: Callable[[str], Iterator]) -> Iterator:
    """Parse lines with a function that yields items.
    Args:
        lines: Raw input lines.
        parse_line_func: Function that takes a stripped line and yields parsed results.
    Yields:
        Parsed results from each line."""
    for line in iter_lines(lines):
        yield from parse_line_func(line)


def map_lines(lines: list[str], parse_func: Callable) -> list:
    """Map a function over each line.
    Args:
        lines: Raw input lines.
        parse_func: Function to apply to each stripped line.
    Returns:
        List of parsed results."""
    return [parse_func(line) for line in iter_lines(lines)]


def _print_results(data, part1_func, part2_func):
    """Print results for both parts.
    Args:
        data: Parsed input data.
        part1_func: Function for part 1.
        part2_func: Function for part 2."""
    print(f"Part 1: {part1_func(data)}")
    print(f"Part 2: {part2_func(data)}")


def run_parts(part1_func, part2_func, input_file="input.txt"):
    """Run both parts with the given functions (functions take lines).
    Args:
        part1_func: Function that takes lines and returns part 1 result.
        part2_func: Function that takes lines and returns part 2 result.
        input_file: Input file path (default: "input.txt")."""
    with open(input_file) as f:
        _print_results(f.readlines(), part1_func, part2_func)


def run(caller_file, parse_func, part1_func, part2_func):
    """Run both parts with parsed input.
    Args:
        caller_file: __file__ from the calling module.
        parse_func: Function that takes file handle and returns parsed data.
        part1_func: Function that takes parsed data and returns part 1 result.
        part2_func: Function that takes parsed data and returns part 2 result."""
    with open(os.path.join(os.path.dirname(caller_file), "input.txt")) as f:
        _print_results(parse_func(f), part1_func, part2_func)
