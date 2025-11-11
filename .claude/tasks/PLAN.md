# Implementation Plan: Toggl to InfluxDB Data Transformation (Revised)

## Overview

This revised plan focuses on implementing the core data transformation functionality from Toggl API to InfluxDB format. Based on user requirements:
- **No authentication testing needed** (Toggl API is reliable)
- **No API format validation needed** (API is strict and solid)
- **Focus on transformation logic** from Toggl schema to InfluxDB schema
- **Simple test setup** without unnecessary complexity
- **Added initial task** for defining Toggl API pydantic contracts

## Task Breakdown

Total Tasks: 5
Estimated Total Effort: 13-15 hours

### Phase 1: Foundation (Sequential)

#### Task 000: Define Toggl API Pydantic Contracts
- **Duration**: 2-3 hours
- **Dependencies**: None
- **Purpose**: Create comprehensive Pydantic models for Toggl API data structures
- **Deliverables**:
  - `src/toggle_pulse/contracts/toggl.py` - Toggl API models (TogglTimeEntry, etc.)
  - Type safety and validation for all Toggl data
  - Helper methods for common operations

#### Task 001: Simple Test Infrastructure Setup
- **Duration**: 2 hours
- **Dependencies**: 000
- **Purpose**: Set up minimal test infrastructure with fixtures
- **Deliverables**:
  - `src/tests/conftest.py` - Basic pytest configuration
  - `src/tests/fixtures/sample_data.py` - Test data factories
  - Simple fixtures without HTTP mocking or authentication

### Phase 2: Core Implementation (Can be parallel after Phase 1)

#### Task 002: Implement Toggl Client with httpx
- **Duration**: 3 hours
- **Dependencies**: 000
- **Purpose**: Create async Toggl API client using httpx
- **Deliverables**:
  - `src/toggle_pulse/clients/toggl.py` - Toggl client
  - Result type error handling from returns library
  - Async context manager support
  - Focus on fetching time entries only

#### Task 003: Implement Data Transformation Logic
- **Duration**: 3 hours
- **Dependencies**: 000
- **Purpose**: Transform Toggl entries to InfluxDB points
- **Deliverables**:
  - `src/toggle_pulse/transformers/influxdb.py` - Transformation logic
  - `src/toggle_pulse/contracts/influxdb.py` - InfluxDB point models
  - Field mappings per PROJECT_OVERVIEW.md:207-218

### Phase 3: Testing

#### Task 004: Create Comprehensive Transformation Tests
- **Duration**: 3-4 hours
- **Dependencies**: 000, 001, 003
- **Purpose**: Test all transformation logic thoroughly
- **Deliverables**:
  - `src/tests/unit/test_influxdb_transformer.py` - Unit tests
  - `src/tests/integration/test_transformation_pipeline.py` - E2E tests
  - 100% coverage of transformation logic

## Execution Strategy

### Parallel Execution Opportunities

After completing Tasks 000 and 001, Tasks 002 and 003 can be executed in parallel:

```
Phase 1 (Sequential):
  Task 000 (Pydantic Contracts)
     ↓
  Task 001 (Test Infrastructure)

Phase 2 (Parallel):
  ┌→ Task 002 (Toggl Client)
  └→ Task 003 (Transformation Logic)

Phase 3 (Sequential):
  Task 004 (Transformation Tests)
```

## Key Changes from Original Plan

1. **Added Task 000**: Define pydantic contracts first for type safety
2. **Removed Authentication Tests**: Task 002 now implements client instead
3. **Simplified Test Setup**: Task 001 no longer includes HTTP mocking
4. **Focused on Transformation**: Primary goal is Toggl → InfluxDB conversion
5. **Reduced Complexity**: No unnecessary authentication or API format testing

## Field Mapping Specification

Per PROJECT_OVERVIEW.md:207-218, the transformation must handle:

| Toggl Field | InfluxDB Mapping | Transformation |
|------------|------------------|----------------|
| `start` | Timestamp | ISO 8601 → Unix ms |
| `duration` | Field | Store as-is (seconds) |
| `description` | Field | Store as string (empty if None) |
| `project_id` | Tag | String conversion ("unknown" if None) |
| `workspace_id` | Tag | String conversion |
| `billable` | Tag | Boolean → string ("true"/"false") |
| `tags` | Tag | Array → pipe-separated string |

## Risk Assessment

### Low Risk Areas
- Pydantic contracts (well-defined, straightforward)
- Simple test infrastructure (minimal complexity)
- Data transformation (clear mapping rules)

### Medium Risk Areas
- Timestamp conversion (timezone handling)
- Special character handling in tags/descriptions
- Batch processing with partial failures

### Mitigation Strategies
- Comprehensive timestamp testing with multiple timezones
- Explicit sanitization functions for special characters
- Graceful degradation for batch failures
- Use Result types for all error handling

## Testing Strategy

1. **No Authentication Tests**: Toggl API assumed reliable
2. **No API Format Tests**: Response format assumed stable
3. **Focus on Transformation**: Core logic thoroughly tested
4. **Simple Fixtures**: Realistic data without complex mocking
5. **Result Types**: All errors handled functionally

## Success Metrics

- ✅ All pydantic models validate Toggl API responses
- ✅ Transformation preserves all data accurately
- ✅ Type safety throughout the pipeline
- ✅ Result types handle all error cases
- ✅ 100% test coverage on transformation logic
- ✅ All tests run in <5 seconds
- ✅ No external dependencies in tests

## Implementation Guidelines

### For python-engineer Agent (Tasks 000, 002, 003)
- Use functional programming with returns library
- Implement all error handling with Result types
- Use async/await for httpx operations
- Follow pydantic best practices for contracts
- Ensure immutability where appropriate

### For test-engineer Agent (Task 004)
- Write tests before implementation (TDD approach)
- Use fixtures from Task 001
- Test each transformation rule individually
- Use parametrized tests for similar cases
- Ensure 100% coverage of transformation logic

## Next Steps After Completion

Once these 5 tasks are complete, the project can proceed with:
1. Implement InfluxDB client for writing points
2. Create FastAPI endpoints for Grafana integration
3. Set up APScheduler for periodic data fetching
4. Docker containerization
5. Integration with existing infrastructure

## Notes

- This plan addresses only Tasks 000-004 as requested
- Authentication complexity removed per requirements
- All tasks sized for manageable implementation windows
- Clear separation between contracts, implementation, and tests
- Focus on data transformation as the core value proposition