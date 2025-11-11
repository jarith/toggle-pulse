from datetime import datetime

from returns.result import Failure, safe

from toggle_pulse.contracts.influxdb import InfluxDBBatch, InfluxDBPoint
from toggle_pulse.contracts.toggl import TogglTimeEntry


def format_timestamp(dt: datetime) -> int:
    if dt.tzinfo is None:
        msg = "datetime must be timezone-aware"
        raise ValueError(msg)

    return int(dt.timestamp() * 1000)


def sanitize_tag_value(value: str) -> str:
    return value.replace(",", ";").strip()


def build_tags(entry: TogglTimeEntry) -> dict[str, str]:
    tags: dict[str, str] = {
        "workspace_id": str(entry.workspace_id),
        "project_id": str(entry.project_id) if entry.project_id else "unknown",
        "billable": "true" if entry.billable else "false",
    }

    if entry.tags:
        tags["tags"] = "|".join(entry.tags)

    return tags


def build_fields(entry: TogglTimeEntry) -> dict[str, int | float | str | bool]:
    return {
        "duration": entry.duration,
        "description": entry.description,
    }


@safe
def transform_time_entry(entry: TogglTimeEntry) -> InfluxDBPoint:
    return InfluxDBPoint(
        measurement="toggl_time_entry",
        tags=build_tags(entry),
        fields=build_fields(entry),
        time=format_timestamp(entry.start),
    )


@safe
def transform_batch(
    entries: list[TogglTimeEntry],
) -> InfluxDBBatch:
    points: list[InfluxDBPoint] = []

    for entry in entries:
        result = transform_time_entry(entry)
        if isinstance(result, Failure):
            raise result.failure()
        points.append(result.unwrap())

    return InfluxDBBatch(points=points)
