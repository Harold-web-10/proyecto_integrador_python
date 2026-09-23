from app.core.dependencies import get_current_user
from app.core.enums import UserRole
from app.crud.review import review_crud
from app.crud.work import work_crud
from app.database.connection import get_db
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewRead, ReviewUpdate

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/reviews",
    tags=["reviews"],
)


@router.get("/", response_model=list[ReviewRead])
def list_reviews(
    work_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[ReviewRead]:
    """
    **Listar reseñas** — listado público.

    ## Parámetros de consulta
    - **work_id**: si se provee, filtra por obra
    - **skip**: paginación
    - **limit**: límite de resultados
    """
    if work_id is not None:
        reviews = review_crud.get_by_work(db, work_id, skip=skip, limit=limit)
    else:
        reviews = review_crud.get_multi(db, skip=skip, limit=limit)
    return [ReviewRead.model_validate(r) for r in reviews]


@router.get("/{review_id}", response_model=ReviewRead)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
) -> ReviewRead:
    """
    **Obtener reseña por ID**.
    """
    review = review_crud.get_by_id(db, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reseña no encontrada.",
        )
    return ReviewRead.model_validate(review)


@router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
def create_review(
    work_id: int,
    payload: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReviewRead:
    """
    **Crear reseña** — requiere autenticación.

    ## Parámetros de consulta
    - **work_id**: ID de la obra a reseñar

    ## Respuestas
    - **201**: Reseña creada
    - **401**: No autenticado
    - **404**: La obra no existe
    """
    work = work_crud.get_by_id(db, work_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Obra no encontrada.",
        )
    review = review_crud.create(db, payload, user_id=current_user.id, work_id=work_id)
    return ReviewRead.model_validate(review)


@router.put("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int,
    payload: ReviewUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReviewRead:
    """
    **Editar reseña** — *solo el autor puede editar su reseña*.
    Los administradores también pueden editar (pero no la reseñan por ellos).
    """
    review = review_crud.get_by_id(db, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reseña no encontrada.",
        )
    if review.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes editar tus propias reseñas.",
        )
    review = review_crud.update(db, review, payload)
    return ReviewRead.model_validate(review)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """
    **Eliminar reseña** — el autor puede eliminar su reseña.
    **Los administradores pueden eliminar cualquier reseña**.
    """
    review = review_crud.get_by_id(db, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reseña no encontrada.",
        )
    is_owner = review.user_id == current_user.id
    is_admin = current_user.role == UserRole.ADMIN
    if not is_owner and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo el autor o un administrador pueden eliminar esta reseña.",
        )
    review_crud.delete(db, review)
