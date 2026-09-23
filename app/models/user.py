from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import UserRole
from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="ID único del usuario")
    username = Column(
        String(50), unique=True, nullable=False, index=True, comment="Nombre de usuario único"
    )
    email = Column(
        String(255), unique=True, nullable=False, index=True, comment="Correo electrónico único"
    )
    full_name = Column(String(100), nullable=True, comment="Nombre completo del usuario")
    hashed_password = Column(
        String(255), nullable=False, comment="Contraseña hasheada con bcrypt"
    )
    avatar_url = Column(String(500), nullable=True, comment="URL de la imagen de perfil")
    role = Column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.USER,
        comment="Rol del usuario: admin o user",
    )
    is_active = Column(
        Boolean, default=True, nullable=False, comment="Indica si el usuario está activo"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Fecha de creación",
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Fecha de última actualización",
    )

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, username={self.username!r})>"
