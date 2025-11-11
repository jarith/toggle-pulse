# Task 007: Test Grafana Endpoints

## Status
- [ ] Not Started
- Dependencies: 001, 005
- Estimated Effort: 4 hours
- Can Run in Parallel: Yes (after 001, 005)

## Objective

Implement comprehensive integration tests for the FastAPI endpoints that serve as a Grafana SimpleJSON datasource, including /search, /query, and /annotations endpoints.

## Context

According to PROJECT_OVERVIEW.md:490-549, the FastAPI application provides three endpoints for Grafana:
- POST /search - Returns available metrics
- POST /query - Returns time series data
- POST /annotations - Returns annotations (optional)
These endpoints follow the Grafana SimpleJSON datasource protocol and must handle specific request/response formats.

## Implementation Details

### Files to Create
- `src/tests/integration/test_grafana_endpoints.py` - Endpoint tests
- `src/tests/fixtures/grafana_requests.py` - Sample Grafana request fixtures

### Files to Modify
- None (new test files)

### Key Functions/Classes to Implement

#### fixtures/grafana_requests.py

1. **get_search_request**
   - Returns sample SearchRequest payload

2. **get_query_request**
   - Returns sample QueryRequest with time range and targets

3. **get_annotations_request**
   - Returns sample annotations request

#### test_grafana_endpoints.py

##### Test Class: TestGrafanaEndpoints

1. **test_health_check_endpoint**
   - **Purpose**: Test GET / health check
   - **Setup**: Create test client
   - **Verification**: Returns {"status": "ok"}

2. **test_search_endpoint_returns_metrics**
   - **Purpose**: Test /search returns available metrics
   - **Setup**: InfluxDB with test measurements
   - **Verification**: Returns list of metric names

3. **test_search_with_empty_database**
   - **Purpose**: Test /search with no data
   - **Setup**: Empty InfluxDB
   - **Verification**: Returns empty array

4. **test_search_with_filter_target**
   - **Purpose**: Test metric filtering
   - **Setup**: SearchRequest with target filter
   - **Verification**: Filtered results returned

5. **test_query_endpoint_single_target**
   - **Purpose**: Test querying single metric
   - **Setup**: QueryRequest with one target
   - **Verification**: TimeSeries response with datapoints

6. **test_query_endpoint_multiple_targets**
   - **Purpose**: Test querying multiple metrics
   - **Setup**: QueryRequest with multiple targets
   - **Verification**: Array of TimeSeries objects

7. **test_query_time_range_filtering**
   - **Purpose**: Test time range boundaries
   - **Setup**: Data across wide time range
   - **Verification**: Only data in range returned

8. **test_query_with_intervalMs**
   - **Purpose**: Test downsampling based on interval
   - **Setup**: High-frequency data, large interval
   - **Verification**: Data appropriately downsampled

9. **test_query_with_maxDataPoints**
   - **Purpose**: Test data point limiting
   - **Setup**: Large dataset, maxDataPoints limit
   - **Verification**: Points limited to max

10. **test_query_invalid_time_range**
    - **Purpose**: Test invalid date handling
    - **Setup**: Malformed from/to dates
    - **Verification**: 400 error with message

11. **test_query_nonexistent_metric**
    - **Purpose**: Test querying missing metric
    - **Setup**: Target that doesn't exist
    - **Verification**: Empty datapoints array

12. **test_query_influxdb_error_handling**
    - **Purpose**: Test database error propagation
    - **Setup**: InfluxDB connection failure
    - **Verification**: 500 error with details

13. **test_annotations_endpoint**
    - **Purpose**: Test annotations endpoint
    - **Setup**: Call /annotations
    - **Verification**: Returns empty array (as designed)

14. **test_cors_headers**
    - **Purpose**: Test CORS for Grafana access
    - **Setup**: Request with Origin header
    - **Verification**: Proper CORS headers returned

15. **test_content_type_validation**
    - **Purpose**: Test JSON content type requirement
    - **Setup**: Request without application/json
    - **Verification**: 415 or handled gracefully

16. **test_concurrent_query_requests**
    - **Purpose**: Test handling multiple simultaneous queries
    - **Setup**: 10 concurrent requests
    - **Verification**: All complete successfully

17. **test_query_response_format**
    - **Purpose**: Validate Grafana-compatible format
    - **Setup**: Various query responses
    - **Verification**: Matches SimpleJSON spec

### Algorithm/Approach

1. Use TestClient from FastAPI for testing
2. Mock or use real InfluxDB container
3. Test request/response format compliance
4. Verify error handling and status codes
5. Test concurrent request handling

### Integration Points

- Uses FastAPI TestClient
- Integrates with InfluxDB fixtures
- Follows Grafana SimpleJSON protocol
- Uses Pydantic models from PROJECT_OVERVIEW.md:385-412

## Testing Requirements

### Test Files
- `src/tests/integration/test_grafana_endpoints.py` - Main test file
- `src/tests/fixtures/grafana_requests.py` - Request fixtures

### Test Cases

1. **Search Request**
   - Input:
     ```json
     {"target": ""}
     ```
   - Expected Output:
     ```json
     ["toggl_time_entry", "other_metric"]
     ```

2. **Query Request**
   - Input:
     ```json
     {
       "range": {"from": "2025-01-01T00:00:00Z", "to": "2025-01-02T00:00:00Z"},
       "targets": [{"target": "toggl_time_entry", "refId": "A"}],
       "intervalMs": 60000,
       "maxDataPoints": 1000
     }
     ```
   - Expected Output:
     ```json
     [{
       "target": "toggl_time_entry",
       "refId": "A",
       "datapoints": [[100, 1704067200000], [150, 1704070800000]]
     }]
     ```

3. **Error Response**
   - Input: Malformed request
   - Expected Output:
     ```json
     {"detail": "Error message"}
     ```
   - Status Code: 400 or 500

### Fixtures Needed
- `test_client` - FastAPI TestClient
- `influxdb_container` - Running InfluxDB
- `sample_grafana_requests` - Request payloads

## Acceptance Criteria

- [ ] All endpoints return correct status codes
- [ ] Response format matches Grafana SimpleJSON spec
- [ ] Time range filtering works correctly
- [ ] Multiple targets handled properly
- [ ] Error responses include helpful details
- [ ] CORS headers present for Grafana
- [ ] Concurrent requests handled efficiently
- [ ] Empty results handled gracefully
- [ ] All async operations properly awaited

## Notes

- Grafana expects specific timestamp format (Unix ms)
- Datapoints must be sorted by timestamp
- RefId must be preserved in responses
- Consider testing with actual Grafana if possible
- Test with various time zones

## References

- PROJECT_OVERVIEW.md:485-549 (endpoint implementations)
- PROJECT_OVERVIEW.md:385-412 (Pydantic models)
- PROJECT_OVERVIEW.md:154-175 (data visualization flow)
- Grafana SimpleJSON datasource documentation