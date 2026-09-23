from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rating": 5,
                "content": "Una obra maestra. Profundamente inquietante y relevante.",
            }
        }
    )

    rating: int = Field(
        ..., ge=1, le=5,
        description="Puntuación de 1 a 5 estrellas.",
    )
    content: Optional[str] = Field(
        None, max_length=2000,
        description="Contenido de la reseña. Máximo 2000 caracteres.",
    )


class ReviewCreate(ReviewBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rating": 5,
                "content": "Una obra maestra. Profundamente inquietante y relevante.",
            }
        }
    )


class ReviewUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rating": 4,
                "content": "Muy buena, aunque algo predecible en la segunda mitad.",
            }
        }
    )

    rating: Optional[int] = Field(None, ge=1, le=5, description="Puntuación de 1 a 5 estrellas.")
    content: Optional[str] = Field(None, max_length=2000, description="Contenido de la reseña.")


class ReviewRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "rating": 5,
                "content": "Una obra maestra. Profundamente inquietante y relevante.",
                "user_id": 1,
                "work_id": 1,
                "created_at": "2026-09-15T20:00:00Z",
                "updated_at": "2026-09-15T20:00:00Z",
            }
        },
    )

    id: int
    rating: int
    content: Optional[str] = None
    user_id: int
    work_id: int
    created_at: datetime
    updated_at: datetime
