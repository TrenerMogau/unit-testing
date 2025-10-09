"""Unit tests for the intro_example module."""
import unittest 
from intro_example import simple_func, returnFalse, returnTrue


class TestSomething(unittest.TestCase):

    # testing no argument
    def test_default(self):
        result = simple_func()
        expect_to_be = "Hello, World!"
# ue, expect_to_be)
        self.assertEqual(result, expect_to_be)

    
    def test_bool(self):
        self.assertTrue(returnTrue())
        self.assertFalse(returnFalse())


    def test_custom_name(self):
        # self.assertEqual(simple_func("Alice"), "Hello, Alice!")
        self.assertEqual(simple_func("Bob"), "Hello, Bob!")


if __name__ == "__main__":
    """Run the unit tests."""
    unittest.main()