# Task 002: Test Authentication Mechanisms

## Status
- [ ] Not Started
- Dependencies: 001
- Estimated Effort: 3-4 hours
- Can Run in Parallel: No

## Objective

Implement comprehensive integration tests for Toggl API authentication including API token auth, email/password auth, and authentication error handling.

## Context

According to PROJECT_OVERVIEW.md:181-183, Toggl uses Basic Auth with either API token or email/password credentials. The base URL is https://api.track.toggl.com/api/v9/. We need to test:
- Successful authentication with API token
- Successful authentication with email/password
- Failed authentication scenarios
- Header validation (Content-Type: application/json)
- Rate limiting behavior (30 requests/hour per user)

## Implementation Details

### Files to Create
- `src/tests/integration/test_toggl_authentication.py` - Authentication tests

### Files to Modify
- None (new test file)

### Key Functions/Classes to Implement

#### test_toggl_authentication.py

##### Test Functions

1. **test_api_token_authentication_success**
   - **Purpose**: Verify successful auth with API token
   - **Setup**: Mock successful /me endpoint response
   - **Verification**: Assert auth header is correct, response is Success

2. **test_api_token_authentication_failure**
   - **Purpose**: Verify handling of invalid API token
   - **Setup**: Mock 401 unauthorized response
   - **Verification**: Assert Result is Failure with auth error

3. **test_email_password_authentication_success**
   - **Purpose**: Verify successful auth with email/password
   - **Setup**: Mock successful /me endpoint response
   - **Verification**: Assert basic auth encoding is correct

4. **test_missing_authentication**
   - **Purpose**: Verify request fails without auth
   - **Setup**: Mock 401 response for missing auth
   - **Verification**: Assert appropriate error is returned

5. **test_malformed_authentication_header**
   - **Purpose**: Test handling of malformed auth headers
   - **Setup**: Various malformed auth header scenarios
   - **Verification**: Assert proper error handling

6. **test_authentication_with_expired_token**
   - **Purpose**: Test expired token handling
   - **Setup**: Mock 403 forbidden response
   - **Verification**: Assert Result contains specific error

7. **test_rate_limit_handling**
   - **Purpose**: Verify rate limit detection and handling
   - **Setup**: Mock 429 Too Many Requests response
   - **Verification**: Assert rate limit error is properly wrapped

8. **test_content_type_header_requirement**
   - **Purpose**: Verify Content-Type header is sent
   - **Setup**: Capture request headers in mock
   - **Verification**: Assert Content-Type: application/json is present

### Algorithm/Approach

1. Create test class TestTogglAuthentication
2. Use httpx_mock to simulate API responses
3. Test each authentication method independently
4. Verify headers are correctly formatted
5. Test error scenarios comprehensively
6. Use Result type assertions from test helpers

### Integration Points

- Uses fixtures from Task 001
- Tests authentication used by all API endpoints
- Validates httpx client configuration
- Tests returns library Result error handling

## Testing Requirements

### Test Files
- `src/tests/integration/test_toggl_authentication.py` - Main test file

### Test Cases

1. **Successful API Token Auth**
   - Input: Valid API token "test_token_123"
   - Expected Output: Result.Success with user data
   - Verification: Auth header = "Basic dGVzdF90b2tlbl8xMjM6YXBpX3Rva2Vu"

2. **Failed API Token Auth**
   - Input: Invalid API token "bad_token"
   - Expected Output: Result.Failure with AuthenticationError
   - Verification: Error message contains "401"

3. **Rate Limit Detection**
   - Input: Any request after rate limit
   - Expected Output: Result.Failure with RateLimitError
   - Verification: Error includes retry-after header value

4. **Missing Content-Type**
   - Input: Request without Content-Type
   - Expected Output: Request includes Content-Type header
   - Verification: Header value is "application/json"

### Fixtures Needed
- `httpx_mock` - From pytest-httpx
- `toggl_api_token` - From Task 001
- `sample_user_data` - From Task 001

## Acceptance Criteria

- [ ] All authentication methods are tested
- [ ] Error scenarios return proper Result.Failure types
- [ ] Rate limiting is detected and handled
- [ ] Headers are correctly validated
- [ ] Base64 encoding for Basic Auth is correct
- [ ] All tests use async/await properly
- [ ] Tests are isolated and idempotent

## Notes

- Basic Auth encoding: base64(api_token:api_token) for token auth
- Basic Auth encoding: base64(email:password) for email auth
- Rate limit is 30 requests/hour per user
- Consider testing token refresh scenarios if applicable

## References

- PROJECT_OVERVIEW.md:181-183 (Authentication details)
- PROJECT_OVERVIEW.md:565-578 (TogglClient auth implementation)
- Toggl API docs on authentication