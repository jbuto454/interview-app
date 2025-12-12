import unittest

from backend.app import clean_user_input, extract_expression

class MyTestCase(unittest.TestCase):

    def test_clean_user_input(self):

        #test the case of '2x'
        self.assertEqual(clean_user_input("2x")[0], "2*x")
        #test the case of 'x2'
        self.assertEqual(clean_user_input("x2")[0], "x*2")
        #test the case of 'x^2'
        self.assertEqual(clean_user_input("x^2")[0], "x**2")
        #test the case of a numerical value
        self.assertEqual(clean_user_input("2")[0], "2")
        # test the case of a numerical value with multiple digits
        self.assertEqual(clean_user_input("222")[0], "222")
        #test a more complex equation
        self.assertEqual(clean_user_input("222x + x")[0], "222*x+x")
        #test a more complex equation
        self.assertEqual(clean_user_input("222*x + x")[0], "222*x+x")
        #test a more complex equation
        self.assertEqual(clean_user_input("222*x + x^2")[0], "222*x+x**2")
        # test a more complex equation
        self.assertEqual(clean_user_input("222*x + x**2")[0], "222*x+x**2")
        # test a more complex equation
        self.assertEqual(clean_user_input("222*x + x**2 - sin(x)")[0], "222*x+x**2-sin(x)")
        # test a sqrt
        self.assertEqual(clean_user_input("sqrt(x)")[0], "sqrt(x)")
        #test division
        self.assertEqual(clean_user_input("x/2")[0], "x/2")
        # test an equation with an equals-sign (left side of equation)
        self.assertEqual(clean_user_input("x/2 = 90")[2], "x/2")
        # test an equation with an equals-sign (right side of equation)
        self.assertEqual(clean_user_input("x/2 = 90")[3], "90")
        #test a double equals
        self.assertEqual(clean_user_input("x/2 == 90")[3], "90")


    # other unit tests to add:
    # 1. test_extract_expression
    # 2. test_pretty_solution


if __name__ == '__main__':
    unittest.main()
