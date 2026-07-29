import unittest
from finance import app, storage


class TestFinance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

        storage.clear()
        storage.update({
            '20231001': 1000,
            '20231015': 500,
            '20231101': 2000,
            '20231115': 300,
            '20231201': 1500,
        })

    def test_add_works(self):
        response = self.client.post('/add/', json={
            'date': '20240101',
            'amount': 1000
        })
        self.assertEqual(response.status_code, 200)

    def test_add_invalid_date(self):
        with self.assertRaises(ValueError):
            self.client.post('/add/', json={
                'date': '2024-01-01',
                'amount': 1000
            })

    def test_calculate_year_works(self):
        response = self.client.get('/calculate/2023/')
        self.assertEqual(response.status_code, 200)

    def test_calculate_year_month_works(self):
        response = self.client.get('/calculate/2023/10/')
        self.assertEqual(response.status_code, 200)

    def test_calculate_empty_storage(self):
        storage.clear()
        response = self.client.get('/calculate/2023/')
        self.assertEqual(response.status_code, 200)


