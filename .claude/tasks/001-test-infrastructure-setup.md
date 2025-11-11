# Task 001: Simple Test Infrastructure Setup

## Status
- [ ] Not Started
- Dependencies: 000
- Estimated Effort: 2 hours
- Can Run in Parallel: No

## Objective

Set up minimal test infrastructure with fixtures for Toggl time entry data and basic test utilities using Result types from the returns library.

## Context

We need a simple test setup focused on data transformation testing. According to the user requirements:
- No authentication testing needed (Toggl API is reliable)
- No API format validation needed (API is strict and solid)
- Focus on transformation from Toggl schema to InfluxDB schema
- Use pydantic contracts from Task 000 for type safety
- Use returns library for functional error handling

## Implementation Details

### Files to Create
- `src/tests/conftest.py` - Pytest configuration with basic fixtures
- `src/tests/fixtures/sample_data.py` - Sample Toggl time entry data

### Files to Modify
- None (all new files)

### Key Functions/Classes to Implement

#### conftest.py
- **Purpose**: Configure pytest and provide base fixtures
- **Configuration**:
  ```python
  import pytest
  from typing import List
  from toggle_pulse.contracts.toggl import TogglTimeEntry
  from tests.fixtures.sample_data import (
      get_complete_entry,
      get_minimal_entry,
      get_running_entry,
      get_entries_batch
  )

  @pytest.fixture
  def complete_time_entry() -> TogglTimeEntry:
      """Fixture for a complete time entry with all fields"""
      return get_complete_entry()

  @pytest.fixture
  def minimal_time_entry() -> TogglTimeEntry:
      """Fixture for minimal time entry with required fields only"""
      return get_minimal_entry()

  @pytest.fixture
  def running_time_entry() -> TogglTimeEntry:
      """Fixture for currently running time entry"""
      return get_running_entry()

  @pytest.fixture
  def batch_time_entries() -> List[TogglTimeEntry]:
      """Fixture for batch of diverse time entries"""
      return get_entries_batch()
  ```

#### fixtures/sample_data.py
- **Purpose**: Factory functions for creating test data
- **Functions**:

  1. **get_complete_entry()**
     ```python
     def get_complete_entry() -> TogglTimeEntry:
         """Create time entry with all fields populated"""
         return TogglTimeEntry(
             id=123456789,
             workspace_id=12345,
             project_id=67890,
             description="Working on feature X",
             start=datetime(2025, 1, 1, 8, 0, 0, tzinfo=timezone.utc),
             stop=datetime(2025, 1, 1, 10, 30, 0, tzinfo=timezone.utc),
             duration=9000,
             billable=True,
             tags=["development", "backend"],
             user_id=98765,
             created_with="web"
         )
     ```

  2. **get_minimal_entry()**
     ```python
     def get_minimal_entry() -> TogglTimeEntry:
         """Create entry with only required fields"""
         return TogglTimeEntry(
             id=987654321,
             workspace_id=12345,
             start=datetime(2025, 1, 2, 14, 0, 0, tzinfo=timezone.utc),
             stop=datetime(2025, 1, 2, 15, 0, 0, tzinfo=timezone.utc),
             duration=3600
         )
     ```

  3. **get_running_entry()**
     ```python
     def get_running_entry() -> TogglTimeEntry:
         """Create currently running time entry"""
         start_time = datetime.now(timezone.utc) - timedelta(hours=1)
         return TogglTimeEntry(
             id=111222333,
             workspace_id=12345,
             project_id=67890,
             description="Current task",
             start=start_time,
             stop=None,  # Running entry has no stop time
             duration=-3600,  # Negative duration for running
             billable=False,
             tags=["urgent"]
         )
     ```

  4. **get_entries_batch()**
     ```python
     def get_entries_batch() -> List[TogglTimeEntry]:
         """Create diverse batch of entries for testing"""
         return [
             get_complete_entry(),
             get_minimal_entry(),
             get_running_entry(),
             # Entry with no project
             TogglTimeEntry(
                 id=444555666,
                 workspace_id=12345,
                 description="Admin work",
                 start=datetime(2025, 1, 3, 9, 0, 0, tzinfo=timezone.utc),
                 stop=datetime(2025, 1, 3, 10, 0, 0, tzinfo=timezone.utc),
                 duration=3600,
                 billable=False
             ),
             # Entry with special characters
             TogglTimeEntry(
                 id=777888999,
                 workspace_id=12345,
                 project_id=11111,
                 description="Bug fix: Issue #123 | \"Quote\" test",
                 start=datetime(2025, 1, 4, 13, 0, 0, tzinfo=timezone.utc),
                 stop=datetime(2025, 1, 4, 14, 30, 0, tzinfo=timezone.utc),
                 duration=5400,
                 billable=True,
                 tags=["bugfix", "high-priority"]
             )
         ]
     ```

  5. **create_raw_toggl_json()**
     ```python
     def create_raw_toggl_json() -> dict:
         """Create raw JSON as returned by Toggl API"""
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
             "at": "2025-01-01T10:30:15Z"
         }
     ```

### Algorithm/Approach

1. Create simple pytest configuration without complex async setup
2. Define factory functions for generating test data
3. Use pydantic models from Task 000 for type safety
4. Provide various entry types (complete, minimal, running, special)
5. Include raw JSON factory for testing deserialization

### Integration Points

- Uses pydantic contracts from Task 000
- Provides fixtures used by transformation tests in Task 004
- Compatible with returns library Result types
- Simple enough to not require mocking infrastructure

## Testing Requirements

### Test Files
- `src/tests/test_test_infrastructure.py` - Verify fixtures work correctly

### Test Cases

1. **Test Fixture Loading**
   - Input: Import all fixtures
   - Expected Output: All fixtures instantiate without error
   - Verification: Assert fixtures return correct types

2. **Test Data Validity**
   - Input: Each fixture
   - Expected Output: Valid TogglTimeEntry models
   - Verification: Pydantic validation passes

3. **Test Running Entry Properties**
   - Input: running_time_entry fixture
   - Expected Output: stop=None, duration<0
   - Verification: is_running() returns True

### Fixtures Needed
- Self-contained within this task

## Acceptance Criteria

- [ ] conftest.py provides basic fixtures
- [ ] All fixtures return valid pydantic models
- [ ] Sample data covers all common scenarios
- [ ] Raw JSON factory matches actual Toggl format
- [ ] No authentication or HTTP mocking needed
- [ ] Simple and maintainable test setup
- [ ] All infrastructure tests pass

## Notes

- Keep infrastructure minimal and focused
- No need for HTTP mocking or async complexity
- Focus on data transformation testing support
- Use realistic sample data based on actual Toggl responses
- Ensure timezone-aware datetime objects

## References

- Task 000 (Pydantic contracts)
- PROJECT_OVERVIEW.md:191-205 (Toggl API response format)
- pytest documentation for fixtures