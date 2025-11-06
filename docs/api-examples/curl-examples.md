# API Request Examples with cURL

## Base Information

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`
- **Authentication**: JWT Bearer Token

## Authentication Endpoints

### Register User

**Request:**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123",
    "username": "John Doe"
  }'
```

**Expected Response (201 Created):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "John Doe",
  "created_at": "2025-10-05T12:00:00Z"
}
```

**Error Response - Passwords don't match (422 Unprocessable Entity):**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "confirm_password": "DifferentPass456",
    "username": "John Doe"
  }'
```

**Error Response:**
```json
{
    "detail": [
        {
            "ctx": {
                "error": {}
            },
            "input": "DifferentPass456",
            "loc": [
                "body",
                "confirm_password"
            ],
            "msg": "Value error, Passwords dont match",
            "type": "value_error"
        }
    ]
}
```

---

### Login User

**Request:**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

**Expected Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDdmMWY3N2JjZjg2Y2Q3OTk0MzkwMTEiLCJleHAiOjE2OTY1MDAwMDB9.example_token",
  "token_type": "bearer"
}
```

**Error Response - Invalid credentials (401 Unauthorized):**
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "WrongPassword"
  }'
```

**Error Response:**
```json
{
  "detail": "Incorrect Credentials"
}
```

---

## User Management Endpoints

### Get User Profile

**Request:**
```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDdmMWY3N2JjZjg2Y2Q3OTk0MzkwMTEiLCJleHAiOjE2OTY1MDAwMDB9.example_token"
```

**Expected Response (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "John Doe",
  "created_at": "2025-10-05T12:00:00Z"
}
```

**Error Response - Invalid token (401 Unauthorized):**
```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer invalid_token_here"
```

**Error Response:**
```json
{
  "detail": "Invalid token"
}
```

**Error Response - Token expired (401 Unauthorized):**
```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer token_expired"
```

**Error Response:**
```json
{
  "detail": "Token expired"
}
```

---

### Update User Profile

**Request:**
```bash
curl -X PUT "http://localhost:8000/users/me" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDdmMWY3N2JjZjg2Y2Q3OTk0MzkwMTEiLCJleHAiOjE2OTY1MDAwMDB9.example_token" \
  -d '{
    "username": "John Michael Doe",
    "email": "new_email@example.com"
  }'
```

**Expected Response (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "new_email@example.com",
  "username": "John Michael Doe",
  "created_at": "2025-10-05T12:00:00Z"
}
```

**Partial Update Request:**
```bash
curl -X PUT "http://localhost:8000/users/me" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDdmMWY3N2JjZjg2Y2Q3OTk0MzkwMTEiLCJleHAiOjE2OTY1MDAwMDB9.example_token" \
  -d '{
    "username": "John Michael Doe"
  }'
```

**Expected Response (200 OK):**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "John Michael Doe",
  "created_at": "2025-10-05T12:00:00Z"
}
```

**Error Response - Empty fields (422 Unprocessable Entity):**
```bash
curl -X PUT "http://localhost:8000/users/me" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDdmMWY3N2JjZjg2Y2Q3OTk0MzkwMTEiLCJleHAiOjE2OTY1MDAwMDB9.example_token" \
```

**Error Response:**
```json
{
    "detail": [
        {
            "input": null,
            "loc": [
                "body"
            ],
            "msg": "Field required",
            "type": "missing"
        }
    ]
}
```

---

### Delete User Account

**Request:**
```bash
curl -X DELETE "http://localhost:8000/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDdmMWY3N2JjZjg2Y2Q3OTk0MzkwMTEiLCJleHAiOjE2OTY1MDAwMDB9.example_token"
```

**Expected Response (204 No Content):**
```
// No response body - account successfully deleted
```

---

## Complete Workflow Example

### Step 1: Register a new user
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "TestPass123",
    "confirm_password": "TestPass123",
    "username": "Test User"
  }'
```

### Step 2: Login to get JWT token
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "TestPass123"
  }'
```

### Step 3: Save the token and use it for protected requests
```bash
# Use the token for protected requests
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Common cURL Options

| Option | Description | Example |
|--------|-------------|---------|
| `-X` | HTTP method | `-X GET`, `-X POST` |
| `-H` | Header | `-H "Content-Type: application/json"` |
| `-d` | Request body | `-d '{"key": "value"}'` |
| `-i` | Include response headers | `curl -i ...` |
| `-v` | Verbose output | `curl -v ...` |
| `--output` | Save response to file | `--output response.json` |

---

**Note**: Replace the example JWT tokens with actual tokens received from the login endpoint.
