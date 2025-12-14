import unittest
import io
from .solve import parse, count_part1

EXAMPLE = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


class TestPart1(unittest.TestCase):
    def test_example(self):
        # After 10 connections: circuits of size 5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1
        # 5 * 4 * 2 = 40
        self.assertEqual(count_part1(parse(io.StringIO(EXAMPLE)), 10), 40)


if __name__ == "__main__":
    unittest.main()
