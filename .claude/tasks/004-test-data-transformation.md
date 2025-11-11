# Task 004: Create Comprehensive Transformation Tests

## Status
- [ ] Not Started
- Dependencies: 000, 001, 003
- Estimated Effort: 3-4 hours
- Can Run in Parallel: No

## Objective

Create comprehensive tests for the data transformation logic, ensuring all mappings from Toggl to InfluxDB format are correct and edge cases are handled properly.

## Context

The transformation is the critical component that converts Toggl time entries into InfluxDB points. According to PROJECT_OVERVIEW.md:207-218, we need to test:
- All field mappings are correct
- Type conversions (especially timestamps and tags)
- Null/missing value handling
- Special character processing
- Batch transformation resilience

Tests should be simple, focused, and use the fixtures from Task 001.

## Implementation Details

### Files to Create
- `src/tests/unit/test_influxdb_transformer.py` - Transformation unit tests
- `src/tests/integration/test_transformation_pipeline.py` - End-to-end tests

### Files to Modify
- None (new test files)

### Key Test Classes to Implement

#### test_influxdb_transformer.py

```python
import pytest
from datetime import datetime, timezone
from returns.result import Success, Failure
from toggle_pulse.contracts.toggl import TogglTimeEntry
from toggle_pulse.contracts.influxdb import InfluxDBPoint, InfluxDBBatch
from toggle_pulse.transformers.influxdb import (
    transform_time_entry,
    transform_batch,
    sanitize_tag_value,
    format_timestamp
)
```

##### Class: TestSingleEntryTransformation

1. **test_complete_entry_all_fields_mapped**
   ```python
   def test_complete_entry_all_fields_mapped(self, complete_time_entry):
       """Test that all fields from a complete entry are correctly mapped."""
       result = transform_time_entry(complete_time_entry)

       assert isinstance(result, Success)
       point = result.unwrap()

       # Verify measurement
       assert point.measurement == "toggl_time_entry"

       # Verify tags (all should be strings)
       assert point.tags["workspace_id"] == "12345"
       assert point.tags["project_id"] == "67890"
       assert point.tags["billable"] == "true"
       assert point.tags["tags"] == "development|backend"

       # Verify fields
       assert point.fields["duration"] == 9000
       assert point.fields["description"] == "Working on feature X"

       # Verify timestamp (2025-01-01T08:00:00Z)
       expected_ts = int(datetime(2025, 1, 1, 8, 0, 0, tzinfo=timezone.utc).timestamp() * 1000)
       assert point.time == expected_ts
   ```

2. **test_minimal_entry_applies_defaults**
   ```python
   def test_minimal_entry_applies_defaults(self, minimal_time_entry):
       """Test that minimal entry gets correct defaults."""
       result = transform_time_entry(minimal_time_entry)

       assert isinstance(result, Success)
       point = result.unwrap()

       # Check defaults
       assert point.tags["project_id"] == "unknown"  # Default for None
       assert point.tags["billable"] == "false"  # Default false
       assert "tags" not in point.tags  # No tags field if empty
       assert point.fields["description"] == ""  # Empty string for None
   ```

3. **test_running_entry_negative_duration**
   ```python
   def test_running_entry_negative_duration(self, running_time_entry):
       """Test running entry preserves negative duration."""
       result = transform_time_entry(running_time_entry)

       assert isinstance(result, Success)
       point = result.unwrap()

       assert point.fields["duration"] == -3600  # Negative preserved
       assert point.tags["project_id"] == "67890"
       # Time should use start time, not stop (which is None)
       assert point.time > 0
   ```

4. **test_empty_tags_array_omitted**
   ```python
   def test_empty_tags_array_omitted(self):
       """Test that empty tags array doesn't create tags field."""
       entry = TogglTimeEntry(
           id=123,
           workspace_id=456,
           start=datetime.now(timezone.utc),
           stop=datetime.now(timezone.utc),
           duration=3600,
           tags=[]  # Empty array
       )

       result = transform_time_entry(entry)
       point = result.unwrap()

       assert "tags" not in point.tags  # Should be omitted
   ```

