# 📚 Detailed Codebase Documentation

A comprehensive guide to the Todo App architecture with **ASP.NET Core comparisons** for developers transitioning from the Microsoft ecosystem.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Concepts with ASP.NET Core Comparisons](#core-concepts-with-aspnet-core-comparisons)
4. [Detailed Component Guide](#detailed-component-guide)
5. [Data Flow & Request Lifecycle](#data-flow--request-lifecycle)
6. [Key Patterns & Best Practices](#key-patterns--best-practices)

---

## Architecture Overview

### Layered Architecture Pattern

```
┌─────────────────────────────────────────┐
│         API Routes (Controllers)         │  ← FastAPI Router (like ASP.NET Core Controller)
│   - auth_routes.py                      │
│   - todo_routes.py                      │
└────────────────┬────────────────────────┘
                 │ (Depends on)
┌────────────────▼────────────────────────┐
│    Services (Business Logic)             │  ← Service layer (like ASP.NET Core Services)
│   - jwt_service.py                      │
│   - security_service.py                 │
└────────────────┬────────────────────────┘
                 │ (Uses)
┌────────────────▼────────────────────────┐
│   Repositories (Data Access)             │  ← Repository pattern (like EF Core DbContext)
│   - user_repository.py                  │
│   - todo_repository.py                  │
└────────────────┬────────────────────────┘
                 │ (Queries)
┌────────────────▼────────────────────────┐
│    Database (SQLAlchemy + MSSQL)         │  ← EF Core equivalent
│   - Models (User, Todo)                 │
│   - Alembic Migrations                  │
└─────────────────────────────────────────┘
```

### Technology Stack Comparison

| Aspect | FastAPI/Python | ASP.NET Core |
|--------|---|---|
| **Framework** | FastAPI | ASP.NET Core |
| **ORM** | SQLAlchemy | Entity Framework Core (EF Core) |
| **Web Server** | Uvicorn (ASGI) | Kestrel (IIS) |
| **Dependency Injection** | FastAPI's `Depends()` | Built-in DI Container |
| **Data Validation** | Pydantic | Data Annotations |
| **Configuration** | python-dotenv + Pydantic Settings | Configuration Providers |
| **Migrations** | Alembic | EF Core Migrations |
| **Authentication** | JWT + OAuth2 | Identity + JWT |
| **Password Hashing** | passlib + PBKDF2 | Identity PasswordHasher |

---

## Project Structure

### Directory Layout with Explanations

```
todo-app/
│
├── app/                                 # Application root (like your ASP.NET project folder)
│   │
│   ├── __init__.py                      # Makes 'app' a Python package
│   │
│   ├── main.py                          # Entry point (≈ Program.cs in ASP.NET)
│   │                                    # ├── Creates FastAPI instance
│   │                                    # ├── Registers routers (controllers)
│   │                                    # └── Initializes database
│   │
│   ├── config.py                        # Configuration management
│   │                                    # ├── Reads from .env file
│   │                                    # ├── Type-validated settings (≈ IOptions<T>)
│   │                                    # └── Pydantic BaseSettings class
│   │
│   ├── database.py                      # Database setup (≈ DbContext)
│   │                                    # ├── SQLAlchemy engine creation
│   │                                    # ├── Session factory (SessionLocal)
│   │                                    # ├── Declarative base (Base metadata)
│   │                                    # └── Dependency injection: get_db()
│   │
│   ├── models/                          # ORM Entity Models (≈ DbSet entities)
│   │   ├── user.py                      # User entity with relationships
│   │   └── todo.py                      # Todo entity with foreign keys
│   │
│   ├── routes/                          # API Endpoints (≈ Controllers)
│   │   ├── auth_routes.py               # Authentication endpoints
│   │   │                                # ├── POST /auth/register
│   │   │                                # └── POST /auth/login
│   │   │
│   │   └── todo_routes.py               # Todo CRUD endpoints
│   │                                    # ├── GET /todos
│   │                                    # └── POST /todos
│   │
│   ├── schemas/                         # Pydantic Models (≈ DTOs - Data Transfer Objects)
│   │   ├── user.py                      # UserRegister, UserLogin schemas
│   │   └── todo.py                      # TodoCreate, TodoResponse schemas
│   │
│   ├── repositories/                    # Data Access Layer (≈ Repository Pattern)
│   │   ├── user_repository.py           # User queries (get_by_email, create_user, etc.)
│   │   └── todo_respository.py          # Todo queries (get_all_todos, create_todo, etc.)
│   │
│   └── services/                        # Business Logic (≈ Service Classes)
│       ├── jwt_service.py               # JWT token creation/verification + auth
│       └── security_service.py          # Password hashing/verification
│
├── alembic/                             # Database Migrations (≈ EF Core Migrations)
│   ├── env.py                           # Alembic environment configuration
│   ├── alembic.ini                      # Alembic settings file
│   └── versions/                        # Migration history
│       └── 0001_add_description_to_todos.py  # Example migration
│
├── .env                                 # Environment secrets (NOT in Git)
│                                        # ├── DATABASE_URL
│                                        # ├── SECRET_KEY
│                                        # ├── JWT_ALGORITHM
│                                        # └── ACCESS_TOKEN_EXPIRE_MINUTES
│
├── .env.example                         # Template (commit to Git)
│
├── requirements.txt                     # Python dependencies (like .csproj)
│
├── debug_runner.py                      # Dev server launcher
│
└── README.md                            # Quick start guide

```

---

## Core Concepts with ASP.NET Core Comparisons

### 1. **FastAPI Framework** vs **ASP.NET Core**

#### FastAPI (routes/auth_routes.py)
```python
from fastapi import APIRouter, Depends

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    return user_repository.create_user(user=user, db=db)
```

#### ASP.NET Core Equivalent (Controllers)
```csharp
[ApiController]
[Route("[controller]")]
public class AuthController : ControllerBase
{
    private readonly IUserRepository _userRepository;
    
    public AuthController(IUserRepository userRepository)
    {
        _userRepository = userRepository;
    }
    
    [HttpPost("register")]
    public IActionResult RegisterUser([FromBody] UserRegisterDto user)
    {
        return Ok(_userRepository.CreateUser(user));
    }
}
```

**Key Differences:**
- FastAPI uses decorators (`@auth_router.post()`) vs ASP.NET attributes (`[HttpPost]`)
- FastAPI routes are grouped with `APIRouter` vs ASP.NET uses `ControllerBase`
- FastAPI uses type hints for automatic validation vs ASP.NET uses attributes
- Both support dependency injection via parameters

---

### 2. **Pydantic Models** vs **DTOs (Data Transfer Objects)**

#### Pydantic (schemas/user.py)
```python
from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    
    class Config:
        from_attributes = True  # ORM mode
```

#### ASP.NET Core Equivalent (DTOs)
```csharp
public class UserRegisterDto
{
    [Required]
    public string Username { get; set; }
    
    [Required]
    [EmailAddress]
    public string Email { get; set; }
    
    [Required]
    public string Password { get; set; }
}
```

**Key Differences:**
- Pydantic validates at runtime vs ASP.NET validates via attributes
- Pydantic automatically serializes to JSON vs ASP.NET uses JsonSerializer
- Pydantic's `from_attributes=True` enables ORM model conversion (like EF Core `AsNoTracking()`)
- Both provide request/response validation

---

### 3. **SQLAlchemy ORM** vs **Entity Framework Core**

#### SQLAlchemy Model (models/user.py)
```python
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Navigation property (like virtual properties in EF Core)
    todos = relationship("Todo", back_populates="user")
```

#### EF Core Equivalent (Models)
```csharp
public class User
{
    [Key]
    public int Id { get; set; }
    
    [Required]
    [MaxLength(50)]
    public string Username { get; set; }
    
    [Required]
    [EmailAddress]
    [MaxLength(255)]
    public string Email { get; set; }
    
    [Required]
    [MaxLength(255)]
    public string PasswordHash { get; set; }
    
    // Navigation property
    public virtual ICollection<Todo> Todos { get; set; }
}
```

**Key Differences:**
- SQLAlchemy uses class attributes vs EF Core uses properties
- SQLAlchemy uses `Column()` vs EF Core uses attributes and Fluent API
- Both support relationships and lazy loading
- Both generate database schema from models

---

### 4. **Dependency Injection** via `Depends()`

#### FastAPI with Dependencies (routes/todo_routes.py)
```python
from fastapi import Depends
from app.database import get_db

@todo_router.get("/")
def get_all_todos(
    db: Session = Depends(get_db),  # Injected dependency
    current_user: dict = Depends(get_current_user)  # JWT verification
):
    return repository.get_all_todos(db)
```

#### ASP.NET Core with DI Container
```csharp
[ApiController]
[Route("[controller]")]
public class TodoController : ControllerBase
{
    private readonly ITodoRepository _repository;
    
    // Constructor injection
    public TodoController(ITodoRepository repository)
    {
        _repository = repository;
    }
    
    [HttpGet]
    [Authorize]  // Equivalent to Depends(get_current_user)
    public IActionResult GetAllTodos()
    {
        return Ok(_repository.GetAllTodos());
    }
}
```

**Key Differences:**
- FastAPI uses `Depends()` in function parameters vs ASP.NET uses constructor injection
- FastAPI dependencies are evaluated per-request vs ASP.NET services registered in DI container
- Both support dependency scoping and lifecycle management
- FastAPI dependencies can be nested and conditional

---

### 5. **Repository Pattern** (Data Access Layer)

#### SQLAlchemy Repository (repositories/user_repository.py)
```python
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def get_user_by_email(self, email: str, db: Session):
        return db.query(User).filter(User.email == email).first()
    
    def create_user(self, user: UserRegister, db: Session):
        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
```

#### EF Core Repository Equivalent
```csharp
public class UserRepository : IUserRepository
{
    private readonly TodoDbContext _context;
    
    public UserRepository(TodoDbContext context)
    {
        _context = context;
    }
    
    public User GetUserByEmail(string email)
    {
        return _context.Users.FirstOrDefault(u => u.Email == email);
    }
    
    public User CreateUser(UserRegisterDto user)
    {
        var newUser = new User
        {
            Username = user.Username,
            Email = user.Email,
            PasswordHash = HashPassword(user.Password)
        };
        _context.Users.Add(newUser);
        _context.SaveChanges();
        return newUser;
    }
}
```

**Key Differences:**
- SQLAlchemy passes `Session` explicitly vs EF Core uses injected `DbContext`
- SQLAlchemy uses `.query()` vs EF Core uses `.DbSet` with LINQ
- Both support transaction management and change tracking
- Both implement the repository pattern for data abstraction

---

### 6. **Authentication & Authorization**

#### FastAPI with JWT (services/jwt_service.py)
```python
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"id": user_id}
```

#### ASP.NET Core with JWT
```csharp
public class AuthService
{
    public string GenerateJwtToken(User user)
    {
        var tokenHandler = new JwtSecurityTokenHandler();
        var key = Encoding.ASCII.GetBytes(_settings.SecretKey);
        
        var tokenDescriptor = new SecurityTokenDescriptor
        {
            Subject = new ClaimsIdentity(new[]
            {
                new Claim("id", user.Id.ToString())
            }),
            Expires = DateTime.UtcNow.AddMinutes(_settings.AccessTokenExpireMinutes),
            SigningCredentials = new SigningCredentials(
                new SymmetricSecurityKey(key), 
                SecurityAlgorithms.HmacSha256Signature
            )
        };
        
        var token = tokenHandler.CreateToken(tokenDescriptor);
        return tokenHandler.WriteToken(token);
    }
}
```

**Key Differences:**
- FastAPI uses `OAuth2PasswordBearer` vs ASP.NET uses `JwtBearerDefaults`
- FastAPI validates tokens in dependency functions vs ASP.NET uses middleware/filters
- Both use JWT with claims for user identification
- Both support custom claims and token expiration

---

### 7. **Database Configuration & Migrations**

#### Alembic Migration (alembic/versions/0001_add_description_to_todos.py)
```python
def upgrade() -> None:
    op.add_column('todos', sa.Column('description', sa.String(length=500), nullable=True))

def downgrade() -> None:
    op.drop_column('todos', 'description')
```

#### EF Core Migration Equivalent
```csharp
protected override void Up(MigrationBuilder migrationBuilder)
{
    migrationBuilder.AddColumn<string>(
        name: "description",
        table: "todos",
        type: "nvarchar(500)",
        maxLength: 500,
        nullable: true
    );
}

protected override void Down(MigrationBuilder migrationBuilder)
{
    migrationBuilder.DropColumn(name: "description", table: "todos");
}
```

**Command Comparison:**

| Operation | SQLAlchemy/Alembic | EF Core |
|-----------|---|---|
| Create migration | `alembic revision --autogenerate -m "message"` | `dotnet ef migrations add MigrationName` |
| Apply migrations | `alembic upgrade head` | `dotnet ef database update` |
| Rollback | `alembic downgrade -1` | `dotnet ef database update PreviousMigration` |
| Check status | `alembic current` | `dotnet ef migrations list` |

---

## Detailed Component Guide

### 1. **app/config.py** - Configuration Management

**Purpose:** Centralized configuration from environment variables

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

**How it works:**
1. Reads from `.env` file automatically
2. Validates types at runtime (Pydantic validation)
3. Provides typed access to config values
4. Raises error if required values missing

**ASP.NET Core Equivalent:**
```csharp
// appsettings.json + IOptions<AppSettings>
services.Configure<AppSettings>(configuration.GetSection("AppSettings"));
```

---

### 2. **app/database.py** - Database Setup

**Purpose:** SQLAlchemy engine, session management, and model registration

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Import models (for registry)
from app.models.user import User
from app.models.todo import Todo

def get_db():
    """Dependency injection for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**Components:**
- **`engine`** - Connection pool (≈ DbContext in EF Core)
- **`SessionLocal`** - Session factory for creating transaction scopes
- **`Base`** - Metadata registry for ORM models
- **`get_db()`** - FastAPI dependency for session injection

**ASP.NET Core Equivalent:**
```csharp
services.AddDbContext<TodoDbContext>(options =>
    options.UseSqlServer(configuration.GetConnectionString("DefaultConnection"))
);
```

---

### 3. **app/models/** - ORM Entity Models

#### **models/user.py**
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # One-to-many relationship: User has many Todos
    todos = relationship("Todo", back_populates="user")
```

**Key Features:**
- ✅ Auto-generates database schema
- ✅ Type-safe queries
- ✅ Relationship management
- ✅ Index definitions
- ✅ Constraint definitions

#### **models/todo.py**
```python
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    is_completed = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Many-to-one relationship: Todo belongs to User
    user = relationship("User", back_populates="todos")
```

**Relationships:**
```
User (1) ──────────── (Many) Todo
  id  <─── user_id ───  user_id
```

---

### 4. **app/routes/** - API Endpoints (Controllers)

#### **routes/auth_routes.py**
```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    
    Equivalent to ASP.NET Core:
    [HttpPost("register")]
    public IActionResult RegisterUser([FromBody] UserRegisterDto user)
    """
    existing_user = user_repository.get_user_by_email(user.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    created_user = user_repository.create_user(user=user, db=db)
    return {"message": "User registered successfully", "user": created_user}

@auth_router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Login user and return JWT token
    
    Equivalent to ASP.NET Core:
    [HttpPost("login")]
    public IActionResult Login([FromForm] LoginModel model)
    """
    user = user_repository.get_user_by_email(form_data.username, db)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
```

#### **routes/todo_routes.py**
```python
from typing import List
from fastapi import APIRouter, Depends

todo_router = APIRouter(prefix="/todos", tags=["Todos"])

@todo_router.get("/", response_model=List[TodoResponse])
def get_all_todos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Get all todos for authenticated user
    
    Equivalent to ASP.NET Core:
    [HttpGet]
    [Authorize]
    public IActionResult GetAllTodos()
    """
    return repository.get_all_todos(db)

@todo_router.post("/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create new todo
    
    Equivalent to ASP.NET Core:
    [HttpPost]
    [Authorize]
    public IActionResult CreateTodo([FromBody] TodoCreateDto todo)
    """
    return repository.create_todo(
        db, 
        todo.title, 
        user_id=current_user["id"],
        description=todo.description
    )
```

---

### 5. **app/schemas/** - Pydantic Models (DTOs)

**schemas/user.py**
```python
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    """Schema for user registration (request)"""
    username: str
    email: EmailStr  # Validates email format
    password: str

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for user response (DTO)"""
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True  # Enables ORM model conversion
```

**schemas/todo.py**
```python
from typing import Optional
from pydantic import BaseModel

class TodoCreate(BaseModel):
    """Request schema for creating todo"""
    title: str
    description: Optional[str] = None

class TodoResponse(BaseModel):
    """Response schema for todo"""
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    
    class Config:
        from_attributes = True
```

**Validation Flow:**
```
Request JSON → Pydantic Model Validation → Route Handler
                (Automatic, typed)          (Receives validated data)
```

---

### 6. **app/repositories/** - Data Access Layer

**repositories/user_repository.py**
```python
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserRegister

class UserRepository:
    """
    Encapsulates database queries for User entity
    Equivalent to ASP.NET Core repository pattern
    """
    
    def get_user_by_email(self, email: str, db: Session):
        """Equivalent to: context.Users.FirstOrDefault(u => u.Email == email)"""
        return db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username: str, db: Session):
        """Query by username"""
        return db.query(User).filter(User.username == username).first()
    
    def create_user(self, user: UserRegister, db: Session):
        """Create new user and commit to database"""
        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # Refresh to get generated ID
        return new_user
    
    def get_all_users(self, db: Session):
        """Get all users"""
        return db.query(User).all()
```

**repositories/todo_respository.py**
```python
from sqlalchemy.orm import Session
from app.models.todo import Todo

class TodoRepository:
    """Encapsulates database queries for Todo entity"""
    
    def get_all_todos(self, db: Session):
        """Get all todos - equivalent to: context.Todos.ToList()"""
        return db.query(Todo).all()
    
    def create_todo(self, db: Session, title: str, user_id: int, description: str = None):
        """Create new todo"""
        new_todo = Todo(
            title=title,
            description=description,
            user_id=user_id
        )
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    
    def get_todo_by_id(self, todo_id: int, db: Session):
        """Get todo by ID - equivalent to: context.Todos.Find(id)"""
        return db.query(Todo).filter(Todo.id == todo_id).first()
    
    def delete_todo(self, todo_id: int, db: Session):
        """Delete todo"""
        todo = self.get_todo_by_id(todo_id, db)
        if todo:
            db.delete(todo)
            db.commit()
        return todo
```

---

### 7. **app/services/** - Business Logic

**services/security_service.py**
```python
from passlib.context import CryptContext

# Configure password hashing algorithm (PBKDF2-SHA256)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash password using PBKDF2-SHA256
    Equivalent to ASP.NET Core: PasswordHasher<User>.HashPassword()
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash
    Equivalent to ASP.NET Core: PasswordHasher<User>.VerifyHashedPassword()
    """
    return pwd_context.verify(plain_password, hashed_password)
```

**services/jwt_service.py**
```python
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(user_id: int) -> str:
    """
    Create JWT token
    Equivalent to ASP.NET Core: JwtSecurityTokenHandler.WriteToken()
    """
    payload = {
        "id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Verify JWT token and extract user info
    Dependency function - called automatically for protected routes
    Equivalent to ASP.NET Core: [Authorize] attribute
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    return {"id": user_id}
```

---

## Data Flow & Request Lifecycle

### Example: User Registration Flow

```
1. CLIENT
   └─ POST /auth/register
      └─ Body: {"username": "john", "email": "john@example.com", "password": "secret"}

2. FASTAPI ROUTE (routes/auth_routes.py)
   └─ @auth_router.post("/register")
   └─ Request → Pydantic validates → UserRegister object

3. DEPENDENCY INJECTION (Depends)
   └─ get_db() called → Database session created
   └─ get_current_user() called (if protected route)

4. ROUTE HANDLER
   └─ def register_user(user: UserRegister, db: Session = Depends(get_db))
   └─ Calls user_repository.create_user(user, db)

5. REPOSITORY LAYER (repositories/user_repository.py)
   └─ Check if email exists: db.query(User).filter(...).first()
   └─ Hash password: hash_password(user.password)
   └─ Create user: db.add(new_user)
   └─ Commit: db.commit()

6. DATABASE (SQLAlchemy + MSSQL)
   └─ Execute INSERT query
   └─ Generate ID from IDENTITY column
   └─ Return new user record

7. RESPONSE (Pydantic)
   └─ TodoResponse schema serializes user to JSON
   └─ {"id": 1, "username": "john", "email": "john@example.com"}

8. CLIENT
   └─ Receives 200 OK with JSON response
```

### Example: Protected Route (Get Todos)

```
1. CLIENT
   └─ GET /todos/
   └─ Header: Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

2. FASTAPI MIDDLEWARE
   └─ Extracts token from header

3. DEPENDENCY: get_current_user
   └─ Verifies JWT signature
   └─ Validates expiration
   └─ Extracts user_id → {"id": 1}
   └─ If invalid → 401 Unauthorized

4. ROUTE HANDLER
   └─ @todo_router.get("/", response_model=List[TodoResponse])
   └─ def get_all_todos(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user))
   └─ current_user["id"] = 1

5. REPOSITORY
   └─ db.query(Todo).all() → Retrieves all todos

6. RESPONSE
   └─ List[TodoResponse] serializes to JSON array
   └─ [
   │    {"id": 1, "title": "Task 1", "description": "...", "is_completed": false},
   │    {"id": 2, "title": "Task 2", "description": "...", "is_completed": true}
   │  ]

7. CLIENT
   └─ Receives 200 OK with todos list
```

---

## Key Patterns & Best Practices

### ✅ **1. Dependency Injection Pattern**

```python
# ✓ GOOD: Dependencies declared in function signature
@router.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

# ✗ BAD: Hard-coded database access
@router.get("/todos")
def get_todos():
    db = SessionLocal()
    todos = db.query(Todo).all()
    db.close()
    return todos
```

---

### ✅ **2. Repository Pattern**

```python
# ✓ GOOD: Abstract data access in repository
@router.post("/todos")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return repository.create_todo(db, todo.title, todo.description)

# ✗ BAD: Database access in route handler
@router.post("/todos")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(title=todo.title, description=todo.description)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo
```

---

### ✅ **3. Configuration Management**

```python
# ✓ GOOD: Centralized config from environment
from app.config import settings
engine = create_engine(settings.DATABASE_URL)

# ✗ BAD: Hard-coded config
DATABASE_URL = "mssql+pyodbc://sa:sa123@localhost/todo_app_python"
engine = create_engine(DATABASE_URL)
```

---

### ✅ **4. Type Safety with Pydantic**

```python
# ✓ GOOD: Request validation automatic
@router.post("/todos")
def create_todo(todo: TodoCreate):  # Pydantic validates type
    return {"title": todo.title}

# ✗ BAD: Manual validation
@router.post("/todos")
def create_todo(data: dict):
    if "title" not in data:
        raise Exception("Missing title")
    return {"title": data["title"]}
```

---

### ✅ **5. Error Handling**

```python
# ✓ GOOD: Specific HTTP exceptions
if not user:
    raise HTTPException(status_code=404, detail="User not found")

# ✗ BAD: Generic exceptions
if not user:
    raise Exception("User not found")
```

---

### ✅ **6. Database Transactions**

```python
# ✓ GOOD: Session management with dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLAlchemy handles commits/rollbacks automatically
```

---

### ✅ **7. Password Security**

```python
# ✓ GOOD: Hash passwords with strong algorithm
password_hash = hash_password(user.password)  # PBKDF2-SHA256

# ✗ BAD: Plain text or weak hashing
user.password = user.password  # Never store plain text!
```

---

### ✅ **8. JWT Token Security**

```python
# ✓ GOOD: Short-lived tokens with expiration
def create_access_token(user_id: int):
    payload = {
        "id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=30)  # 30 min expiry
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

# ✗ BAD: Long-lived or no expiration
def create_access_token(user_id: int):
    payload = {"id": user_id}  # No expiration!
    return jwt.encode(payload, settings.SECRET_KEY)
```

---

### ✅ **9. Environment Variables**

```python
# ✓ GOOD: Secrets in .env (never in code)
# .env file:
DATABASE_URL=mssql+pyodbc:///?odbc_connect=...
SECRET_KEY=your_secret_key_here

# ✗ BAD: Hard-coded secrets
SECRET_KEY = "hardcoded_secret"  # Never!
```

---

### ✅ **10. Database Migrations**

```bash
# ✓ GOOD: Track schema changes in version control
alembic revision --autogenerate -m "Add description column"
alembic upgrade head

# ✗ BAD: Manual SQL changes
# Manually run: ALTER TABLE todos ADD description nvarchar(500)
```

---

## Comparison Table: Key Concepts

| Concept | FastAPI/Python | ASP.NET Core |
|---------|---|---|
| **Web Framework** | FastAPI | ASP.NET Core MVC/API |
| **Routing** | `@router.get()` | `[HttpGet]` attributes |
| **Controllers** | `APIRouter` classes | `ControllerBase` classes |
| **Dependency Injection** | `Depends()` | Constructor injection + DI container |
| **DTOs** | Pydantic `BaseModel` | C# classes with properties |
| **Validation** | Pydantic automatic | Data Annotations + FluentValidation |
| **ORM** | SQLAlchemy | Entity Framework Core |
| **Models** | SQLAlchemy declarative | EF Core DbSet + DbContext |
| **Queries** | `.query().filter()` | LINQ `.Where()` |
| **Migrations** | Alembic | EF Core Migrations |
| **Authentication** | JWT + OAuth2 | Identity + JWT |
| **Password Hashing** | passlib + PBKDF2 | Identity PasswordHasher |
| **Configuration** | python-dotenv + Pydantic | appsettings.json + IOptions<T> |
| **Web Server** | Uvicorn (ASGI) | Kestrel (IIS) |
| **Request Body** | Pydantic models | Model binding |
| **Response** | Return dict/object | ActionResult |
| **Status Codes** | `HTTPException` | `StatusCodes` |

---

## Directory Tree with Descriptions

```
d:\AI\todo-app\                                    # Project root
│
├── app/                                           # Application package
│   ├── __init__.py                                # Makes app a package
│   ├── main.py                                    # FastAPI app entry point
│   ├── config.py                                  # Environment configuration
│   ├── database.py                                # SQLAlchemy setup
│   │
│   ├── models/                                    # ORM entity models
│   │   ├── __init__.py
│   │   ├── user.py                                # User entity (with relationships)
│   │   └── todo.py                                # Todo entity (with FK to User)
│   │
│   ├── routes/                                    # API route handlers (Controllers)
│   │   ├── __init__.py
│   │   ├── auth_routes.py                         # /auth endpoint handlers
│   │   └── todo_routes.py                         # /todos endpoint handlers
│   │
│   ├── schemas/                                   # Pydantic models (DTOs)
│   │   ├── __init__.py
│   │   ├── user.py                                # User request/response schemas
│   │   └── todo.py                                # Todo request/response schemas
│   │
│   ├── repositories/                              # Data access layer (Repository pattern)
│   │   ├── __init__.py
│   │   ├── user_repository.py                     # User database operations
│   │   └── todo_respository.py                    # Todo database operations
│   │
│   └── services/                                  # Business logic services
│       ├── __init__.py
│       ├── jwt_service.py                         # JWT token creation & verification
│       └── security_service.py                    # Password hashing & verification
│
├── alembic/                                       # Database migration tool
│   ├── env.py                                     # Alembic environment configuration
│   ├── script.py.mako                             # Migration template
│   ├── alembic.ini                                # Alembic settings
│   └── versions/                                  # Migration history
│       └── 0001_add_description_to_todos.py       # Example migration (schema change)
│
├── .env                                           # Environment secrets (NOT in Git)
├── .env.example                                   # Template for .env (commit to Git)
├── .gitignore                                     # Git ignore rules
├── requirements.txt                               # Python package dependencies
├── debug_runner.py                                # Development server launcher
├── README.md                                      # Quick start guide
└── CODEBASE.md                                    # This comprehensive documentation
```

---

## Quick Reference: Common Tasks

### Create a New Endpoint

```python
# 1. Define request/response schemas (schemas/example.py)
class ExampleCreate(BaseModel):
    name: str
    value: int

class ExampleResponse(BaseModel):
    id: int
    name: str
    value: int
    class Config:
        from_attributes = True

# 2. Add repository method (repositories/example_repository.py)
def create_example(self, db: Session, name: str, value: int):
    new_example = Example(name=name, value=value)
    db.add(new_example)
    db.commit()
    db.refresh(new_example)
    return new_example

# 3. Add route handler (routes/example_routes.py)
@example_router.post("/", response_model=ExampleResponse)
def create_example(item: ExampleCreate, db: Session = Depends(get_db)):
    return repository.create_example(db, item.name, item.value)

# 4. Register router (app/main.py)
app.include_router(example_router)
```

---

### Add Database Migration

```bash
# 1. Modify model (app/models/example.py)
# Add new column: new_field = Column(String(100))

# 2. Generate migration
alembic revision --autogenerate -m "Add new_field to example table"

# 3. Review generated migration file (alembic/versions/xxxx_...)

# 4. Apply migration
alembic upgrade head

# 5. Verify schema changed in SQL Server
```

---

### Handle Protected Routes

```python
from fastapi import Depends
from app.services.jwt_service import get_current_user

@router.get("/my-data")
def get_my_data(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # current_user["id"] contains authenticated user's ID
    user_id = current_user["id"]
    return repository.get_user_data(db, user_id)
```

---

## ASP.NET Core Developer Cheat Sheet

| ASP.NET Core | FastAPI/Python |
|---|---|
| `new ControllerBase()` | `APIRouter()` |
| `[HttpPost]` | `@router.post()` |
| `[Authorize]` | `Depends(get_current_user)` |
| `IUserRepository userRepo` (constructor) | `Depends(get_user_repository)` |
| `DbContext` | `Session` |
| `IOptions<T>` | `BaseSettings` |
| `var user = await context.Users.FirstOrDefault()` | `db.query(User).first()` |
| `context.SaveChanges()` | `db.commit()` |
| `new User { }` | `User()` |
| `Migrations` | `Alembic` |
| `Add-Migration` | `alembic revision --autogenerate` |
| `Update-Database` | `alembic upgrade head` |
| `appsettings.json` | `.env` file |
| `PasswordHasher<T>` | `CryptContext` (passlib) |
| `JwtSecurityTokenHandler` | `python-jose` |

---

## Troubleshooting Guide

| Problem | Cause | Solution |
|---------|-------|----------|
| `ModuleNotFoundError: No module named 'app'` | Missing `__init__.py` in folders | Create `app/__init__.py` |
| `404 Not Found` on route | Router not registered | Add `app.include_router(router)` in main.py |
| `422 Unprocessable Entity` | Pydantic validation failed | Check request body matches schema |
| `401 Unauthorized` | Missing/invalid JWT token | Include `Authorization: Bearer <token>` header |
| `Connection timeout` | Database unreachable | Verify DATABASE_URL and SQL Server is running |
| `Circular import error` | Models importing each other | Use `TYPE_CHECKING` or import in database.py |
| `AttributeError: 'User' not found` | Relationship string not registered | Import models in database.py |

---

## Resources & Further Learning

### FastAPI
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)

### SQLAlchemy & ORM
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Relationships Guide](https://docs.sqlalchemy.org/en/20/orm/relationships.html)

### Pydantic
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Data Validation](https://docs.pydantic.dev/latest/concepts/validators/)

### Alembic
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [Migration Scripts](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

### JWT & Security
- [JWT.io](https://jwt.io/)
- [OAuth2 Specification](https://tools.ietf.org/html/rfc6749)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

---

**Last Updated:** 2026-06-29  
**Version:** 1.0  
**For ASP.NET Core Developers:** This codebase implements the same layered architecture and design patterns you're familiar with from ASP.NET Core, just using Python's FastAPI ecosystem.
