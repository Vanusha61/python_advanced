import unittest
from block_errors import BlockErrors

class TestWith(unittest.TestCase):
    def test_with_1(self):
        flag = False
        err_types = {ZeroDivisionError, TypeError}
        with BlockErrors(err_types):
            a = 1 / 0
        flag = True
        print('Выполнено без ошибок')
        self.assertTrue(flag)

    def test_with_2(self):
        flag = False
        err_types = {ZeroDivisionError}
        with self.assertRaises(TypeError):
            with BlockErrors(err_types):
                a = 1 / '0'
                flag = True
            print('Выполнено без ошибок')

    def test_with_3(self):
        outer_err_types = {TypeError}
        flag = False
        with BlockErrors(outer_err_types):
            inner_err_types = {ZeroDivisionError}
            with self.assertRaises(TypeError):
                with BlockErrors(inner_err_types):
                    a = 1 / '0'
                print('Внутренний блок: выполнено без ошибок')
            print('Внешний блок: выполнено без ошибок')
            flag = True
        self.assertTrue(flag)

    def test_with_4(self):
        flag = False
        err_types = {Exception}
        with BlockErrors(err_types):
            a = 1 / '0'
        print('Выполнено без ошибок')
        flag = True
        self.assertTrue(flag)




if __name__ == '__main__':
    unittest.main()
