from unittest import TestCase

from remote_execution import app

class TestSyb(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["WTF_CSRF_ENABLED"] = False
        cls.app = app.test_client()
        cls.url = "/subprocess_api"

    def test_good_print(self):
        result = {'stderr': '', 'stdout': 'Hello World\n', 'код_возврата': 0}
        response = self.app.post(self.url, data={
            "code": "print('Hello World')",
            "timeout": 5
        })
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, result)

    def test_bad_sleep(self):
        result = {'error': 'Выполнение прервано по таймауту 3 секунд', 'частичная_ошибка': '', 'частичный_вывод': ''}
        response = self.app.post(self.url, data={
            "code": "import time; time.sleep(5)",
            "timeout": "3"
        })
        self.assertEqual(response.status_code, 408)
        self.assertEqual(response.json, result)

    def test_bad_code(self):
        result = {'errors': {'code': ['Код не передан']}}
        response = self.app.post(self.url, data={
            "timeout": 3
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, result)

    def test_bad_timeout_default(self):
        result = {'error': 'Выполнение прервано по таймауту 5 секунд', 'частичная_ошибка': '', 'частичный_вывод': ''}
        response = self.app.post(self.url, data={
            "code": "import time; time.sleep(5)"
        })
        self.assertEqual(response.status_code, 408)
        self.assertEqual(response.json, result)

    def test_timeout_not_int(self):
        result = {'errors': {'timeout': ['Not a valid integer value.','Таймаут должен быть от 1 до 30 секунд']}}
        response = self.app.post(self.url, data={
            "code": "print('Hello World')",
            "timeout": "abc"
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, result)

    def test_timeout_zero(self):
        result = {'errors': {'timeout': ['Таймаут должен быть от 1 до 30 секунд']}}
        response = self.app.post(self.url, data={
            "code": "print('Hello World')",
            "timeout": 0})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, result)

    def test_timeout_31(self):
        result = {'errors': {'timeout': ['Таймаут должен быть от 1 до 30 секунд']}}
        response = self.app.post(self.url, data={
            "code": "print('Hello World')",
            "timeout": 31})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, result)

    def test_syntax_error(self):
        result = {'stderr': '  File "<string>", line 1\n    print(\'Hello World\'\n         ^\nSyntaxError: \'(\' was never closed\n', 'stdout': '', 'код_возврата': 1}
        response = self.app.post(self.url, data={
            "code": "print('Hello World'",

        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, result)





if __name__ == '__main__':
    unittest.main()
