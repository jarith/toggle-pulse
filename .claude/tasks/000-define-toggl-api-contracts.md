# Task 000: Define Toggl API Pydantic Contracts

## Status
- [ ] Not Started
- Dependencies: None
- Estimated Effort: 2-3 hours
- Can Run in Parallel: No

## Objective

Define comprehensive Pydantic contracts for the Toggl API data structures to ensure type safety and data validation throughout the application.

## Context

According to PROJECT_OVERVIEW.md:186-205, the Toggl API returns time entry data in a specific JSON format. We need to create Pydantic models that:
- Accurately represent the Toggl API response structure
- Handle optional fields appropriately
- Validate data types and formats (especially ISO 8601 timestamps)
- Provide a foundation for safe data transformation to InfluxDB format

The contracts will be used by both the Toggl client and the transformation logic, ensuring type safety across the entire data pipeline.

## Implementation Details

### Files to Create
- `src/toggle_pulse/contracts/toggl.py` - Pydantic models for Toggl API data

### Files to Modify
- None (new file)

### Key Functions/Classes to Implement

#### TogglTimeEntry
- **Purpose**: Main model representing a single Toggl time entry
- **Fields**:
  ```python
  class TogglTimeEntry(BaseModel):
      id: int
      workspace_id: int
      project_id: Optional[int] = None
      description: Optional[str] = ""
      start: datetime  # ISO 8601 string auto-parsed to datetime
      stop: Optional[datetime] = None  # None for running entries
      duration: int  # Seconds (negative for running)
      billable: bool = False
      tags: Optional[List[str]] = None
      user_id: Optional[int] = None
      created_with: Optional[str] = None
      at: Optional[datetime] = None  # Last update timestamp
  ```
- **Validation**:
  - `start` must be valid ISO 8601 timestamp
  - `stop` can be None (for running entries) or valid ISO 8601
  - `duration` must be integer (negative indicates running)
  - `tags` should be None or list of strings (not empty list)

#### TogglTimeEntriesResponse
- **Purpose**: Container for list of time entries from API
- **Fields**:
  ```python
  class TogglTimeEntriesResponse(BaseModel):
      __root__: List[TogglTimeEntry]
  ```
- **Methods**:
  - `__iter__()` - Allow iteration over entries
  - `__len__()` - Return count of entries
  - `__getitem__()` - Support indexing

#### TogglWorkspace
- **Purpose**: Model for workspace information
- **Fields**:
  ```python
  class TogglWorkspace(BaseModel):
      id: int
      name: str
      organization_id: Optional[int] = None
  ```

#### TogglProject
- **Purpose**: Model for project information
- **Fields**:
  ```python
  class TogglProject(BaseModel):
      id: int
      name: str
      workspace_id: int
      active: bool = True
      color: Optional[str] = None
      client_id: Optional[int] = None
  ```

#### Configuration Classes
- **Purpose**: Shared configuration for all models
- **Implementation**:
  ```python
  class TogglBaseModel(BaseModel):
      class Config:
          # Allow population by field name or alias
          allow_population_by_field_name = True
          # Use ISO 8601 for datetime serialization
          json_encoders = {
              datetime: lambda v: v.isoformat()
          }
          # Validate on assignment
          validate_assignment = True
          # Use enum values directly
          use_enum_values = True
  ```

### Algorithm/Approach

1. Define base configuration class with common settings
2. Create core data models inheriting from base
3. Add field validators for complex validation logic:
   - Validate ISO 8601 timestamp formats
   - Ensure duration matches running state (negative when stop is None)
   - Convert empty strings to None for optional fields
4. Add helper methods for common operations:
   - `is_running()` - Check if entry is currently running
   - `calculate_duration()` - Compute duration from start/stop
5. Include model examples in docstrings for clarity

### Integration Points

- Used by `toggl_client.py` to parse API responses
- Used by `transformer.py` to ensure type-safe transformation
- Used in tests to create valid test data fixtures
- Provides validation for all Toggl API data entering the system

## Testing Requirements

### Test Files
- `src/tests/unit/test_toggl_contracts.py` - Unit tests for contracts

### Test Cases

1. **Valid Complete Entry**
   - Input: JSON with all fields populated
   - Expected Output: Successfully parsed TogglTimeEntry
   - Verification: All fields accessible with correct types

2. **Minimal Required Fields**
   - Input: JSON with only required fields
   - Expected Output: Model with defaults for optional fields
   - Verification: Optional fields are None or default values

3. **Running Entry Validation**
   - Input: Entry with stop=null, duration=-3600
   - Expected Output: Valid model with is_running() = True
   - Verification: Duration is negative, stop is None

4. **ISO 8601 Parsing Variations**
   - Input: Various valid ISO 8601 formats:
     - "2025-01-01T12:00:00Z"
     - "2025-01-01T12:00:00+00:00"
     - "2025-01-01T12:00:00-05:00"
   - Expected Output: All parse to correct datetime
   - Verification: Timezone info preserved

5. **Invalid Data Rejection**
   - Input: Invalid field types, malformed dates
   - Expected Output: ValidationError raised
   - Verification: Error message describes issue

6. **Tags Field Handling**
   - Input: tags as null, [], ["tag1", "tag2"]
   - Expected Output: None for null, None for [], list for valid
   - Verification: Empty list normalized to None

### Fixtures Needed
- Sample JSON responses from actual Toggl API
- Edge case entries (running, minimal, complete)

## Acceptance Criteria

- [ ] All Toggl API fields are represented in models
- [ ] Optional fields use Optional[T] with appropriate defaults
- [ ] ISO 8601 timestamps parse correctly with timezone support
- [ ] Running entries validated (stop=None, duration<0)
- [ ] Empty arrays/strings normalized to None
- [ ] Models are immutable after creation (frozen=True)
- [ ] Comprehensive field validation with clear error messages
- [ ] 100% test coverage for all model validations
- [ ] Type hints pass mypy/pyright strict mode

## Notes

- Toggl API uses ISO 8601 (RFC 3339 subset) for all timestamps
- Duration is in seconds, negative for currently running entries
- Tags field can be null or array, never empty array in practice
- Consider using pydantic.Field for additional validation constraints
- All models should inherit from common base for consistency
- Use Result type from returns library for parse operations

## References

- PROJECT_OVERVIEW.md:191-205 (Toggl API response format)
- Pydantic documentation on datetime handling
- ISO 8601/RFC 3339 specification for timestamp formats