# Task 002: Implement Toggl Client with httpx

## Status
- [ ] Not Started
- Dependencies: 000
- Estimated Effort: 3 hours
- Can Run in Parallel: No

## Objective

Implement the Toggl API client using httpx for async HTTP requests, with Result type error handling from the returns library.

## Context

According to PROJECT_OVERVIEW.md:556-579, we need a Toggl client that:
- Uses httpx for async HTTP communication
- Returns Result types for proper error handling
- Fetches time entries with configurable date ranges
- Handles the Toggl API authentication and rate limits gracefully
- Uses pydantic contracts from Task 000 for type safety

The client focuses on fetching time entries - the core data we need for the pipeline.

## Implementation Details

### Files to Create
- `src/toggle_pulse/clients/toggl.py` - Toggl API client implementation

### Files to Modify
- None (new file)

### Key Functions/Classes to Implement

#### TogglClient Class
- **Purpose**: Async client for Toggl Track API v9
- **Constructor**:
  ```python
  class TogglClient:
      def __init__(self, api_token: str, base_url: str = "https://api.track.toggl.com/api/v9"):
          self.api_token = api_token
          self.base_url = base_url
          self._client: Optional[httpx.AsyncClient] = None
  ```

#### Core Methods

1. **async def get_time_entries()**
   ```python
   async def get_time_entries(
       self,
       start_date: Optional[datetime] = None,
       end_date: Optional[datetime] = None
   ) -> Result[List[TogglTimeEntry], Exception]:
       """
       Fetch time entries within date range.

       Args:
           start_date: Start of range (default: 7 days ago)
           end_date: End of range (default: now)

       Returns:
           Result[List[TogglTimeEntry], Exception]: Success with entries or Failure with error
       """
   ```
   - **Logic**:
     1. Default to last 7 days if no dates provided
     2. Validate date range (max 3 months)
     3. Format dates as ISO 8601 strings
     4. Make GET request to /me/time_entries
     5. Parse response using pydantic contracts
     6. Return Result.Success or Result.Failure

2. **async def get_current_time_entry()**
   ```python
   async def get_current_time_entry(self) -> Result[Optional[TogglTimeEntry], Exception]:
       """
       Fetch the currently running time entry if any.

       Returns:
           Result[Optional[TogglTimeEntry], Exception]:
           Success(entry) if running, Success(None) if not, Failure on error
       """
   ```
   - **Logic**:
     1. GET /me/time_entries/current
     2. Parse response or None if no entry running
     3. Return Result type

3. **async def _ensure_client()**
   ```python
   async def _ensure_client(self) -> httpx.AsyncClient:
       """Ensure httpx client is initialized with proper config."""
       if not self._client:
           self._client = httpx.AsyncClient(
               base_url=self.base_url,
               auth=(self.api_token, "api_token"),
               headers={"Content-Type": "application/json"},
               timeout=httpx.Timeout(30.0)
           )
       return self._client
   ```

4. **async def _make_request()**
   ```python
   async def _make_request(
       self,
       method: str,
       endpoint: str,
       params: Optional[Dict] = None
   ) -> Result[Dict, Exception]:
       """
       Make HTTP request with error handling.

       Returns Result.Failure for:
       - Network errors
       - HTTP errors (4xx, 5xx)
       - JSON decode errors
       """
   ```
   - **Error Handling**:
     - HTTPStatusError → Result.Failure with status code
     - RequestError → Result.Failure with network error
     - JSONDecodeError → Result.Failure with parse error
     - Rate limit (429) → Result.Failure with retry info

5. **async def close()**
   ```python
   async def close(self) -> None:
       """Close the httpx client connection."""
       if self._client:
           await self._client.aclose()
           self._client = None
   ```

6. **Context Manager Support**
   ```python
   async def __aenter__(self) -> "TogglClient":
       await self._ensure_client()
       return self

   async def __aexit__(self, *args) -> None:
       await self.close()
   ```

### Error Types

Define custom exceptions for better error handling:
```python
class TogglAPIError(Exception):
    """Base exception for Toggl API errors."""
    pass

class TogglAuthenticationError(TogglAPIError):
    """Authentication failed (401)."""
    pass

class TogglRateLimitError(TogglAPIError):
    """Rate limit exceeded (429)."""
    def __init__(self, retry_after: Optional[int] = None):
        self.retry_after = retry_after
        super().__init__(f"Rate limit exceeded. Retry after {retry_after} seconds")

class TogglValidationError(TogglAPIError):
    """Invalid request parameters (400)."""
    pass
```

### Algorithm/Approach

1. Initialize httpx client with auth and default headers
2. Use Result type for all public methods
3. Parse responses with pydantic contracts
4. Map HTTP errors to specific exception types
5. Support async context manager for resource cleanup
6. Default to sensible date ranges (last 7 days)
7. Validate constraints (3-month max range)

### Integration Points

- Uses pydantic contracts from Task 000
- Returns Result types for functional error handling
- Compatible with async/await patterns
- Used by main.py scheduler for data fetching
- Provides typed responses for transformation

## Testing Requirements

### Test Files
- `src/tests/unit/test_toggl_client.py` - Unit tests for client

### Test Cases

1. **Successful Time Entries Fetch**
   - Input: Valid date range
   - Expected Output: Result.Success with List[TogglTimeEntry]
   - Verification: Entries parsed correctly

2. **Default Date Range**
   - Input: No date parameters
   - Expected Output: Last 7 days of entries
   - Verification: Date calculation correct

3. **Date Range Validation**
   - Input: >3 month range
   - Expected Output: Result.Failure with validation error
   - Verification: Error message explains limit

4. **Empty Response Handling**
   - Input: Date range with no entries
   - Expected Output: Result.Success with empty list
   - Verification: No error for empty data

5. **Current Entry - Running**
   - Input: Request when entry running
   - Expected Output: Result.Success(TogglTimeEntry)
   - Verification: Entry has stop=None

6. **Current Entry - None Running**
   - Input: Request when no entry running
   - Expected Output: Result.Success(None)
   - Verification: None is valid response

7. **Network Error Handling**
   - Input: Simulated connection error
   - Expected Output: Result.Failure with network error
   - Verification: Error wrapped properly

8. **Context Manager Usage**
   - Input: Use with async with
   - Expected Output: Client opens and closes properly
   - Verification: Resources cleaned up

### Fixtures Needed
- Mock httpx responses
- Sample API response data from Task 001

## Acceptance Criteria

- [ ] Client uses httpx for all HTTP operations
- [ ] All methods return Result types
- [ ] Responses parsed with pydantic contracts
- [ ] Date ranges default to last 7 days
- [ ] 3-month range limit enforced
- [ ] Proper authentication headers sent
- [ ] Context manager support works
- [ ] All error types handled gracefully
- [ ] Type hints complete and correct
- [ ] Unit tests achieve 100% coverage

## Notes

- Toggl API uses Basic Auth: base64(api_token:api_token)
- Rate limit: 30 requests/hour per user
- All dates must be ISO 8601 format
- API returns empty array for no entries (not error)
- Consider connection pooling for efficiency
- Use httpx.Timeout for request timeouts

## References

- PROJECT_OVERVIEW.md:559-578 (TogglClient implementation)
- PROJECT_OVERVIEW.md:181-183 (Authentication details)
- Task 000 (Pydantic contracts)
- httpx documentation for async clients
- returns library Result type documentation