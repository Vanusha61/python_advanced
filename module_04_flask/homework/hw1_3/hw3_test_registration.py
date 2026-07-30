"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""
from hw1_registration import app
from unittest import TestCase

class TestRegisterForm(TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.url = "/registration/"

        self.data = {
            "email": "test@mail.ru",
            "phone": "9999999999",
            "name": "Ivan",
            "address": "Street",
            "index": 3,
            "comment": ""
        }

    def test_register_good(self):
        result = {
            "address": "Street",
            "comment": "",
            "email": "test@mail.ru",
            "index": 3,
            "name": "Ivan",
            "phone": "+79999999999"
        }

        response = self.app.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, response.get_json())

    def test_register_bad_email(self):
        result = {'email': ['Невалидный email']}
        self.data['email'] = "testmail"
        response = self.app.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result, response.get_json())

    def test_register_bad_phone(self):
        result = {'phone': ['Телефон должен содержать ровно 10 цифр (только числа)']}
        self.data['phone'] = "+79999999999"
        response = self.app.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result, response.get_json())

    def test_register_bad_name(self):
        result = {'name': ['Ошибка, пустой name']}
        self.data['name'] = ""
        response = self.app.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result, response.get_json())

    def test_register_bad_address(self):
        result = {'address': ['Ошибка, пустой address']}
        self.data['address'] = ""
        response = self.app.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result, response.get_json())

    def test_register_bad_index(self):
        result = {'index': ['Ошибка, пустой index']}
        self.data['index'] = ""
        response = self.app.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result, response.get_json())

    def test_register_bad_full(self):
        result = {'address': ['Ошибка, пустой address'], 'email': ['Невалидный email'], 'index': ['Ошибка, пустой index'], 'name': ['Ошибка, пустой name'], 'phone': ['Телефон должен содержать ровно 10 цифр (только числа)']}
        response = self.app.post(self.url, data={
            "email": "testmail.ru",
            "phone": "89999999999",
            "name": "",
            "address": "",
            "index": "",
            "comment": ""
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result, response.get_json())

if __name__ == '__main__':
    unittest.main()
