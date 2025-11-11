import pytest

from tests.fixtures.sample_data import (
    get_complete_entry,
    get_entries_batch,
    get_minimal_entry,
    get_running_entry,
)
from toggle_pulse.contracts.toggl import TogglTimeEntry


@pytest.fixture
def complete_time_entry() -> TogglTimeEntry:
    return get_complete_entry()


@pytest.fixture
def minimal_time_entry() -> TogglTimeEntry:
    return get_minimal_entry()


@pytest.fixture
def running_time_entry() -> TogglTimeEntry:
    return get_running_entry()


@pytest.fixture
def batch_time_entries() -> list[TogglTimeEntry]:
    return get_entries_batch()
