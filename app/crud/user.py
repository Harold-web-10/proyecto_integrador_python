from sqlalchemy.orm import Session
from typing import Optional

from app.core.security import hash_password
from app.core.enums import UserRole
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser:
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.get(User, user_id)

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def create(self, db: Session, schema: UserCreate, role: UserRole = UserRole.USER) -> User:
        db_user = User(
            username=schema.username,
            email=schema.email,
            full_name=schema.full_name,
            hashed_password=hash_password(schema.password),
            role=role,
            is_active=True,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def update(self, db: Session, db_user: User, schema: UserUpdate) -> User:
        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete(self, db: Session, db_user: User) -> None:
        db.delete(db_user)
        db.commit()

    def authenticate(self, db: Session, username: str, password: str) -> Optional[User]:
        from app.core.security import verify_password

        user = self.get_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user_crud = CRUDUser()
