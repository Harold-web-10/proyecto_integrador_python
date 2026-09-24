from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import GenreEnum, MediaType


class WorkBase(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "1984",
                "description": "Una distopía sobre el control totalitario.",
                "type": "BOOK",
                "genre": "DISTOPICO",
                "author": "George Orwell",
                "release_date": "1949-06-08",
                "poster_url": "https://example.com/1984-cover.jpg",
            }
        }
    )

    title: str = Field(
        ..., min_length=1, max_length=200,
        description="Título de la obra. Máximo 200 caracteres.",
    )
    description: Optional[str] = Field(
        None, max_length=5000,
        description="Descripción de la obra. Máximo 5000 caracteres.",
    )
    type: MediaType = Field(..., description="Tipo de obra: 'book' o 'movie'.")
    genre: GenreEnum = Field(..., description="Género de la obra.")
    author: Optional[str] = Field(
        None, max_length=200,
        description="Autor del libro o director de la película.",
    )
    release_date: Optional[date] = Field(
        None, description="Fecha de lanzamiento."
    )
    poster_url: Optional[str] = Field(
        None, max_length=500,
        description="URL de la portada o poster.",
    )


class WorkCreate(WorkBase):
    pass


class WorkUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "1984 (Edición de bolsillo)",
                "description": "Edición actualizada con notas del autor.",
                "poster_url": "https://example.com/1984-pocket.jpg",
            }
        }
    )

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    type: Optional[MediaType] = None
    genre: Optional[GenreEnum] = None
    author: Optional[str] = Field(None, max_length=200)
    release_date: Optional[date] = None
    poster_url: Optional[str] = Field(None, max_length=500)


class WorkRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "1984",
                "description": "Una distopía sobre el control totalitario.",
                "type": "BOOK",
                "genre": "DISTOPICO",
                "author": "George Orwell",
                "release_date": "1949-06-08",
                "poster_url": "https://example.com/1984-cover.jpg",
                "created_at": "2026-09-15T20:00:00Z",
                "updated_at": "2026-09-15T20:00:00Z",
            }
        },
    )

    id: int
    title: str
    description: Optional[str] = None
    type: MediaType
    genre: GenreEnum
    author: Optional[str] = None
    release_date: Optional[date] = None
    poster_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
