from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Review(Base):
    __tablename__ = "reviews"

    __table_args__ = (
        CheckConstraint(
            "rating >= 1 AND rating <= 5",
            name="ck_reviews_rating_range",
        ),
    )

    id = Column(Integer, primary_key=True, index=True, comment="ID único de la reseña")
    rating = Column(Integer, nullable=False, comment="Puntuación de 1 a 5 estrellas")
    content = Column(Text, nullable=True, comment="Contenido texto de la reseña")
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID del usuario que escribió la reseña",
    )
    work_id = Column(
        Integer,
        ForeignKey("works.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID de la obra reseñada",
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

    user = relationship("User", back_populates="reviews")
    work = relationship("Work", back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review(id={self.id!r}, rating={self.rating!r}, user_id={self.user_id!r}, work_id={self.work_id!r})>"
