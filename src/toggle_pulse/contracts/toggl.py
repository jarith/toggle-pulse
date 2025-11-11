from collections.abc import Iterator
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class TogglBaseModel(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        validate_assignment=True,
    )


class TogglTimeEntry(TogglBaseModel):
    id: int
    workspace_id: int
    project_id: int | None = None
    description: str = ""
    start: datetime
    stop: datetime | None = None
    duration: int
    billable: bool = False
    tags: list[str] | None = None
    user_id: int | None = None
    created_with: str | None = None
    at: datetime | None = None

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v: list[str] | None) -> list[str] | None:
        if v is not None and len(v) == 0:
            return None
        return v

    @field_validator("description", mode="before")
    @classmethod
    def normalize_description(cls, v: str | None) -> str:
        if v is None:
            return ""
        return v

    def is_running(self) -> bool:
        return self.stop is None

    def calculate_duration(self) -> int:
        if not self.is_running():
            return self.duration

        now = datetime.now(UTC)
        elapsed = now - self.start
        return int(elapsed.total_seconds())


class TogglTimeEntriesResponse(BaseModel):
    root: list[TogglTimeEntry]

    model_config = ConfigDict(frozen=True)

    def __init__(
        self,
        root: list[dict[str, Any] | TogglTimeEntry] | None = None,
        **data: dict[str, list[TogglTimeEntry]],
    ) -> None:
        if root is not None:
            entries = [
                TogglTimeEntry(**entry) if isinstance(entry, dict) else entry for entry in root
            ]
            super().__init__(root=entries)
        else:
            super().__init__(**data)

    def __iter__(self) -> Iterator[TogglTimeEntry]:  # type: ignore[override]
        return iter(self.root)

    def __len__(self) -> int:
        return len(self.root)

    def __getitem__(self, index: int) -> TogglTimeEntry:
        return self.root[index]


class TogglWorkspace(TogglBaseModel):
    id: int
    name: str
    organization_id: int | None = None


class TogglProject(TogglBaseModel):
    id: int
    name: str
    workspace_id: int
    active: bool = True
    color: str | None = None
    client_id: int | None = None
