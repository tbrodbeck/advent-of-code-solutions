import unittest
import io
from .solve import parse, count_part1, count_part2

EXAMPLE = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


class TestPart1(unittest.TestCase):
    def test_example(self):
        self.assertEqual(count_part1(parse(io.StringIO(EXAMPLE))), 50)


class TestPart2(unittest.TestCase):
    def test_example(self):
        self.assertEqual(count_part2(parse(io.StringIO(EXAMPLE))), 24)


if __name__ == "__main__":
    unittest.main()
