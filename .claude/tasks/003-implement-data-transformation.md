# Task 003: Implement Data Transformation Logic

## Status
- [ ] Not Started
- Dependencies: 000
- Estimated Effort: 3 hours
- Can Run in Parallel: No

## Objective

Implement the transformation logic that converts Toggl time entries (using pydantic contracts) into InfluxDB point format, handling all field mappings and type conversions.

## Context

According to PROJECT_OVERVIEW.md:641-675 and the field mapping table at lines 207-218, we need to transform:
- Toggl API time entries → InfluxDB time series points
- Convert ISO 8601 timestamps → Unix milliseconds
- Map fields to appropriate tags and fields
- Handle null/missing values with sensible defaults
- Transform arrays (tags) to pipe-separated strings

This is the core data transformation that prepares Toggl data for time series storage.

## Implementation Details

### Files to Create
- `src/toggle_pulse/transformers/influxdb.py` - Transformation logic
- `src/toggle_pulse/contracts/influxdb.py` - InfluxDB point contracts

### Files to Modify
- None (new files)

### Key Functions/Classes to Implement

#### contracts/influxdb.py

1. **InfluxDBPoint**
   ```python
   class InfluxDBPoint(BaseModel):
       """Represents a single InfluxDB data point."""
       measurement: str
       tags: Dict[str, str]  # All tag values must be strings
       fields: Dict[str, Union[str, int, float, bool]]
       time: int  # Unix timestamp in milliseconds

       class Config:
           frozen = True  # Immutable after creation

       def to_line_protocol(self) -> str:
           """Convert to InfluxDB line protocol format."""
           # Format: measurement,tag1=val1,tag2=val2 field1=val1,field2=val2 timestamp
   ```

2. **InfluxDBBatch**
   ```python
   class InfluxDBBatch(BaseModel):
       """Container for batch of InfluxDB points."""
       points: List[InfluxDBPoint]

       def __len__(self) -> int:
           return len(self.points)

       def to_line_protocol(self) -> str:
           """Convert all points to line protocol format."""
           return "\n".join(point.to_line_protocol() for point in self.points)
   ```

#### transformers/influxdb.py

1. **transform_time_entry()**
   ```python
   def transform_time_entry(entry: TogglTimeEntry) -> Result[InfluxDBPoint, Exception]:
       """
       Transform a single Toggl time entry to InfluxDB point.

       Args:
           entry: Toggl time entry from API

       Returns:
           Result[InfluxDBPoint, Exception]: Success with point or Failure with error

       Field Mappings:
           - start → time (Unix ms)
           - duration → fields.duration (seconds)
           - description → fields.description (string, empty if None)
           - project_id → tags.project_id (string, "unknown" if None)
           - workspace_id → tags.workspace_id (string)
           - billable → tags.billable ("true" or "false")
           - tags → tags.tags (pipe-separated, omitted if empty)
       """
       try:
           # Convert timestamp to Unix milliseconds
           timestamp_ms = int(entry.start.timestamp() * 1000)

           # Build tags (all must be strings)
           tags = {
               "workspace_id": str(entry.workspace_id)
           }

           # Add project_id with default
           tags["project_id"] = str(entry.project_id) if entry.project_id else "unknown"

           # Convert billable to string
           tags["billable"] = "true" if entry.billable else "false"

           # Handle tags array
           if entry.tags and len(entry.tags) > 0:
               tags["tags"] = "|".join(entry.tags)

           # Build fields
           fields = {
               "duration": entry.duration,
               "description": entry.description or ""
           }

           point = InfluxDBPoint(
               measurement="toggl_time_entry",
               tags=tags,
               fields=fields,
               time=timestamp_ms
           )

           return Success(point)

       except Exception as e:
           return Failure(e)
   ```

2. **transform_batch()**
   ```python
   def transform_batch(
       entries: List[TogglTimeEntry]
   ) -> Result[InfluxDBBatch, Exception]:
       """
       Transform batch of Toggl entries to InfluxDB points.

       Args:
           entries: List of Toggl time entries

       Returns:
           Result[InfluxDBBatch, Exception]: Success with batch or Failure

       Notes:
           - Continues processing on individual failures
           - Returns Failure only if all transformations fail
           - Logs warnings for individual failures
       """
       points = []
       failures = []

       for entry in entries:
           result = transform_time_entry(entry)
           if isinstance(result, Success):
               points.append(result.unwrap())
           else:
               failures.append((entry.id, result.failure()))

       if not points and failures:
           return Failure(Exception(f"All {len(failures)} transformations failed"))

       if failures:
           # Log warnings for partial failures
           for entry_id, error in failures:
               logger.warning(f"Failed to transform entry {entry_id}: {error}")

       return Success(InfluxDBBatch(points=points))
   ```

