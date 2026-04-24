from argparse import ArgumentParser, Namespace
from datetime import datetime
from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from logterm.app.widgets.logtable import LogTable
from logterm.core.log.stream import LogStream


class LogTerm(App):
    BINDINGS = [("escape", "quit", "Quit")]

    def __init__(self, stream: LogStream, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stream: LogStream = stream

    def compose(self) -> ComposeResult:
        yield Header()
        yield LogTable(
            self._stream,
            datetime.now().tzinfo,  # type: ignore
        )
        yield Footer()

    def on_mount(self) -> None:
        self.sub_title = str(Path(self._stream._file.name).resolve())
        log_table = self.query_one(LogTable)
        self.set_interval(1, log_table.update_logs)


def _cli():
    parser = ArgumentParser()
    parser.add_argument("file", help="The log file.")
    args: Namespace = parser.parse_args()
    run(args.file)


def run(file: Path):
    LogTerm(LogStream(Path(file))).run()
