import datetime

class Person:
    def __init__(self, name: str, year_of_birth: int, address: str = '') -> None:
        self._name: str = name
        self._yob: int = year_of_birth
        self._address: str = address

    def get_age(self) -> int:
        now: datetime.datetime = datetime.datetime.now()
        return now.year - self._yob

    def get_name(self) -> str:
        return self._name

    def set_name(self, name: str) -> None:
        self._name = name

    def set_address(self, address: str) -> None:
        self._address = address

    def get_address(self) -> str:
        return self._address

    def is_homeless(self) -> bool:
        '''
        returns True if address is not set, false in other case
        '''
        return self._address is None