5. **test_special_characters_in_description**
   ```python
   def test_special_characters_in_description(self):
       """Test special characters are preserved in description."""
       entry = TogglTimeEntry(
           id=123,
           workspace_id=456,
           description='Task: "Fix bug" | Issue #123 & UTF-8: 你好',
           start=datetime.now(timezone.utc),
           stop=datetime.now(timezone.utc),
           duration=3600
       )

       result = transform_time_entry(entry)
       point = result.unwrap()

       assert point.fields["description"] == 'Task: "Fix bug" | Issue #123 & UTF-8: 你好'
   ```

##### Class: TestBatchTransformation

1. **test_batch_all_successful**
   ```python
   def test_batch_all_successful(self, batch_time_entries):
       """Test batch transformation with all valid entries."""
       result = transform_batch(batch_time_entries)

       assert isinstance(result, Success)
       batch = result.unwrap()

       assert len(batch) == len(batch_time_entries)
       for point in batch.points:
           assert point.measurement == "toggl_time_entry"
   ```

2. **test_batch_partial_failure_continues**
   ```python
   def test_batch_partial_failure_continues(self, complete_time_entry):
       """Test batch continues processing despite individual failures."""
       # Create a mix of valid and invalid entries
       entries = [
           complete_time_entry,  # Valid
           None,  # This will cause a failure in transformation
           complete_time_entry,  # Valid
       ]

       # Note: Need to handle None case in actual implementation
       # For testing, we'd mock a failure scenario
   ```

3. **test_empty_batch_handling**
   ```python
   def test_empty_batch_handling(self):
       """Test empty batch returns empty result."""
       result = transform_batch([])

       assert isinstance(result, Success)
       batch = result.unwrap()
       assert len(batch) == 0
   ```

##### Class: TestTimestampConversion

1. **test_utc_timestamp_conversion**
   ```python
   def test_utc_timestamp_conversion(self):
       """Test UTC timestamp converts correctly."""
       dt = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
       ms = format_timestamp(dt)

       expected = 1735732800000  # 2025-01-01T12:00:00Z in ms
       assert ms == expected
   ```

2. **test_timezone_offset_conversion**
   ```python
   @pytest.mark.parametrize("offset,hours", [
       (timezone(timedelta(hours=-5)), -5),  # EST
       (timezone(timedelta(hours=2)), 2),     # CEST
       (timezone(timedelta(hours=9)), 9),     # JST
   ])
   def test_timezone_offset_conversion(self, offset, hours):
       """Test various timezone offsets convert correctly."""
       dt = datetime(2025, 1, 1, 12, 0, 0, tzinfo=offset)
       ms = format_timestamp(dt)

       # Should adjust for timezone offset
       expected_utc_hour = 12 - hours
       # Calculate expected timestamp...
   ```

3. **test_naive_datetime_rejected**
   ```python
   def test_naive_datetime_rejected(self):
       """Test timezone-naive datetime raises error."""
       dt = datetime(2025, 1, 1, 12, 0, 0)  # No timezone

       with pytest.raises(ValueError, match="timezone-aware"):
           format_timestamp(dt)
   ```

##### Class: TestTagSanitization

1. **test_tag_value_sanitization**
   ```python
   @pytest.mark.parametrize("input_val,expected", [
       ("normal", "normal"),
       ("has,comma", "has;comma"),  # Comma replacement
       ("  spaces  ", "spaces"),     # Trimming
       ("", ""),                      # Empty allowed
   ])
   def test_tag_value_sanitization(self, input_val, expected):
       """Test tag values are sanitized correctly."""
       result = sanitize_tag_value(input_val)
       assert result == expected
   ```

##### Class: TestLineProtocol

