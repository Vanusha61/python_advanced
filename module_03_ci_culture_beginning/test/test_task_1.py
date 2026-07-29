from unittest import TestCase
from freezegun import freeze_time
from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app

class TestTask1(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        cls.app = app.test_client()
        cls.url = "/hello-world/"
        cls.name = "Test"

    def test_task_1_name(self):
        response = self.app.get(self.url + self.name)
        response = response.text
        self.assertIn(self.name, response)

    def test_task_1_day(self):
        GREETINGS = (
            'Хорошего понедельника!',
            'Хорошего вторника!',
            'Хорошей среды!',
            'Хорошего четверга!',
            'Хорошей пятницы!',
            'Хорошей субботы!',
            'Хорошего воскресенья!'
        )
        response = self.app.get(self.url + self.name)
        response = response.text.split()
        self.assertIn(response[2] + " " + response[3], GREETINGS)

    def test_greeting_for_all_days(self):

        expected_greetings = {
            0: 'Хорошего понедельника!',
            1: 'Хорошего вторника!',
            2: 'Хорошей среды!',
            3: 'Хорошего четверга!',
            4: 'Хорошей пятницы!',
            5: 'Хорошей субботы!',
            6: 'Хорошего воскресенья!'
        }


        for day, expected_greeting in expected_greetings.items():
            with freeze_time(f"2023-01-0{day + 2}"):  # +2 потому что 2023-01-02 это понедельник
                response = self.app.get(self.url + self.name)
                response_text = response.text
                self.assertIn(expected_greeting, response_text,
                              f"Неверное приветствие для дня с индексом {day}")

    def test_can_get_correct_username_with_weekdate(self):

        test_name = "Анна"
        expected_greeting = "Хорошей среды!"  # Используем среду для примера


        with freeze_time("2023-01-04"):  # 4 января 2023 - среда
            response = self.app.get(self.url + test_name)
            response_text = response.text
            self.assertIn(test_name, response_text)
            self.assertIn(expected_greeting, response_text)
            response_parts = response_text.split()
            actual_greeting = response_parts[2] + " " + response_parts[3]
            self.assertEqual(expected_greeting, actual_greeting)

    def test_good_day_greeting_case(self):

        with freeze_time("2023-01-02"):  # Понедельник
            response = self.app.get(self.url + "Мария")
            self.assertIn("Мария", response.text)
        with freeze_time("2023-01-02"):
            response = self.app.get(self.url + "Хорошего дня!")
            self.assertIn("Хорошего понедельника!", response.text)
            self.assertNotIn("Хорошего дня! Хорошего понедельника!", response.text)