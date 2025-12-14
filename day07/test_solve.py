import unittest
import io
from .solve import parse, count_visited, count_paths

EXAMPLE = """\
..S..
..^..
.^.^.
.....
"""


class TestPart1(unittest.TestCase):
    def test_example(self):
        # Visits: (1,2)=^, (2,1)=^, (2,3)=^  -> 3 carets
        self.assertEqual(count_visited(parse(io.StringIO(EXAMPLE))), 3)


class TestPart2(unittest.TestCase):
    def test_example(self):
        # 4 paths: each ^ doubles paths (1->2->4)
        self.assertEqual(count_paths(parse(io.StringIO(EXAMPLE))), 4)


if __name__ == "__main__":
    unittest.main()
