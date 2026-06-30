# Todo App - FastAPI + SQLAlchemy + MSSQL

A modern REST API for managing todos with secure JWT authentication, built with FastAPI and SQL Server.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- SQL Server (MSSQL Server with ODBC Driver 18)
- pip

### Installation

1. **Clone the repository**
   ```bash
   cd d:\AI\todo-app
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update database credentials in `.env`:
     ```
     DATABASE_URL="mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC+Driver+18+for+SQL+Server%7D%3BSERVER%3DDESKTOP-8TOH6OI%3BDATABASE%3Dtodo_app_python%3BUID%3Dsa%3BPWD%3Dsa123%3BTrustServerCertificate%3Dyes%3B"
     SECRET_KEY=your_super_secret_key_change_this_in_production
     JWT_ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

5. **Run database migrations**
   ```bash
   .\venv\Scripts\alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   python debug_runner.py
   ```
   Server runs on: http://127.0.0.1:8001
   API Docs: http://127.0.0.1:8001/docs (Swagger UI)

---

## 📋 API Endpoints

### Authentication

**Register User**
```
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

**Login**
```
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=john_doe&password=secure_password
```
Returns: `{"access_token": "jwt_token_here", "token_type": "bearer"}`

### Todos (Requires Authentication)

**Get All Todos**
```
GET /todos/
Authorization: Bearer {access_token}
```

**Create Todo**
```
POST /todos/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

---

## 🏗️ Project Structure

```
todo-app/
├── app/                          # Main application code
│   ├── __init__.py
│   ├── main.py                   # FastAPI app initialization
│   ├── config.py                 # Configuration from .env (BaseSettings)
│   ├── database.py               # SQLAlchemy setup & session management
│   ├── models/                   # ORM models
│   │   ├── user.py               # User entity
│   │   └── todo.py               # Todo entity
│   ├── routes/                   # API endpoints
│   │   ├── auth_routes.py        # Authentication endpoints
│   │   └── todo_routes.py        # Todo CRUD endpoints
│   ├── schemas/                  # Pydantic models (DTOs)
│   │   ├── user.py               # User DTOs
│   │   └── todo.py               # Todo DTOs
│   ├── repositories/             # Data access layer
│   │   ├── user_repository.py    # User queries
│   │   └── todo_respository.py   # Todo queries
│   └── services/                 # Business logic
│       ├── jwt_service.py        # JWT token creation/verification
│       └── security_service.py   # Password hashing
├── alembic/                      # Database migrations
│   ├── env.py                    # Alembic configuration
│   ├── versions/                 # Migration files
│   └── alembic.ini               # Migration settings
├── .env                          # Environment variables (NOT in Git)
├── .env.example                  # Template for .env
├── requirements.txt              # Python dependencies
├── debug_runner.py               # Development server launcher
├── README.md                     # This file
└── CODEBASE.md                   # Detailed documentation
```

---

## 🔐 Security Features

- ✅ **JWT Authentication** - Secure token-based authentication
- ✅ **Password Hashing** - PBKDF2-SHA256 with passlib
- ✅ **OAuth2 Bearer Tokens** - FastAPI security schemes
- ✅ **Environment Variables** - Secrets stored in `.env`
- ✅ **HTTPS Ready** - Production-ready configuration

---

## 💾 Database

### Technology Stack
- **Database**: Microsoft SQL Server (MSSQL)
- **Driver**: ODBC Driver 18 for SQL Server
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic 1.18

### Connection
```
Server: DESKTOP-8TOH6OI
Database: todo_app_python
User: sa
```

### Tables
- **users** - User accounts with hashed passwords
- **todos** - User todos with description and completion status

---

## 🛠️ Development

### Run Tests
```bash
pytest
```

### Apply New Migrations
```bash
alembic revision --autogenerate -m "Description of change"
alembic upgrade head
```

### Check Database Status
```bash
alembic current
alembic history
```

---

## 📦 Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.138.0 | Web framework |
| SQLAlchemy | 2.0.51 | ORM |
| python-jose | - | JWT handling |
| passlib | 1.7.4 | Password hashing |
| pydantic-settings | 2.0.0 | Config management |
| alembic | 1.18.4 | Database migrations |
| uvicorn | 0.49.0 | ASGI server |

---

## 📝 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | SQL Server connection string | `mssql+pyodbc:///?odbc_connect=...` |
| `SECRET_KEY` | JWT signing key | `your_secret_key_here` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

---

## 🐛 Troubleshooting

**Issue**: `ModuleNotFoundError: No module named 'pydantic_settings'`
- **Solution**: `pip install pydantic-settings`

**Issue**: Cannot connect to SQL Server
- **Solution**: Verify DATABASE_URL in `.env` and ensure SQL Server is running. If running SQL Server locally on Windows and connecting from a Docker container, configure SQL Server to listen on `IPAll` port 1433 in SQL Server Configuration Manager and map the hostname using `--add-host=DESKTOP-8TOH6OI:host-gateway`.

**Issue**: SQL Server container crashes with `This program requires a machine with at least 2000 megabytes of memory`
- **Solution**: If running on a 1 GB instance like a `t2.micro` EC2 instance, you must configure a swap file (virtual RAM) on the host (e.g. `sudo fallocate -l 1.5G /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile`). Alternatively, host your SQL Server instance in AWS RDS (which offers a Free Tier-eligible Express Edition) to offload the database entirely from the EC2 instance.

**Issue**: `no space left on device` when pulling/extracting Docker images on EC2
- **Solution**: The default EC2 storage is often 8 GB. You can clean up the Docker cache using `sudo docker system prune -a -f --volumes`. You should also use the `python:3.12-slim` base image to minimize disk footprint. If necessary, modify your EC2 EBS volume size to 15 GB or 20 GB in the AWS Console and reboot to automatically expand the filesystem.

**Issue**: `CREATE TABLE permission denied in database 'master'` on AWS RDS
- **Solution**: RDS administrative users do not have permissions to write tables directly inside the system `master` database. Connect to `master` first and execute `CREATE DATABASE todo_app_python;` to create a dedicated application database, then configure your FastAPI connection string to point to this new database.

**Issue**: Alembic migration fails
- **Solution**: Run `alembic upgrade head` and check migration version.

---

## 📚 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8949)

---

## 📄 License

MIT License - Feel free to use this project for learning and development.

---

**For detailed codebase documentation with ASP.NET Core comparisons, see [CODEBASE.md](CODEBASE.md)**
