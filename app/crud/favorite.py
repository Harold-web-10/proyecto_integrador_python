from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.favorite import Favorite


class CRUDFavorite:
    def get_by_id(self, db: Session, favorite_id: int) -> Optional[Favorite]:
        return db.get(Favorite, favorite_id)

    def get_by_user_and_work(
        self, db: Session, user_id: int, work_id: int
    ) -> Optional[Favorite]:
        return (
            db.query(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.work_id == work_id)
            .first()
        )

    def list_by_user(self, db: Session, user_id: int) -> List[Favorite]:
        return db.query(Favorite).filter(Favorite.user_id == user_id).all()

    def add_to_favorites(self, db: Session, user_id: int, work_id: int) -> Favorite:
        db_favorite = Favorite(user_id=user_id, work_id=work_id)
        db.add(db_favorite)
        db.commit()
        db.refresh(db_favorite)
        return db_favorite

    def remove_from_favorites(self, db: Session, user_id: int, work_id: int) -> bool:
        favorite = self.get_by_user_and_work(db, user_id, work_id)
        if not favorite:
            return False
        db.delete(favorite)
        db.commit()
        return True


favorite_crud = CRUDFavorite()
