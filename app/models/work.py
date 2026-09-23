from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import GenreEnum, MediaType
from app.database.base import Base


class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True, index=True, comment="ID único de la obra")
    title = Column(
        String(200), nullable=False, index=True, comment="Título de la obra"
    )
    description = Column(Text, nullable=True, comment="Descripción de la obra")
    type = Column(
        "media_type",
        Enum(MediaType, name="media_type"),
        nullable=False,
        comment="Tipo de obra: book o movie",
    )
    genre = Column(
        Enum(GenreEnum, name="genre"),
        nullable=False,
        comment="Género de la obra",
    )
    author = Column(
        String(200), nullable=True, comment="Autor del libro o director de la película"
    )
    release_date = Column(Date, nullable=True, comment="Fecha de lanzamiento")
    poster_url = Column(String(500), nullable=True, comment="URL de la portada/poster")
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

    reviews = relationship(
        "Review", back_populates="work", cascade="all, delete-orphan"
    )
    favorites = relationship(
        "Favorite", back_populates="work", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Work(id={self.id!r}, title={self.title!r})>"
