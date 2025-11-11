# Task 005: Test InfluxDB Operations

## Status
- [ ] Not Started
- Dependencies: 001, 004
- Estimated Effort: 4 hours
- Can Run in Parallel: No

## Objective

Implement comprehensive integration tests for InfluxDB operations including writing points, querying data, and handling connection/authentication errors using testcontainers.

## Context

According to PROJECT_OVERVIEW.md:581-638, the InfluxDBClient handles both writing transformed time entries and querying for Grafana. The implementation uses influxdb-client-async for async operations. We need to test:
- Writing single and batch points
- Querying with Flux queries
- Connection error handling
- Authentication failures
- Query result parsing

## Implementation Details

### Files to Create
- `src/tests/integration/test_influxdb_operations.py` - InfluxDB operation tests
- `src/tests/fixtures/influxdb_container.py` - Testcontainer setup for InfluxDB

### Files to Modify
- None (new test files)

### Key Functions/Classes to Implement

#### fixtures/influxdb_container.py

1. **influxdb_container fixture**
   - **Purpose**: Provide running InfluxDB instance for tests
   - **Setup**: Start InfluxDB 2.7 container with testcontainers
   - **Configuration**: Create test org, bucket, and token
   - **Teardown**: Stop and remove container

#### test_influxdb_operations.py

##### Test Class: TestInfluxDBOperations

1. **test_write_single_point**
   - **Purpose**: Test writing a single data point
   - **Setup**: InfluxDB container, single transformed point
   - **Verification**: Query confirms point was written

2. **test_write_batch_points**
   - **Purpose**: Test writing multiple points efficiently
   - **Setup**: List of 100+ transformed points
   - **Verification**: All points queryable, performance acceptable

3. **test_write_with_duplicate_timestamps**
   - **Purpose**: Test handling of duplicate timestamps
   - **Setup**: Multiple points with same timestamp
   - **Verification**: Latest write wins or all preserved

4. **test_write_connection_error**
   - **Purpose**: Test handling of connection failures
   - **Setup**: Invalid InfluxDB URL
   - **Verification**: Result.Failure with connection error

5. **test_write_authentication_error**
   - **Purpose**: Test handling of auth failures
   - **Setup**: Invalid token
   - **Verification**: Result.Failure with auth error

6. **test_query_time_range**
   - **Purpose**: Test querying with time range
   - **Setup**: Write points, query subset
   - **Verification**: Only points in range returned

7. **test_query_with_filters**
   - **Purpose**: Test Flux query with filters
   - **Setup**: Points with different tags
   - **Verification**: Filtered results match criteria

8. **test_query_aggregations**
   - **Purpose**: Test aggregation functions
   - **Setup**: Multiple points, sum/mean queries
   - **Verification**: Aggregations calculate correctly

9. **test_query_empty_result**
   - **Purpose**: Test handling of no matching data
   - **Setup**: Query for non-existent data
   - **Verification**: Result.Success with empty list

10. **test_query_malformed_flux**
    - **Purpose**: Test invalid Flux query handling
    - **Setup**: Syntactically incorrect Flux query
    - **Verification**: Result.Failure with query error

11. **test_get_available_metrics**
    - **Purpose**: Test measurement discovery
    - **Setup**: Write various measurements
    - **Verification**: All measurements listed

12. **test_concurrent_writes**
    - **Purpose**: Test concurrent write operations
    - **Setup**: Multiple async writes simultaneously
    - **Verification**: All writes succeed, no data loss

13. **test_large_batch_handling**
    - **Purpose**: Test writing very large batches
    - **Setup**: 10,000+ points in single batch
    - **Verification**: Batch size limits handled

14. **test_connection_pooling**
    - **Purpose**: Test connection reuse
    - **Setup**: Multiple operations in sequence
    - **Verification**: Connections properly managed

15. **test_bucket_creation**
    - **Purpose**: Test bucket existence validation
    - **Setup**: Query non-existent bucket
    - **Verification**: Appropriate error returned

### Algorithm/Approach

1. Use testcontainers to spin up real InfluxDB
2. Create test org, bucket, and auth token
3. Test write operations with various batch sizes
4. Test Flux queries with different complexities
5. Simulate error conditions
6. Verify async context manager usage

### Integration Points

- Uses transformed data from Task 004
- Uses testcontainers for real InfluxDB
- Tests async operations with influxdb-client-async
- Validates Result type error handling

## Testing Requirements

### Test Files
- `src/tests/integration/test_influxdb_operations.py` - Main test file
- `src/tests/fixtures/influxdb_container.py` - Container fixture

### Test Cases

1. **Write and Query Cycle**
   - Input: Transformed point from Task 004
   - Expected Output: Point retrievable via query
   - Verification: Field values match written data

2. **Batch Performance**
   - Input: 1000 points
   - Expected Output: All written within 5 seconds
   - Verification: Query returns 1000 points

3. **Flux Query Execution**
   - Input:
     ```flux
     from(bucket: "test_bucket")
     |> range(start: -1h)
     |> filter(fn: (r) => r["_measurement"] == "toggl_time_entry")
     ```
   - Expected Output: Filtered time entries
   - Verification: Only matching records returned

4. **Connection Resilience**
   - Input: Temporary network interruption
   - Expected Output: Automatic retry succeeds
   - Verification: Write eventually succeeds

### Fixtures Needed
- `influxdb_container` - Running InfluxDB instance
- `sample_influxdb_points` - Transformed points from Task 004

## Acceptance Criteria

- [ ] All write operations use async context manager
- [ ] Batch writes are performant (<1ms per point)
- [ ] Flux queries execute correctly
- [ ] Error conditions return Result.Failure
- [ ] Connection pooling works efficiently
- [ ] Testcontainers properly managed
- [ ] No resource leaks in async operations
- [ ] Large batches handled without OOM
- [ ] Concurrent operations are thread-safe

## Notes

- InfluxDB 2.7+ required for compatibility
- Use testcontainers for isolation
- Consider memory usage for large batches
- Test both write_api and query_api
- Ensure proper async cleanup

## References

- PROJECT_OVERVIEW.md:581-638 (InfluxDBClient implementation)
- PROJECT_OVERVIEW.md:594-602 (write_points method)
- PROJECT_OVERVIEW.md:604-617 (query method)
- PROJECT_OVERVIEW.md:619-637 (get_available_metrics)
- pyproject.toml:11 (influxdb-client[async] dependency)