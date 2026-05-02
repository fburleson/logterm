import json
from datetime import datetime, timezone

from logterm import Log


def from_jsonl(
    entry: str,
    *,
    event: str = "event",
    dt: str = "timestamp",
    level: str = "level",
    tz: timezone = timezone.utc,
) -> Log:
    log: dict[str, str] = json.loads(entry)
    metadata = {k: v for k, v in log.items() if k not in {event, dt, level}}
    return Log(
        datetime.fromisoformat(log[dt]).astimezone(tz),
        Log.Level(log[level]),
        log[event],
        metadata,
    )
