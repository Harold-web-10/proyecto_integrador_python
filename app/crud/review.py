from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate


class CRUDReview:
    def get_by_id(self, db: Session, review_id: int) -> Optional[Review]:
        return db.get(Review, review_id)

    def get_by_user(self, db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Review]:
        return (
            db.query(Review)
            .filter(Review.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_work(self, db: Session, work_id: int, skip: int = 0, limit: int = 100) -> List[Review]:
        return (
            db.query(Review)
            .filter(Review.work_id == work_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Review]:
        return db.query(Review).offset(skip).limit(limit).all()

    def create(self, db: Session, schema: ReviewCreate, user_id: int, work_id: int) -> Review:
        db_review = Review(**schema.model_dump(), user_id=user_id, work_id=work_id)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review

    def update(self, db: Session, db_review: Review, schema: ReviewUpdate) -> Review:
        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_review, field, value)
        db.commit()
        db.refresh(db_review)
        return db_review

    def delete(self, db: Session, db_review: Review) -> None:
        db.delete(db_review)
        db.commit()


review_crud = CRUDReview()
