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
    BINDINGS = [
        ("i", "toggle_info", Log.Level.INFO),
        ("w", "toggle_warning", Log.Level.WARNING),
        ("e", "toggle_error", Log.Level.ERROR),
        ("c", "toggle_critical", Log.Level.CRITICAL),
        ("d", "toggle_debug", Log.Level.DEBUG),
    ]

    def __init__(self, stream: LogStream, tz: timezone = timezone.utc, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stream = stream
        self._tz: timezone = tz
        self._highlighter = ReprHighlighter()
        self._logs: deque[Log] = deque()
        self._filtered_logs: list[Log] = list()
        self._log_levels: set[Log.Level] = {
            Log.Level.INFO,
            Log.Level.ERROR,
            Log.Level.WARNING,
            Log.Level.CRITICAL,
        }

    def on_mount(self):
        self.cursor_type = "row"
        self.add_columns(*LogTable.COLUMNS)
        self._update_border_title()
        self.update_logs()

    def on_unmount(self):
        self._stream.close()

    def _add_log(self, log: Log):
        self.add_row(
            self._highlighter(
                log.datetime.astimezone(self._tz).strftime(LogTable.DT_FMT)
            ),
            f"{log.level:rich}",
            self._highlighter(log.event),
        )

    def _update_filtered(self):
        self._filtered_logs = [
            log for log in self._logs if log.level in self._log_levels
        ]
        self._update_border_title()
        self.refresh_logs()

    def update_logs(self):
        if self._stream:
            for log in self._stream:
                self._logs.append(log)
                if log.level in self._log_levels:
                    self._filtered_logs.append(log)
                    self._add_log(log)

    def refresh_logs(self):
        self.clear()
        for log in self._filtered_logs:
            self._add_log(log)

    def _update_border_title(self):
        levels = ", ".join(sorted(str(level) for level in self._log_levels))
        self.border_title = f"Filter: {levels}"

    def _toggle_level(self, level: Log.Level):
        if level in self._log_levels:
            self._log_levels.discard(level)
        else:
            self._log_levels.add(level)
        self._update_filtered()
        self.refresh_logs()

    def action_toggle_info(self):
        self._toggle_level(Log.Level.INFO)

    def action_toggle_warning(self):
        self._toggle_level(Log.Level.WARNING)

    def action_toggle_error(self):
        self._toggle_level(Log.Level.ERROR)

    def action_toggle_critical(self):
        self._toggle_level(Log.Level.CRITICAL)

    def action_toggle_debug(self):
        self._toggle_level(Log.Level.DEBUG)

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        log: Log = self._filtered_logs[event.cursor_row]
        self.app.push_screen(MetadataModal(log))
