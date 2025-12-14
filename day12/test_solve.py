import unittest
import io
from .solve import parse, count_part1

EXAMPLE = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""


class TestPart1(unittest.TestCase):
    def test_example(self):
        self.assertEqual(count_part1(parse(io.StringIO(EXAMPLE))), 2)


if __name__ == "__main__":
    unittest.main()
