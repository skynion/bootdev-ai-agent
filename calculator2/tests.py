import unittest

from main import add, divide, multiply, subtract


class CalculatorTests(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-2, -3), -5)

    def test_add_mixed_numbers(self):
        self.assertEqual(add(-2, 3), 1)

    def test_subtract_positive_numbers(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_subtract_negative_numbers(self):
        self.assertEqual(subtract(-5, -3), -2)

    def test_multiply_positive_numbers(self):
        self.assertEqual(multiply(4, 3), 12)

    def test_multiply_by_zero(self):
        self.assertEqual(multiply(4, 0), 0)

    def test_divide_positive_numbers(self):
        self.assertEqual(divide(8, 2), 4)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(8, 0)


if __name__ == "__main__":
    unittest.main()
