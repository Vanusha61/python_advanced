from unittest import TestCase

from module_03_ci_culture_beginning.homework.hw4.person import Person

class TestPerson(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.name: str = "Test"
        cls.yob: int = 2008
        cls.address: str = ""
        cls.person: Person = Person(cls.name, cls.yob, cls.address)

    def test_init(self) -> None:
        self.assertEqual(self.person._name, self.name)
        self.assertEqual(self.person._yob, self.yob)
        self.assertEqual(self.person._address, self.address)

    def test_get_age(self) -> None:
        self.assertEqual(self.person.get_age(), 18)

    def test_get_name(self) -> None:
        self.assertEqual(self.person.get_name(), "Test")

    def test_get_address(self) -> None:
        self.assertEqual(self.person.get_address(), "")

    def test_set_name(self) -> None:
        self.person.set_name("Test1")
        self.assertEqual(self.person.get_name(), "Test1")

    def test_set_address(self) -> None:
        self.person.set_address("1")
        self.assertEqual(self.person.get_address(), "1")

    def test_is_homeless(self) -> None:
        self.assertFalse(self.person.is_homeless())