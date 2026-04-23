from collections import deque
from io import TextIOWrapper
from pathlib import Path
from typing import Any, Callable, Iterable, Self

from logterm.core.fmt import from_jsonl
from logterm.core.log.log import Log


class LogDeque(deque[Log]):
    def __init__(self, logs: Iterable[Log] = tuple(), maxlen: int | None = None):
        super().__init__(logs, maxlen)

    def __rich__(self):
        return "\n".join([f"{log:rich}" for log in self]).rstrip()


class LogStream:
    def __init__(
        self,
        path: Path,
        *,
        maxlen: int | None = None,
        fmt_func: Callable[..., Log] = from_jsonl,
        **fmt_kwargs: Any,
    ):
        self._file: TextIOWrapper = open(path, mode="r")
        self._fmt_func: Callable[..., Log] = fmt_func
        self._fmt_kwargs: dict[str, Any] = fmt_kwargs
        self._data: LogDeque = LogDeque(maxlen=maxlen)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._file.close()

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> Log:
        log: Log = self._fmt_func(next(self._file), **self._fmt_kwargs)
        self._data.append(log)
        return log

    @property
    def data(self) -> LogDeque:
        return LogDeque(self._data, maxlen=self._data.maxlen)
