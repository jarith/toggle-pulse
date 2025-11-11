# Task 010: Test End-to-End Integration

## Status
- [ ] Not Started
- Dependencies: 001, 002, 003, 004, 005, 006, 007
- Estimated Effort: 4 hours
- Can Run in Parallel: No

## Objective

Implement comprehensive end-to-end integration tests that validate the complete system working together, from Toggl API through to Grafana visualization, using Docker containers to simulate production environment.

## Context

According to PROJECT_OVERVIEW.md:223-302, the system runs in Docker containers with Caddy, Grafana, InfluxDB, and the Python service. This task tests the complete integrated system including:
- Full data pipeline from Toggl to Grafana
- Container orchestration and networking
- Service discovery and communication
- Complete user workflows

## Implementation Details

### Files to Create
- `src/tests/e2e/test_complete_integration.py` - End-to-end tests
- `src/tests/e2e/docker_compose_test.yml` - Test Docker configuration
- `src/tests/utils/grafana_client.py` - Grafana API client for testing

### Files to Modify
- None (new test files)

### Key Functions/Classes to Implement

#### utils/grafana_client.py

1. **GrafanaTestClient**
   - **Purpose**: Interact with Grafana for testing
   - **Methods**:
     - add_datasource()
     - create_dashboard()
     - query_panel()
     - verify_visualization()

#### test_complete_integration.py

##### Test Class: TestEndToEndIntegration

1. **test_complete_data_pipeline_flow**
   - **Purpose**: Test entire data flow
   - **Setup**: All containers running
   - **Flow**:
     1. Trigger scheduler
     2. Fetch from Toggl (mocked)
     3. Transform and store
     4. Query via Grafana
   - **Verification**: Data visible in Grafana

2. **test_scheduler_triggers_at_correct_times**
   - **Purpose**: Verify scheduling works
   - **Setup**: Fast-forward time
   - **Verification**: Runs at 2 AM and 2 PM UTC

3. **test_grafana_dashboard_creation**
   - **Purpose**: Test dashboard setup
   - **Setup**: Create dashboard via API
   - **Verification**: Panels show data correctly

4. **test_multiple_workspace_handling**
   - **Purpose**: Test multi-workspace support
   - **Setup**: Data from multiple workspaces
   - **Verification**: All workspaces visible

5. **test_historical_data_import**
   - **Purpose**: Test bulk historical import
   - **Setup**: Import 3 months of data
   - **Verification**: All data queryable

6. **test_incremental_updates**
   - **Purpose**: Test incremental fetching
   - **Setup**: Run scheduler multiple times
   - **Verification**: No duplicates, new data added

7. **test_container_restart_recovery**
   - **Purpose**: Test resilience to restarts
   - **Setup**: Restart each container
   - **Verification**: System recovers, no data loss

8. **test_network_partition_handling**
   - **Purpose**: Test network failures
   - **Setup**: Disconnect containers temporarily
   - **Verification**: Reconnects and continues

9. **test_data_persistence_across_restarts**
   - **Purpose**: Test data persistence
   - **Setup**: Stop all, restart all
   - **Verification**: All data still present

10. **test_grafana_query_performance_e2e**
    - **Purpose**: Test query speed end-to-end
    - **Setup**: Large dataset, complex queries
    - **Verification**: Queries complete quickly

11. **test_concurrent_user_simulation**
    - **Purpose**: Test multiple users
    - **Setup**: Simulate 10 Grafana users
    - **Verification**: All get correct data

12. **test_timezone_handling_e2e**
    - **Purpose**: Test timezone consistency
    - **Setup**: Data from different timezones
    - **Verification**: Displayed correctly in UTC

13. **test_filtering_by_project_and_tags**
    - **Purpose**: Test Grafana filtering
    - **Setup**: Query with filters
    - **Verification**: Correct subset returned

14. **test_billable_hours_calculation**
    - **Purpose**: Test business logic
    - **Setup**: Mix of billable/non-billable
    - **Verification**: Calculations correct

15. **test_complete_deployment_simulation**
    - **Purpose**: Test deployment process
    - **Setup**: Deploy from scratch
    - **Verification**: Everything starts correctly

### Algorithm/Approach

1. Use docker-compose for test environment
2. Start all services in containers
3. Execute complete workflows
4. Verify via multiple interfaces
5. Test failure and recovery scenarios

### Integration Points

- Tests all components together
- Uses real Docker containers
- Validates complete workflows
- Tests production configuration

## Testing Requirements

### Test Files
- `src/tests/e2e/test_complete_integration.py` - E2E tests
- `src/tests/e2e/docker_compose_test.yml` - Docker config
- `src/tests/utils/grafana_client.py` - Grafana client

### Test Cases

1. **Complete Workflow**
   - Steps:
     1. Start all containers
     2. Wait for health checks
     3. Trigger data fetch
     4. Transform and store
     5. Create Grafana dashboard
     6. Query data via panels
   - Expected: Data flows through entire pipeline
   - Verification: Grafana shows correct visualizations

2. **Multi-Day Operation**
   - Duration: Simulate 3 days
   - Schedule: 2 AM and 2 PM triggers
   - Expected: 6 successful runs
   - Verification: All data points present

3. **Recovery from Failure**
   - Scenario: InfluxDB crashes mid-write
   - Recovery: Restart and retry
   - Expected: No data loss
   - Verification: All entries eventually written

### Fixtures Needed
- `docker_environment` - Managed Docker containers
- `grafana_client` - Grafana API access
- `mock_toggl_server` - Mock Toggl API

## Acceptance Criteria

- [ ] Complete pipeline works end-to-end
- [ ] All containers communicate correctly
- [ ] Data flows from Toggl to Grafana
- [ ] Scheduler runs at correct times
- [ ] System recovers from failures
- [ ] No data loss during restarts
- [ ] Grafana dashboards display correctly
- [ ] Performance meets requirements
- [ ] Multi-workspace support works
- [ ] All integration points tested

## Notes

- Use testcontainers or docker-py
- Consider using pytest-docker
- Mock external Toggl API
- Test with realistic data volumes
- Verify logs from all services
- Check resource usage

## References

- PROJECT_OVERVIEW.md:223-302 (Docker configuration)
- PROJECT_OVERVIEW.md:304-323 (Caddyfile)
- PROJECT_OVERVIEW.md:52-60 (Architecture overview)
- PROJECT_OVERVIEW.md:130-175 (Complete data flow)