# Task 006: Test Scheduler Integration

## Status
- [ ] Not Started
- Dependencies: 001, 002, 003, 004, 005
- Estimated Effort: 3-4 hours
- Can Run in Parallel: No

## Objective

Implement integration tests for the APScheduler-based data fetching pipeline that runs twice daily, testing the complete flow from Toggl API to InfluxDB storage.

## Context

According to PROJECT_OVERVIEW.md:433-465, the scheduler runs at 2 AM and 2 PM UTC, fetching time entries from Toggl and storing them in InfluxDB. This task tests the complete scheduled pipeline including:
- Scheduler configuration and triggering
- Complete fetch-transform-store pipeline
- Error handling and recovery
- Incremental data fetching
- Idempotency of scheduled runs

## Implementation Details

### Files to Create
- `src/tests/integration/test_scheduler_integration.py` - Scheduler integration tests

### Files to Modify
- None (new test file)

### Key Functions/Classes to Implement

#### test_scheduler_integration.py

##### Test Class: TestSchedulerIntegration

1. **test_scheduler_cron_configuration**
   - **Purpose**: Verify scheduler runs at correct times
   - **Setup**: Create scheduler with test cron trigger
   - **Verification**: Job scheduled for 2 AM and 2 PM UTC

2. **test_complete_fetch_and_store_pipeline**
   - **Purpose**: Test end-to-end data pipeline
   - **Setup**: Mock Toggl API, real InfluxDB container
   - **Verification**: Data flows from API to database

3. **test_incremental_data_fetching**
   - **Purpose**: Test fetching only new entries
   - **Setup**: Run twice with different data sets
   - **Verification**: No duplicate writes, only new data

4. **test_scheduler_error_recovery**
   - **Purpose**: Test handling of API failures
   - **Setup**: First run fails, second succeeds
   - **Verification**: Scheduler continues after error

5. **test_partial_failure_handling**
   - **Purpose**: Test handling of partial batch failures
   - **Setup**: Some points fail to write
   - **Verification**: Successful points are preserved

6. **test_toggl_api_rate_limiting**
   - **Purpose**: Test rate limit handling in scheduler
   - **Setup**: Mock 429 response from Toggl
   - **Verification**: Scheduler retries with backoff

7. **test_influxdb_connection_failure**
   - **Purpose**: Test database unavailability
   - **Setup**: Stop InfluxDB container mid-run
   - **Verification**: Error logged, no data loss

8. **test_concurrent_scheduler_runs**
   - **Purpose**: Test preventing concurrent executions
   - **Setup**: Trigger while previous run active
   - **Verification**: Second run skipped or queued

9. **test_scheduler_with_no_new_data**
   - **Purpose**: Test handling of no new entries
   - **Setup**: Mock empty response from Toggl
   - **Verification**: Graceful completion, no errors

10. **test_scheduler_timezone_handling**
    - **Purpose**: Verify UTC scheduling regardless of local TZ
    - **Setup**: Set various system timezones
    - **Verification**: Always triggers at UTC times

11. **test_scheduler_memory_cleanup**
    - **Purpose**: Test memory management in long runs
    - **Setup**: Process large datasets
    - **Verification**: Memory released after each run

12. **test_fetch_date_range_calculation**
    - **Purpose**: Test dynamic date range for fetching
    - **Setup**: Various current times
    - **Verification**: Correct start_date calculated

### Algorithm/Approach

1. Create test scheduler with shorter intervals
2. Mock Toggl API responses
3. Use real InfluxDB container
4. Trigger scheduler manually for testing
5. Verify complete pipeline execution
6. Test error scenarios and recovery

### Integration Points

- Combines all previous components
- Uses APScheduler with CronTrigger
- Integrates Toggl client, transformer, and InfluxDB client
- Tests from PROJECT_OVERVIEW.md:433-465

## Testing Requirements

### Test Files
- `src/tests/integration/test_scheduler_integration.py` - Main test file

### Test Cases

1. **Successful Pipeline Run**
   - Input: Trigger scheduler manually
   - Flow:
     1. Fetch from Toggl (mocked)
     2. Transform entries
     3. Write to InfluxDB
   - Expected Output: All entries in database
   - Verification: Query InfluxDB for written data

2. **Incremental Fetch**
   - Input: Run scheduler twice
   - First Run: Returns entries A, B, C
   - Second Run: Returns entries C, D, E
   - Expected Output: Database has A, B, C, D, E (no duplicates)
   - Verification: Count unique entries

3. **Error Recovery**
   - Input: API fails then succeeds
   - First Run: 500 error from Toggl
   - Second Run: Success with data
   - Expected Output: Data eventually written
   - Verification: Scheduler continues operation

4. **Rate Limit Handling**
   - Input: 429 from Toggl
   - Expected Output: Retry after delay
   - Verification: Backoff applied, eventual success

### Fixtures Needed
- `httpx_mock` - Mock Toggl API
- `influxdb_container` - Real database
- `test_scheduler` - Scheduler with test configuration

## Acceptance Criteria

- [ ] Scheduler triggers at configured times
- [ ] Complete pipeline executes successfully
- [ ] Incremental fetching prevents duplicates
- [ ] Error recovery works properly
- [ ] Rate limiting handled with backoff
- [ ] No memory leaks in long-running process
- [ ] Concurrent runs prevented
- [ ] UTC timezone used consistently
- [ ] All async operations properly awaited

## Notes

- Use shorter intervals for testing (seconds not hours)
- Consider using time-machine or freezegun for time control
- Test both manual triggering and time-based
- Verify logging at each pipeline stage
- Ensure graceful shutdown

## References

- PROJECT_OVERVIEW.md:433-465 (fetch_and_store_toggl function)
- PROJECT_OVERVIEW.md:469-474 (scheduler configuration)
- PROJECT_OVERVIEW.md:130-152 (data ingestion flow)