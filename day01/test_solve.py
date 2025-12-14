import unittest
from .solve import Part1Simulator, Part2Simulator

EXAMPLE = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]


class TestPart1(unittest.TestCase):
    def test_example(self):
        self.assertEqual(Part1Simulator.solve(EXAMPLE), 3)

    def test_land_on_zero(self):
        self.assertEqual(Part1Simulator.solve(["R50"]), 1)


class TestPart2(unittest.TestCase):
    def test_example(self):
        self.assertEqual(Part2Simulator.solve(EXAMPLE), 6)

    def test_right_to_zero(self):
        self.assertEqual(Part2Simulator.solve(["R50"]), 1)

    def test_left_cross(self):
        self.assertEqual(Part2Simulator.solve(["L55"]), 1)

    def test_left_land(self):
        self.assertEqual(Part2Simulator.solve(["L50"]), 1)

    def test_right_multi_wrap(self):
        self.assertEqual(Part2Simulator.solve(["R150"]), 2)

    def test_no_cross(self):
        self.assertEqual(Part2Simulator.solve(["R10"]), 0)

    def test_left_from_zero(self):
        self.assertEqual(Part2Simulator.solve(["R50", "L5"]), 1)

    def test_left_full_circle(self):
        self.assertEqual(Part2Simulator.solve(["R50", "L100"]), 2)


if __name__ == "__main__":
    unittest.main()
