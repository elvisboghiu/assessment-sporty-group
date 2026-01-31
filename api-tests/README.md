# API Tests - JSONPlaceholder (Pytest + Requests)

## Overview
Automated API tests for the JSONPlaceholder public API.

Base URL: `https://jsonplaceholder.typicode.com`

## Repository Structure
```
api-tests/
├── tests/                 # Test files
│   └── test_jsonplaceholder_api.py
├── pytest.ini            # Pytest configuration
└── README.md            # This file
```

## Requirements
- Python 3.10+

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r ../requirements.txt
```
Or from the repo root:
```bash
pip install -r requirements.txt
```

## Run
```bash
python -m pytest
```

## Test Cases

| ID | Test Case | Endpoint | Method | Validation |
| --- | --- | --- | --- | --- |
| API-01 | List endpoints return 200 and non-empty | `/posts`, `/comments`, `/users`, `/albums`, `/photos`, `/todos` | GET | Status code 200, response is list, length > 0 |
| API-02 | Get post by id returns expected schema | `/posts/{id}` | GET | Status code 200, `id` matches, has `userId`, `title`, `body` |
| API-03 | Comments for post match post id | `/posts/{id}/comments` | GET | Status code 200, list non-empty, every `postId` equals requested id |
| API-04 | Nested comments match filtered query | `/posts/{id}/comments` and `/comments?postId={id}` | GET | Status code 200, lists non-empty, same comment ids |
| API-05 | Create post returns 201 and echoes payload | `/posts` | POST | Status code 201, response contains posted `title`, `body`, `userId`, `id` |
| API-06 | PUT update returns 200 and echoes payload | `/posts/1` | PUT | Status code 200, response matches full payload |
| API-07 | PATCH update returns 200 and merges fields | `/posts/1` | PATCH | Status code 200, `title` updated, `body`/`userId` still present |
| API-08 | Delete returns 200 and empty body | `/posts/1` | DELETE | Status code 200, response body is `{}` |

## Validation Strategy

### Why These Validations?

1. **Status Code Validation** - Ensures API contract stability and correct HTTP semantics
   - 200 for successful GET requests
   - 201 for successful POST requests (resource created)

2. **Response Type Validation** - Confirms data structure integrity
   - List endpoints return arrays
   - Single resource endpoints return objects

3. **Schema Validation** - Verifies required fields are present
   - Ensures all expected fields exist in responses
   - Validates data types implicitly through assertions

4. **Content Validation** - Confirms relational correctness
   - `postId` in comments matches the requested post
   - Nested route `/posts/{id}/comments` matches filtered `/comments?postId={id}`
   - Posted data is echoed back correctly in POST responses
   - PUT/PATCH responses echo the update payload (JSONPlaceholder fakes updates)
   - Ensures the API processes and stores data correctly

5. **Parametrization** - Reduces code duplication while maintaining coverage
   - Tests multiple scenarios with the same logic
   - Easier to add new test cases
   - Clear test output showing which parameters were tested

## Framework Design
- **Pytest Parametrize**: Reduces code duplication while testing multiple scenarios
- **Timeout Handling**: All requests have 10-second timeouts to prevent hanging
- **Clear Assertions**: Each assertion validates a specific aspect of the API contract
- **Scalable Structure**: Easy to add new endpoints and test cases

## Notes
- Tests use the public JSONPlaceholder mock API (no authentication required)
- JSONPlaceholder fakes writes; POST/PUT/PATCH/DELETE responses echo expected data but do not persist changes
- All tests are independent and can run in any order
- Parametrized tests provide clear output showing which parameters were tested

## GIF
![API tests demo](../assets/api-tests.gif)
