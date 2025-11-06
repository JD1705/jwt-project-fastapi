# JWT FastAPI Project
## Description 
Authentication and user management microservice that provides a secure registration, login, and profile management system using JWT authentication. Developed with FastAPI for high performance and MongoDB for flexible data storage.

Note: Service specialized in user management with RESTful API and JWT authentication.
## Features

- **JWT Authentication**: safe authentication system with tokens
	
- **FastAPI**: modern and fast framework with automatic documentation
	
- **MongoDB**: flexible and scalable NoSQL database
	
- **User Management**: full CRUD for user profiles
	
- **Security**: password hashing with bcrypt
    
- **API RESTful**: well defined endpoints and documented
    
- **Documentation**: API documented with Swagger/OpenAPI
    
- **Tests**: complete testing system with pytest
    
## Technologies

### Backend

- **language**: Python 3.8+
    
- **Framework**: FastAPI
    
- **Database**: MongoDB
	
- **Authentication**: JWT (python-jose[cryptography])
	
- **Hashing**: bcrypt 
### Desarrollo

- **Testing**: Pytest
    
- **Documentación**: Swagger UI / ReDoc (automatic)
    
- **Validation**: Pydantic
	
- **ASGI Server**: Uvicorn 

## Instalation

### Prerequisites

- Python 3.8 or higher
    
- MongoDB 5.0 or higher
    
- pip (python package manager)

### Local configuration

1. **clone the repository**
```bash
git clone https://github.com/JD1705/jwt-fastapi-project.git
cd jwt-fastapi-project
```
**Configurate the virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```
**Install dependencies**
```bash
pip install -r requirements.txt
```
**Configurate environment variables**
```bash
cp .env.example .env
# Edit .env with your configurations
```
**Execute developer server**
```bash
uvicorn main:app --reload --port 8000
```
## Configuration

### Environment variables
```env
# Database
MONGO_URI=mongodb://localhost:27017

# JWT
SECRET_KEY=tu-clave-secreta-super-segura-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_TIME=30
```
## Usage

### Execute in development
```bash
uvicorn main:app --reload --port 8000
```
Application will be available on:

- **API**: [http://localhost:8000](http://localhost:8000)
    
- **Interactive Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
    
- **Alternative Documentation**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
### Execute tests
```bash
pytest
```
## API Endpoints

| Método | Endpoint         | Descripción      | Autenticación |
| ------ | ---------------- | ---------------- | ------------- |
| POST   | `/auth/login`    | Sign in          | no            |
| POST   | `/auth/register` | Register user    | no            |
| GET    | `/users/me`      | User profile     | yes           |
| PUT    | `/users/me`      | Update self user | yes           |
| DELETE | `/users/me`      | Delete self user | yes           |

**Note**: see a more detailed endpoints information [here](docs/endpoints.md)

### Request Example
#### User Register
**curl**
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "safe_password",
    "confirm_password":"safe_password",
    "username": "Jhon Doe"
  }'
```
**httpie**
```bash
http POST http://localhost:8000/auth/register \
  email="user@example.com" \
  password="safe_password" \
  confirm_password="safe_password" \
  username="Jhon Doe"
```
**Postman**
```text
POST http://localhost:8000/auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "safe_password",
    "confirm_password":"safe_password",
    "username": "Jhon Doe"
}
```
**Expected Response:**
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "username": "Jhon Doe",
  "created_at": "2025-10-05T12:00:00Z"
}
```

for full request examples you can check see the [HTTPie](docs/api-examples/httpie-commands.md) file or the [curl](docs/api-examples/curl-examples.md) file

## Project Structure

```text
jwt-fastapi-project/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── auth.py
│   │   └── users.py
│   ├── utils/
│   │   ├── dependencies.py
│   │   └── security.py
│   ├── models.py
│   ├── database.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_users.py
├── docs/
│   ├── api-examples/
│   │   ├── httpie-commands.md
│   │   └── curl-examples.md
│   └── endpoints.md
│
├── __init__.py
├── .env
├── .env_example
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

## Testing

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests específicos
pytest tests/test_auth.py -v
```

## Contribution

1. Fork the project
    
2. Create a branch for your feature (`git checkout -b feature/ExampleFeature`)
    
3. Commit your changes (`git commit -m 'Add some ExampleFeature'`)
    
4. Push to the branch (`git push origin feature/ExampleFeature`)
    
5. Open a Pull Request
### Development Guide
- Add test for new features
    
- Update documentation after adding features
    
- Use descriptive commit messages
## License

This project is under MIT License - check the file [LICENSE](LICENSE) for more details.
