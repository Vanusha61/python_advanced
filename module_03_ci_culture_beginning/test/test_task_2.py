from unittest import TestCase

from module_03_ci_culture_beginning.homework.hw2.decrypt import decrypt

class TestDecrypt(TestCase):

    def test_all_cases(self):
        cases = [
            ("абра-кадабра.", "абра-кадабра"),
            ("абраа..-кадабра", "абра-кадабра"),
            ("абраа..-.кадабра", "абра-кадабра"),
            ("абра--..кадабра", "абра-кадабра"),
            ("абрау...-кадабра", "абра-кадабра"),
            ("абра........", ""),
            ("абр......a.", "a"),
            ("1..2.3", "23"),
            (".", ""),
            ("1.......................", ""),
        ]

        for input_str, expected in cases:
            with self.subTest(input=input_str):
                self.assertEqual(decrypt(input_str), expected)
