import unittest
import io
from .solve import parse, count_part1, count_part2

EXAMPLE = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
"""


class TestPart1(unittest.TestCase):
    def test_example(self):
        self.assertEqual(count_part1(parse(io.StringIO(EXAMPLE))), 2)


class TestPart2(unittest.TestCase):
    def test_example(self):
        self.assertEqual(count_part2(parse(io.StringIO(EXAMPLE))), 10)


if __name__ == "__main__":
    unittest.main()
