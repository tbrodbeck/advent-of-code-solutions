import unittest
import io
from .solve import parse, count_part1, count_part2

EXAMPLE = """\
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""


class TestPart1(unittest.TestCase):
    def test_example(self):
        self.assertEqual(count_part1(parse(io.StringIO(EXAMPLE))), 5)


class TestPart2(unittest.TestCase):
    def test_example(self):
        self.assertEqual(count_part2(parse(io.StringIO(EXAMPLE))), 0)


if __name__ == "__main__":
    unittest.main()
