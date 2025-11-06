# API Request Examples with HTTPie

## Base Information

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json` (default in HTTPie)
- **Authentication**: JWT Bearer Token

## Installation

```bash
# Install HTTPie
pip install httpie

# Or using package manager (Ubuntu/Debian)
sudo apt install httpie

# Or using Homebrew (macOS)
brew install httpie
```

## Authentication Endpoints

### Register User

**Request:**
```bash
http POST http://localhost:8000/auth/register \
  email="user@example.com" \
  password="SecurePass123" \
  confirm_password="SecurePass123" \
  username="John Doe"
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
http POST http://localhost:8000/auth/register \
  email="user@example.com" \
  password="SecurePass123" \
  confirm_password="DifferentPass456" \
  username="John Doe"
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
http POST http://localhost:8000/auth/login \
  email="user@example.com" \
  password="SecurePass123"
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
http POST http://localhost:8000/auth/login \
  email="user@example.com" \
  password="WrongPassword"
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
http GET http://localhost:8000/users/me \
  "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDdmMWY3N2JjZjg2Y2Q3OTk0MzkwMTEiLCJleHAiOjE2OTY1MDAwMDB9.example_token"
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

**Alternative syntax for Authorization header:**
```bash
http GET http://localhost:8000/users/me \
  Authorization:"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Error Response - Invalid token (401 Unauthorized):**
```bash
http GET http://localhost:8000/users/me \
	"Authorization: Bearer invalid_token_here"
```

**Error Response:**
```json
{
  "detail": "Invalid token"
}
```

**Error Response - Token expired (401 Unauthorized):**
```bash
http GET http://localhost:8000/users/me \
	"Authorization: Bearer token_expired"
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
http PUT http://localhost:8000/users/me \
  "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDdmMWY3N2JjZjg2Y2Q3OTk0MzkwMTEiLCJleHAiOjE2OTY1MDAwMDB9.example_token" \
  username="John Michael Doe" \
  email="new_email@example.com"
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
http PUT http://localhost:8000/users/me \
  "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  username="John Michael Doe"
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
http PUT http://localhost:8000/users/me \
	"Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDdmMWY3N2JjZjg2Y2Q3OTk0MzkwMTEiLCJleHAiOjE2OTY1MDAwMDB9.example_token"
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
http DELETE http://localhost:8000/users/me \
  "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1MDdmMWY3N2JjZjg2Y2Q3OTk0MzkwMTEiLCJleHAiOjE2OTY1MDAwMDB9.example_token"
```

**Expected Response (204 No Content):**
```
// No response body - account successfully deleted
```

---

## Complete Workflow Example

### Step 1: Register a new user
```bash
http POST http://localhost:8000/auth/register \
  email="testuser@example.com" \
  password="TestPass123" \
  confirm_password="TestPass123" \
  username="Test User"
```

### Step 2: Login to get JWT token
```bash
http POST http://localhost:8000/auth/login \
  email="testuser@example.com" \
  password="TestPass123"
```

### Step 3: Save the token and use it for protected requests
```bash
# Use the token for protected requests
http GET http://localhost:8000/users/me \
  "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Useful HTTPie Options and Features

### Output Formatting
```bash
# Pretty print with colors (default)
http http://localhost:8000/api/users/me

# Output without colors
http --pretty=none http://localhost:8000/api/users/me

# View response headers only
http --headers http://localhost:8000/api/users/me

# View entire HTTP exchange
http --verbose http://localhost:8000/api/users/me

# Save response to file
http http://localhost:8000/api/users/me > response.json
```

### Session Management
```bash
# Create a session to persist headers
http --session=my_session POST http://localhost:8000/api/auth/login \
  email="user@example.com" password="SecurePass123"

# Use the session (Authorization header is persisted)
http --session=my_session GET http://localhost:8000/api/users/me
```

### Different HTTP Methods
```bash
# GET (default method)
http http://localhost:8000/users/me

# POST
http POST http://localhost:8000/auth/register ...

# PUT
http PUT http://localhost:8000/users/me ...

# PATCH
http PATCH http://localhost:8000/users/me ...

# DELETE
http DELETE http://localhost:8000/users/me
```

### Query Parameters
```bash
# For endpoints that support query parameters
http GET http://localhost:8000/api/users page==1 limit==10
```

### Form Data
```bash
# For form-encoded data (instead of JSON)
http --form POST http://localhost:8000/api/upload \
  field_name="value" file@/path/to/file.txt
```

## Environment Variables in HTTPie

```bash
# Set base URL as environment variable
export API_BASE="http://localhost:8000"

# Use environment variable in requests
http GET $API_BASE/api/users/me

# Or use HTTPie's environment feature
http --offline --print=HhBb localhost:8000/api/users/me | \
  sed "s|localhost:8000|$API_BASE|" | http
```

## Testing Tips

1. **Use verbose mode for debugging:**
   ```bash
   http --verbose POST http://localhost:8000/auth/login ...
   ```

2. **Follow redirects:**
   ```bash
   http --follow http://localhost:8000/api/redirect
   ```

3. **Ignore SSL certificate errors (for testing):**
   ```bash
   http --verify=no https://localhost:8000/users/me
   ```

4. **Set custom timeout:**
   ```bash
   http --timeout=30 http://localhost:8000/users/me
   ```

5. **Use jq for JSON processing:**
   ```bash
   http http://localhost:8000/users/me | jq '.email'
   ```

6. **Download files:**
   ```bash
   http --download http://localhost:8000/api/files/myfile.pdf
   ```

---

**Note**: HTTPie automatically sets the `Content-Type: application/json` header when you pass JSON data, and it formats JSON responses in a readable way by default.
