from datetime import UTC, datetime, timedelta

from toggle_pulse.contracts.toggl import TogglTimeEntry


def get_complete_entry() -> TogglTimeEntry:
    return TogglTimeEntry(
        id=123456789,
        workspace_id=12345,
        project_id=67890,
        description="Working on feature X",
        start=datetime(2025, 1, 1, 8, 0, 0, tzinfo=UTC),
        stop=datetime(2025, 1, 1, 10, 30, 0, tzinfo=UTC),
        duration=9000,
        billable=True,
        tags=["development", "backend"],
        user_id=98765,
        created_with="web",
    )


def get_minimal_entry() -> TogglTimeEntry:
    return TogglTimeEntry(
        id=987654321,
        workspace_id=12345,
        start=datetime(2025, 1, 2, 14, 0, 0, tzinfo=UTC),
        stop=datetime(2025, 1, 2, 15, 0, 0, tzinfo=UTC),
        duration=3600,
    )


def get_running_entry() -> TogglTimeEntry:
    start_time = datetime.now(UTC) - timedelta(hours=1)
    return TogglTimeEntry(
        id=111222333,
        workspace_id=12345,
        project_id=67890,
        description="Current task",
        start=start_time,
        stop=None,
        duration=-3600,
        billable=False,
        tags=["urgent"],
    )


def get_entries_batch() -> list[TogglTimeEntry]:
    return [
        get_complete_entry(),
        TogglTimeEntry(
            id=444555666,
            workspace_id=12345,
            description="Admin work",
            start=datetime(2025, 1, 3, 9, 0, 0, tzinfo=UTC),
            stop=datetime(2025, 1, 3, 10, 0, 0, tzinfo=UTC),
            duration=3600,
            billable=False,
        ),
        get_minimal_entry(),
        get_running_entry(),
        TogglTimeEntry(
            id=777888999,
            workspace_id=12345,
            project_id=11111,
            description='Bug fix: Issue #123 | "Quote" test',
            start=datetime(2025, 1, 4, 13, 0, 0, tzinfo=UTC),
            stop=datetime(2025, 1, 4, 14, 30, 0, tzinfo=UTC),
            duration=5400,
            billable=True,
            tags=["bugfix", "high-priority"],
        ),
    ]


def create_raw_toggl_json() -> dict[str, object]:
    return {
        "id": 123456789,
        "workspace_id": 12345,
        "project_id": 67890,
        "description": "Working on feature X",
        "start": "2025-01-01T08:00:00Z",
        "stop": "2025-01-01T10:30:00Z",
        "duration": 9000,
        "billable": True,
        "tags": ["development", "backend"],
        "user_id": 98765,
        "created_with": "web",
        "at": "2025-01-01T10:30:15Z",
    }
