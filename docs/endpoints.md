# Endpoints Documentation

## General Information

- **Base URL**: `http://localhost:8000`
- **Response format**: JSON
- **Authentication**: JWT Bearer Token for protected endpoints

## Authentication Schema

```http
Authorization: Bearer <jwt_token>
```

## Endpoints

### Authentication

#### POST /auth/register

Register a new user to the system.

**Body parameters:**
```json
{
  "email": "string",
  "password": "string",
  "confirm_password": "string",
  "username": "string"
}
```

**Custom Validations:**

- `confirm_password` should be the same as `password`
- Validation implemented on the user create model

**Response:**
- `201 Created`: user registered successfully
- `409 Conflict`: email already exists
- `422 Unprocessable Entity`: Invalid data

**Example of successful response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "Jhon Doe",
  "created_at": "2025-10-05T12:00:00Z"
}
```

---

#### POST /auth/login

Authenticate an user and return a JWT token.

**Body parameters:**
```json
{
  "email": "string (requerido)",
  "password": "string (requerido)"
}
```

**Responses:**
- `200 OK`: Successful login
- `401 Unauthorized`: Invalid Credentials

**Example of successful response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### User Management

#### GET /users/me

Return the information of the authenticated user.

**Required Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Response:**
- `200 OK`: User data obtained successfully
- `401 Unauthorized`: Invalid token or expired

**Example of successful response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "usuario@example.com",
  "username": "Jhon Doe",
  "created_at": "2023-10-05T12:00:00Z"
}
```

---

#### PUT /users/me

Update the email, username or both for the authenticated user.

**Required Headers:**
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Parámetros del Body:**
```json
{
  "email": "string (optional)",
  "username": "string (optional)"
}
```

**Note:** At least one field should be passed.

**Respuestas:**
- `200 OK`: User updated successfully
- `422 Unprocessable Entity`: Validation Error
- `401 Unauthorized`: Invalid token or expired
- `409 Conflict`: Invalid Credentials or conflict with email

**Example of successful response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "updated_email@example.com",
  "full_name": "Jhon Doe",
  "created_at": "2023-10-05T12:00:00Z"
}
```

---

#### DELETE /users/me

Delete self account for the authenticated user.

**Required Headers:**
```http
Authorization: Bearer <jwt_token>
```

**Respuestas:**
- `204 No Content`: User deleted successfully
- `401 Unauthorized`: Invalid token or expired
- `404 Not Found`: User not found (weird but still handled)

**Note:** This endpoint returns a 204 status code with no response body upon successful deletion.

---

## Data Models

### UserCreate
```python
class UserCreate(BaseModel):
	username: str
	email: EmailStr
	password: SecretStr
	confirm_password: SecretStr
	
	@field_validator("confirm_password")
	def validate_passwords(cls, v, values):
	if "password" in values.data and v != values.data["password"]:
		raise ValueError("Passwords dont match")
	return v
```

### UserResponse
```python
class UserResponse(BaseModel):
	id: str
	username: str
	email: EmailStr
	created_at: datetime
```

### UserDB
```python
class UserResponse(BaseModel):
	id: str
	username: str
	email: EmailStr
	hashed_password: str
	created_at: datetime
	role: str = "user"
```

### UserLogin
```python
class UserLogin(BaseModel):
	email: EmailStr
	password: SecretStr
```

### UserUpdate
```python
class UserUpdate(BaseModel):
	username: Optional[str] = None
	email: Optional[EmailStr] = None
	
	# use model_validator because we need to validate multiple fields
	@model_validator(mode="after")
	def validate_fields(self):
	# use the parenthesis to handle the conditions correctly
	if (self.username is None or self.username == "") and (self.email is None):
		raise ValueError("at least one field should be passed")
	return self
```

---

## HTTP Status codes

| Código | Descripción           | Casos de Uso                                   |
| ------ | --------------------- | ---------------------------------------------- |
| 200    | OK                    | Successful request (GET, PUT)                  |
| 201    | Created               | Resource created successfully (POST /register) |
| 401    | Unauthorized          | Invalid token, expired or missing              |
| 404    | Not Found             | Resource not found                             |
| 409    | Conflict              | Email already registered                       |
| 422    | Unprocessable Entity  | Error on the data validation                   |
| 500    | Internal Server Error | Error on the server                            |

---

## Validations

### Email
- Valid email format
- Unique in the system

### Password
- Validate that `password` and `confirm_password` are the same (on `POST /auth/register`)
- It is saved with Bcrypt hashing

---

## Authentication flow

1. **Register** → `POST /auth/register`
2. **Login** → `POST /auth/login` (obtain token)
3. **Access to protected endpoints** → Include header `Authorization: Bearer <token>`
4. **Profile management** → Use endpoints under `/users/me`

---

## Important notes

- JWT tokens expire after 30 minutes by default
- Passwords are hashed before uploading to database
- Email is converted to lower case automatically
- Only the authenticated user can access to their data

---

**Last Update**: November 2025  
