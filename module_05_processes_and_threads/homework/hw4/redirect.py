"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""

from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, *, file_stdout = None, file_stderr = None):
        self.file_stdout = file_stdout
        self.file_stderr = file_stderr
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

    def __enter__(self):
        if self.file_stdout is not None:
            sys.stdout = self.file_stdout
        if self.file_stderr is not None:
            sys.stderr = self.file_stderr

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_val, exc_tb, file=sys.stderr)
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        return True
