from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRegister
from app.services.security_service import hash_password


class UserRepository:

    # region auth
    def get_user_by_email(self, email: str, db: Session):
        return db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str, db: Session):
        return db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserRegister, db: Session):
        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    # endregion auth

    def get_all_users(self, db: Session):
        return db.query(User).all()