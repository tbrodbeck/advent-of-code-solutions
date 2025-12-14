import unittest
from .solve import sum_invalid_ids, is_invalid, is_invalid_v2

EXAMPLE = [
    "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
]


class TestPart1(unittest.TestCase):
    def test_example(self):
        self.assertEqual(sum_invalid_ids(EXAMPLE, is_invalid), 1227775554)

    def test_is_invalid(self):
        self.assertTrue(is_invalid(55))  # 5 twice
        self.assertTrue(is_invalid(6464))  # 64 twice
        self.assertTrue(is_invalid(123123))  # 123 twice
        self.assertTrue(is_invalid(99))  # 9 twice
        self.assertFalse(is_invalid(101))  # Odd length


class TestPart2(unittest.TestCase):
    def test_example(self):
        self.assertEqual(sum_invalid_ids(EXAMPLE, is_invalid_v2), 4174379265)

    def test_is_invalid_v2(self):
        self.assertTrue(is_invalid_v2(111))  # 1×3
        self.assertTrue(is_invalid_v2(1212121212))  # 12×5
        self.assertTrue(is_invalid_v2(565656))  # 56×3
        self.assertTrue(is_invalid_v2(824824824))  # 824×3
        self.assertFalse(is_invalid_v2(101))  # Not repeated


if __name__ == "__main__":
    unittest.main()
