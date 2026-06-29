from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegister
from app.services.jwt_service import create_access_token
from app.services.security_service import verify_password

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
user_repository = UserRepository()


@auth_router.post("/register")
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    created_user = user_repository.create_user(user=user, db=db)
    return {"message": "User registered successfully", "user": created_user}


@auth_router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Token endpoint for OAuth2 password flow (form-encoded).

    Accepts `username` and `password` as form fields (application/x-www-form-urlencoded).
    """
    username = form_data.username
    password = form_data.password

    # Support login by email or username depending on what the client provides
    existing_user = user_repository.get_user_by_email(email=username, db=db)
    if not existing_user:
        existing_user = user_repository.get_user_by_username(username=username, db=db)

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, existing_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(existing_user.id)})
    return {"access_token": token, "token_type": "bearer"}