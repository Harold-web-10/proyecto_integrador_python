from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.work import Work
from app.schemas.work import WorkCreate, WorkUpdate


class CRUDWork:
    def get_by_id(self, db: Session, work_id: int) -> Optional[Work]:
        return db.get(Work, work_id)

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Work]:
        return db.query(Work).offset(skip).limit(limit).all()

    def create(self, db: Session, schema: WorkCreate) -> Work:
        db_work = Work(**schema.model_dump())
        db.add(db_work)
        db.commit()
        db.refresh(db_work)
        return db_work

    def update(self, db: Session, db_work: Work, schema: WorkUpdate) -> Work:
        update_data = schema.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_work, field, value)
        db.commit()
        db.refresh(db_work)
        return db_work

    def delete(self, db: Session, db_work: Work) -> None:
        db.delete(db_work)
        db.commit()


work_crud = CRUDWork()
