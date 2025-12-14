import unittest
from .solve import (
    solve_part1,
    solve_part2,
    _parse_problems,
    _extract_numbers_part1,
    _extract_operation_part1,
    _solve_problem,
)

EXAMPLE = [
    "123 328  51 64 ",
    " 45 64  387 23 ",
    "  6 98  215 314",
    "*   +   *   +  ",
]


class TestPart1(unittest.TestCase):
    def test_example(self):
        result = solve_part1(EXAMPLE)
        self.assertEqual(result, 4277556)

    def test_parse_problems(self):
        problems = _parse_problems(
            EXAMPLE, _extract_numbers_part1, _extract_operation_part1
        )
        self.assertEqual(len(problems), 4)
        # Problem 1: 123 * 45 * 6
        self.assertEqual(problems[0], ([123, 45, 6], "*"))
        # Problem 2: 328 + 64 + 98
        self.assertEqual(problems[1], ([328, 64, 98], "+"))
        # Problem 3: 51 * 387 * 215
        self.assertEqual(problems[2], ([51, 387, 215], "*"))
        # Problem 4: 64 + 23 + 314
        self.assertEqual(problems[3], ([64, 23, 314], "+"))

    def test_solve_problem(self):
        self.assertEqual(_solve_problem([123, 45, 6], "*"), 33210)
        self.assertEqual(_solve_problem([328, 64, 98], "+"), 490)
        self.assertEqual(_solve_problem([51, 387, 215], "*"), 4243455)
        self.assertEqual(_solve_problem([64, 23, 314], "+"), 401)


class TestPart2(unittest.TestCase):
    def test_example(self):
        from .solve import (
            _parse_problems,
            _extract_numbers_part2,
            _extract_operation_part2,
        )

        problems = _parse_problems(
            EXAMPLE,
            _extract_numbers_part2,
            _extract_operation_part2,
            reverse_problems=True,
        )
        # Should have 4 problems in right-to-left order
        self.assertEqual(len(problems), 4)
        # Rightmost problem: 4 + 431 + 623 = 1058
        # Second from right: 175 * 581 * 32 = 3253600
        # Third from right: 8 + 248 + 369 = 625
        # Leftmost: 356 * 24 * 1 = 8544
        # Grand total: 1058 + 3253600 + 625 + 8544 = 3263827
        result = solve_part2(EXAMPLE)
        self.assertEqual(result, 3263827)


if __name__ == "__main__":
    unittest.main()
