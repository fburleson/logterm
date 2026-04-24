from collections import deque
from datetime import timezone

from rich import box
from rich.highlighter import ReprHighlighter
from rich.table import Table
from rich.text import Text
from textual.containers import VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import DataTable, Footer, Static

from logterm import Log
from logterm.core.log.stream import LogStream


def _log_to_table(log: Log) -> Static:
    highlighter = ReprHighlighter()
    title: Text = highlighter(Text.from_markup(f"{log:rich}"))
    title.stylize("bold")
    table = Table(
        title=title,
        title_justify="left",
        expand=True,
        show_header=False,
        box=box.HORIZONTALS,
    )
    table.add_column("key")
    table.add_column("value")
    for key, value in log.metadata.items():
        table.add_row(highlighter(key), highlighter(str(value)))
    return Static(table)


class MetadataModal(ModalScreen):
    BINDINGS = [("enter", "app.pop_screen", "Close")]

    def __init__(self, log: Log):
        super().__init__()
        self._log: Log = log

    def compose(self):
        with VerticalScroll():
            yield _log_to_table(self._log)
        yield Footer()


class LogTable(DataTable):
    COLUMNS: tuple[str, ...] = ("datetime", "level", "event")
    DT_FMT: str = "%Y-%m-%d %H:%M:%S%:z"

    def __init__(self, stream: LogStream, tz: timezone = timezone.utc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stream = stream
        self._tz: timezone = tz
        self._highlighter = ReprHighlighter()
        self._logs: deque[Log] = deque()

    def on_mount(self):
        self.cursor_type = "row"
        self.add_columns(*LogTable.COLUMNS)
        self.update_logs()

    def on_unmount(self):
        self._stream.close()

    def update_logs(self):
        if self._stream:
            for log in self._stream:
                self.add_row(
                    self._highlighter(
                        log.datetime.astimezone(self._tz).strftime(LogTable.DT_FMT)
                    ),
                    f"{log.level:rich}",
                    self._highlighter(log.event),
                )
                self._logs.append(log)

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        log: Log = self._logs[event.cursor_row]
        self.app.push_screen(MetadataModal(log))
