"""Module with some typical mistakes. They aimed to be find by linters."""
import multiprocessing
import sys
import tempfile
from typing import Optional

import flask
from third_party import (
    lib1,
    lib2,
    lib3,
    lib4,
    lib5,
    lib6,
    lib7,
    lib8,
    lib9,
    lib10,
    lib11,
    lib12,
    lib13,
    lib14,
    lib15,
)


class BadClass:
    value: str = 42

    def get_value(self) -> "BadClass":
        return "some_other_value"

    def compute_something(self) -> None:
        if self.value == 42:
            return True
        else:
            return False

    def it_will_fail(self):
        return self.other_value


def viking_cafe_order(spam: None, beans: str, eggs: Optional[str] = None)\
        -> str:
    del beans, eggs
    return spam + spam + spam


import tempfile


def compute_other_thing():
    try: 1 / 0
    except: print("oops")
