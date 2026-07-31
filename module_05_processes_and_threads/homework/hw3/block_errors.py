"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    def __init__(self, error: set[Exception]) -> None:
        self.error = error

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type in self.error or Exception in self.error:
            return True
        return False