3. **Helper Functions**

   ```python
   def sanitize_tag_value(value: str) -> str:
       """
       Sanitize tag value for InfluxDB.

       - Remove leading/trailing whitespace
       - Replace commas with semicolons (InfluxDB restriction)
       - Escape special characters if needed
       """
       return value.strip().replace(",", ";")

   def format_timestamp(dt: datetime) -> int:
       """
       Convert datetime to Unix milliseconds.

       Args:
           dt: Timezone-aware datetime

       Returns:
           Unix timestamp in milliseconds

       Raises:
           ValueError: If datetime is not timezone-aware
       """
       if dt.tzinfo is None:
           raise ValueError("Datetime must be timezone-aware")
       return int(dt.timestamp() * 1000)

   def validate_measurement_name(name: str) -> bool:
       """
       Validate InfluxDB measurement name.

       Rules:
       - Cannot start with underscore
       - Cannot contain spaces
       - Must be non-empty
       """
       return (
           name and
           not name.startswith("_") and
           " " not in name
       )
   ```

### Algorithm/Approach

1. **Single Entry Transformation**:
   - Extract timestamp from start field
   - Convert to Unix milliseconds
   - Map all tag fields as strings
   - Apply defaults for missing values
   - Combine arrays into pipe-separated strings
   - Return InfluxDBPoint wrapped in Result

2. **Batch Processing**:
   - Transform each entry individually
   - Collect successes and failures
   - Continue on individual failures
   - Return batch of successful transforms
   - Log warnings for failures

3. **Error Handling**:
   - Use Result type for all operations
   - Validate timezone-aware datetimes
   - Sanitize tag values for InfluxDB
   - Handle None/null gracefully

### Integration Points

- Uses pydantic contracts from Task 000 (TogglTimeEntry)
- Provides InfluxDBPoint for database writing
- Compatible with returns library Result types
- Used by main pipeline for data processing
- Supports batch operations for efficiency

## Testing Requirements

### Test Files
- `src/tests/unit/test_influxdb_transformer.py` - Unit tests

### Test Cases

1. **Complete Entry Transformation**
   - Input: Entry with all fields populated
   - Expected Output: InfluxDBPoint with all mappings
   - Verification: Each field correctly mapped

2. **Minimal Entry Transformation**
   - Input: Entry with only required fields
   - Expected Output: Point with defaults applied
   - Verification: Missing fields handled properly

3. **Running Entry Handling**
   - Input: Entry with stop=None, duration=-3600
   - Expected Output: Point with negative duration
   - Verification: Time uses start, duration preserved

4. **Timestamp Conversion**
   - Input: Various timezone formats
   - Expected Output: Correct Unix milliseconds
   - Verification: Timezone math correct

5. **Tag String Conversion**
   - Input: Integer/boolean/null values
   - Expected Output: All converted to strings
   - Verification: Type checking passes

6. **Tags Array Processing**
   - Input: [], ["tag1"], ["tag1", "tag2"]
   - Expected Output: Omitted, "tag1", "tag1|tag2"
   - Verification: Pipe separation correct

7. **Batch Success**
   - Input: List of valid entries
   - Expected Output: InfluxDBBatch with all points
   - Verification: All entries transformed

8. **Batch Partial Failure**
   - Input: Mix of valid and invalid entries
   - Expected Output: Success with valid points only
   - Verification: Failures logged, successes returned

9. **Special Character Handling**
   - Input: Description with quotes, commas, unicode
   - Expected Output: Properly escaped/sanitized
   - Verification: InfluxDB compatible

10. **Line Protocol Generation**
    - Input: InfluxDBPoint
    - Expected Output: Valid line protocol string
    - Verification: Format matches InfluxDB spec

### Fixtures Needed
- Sample time entries from Task 001
- Edge case entries (nulls, special chars)

## Acceptance Criteria

- [ ] All field mappings match specification
- [ ] Timestamps convert correctly to Unix ms
- [ ] All tag values are strings
- [ ] Null handling follows defaults
- [ ] Arrays convert to pipe-separated
- [ ] Result types used throughout
- [ ] Batch processing handles failures gracefully
- [ ] Line protocol format is valid
- [ ] Special characters sanitized
- [ ] 100% test coverage achieved

## Notes

- Measurement name is always "toggl_time_entry"
- Time field uses start time, not stop time
- Duration can be negative (running entries)
- Empty arrays should not create tags
- All tag values MUST be strings in InfluxDB
- Consider memory efficiency for large batches
- Line protocol format: `measurement,tag=value field=value timestamp`

## References

- PROJECT_OVERVIEW.md:641-675 (transformer implementation)
- PROJECT_OVERVIEW.md:207-218 (field mapping table)
- Task 000 (Pydantic contracts)
- InfluxDB documentation on data format
- returns library for Result types