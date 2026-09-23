from app.core.dependencies import get_current_user
from app.crud.favorite import favorite_crud
from app.crud.work import work_crud
from app.database.connection import get_db
from app.models.favorite import Favorite
from app.models.user import User
from app.schemas.favorite import FavoriteCreate, FavoriteRead

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/favorites",
    tags=["favorites"],
)


@router.get("/", response_model=list[FavoriteRead])
def list_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[FavoriteRead]:
    """
    **Listar favoritos** — obtiene la lista personal de favoritos del usuario autenticado.
    """
    favorites = favorite_crud.list_by_user(db, current_user.id)
    return [FavoriteRead.model_validate(f) for f in favorites]


@router.post("/{work_id}", response_model=FavoriteRead, status_code=status.HTTP_201_CREATED)
def add_to_favorites(
    work_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FavoriteRead:
    """
    **Añadir a favoritos** — marca una obra como favorita.

    ## Parámetros de ruta
    - **work_id**: ID de la obra a marcar como favorita

    ## Respuestas
    - **201**: Obra añadida a favoritos
    - **401**: No autenticado
    - **404**: La obra no existe
    - **409**: La obra ya está en favoritos
    """
    work = work_crud.get_by_id(db, work_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Obra no encontrada.",
        )
    try:
        favorite = favorite_crud.add_to_favorites(db, current_user.id, work_id)
        return FavoriteRead.model_validate(favorite)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La obra ya está en tu lista de favoritos.",
        )


@router.delete("/{work_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_favorites(
    work_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """
    **Remover de favoritos** — quita una obra de la lista de favoritos.

    ## Parámetros de ruta
    - **work_id**: ID de la obra a remover

    ## Respuestas
    - **204**: Obra removida de favoritos
    - **401**: No autenticado
    - **404**: La obra no está en favoritos
    """
    work = work_crud.get_by_id(db, work_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Obra no encontrada.",
        )
    success = favorite_crud.remove_from_favorites(db, current_user.id, work_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La obra no está en tu lista de favoritos.",
        )
