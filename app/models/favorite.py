from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Favorite(Base):
    __tablename__ = "favorites"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "work_id",
            name="uq_favorites_user_work",
        ),
    )

    id = Column(Integer, primary_key=True, index=True, comment="ID único del favorito")
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID del usuario que marcó la obra como favorita",
    )
    work_id = Column(
        Integer,
        ForeignKey("works.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID de la obra marcada como favorita",
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Fecha de creación",
    )

    user = relationship("User", back_populates="favorites")
    work = relationship("Work", back_populates="favorites")

    def __repr__(self) -> str:
        return f"<Favorite(id={self.id!r}, user_id={self.user_id!r}, work_id={self.work_id!r})>"
