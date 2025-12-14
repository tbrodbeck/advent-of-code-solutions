import unittest
from .solve import solve_part1, solve_part2, _count_neighbors

EXAMPLE = [
    "@.@@",
    "@@.@",
    ".@@@",
]


class TestPart1(unittest.TestCase):
    def test_example(self):
        # 9 total rolls, 3 have >= 4 neighbors, so 6 accessible
        self.assertEqual(solve_part1(EXAMPLE), 6)

    def test_count_neighbors(self):
        grid = ["@.@@", "@@.@", ".@@@"]
        self.assertEqual(_count_neighbors(grid, 0, 0), 2)  # corner
        self.assertEqual(_count_neighbors(grid, 1, 1), 5)  # middle


class TestPart2(unittest.TestCase):
    def test_example(self):
        # Round 1: remove 6, Round 2: remove 3 remaining = 9 total
        self.assertEqual(solve_part2(EXAMPLE), 9)


if __name__ == "__main__":
    unittest.main()
