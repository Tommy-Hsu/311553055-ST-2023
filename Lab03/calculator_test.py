import unittest
import math
from calculator import Calculator


class ApplicationTest(unittest.TestCase):

    param_list_1 = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
    param_list_2 = [1, 2, 3, 4, 5]

    def test_add(self):

        for p1, p2 in self.param_list_1:
            with self.subTest():
                self.assertEqual(Calculator.add(p1, p2), p1+p2)

        self.assertRaises(TypeError, Calculator.add, ('test', 3))

        pass

    def test_divide(self):

        for p1, p2 in self.param_list_1:
            with self.subTest():
                self.assertEqual(Calculator.divide(p1, p2), p1/p2)

        self.assertRaises(TypeError, Calculator.divide, ('test', 3))

        pass

    def test_sqrt(self):

        for p in self.param_list_2:
            with self.subTest():
                self.assertEqual(Calculator.sqrt(p), math.sqrt(p))

        self.assertRaises(TypeError, Calculator.sqrt, ("test"))

        pass

    def test_exp(self):

        for p in self.param_list_2:
            with self.subTest():
                self.assertEqual(Calculator.exp(p), math.exp(p))

        self.assertRaises(TypeError, Calculator.exp, ("test"))

        pass


if __name__ == '__main__':
    unittest.main()
