from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any, ClassVar

from rich.text import Text


@dataclass
class Log:
    DT_FMT: ClassVar[str] = "%Y-%m-%d %H:%M:%S%:z"

    class Level(StrEnum):
        INFO = ("info", "green")
        WARNING = ("warning", "yellow")
        ERROR = ("error", "red")
        CRITICAL = ("critical", "red bold")
        DEBUG = ("debug", "dim")

        def __new__(cls, value: str, style: str):
            obj = str.__new__(cls, value)
            obj._value_ = value
            return obj

        def __init__(self, _, style: str):
            self._style: str = style

        def __format__(self, format_spec: str):
            if format_spec == "rich":
                return self.__rich__()
            return super().__format__(format_spec)

        def __rich__(self):
            return f"[{self._style}]{self}[/]"

    datetime: datetime
    level: Level
    event: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __getattr__(self, name: str):
        try:
            return self.metadata[name]
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    def __getitem__(self, key: str):
        return self.__getattribute__(key)

    def __format__(self, format_spec: str):
        if format_spec == "rich":
            return self.__rich__()
        return super().__format__(format_spec)

    def __rich__(self) -> str:
        level = Text(f"{self.level:rich}", justify="left")
        level.pad_right(10 - len(str(self.level)))
        return f"{self.datetime.strftime(Log.DT_FMT)} \[{level}] {self.event}"
