"""Day 6: Trash Compactor - Solve cephalopod math problems."""

import sys
import os
import re
from collections.abc import Callable

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run_parts


def _preprocess_lines(lines: list[str]) -> tuple[list[str], str, int]:
    """Preprocess input lines into padded format.

    Args:
        lines: Raw input lines.
    Returns:
        Tuple of (number_lines, operation_line, max_width).
    """
    non_empty = [line.rstrip() for line in lines if line.strip()]
    if not non_empty:
        return [], "", 0

    max_width = max(len(line) for line in non_empty)
    padded = [line.ljust(max_width) for line in non_empty]

    operation_line = padded[-1]
    number_lines = padded[:-1]

    return number_lines, operation_line, max_width


def _find_problem_boundaries(
    padded: list[str], max_width: int
) -> list[tuple[int, int]]:
    """Find start and end columns for each problem.

    Problems are separated by columns that are all spaces.

    Args:
        padded: All lines padded to the same width.
        max_width: Maximum width of lines.
    Returns:
        List of (start_col, end_col) tuples for each problem.
    """
    boundaries = []
    i = 0

    while i < max_width:
        # Skip separator columns (all spaces)
        while i < max_width and all(line[i] == " " for line in padded):
            i += 1

        if i >= max_width:
            break

        # Find the end of this problem (next all-space column)
        start_col = i
        while i < max_width and not all(line[i] == " " for line in padded):
            i += 1
        end_col = i

        boundaries.append((start_col, end_col))

    return boundaries


def _extract_operation_part1(
    operation_line: str, start_col: int, end_col: int
) -> str | None:
    """Extract operation from operation line (Part 1: left-to-right).

    Args:
        operation_line: Line containing operations.
        start_col: Start column of problem.
        end_col: End column of problem.
    Returns:
        Operation symbol ('+' or '*'), or None if not found.
    """
    op_segment = operation_line[start_col:end_col].strip()
    return op_segment[0] if op_segment else None


def _extract_operation_part2(
    operation_line: str, start_col: int, end_col: int
) -> str | None:
    """Extract operation from operation line (Part 2: right-to-left).

    Args:
        operation_line: Line containing operations.
        start_col: Start column of problem.
        end_col: End column of problem.
    Returns:
        Operation symbol ('+' or '*'), or None if not found.
    """
    for col in range(end_col - 1, start_col - 1, -1):
        if col < len(operation_line) and operation_line[col] in "+*":
            return operation_line[col]
    return None


def _extract_numbers_part1(
    number_lines: list[str], start_col: int, end_col: int
) -> list[int]:
    """Extract numbers from problem (Part 1: horizontal reading).

    Args:
        number_lines: Lines containing numbers.
        start_col: Start column of problem.
        end_col: End column of problem.
    Returns:
        List of numbers in the problem.
    """
    problem_numbers = []
    for line in number_lines:
        segment = line[start_col:end_col]
        numbers = re.findall(r"\d+", segment)
        if numbers:
            problem_numbers.append(int(numbers[0]))
    return problem_numbers


def _extract_numbers_part2(
    number_lines: list[str], start_col: int, end_col: int
) -> list[int]:
    """Extract numbers from problem (Part 2: vertical reading, right-to-left).

    Args:
        number_lines: Lines containing numbers.
        start_col: Start column of problem.
        end_col: End column of problem.
    Returns:
        List of numbers in the problem (in left-to-right order).
    """
    problem_numbers = []
    # Read columns right-to-left
    for col in range(end_col - 1, start_col - 1, -1):
        # Read digits top-to-bottom
        number_digits = []
        for line in number_lines:
            if col < len(line) and line[col].isdigit():
                number_digits.append(line[col])

        if number_digits:
            number_str = "".join(number_digits)
            problem_numbers.append(int(number_str))

    # Reverse since we collected right-to-left
    problem_numbers.reverse()
    return problem_numbers


def _parse_problems(
    lines: list[str],
    extract_numbers: Callable[[list[str], int, int], list[int]],
    extract_operation: Callable[[str, int, int], str | None],
    reverse_problems: bool = False,
) -> list[tuple[list[int], str]]:
    """Parse problems from the worksheet.

    Args:
        lines: Raw input lines.
        extract_numbers: Function to extract numbers from a problem region.
        extract_operation: Function to extract operation from operation line.
        reverse_problems: If True, reverse the order of problems.
    Returns:
        List of (numbers, operation) tuples for each problem.
    """
    number_lines, operation_line, max_width = _preprocess_lines(lines)
    if not number_lines:
        return []

    # Create padded list for boundary finding
    padded = number_lines + [operation_line]

    boundaries = _find_problem_boundaries(padded, max_width)
    problems = []

    for start_col, end_col in boundaries:
        problem_numbers = extract_numbers(number_lines, start_col, end_col)
        problem_op = extract_operation(operation_line, start_col, end_col)

        if problem_numbers and problem_op:
            problems.append((problem_numbers, problem_op))

    if reverse_problems:
        problems.reverse()

    return problems


def _solve_problem(numbers: list[int], operation: str) -> int:
    """Solve a single problem.

    Args:
        numbers: List of numbers in the problem.
        operation: Operation to perform ('+' or '*').
    Returns:
        Result of the problem.
    """
    if not numbers:
        return 0

    if operation == "+":
        return sum(numbers)
    elif operation == "*":
        result = 1
        for n in numbers:
            result *= n
        return result
    else:
        raise ValueError(f"Unknown operation: {operation}")


def _calculate_grand_total(problems: list[tuple[list[int], str]]) -> int:
    """Calculate grand total from all problems.

    Args:
        problems: List of (numbers, operation) tuples.
    Returns:
        Grand total (sum of all problem answers).
    """
    total = 0
    for numbers, operation in problems:
        total += _solve_problem(numbers, operation)
    return total


def solve_part1(lines: list[str]) -> int:
    """Calculate grand total of all problem answers.

    Args:
        lines: Raw input lines.
    Returns:
        Grand total (sum of all problem answers).
    """
    problems = _parse_problems(lines, _extract_numbers_part1, _extract_operation_part1)
    return _calculate_grand_total(problems)


def solve_part2(lines: list[str]) -> int:
    """Calculate grand total with right-to-left, vertical number reading.

    In Part 2, cephalopod math is written right-to-left in columns.
    Each number is in its own column, with the most significant digit at
    the top and the least significant digit at the bottom. Problems are
    still separated by space columns, and are read right-to-left.

    Args:
        lines: Raw input lines.
    Returns:
        Grand total (sum of all problem answers).
    """
    problems = _parse_problems(
        lines,
        _extract_numbers_part2,
        _extract_operation_part2,
        reverse_problems=True,
    )
    return _calculate_grand_total(problems)


if __name__ == "__main__":
    run_parts(solve_part1, solve_part2)
