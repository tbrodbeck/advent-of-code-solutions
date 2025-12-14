import unittest
from .solve import solve_part1, solve_part2, _is_fresh

EXAMPLE = [
    "1-5",
    "10-15",
    "3-8",
    "",
    "2",
    "7",
    "9",
    "12",
]


class TestPart1(unittest.TestCase):
    def test_example(self):
        # 2 in 1-5, 7 in 3-8, 12 in 10-15 = 3 fresh
        self.assertEqual(solve_part1(EXAMPLE), 3)

    def test_is_fresh(self):
        ranges = [(1, 5), (10, 15)]
        self.assertTrue(_is_fresh(3, ranges))
        self.assertTrue(_is_fresh(12, ranges))
        self.assertFalse(_is_fresh(7, ranges))


class TestPart2(unittest.TestCase):
    def test_example(self):
        # Merged: 1-8, 10-15 = 8 + 6 = 14 unique fresh IDs
        self.assertEqual(solve_part2(EXAMPLE), 14)


if __name__ == "__main__":
    unittest.main()
