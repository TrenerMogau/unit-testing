"""Unit tests for the glass_box module."""
import unittest
from glass_box import FizzBuzz

class TestGlassBox(unittest.TestCase):
    """testing different cases for the FizzBuzz function"""

    def test_Fizz(self):
        self.assertEqual(FizzBuzz(3), "Fizz")
        self.assertEqual(FizzBuzz(9), "Fizz")
        self.assertEqual(FizzBuzz(18), "Fizz")

    def test_Buzz(self):
        self.assertEqual(FizzBuzz(5), "Buzz")
        self.assertEqual(FizzBuzz(10), "Buzz")
        self.assertEqual(FizzBuzz(20), "Buzz")

    def test_FizzBuzz(self):
        self.assertEqual(FizzBuzz(15), "FizzBuzz")
        self.assertEqual(FizzBuzz(30), "FizzBuzz")
        self.assertEqual(FizzBuzz(45), "FizzBuzz")

    def test_number(self):
        self.assertEqual(FizzBuzz(1), "1")
        self.assertEqual(FizzBuzz(2), "2")
        self.assertEqual(FizzBuzz(4), "4")
        self.assertEqual(FizzBuzz(7), "7")

    def test_zero(self):
        self.assertEqual(FizzBuzz(0), "FizzBuzz")

    def test_negative(self):
        self.assertEqual(FizzBuzz(-3), "Fizz")
        self.assertEqual(FizzBuzz(-5), "Buzz")
        self.assertEqual(FizzBuzz(-15), "FizzBuzz")
        self.assertEqual(FizzBuzz(-1), "-1")

    def test_errors(self):
        with self.assertRaises(TypeError):
            FizzBuzz("string")
        with self.assertRaises(TypeError):
            FizzBuzz(3.5)
        with self.assertRaises(TypeError):
            FizzBuzz(None)

if __name__ == "__main__":
    """Run the unit tests."""
    unittest.main()