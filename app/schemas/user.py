from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enums import UserRole


class UserBase(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
            }
        }
    )

    username: str = Field(
        ..., min_length=3, max_length=50,
        description="Nombre de usuario único. 3-50 caracteres.",
    )
    email: EmailStr = Field(
        ..., max_length=255,
        description="Correo electrónico único.",
    )
    full_name: Optional[str] = Field(
        None, max_length=100,
        description="Nombre completo del usuario.",
    )


class UserCreate(UserBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "password": "SuperSecret123!",
            }
        }
    )

    password: str = Field(
        ..., min_length=8, max_length=128,
        description="Contraseña. Mínimo 8 caracteres.",
    )


class UserUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "full_name": "John Doe Jr.",
                "avatar_url": "https://example.com/avatar.png",
            }
        }
    )

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None, max_length=255)
    full_name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None


class UserRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "johndoe",
                "email": "john.doe@example.com",
                "full_name": "John Doe",
                "avatar_url": None,
                "role": "user",
                "is_active": True,
                "created_at": "2026-09-15T20:00:00Z",
                "updated_at": "2026-09-15T20:00:00Z",
            }
        },
    )

    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime
