import json
from datetime import datetime

from logterm import Log


def from_jsonl(
    entry: str,
    *,
    event: str = "event",
    dt: str = "datetime",
    level: str = "level",
) -> Log:
    log: dict[str, str] = json.loads(entry)
    metadata = {k: v for k, v in log.items() if k not in {event, dt, level}}
    return Log(
        datetime.fromisoformat(log[dt]), Log.Level(log[level]), log[event], metadata
    )