1. **test_line_protocol_format**
   ```python
   def test_line_protocol_format(self):
       """Test InfluxDB line protocol generation."""
       point = InfluxDBPoint(
           measurement="toggl_time_entry",
           tags={"workspace_id": "123", "project_id": "456"},
           fields={"duration": 3600, "description": "Test"},
           time=1735732800000
       )

       line = point.to_line_protocol()

       # Should match format: measurement,tag=val field=val timestamp
       expected_pattern = r"toggl_time_entry,.*workspace_id=123.*duration=3600.*1735732800000"
       assert re.match(expected_pattern, line)
   ```

#### test_transformation_pipeline.py

##### Class: TestEndToEndTransformation

1. **test_json_to_influxdb_pipeline**
   ```python
   def test_json_to_influxdb_pipeline(self):
       """Test complete pipeline from JSON to InfluxDB point."""
       # Raw JSON as from Toggl API
       json_data = {
           "id": 123456789,
           "workspace_id": 12345,
           "project_id": 67890,
           "description": "Working on feature X",
           "start": "2025-01-01T08:00:00Z",
           "stop": "2025-01-01T10:30:00Z",
           "duration": 9000,
           "billable": True,
           "tags": ["development", "backend"]
       }

       # Parse to pydantic
       entry = TogglTimeEntry(**json_data)

       # Transform to InfluxDB
       result = transform_time_entry(entry)

       assert isinstance(result, Success)
       point = result.unwrap()

       # Verify complete transformation
       assert point.measurement == "toggl_time_entry"
       assert all(isinstance(v, str) for v in point.tags.values())
       assert point.time > 0
   ```

2. **test_batch_json_processing**
   ```python
   def test_batch_json_processing(self):
       """Test processing batch of JSON entries."""
       json_batch = [
           {...},  # Multiple JSON entries
           {...},
           {...}
       ]

       entries = [TogglTimeEntry(**json_entry) for json_entry in json_batch]
       result = transform_batch(entries)

       assert isinstance(result, Success)
       # Verify all transformed
   ```

### Test Data Scenarios

1. **Standard Cases**:
   - Complete entry with all fields
   - Minimal entry with required fields only
   - Running entry (negative duration, no stop)

2. **Edge Cases**:
   - Null/None values for optional fields
   - Empty arrays and strings
   - Very long descriptions
   - Unicode characters
   - Special characters in tags

3. **Error Cases**:
   - Invalid timestamp formats
   - Missing required fields
   - Type mismatches

### Algorithm/Approach

1. Use fixtures from Task 001 for consistent test data
2. Test each transformation rule individually
3. Verify Result type handling (Success/Failure)
4. Use parametrized tests for similar scenarios
5. Test both unit level and integration level
6. Ensure 100% code coverage

### Integration Points

- Uses fixtures from Task 001
- Tests contracts from Task 000
- Tests transformer from Task 003
- Validates against InfluxDB requirements

## Testing Requirements

### Coverage Requirements
- 100% line coverage for transformer module
- All edge cases documented and tested
- All error paths tested

### Performance Tests
- Batch of 1000 entries should transform in <100ms
- Memory usage should be linear with batch size

## Acceptance Criteria

- [ ] All field mappings tested individually
- [ ] Timestamp conversion tested with multiple timezones
- [ ] Null/default handling verified
- [ ] Special character handling tested
- [ ] Batch processing tested with failures
- [ ] Line protocol format validated
- [ ] Result type Success/Failure paths tested
- [ ] Integration tests pass end-to-end
- [ ] 100% code coverage achieved
- [ ] All tests run in <5 seconds

## Notes

- Use pytest.mark.parametrize for similar test cases
- Mock where necessary but prefer real objects
- Test data should be realistic (from actual API)
- Consider property-based testing for edge cases
- Document why each test exists

## References

- Task 000 (Pydantic contracts)
- Task 001 (Test fixtures)
- Task 003 (Transformation implementation)
- PROJECT_OVERVIEW.md:207-218 (Field mappings)
- pytest documentation for best practices