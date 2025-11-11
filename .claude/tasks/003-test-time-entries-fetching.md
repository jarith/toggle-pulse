# Task 003: Test Time Entries Fetching

## Status
- [ ] Not Started
- Dependencies: 001, 002
- Estimated Effort: 4 hours
- Can Run in Parallel: No

## Objective

Implement comprehensive integration tests for fetching time entries from the Toggl API, covering all query parameters, pagination, and response parsing.

## Context

According to PROJECT_OVERVIEW.md:186-205 and 567-578, the TogglClient needs to fetch time entries with various parameters. The API endpoint is GET /me/time_entries with support for:
- Date range filtering (start_date, end_date)
- Default to last 7-9 days if no dates specified
- 3-month maximum date range limitation
- Response includes comprehensive time entry data

## Implementation Details

### Files to Create
- `src/tests/integration/test_time_entries_fetching.py` - Time entries fetching tests

### Files to Modify
- None (new test file)

### Key Functions/Classes to Implement

#### test_time_entries_fetching.py

##### Test Class: TestTimeEntriesFetching

1. **test_fetch_all_time_entries_default**
   - **Purpose**: Test fetching without date parameters (last 7 days)
   - **Setup**: Mock response with multiple time entries
   - **Verification**: Assert correct endpoint called, Result is Success

2. **test_fetch_time_entries_with_date_range**
   - **Purpose**: Test fetching with specific date range
   - **Setup**: Mock response for date-filtered request
   - **Verification**: Assert query params are correct

3. **test_fetch_time_entries_exceeding_three_months**
   - **Purpose**: Test 3-month limitation error handling
   - **Setup**: Mock 400 error for >3 month range
   - **Verification**: Assert appropriate error is returned

4. **test_fetch_empty_time_entries**
   - **Purpose**: Test handling of no time entries
   - **Setup**: Mock empty array response
   - **Verification**: Assert Result.Success with empty list

5. **test_parse_time_entry_fields**
   - **Purpose**: Verify all fields are correctly parsed
   - **Setup**: Mock response with all fields populated
   - **Verification**: Assert each field is correctly typed and present

6. **test_handle_running_time_entry**
   - **Purpose**: Test parsing of currently running entry
   - **Setup**: Mock response with null stop field, negative duration
   - **Verification**: Assert running entry is handled correctly

7. **test_fetch_time_entries_with_pagination**
   - **Purpose**: Test handling multiple pages of results
   - **Setup**: Mock paginated responses
   - **Verification**: Assert all pages are fetched

8. **test_fetch_time_entries_network_error**
   - **Purpose**: Test network failure handling
   - **Setup**: Simulate connection error
   - **Verification**: Assert Result.Failure with network error

9. **test_fetch_time_entries_timeout**
   - **Purpose**: Test request timeout handling
   - **Setup**: Simulate timeout exception
   - **Verification**: Assert Result.Failure with timeout error

10. **test_fetch_time_entries_invalid_json**
    - **Purpose**: Test malformed JSON response handling
    - **Setup**: Mock invalid JSON response
    - **Verification**: Assert Result.Failure with parse error

11. **test_iso8601_datetime_parsing**
    - **Purpose**: Test ISO 8601 datetime field parsing
    - **Setup**: Various datetime formats in response
    - **Verification**: Assert datetimes are correctly parsed

12. **test_billable_field_handling**
    - **Purpose**: Test billable boolean field
    - **Setup**: Mix of billable true/false entries
    - **Verification**: Assert billable field is boolean

### Algorithm/Approach

1. Use httpx_mock to simulate API responses
2. Test various query parameter combinations
3. Verify response parsing for all field types
4. Test edge cases (empty, running, malformed)
5. Use Result type for all error handling
6. Test pagination if multiple requests needed

### Integration Points

- Uses authentication from Task 002
- Uses fixtures from Task 001
- Response format matches PROJECT_OVERVIEW.md:191-205
- Follows functional programming with Result types

## Testing Requirements

### Test Files
- `src/tests/integration/test_time_entries_fetching.py` - Main test file

### Test Cases

1. **Fetch Last 7 Days**
   - Input: No date parameters
   - Expected Output: Result.Success with time entries from last 7 days
   - Verification: Request URL has no date params

2. **Fetch Specific Date Range**
   - Input: start_date="2025-01-01", end_date="2025-01-31"
   - Expected Output: Result.Success with filtered entries
   - Verification: Query params match input dates

3. **Running Entry Parsing**
   - Input: Entry with stop=null, duration=-3600
   - Expected Output: Entry marked as running
   - Verification: Running flag is True, duration is negative

4. **Field Type Validation**
   - Input: Complete time entry response
   - Expected Output: All fields with correct types
   - Verification:
     - id: integer
     - description: string/null
     - duration: integer
     - billable: boolean
     - start/stop: datetime strings
     - project_id: integer/null
     - workspace_id: integer
     - tags: array/null

### Fixtures Needed
- `httpx_mock` - From pytest-httpx
- `toggl_api_token` - From Task 001
- `sample_time_entries` - From Task 001

## Acceptance Criteria

- [ ] All query parameter combinations are tested
- [ ] Date range limitations are enforced
- [ ] Empty responses are handled gracefully
- [ ] Running entries are correctly identified
- [ ] All field types are validated
- [ ] Network errors return Result.Failure
- [ ] Pagination works if implemented
- [ ] ISO 8601 datetime parsing is robust
- [ ] Tests use async/await properly

## Notes

- Time entries can have null fields (description, stop, project_id)
- Duration is negative for running entries
- Dates use ISO 8601 format (RFC 3339 subset)
- Consider testing with various timezone formats
- Test both single entries and bulk responses

## References

- PROJECT_OVERVIEW.md:186-205 (API response format)
- PROJECT_OVERVIEW.md:567-578 (TogglClient.get_all_time_entries)
- PROJECT_OVERVIEW.md:191-218 (Response field mappings)