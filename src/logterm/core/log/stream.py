from io import TextIOWrapper
from pathlib import Path
from typing import Callable, Self

from logterm.core.fmt import from_jsonl
from logterm.core.log.log import Log


class LogStream:
    def __init__(
        self,
        path: Path,
        *,
        fmt_func: Callable[..., Log] = from_jsonl,
    ):
        self._file: TextIOWrapper = open(path, mode="r")
        self._fmt_func: Callable[..., Log] = fmt_func

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Log:
        log: Log = self._fmt_func(next(self._file))
        return log

    def close(self):
        return self._file.close()
