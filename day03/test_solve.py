import unittest
from .solve import solve, _max_joltage

EXAMPLE = ["987654321111111", "811111111111119", "234234234234278", "818181911112111"]


class TestPart1(unittest.TestCase):
    def test_example(self):
        self.assertEqual(solve(EXAMPLE, 2), 357)

    def test_max_joltage(self):
        self.assertEqual(_max_joltage("987654321111111", 2), 98)
        self.assertEqual(_max_joltage("811111111111119", 2), 89)
        self.assertEqual(_max_joltage("818181911112111", 2), 92)


class TestPart2(unittest.TestCase):
    def test_example(self):
        self.assertEqual(solve(EXAMPLE, 12), 3121910778619)

    def test_max_joltage_12(self):
        self.assertEqual(_max_joltage("987654321111111", 12), 987654321111)
        self.assertEqual(_max_joltage("234234234234278", 12), 434234234278)
        self.assertEqual(_max_joltage("818181911112111", 12), 888911112111)


if __name__ == "__main__":
    unittest.main()
