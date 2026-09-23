from app.core.dependencies import get_current_admin
from app.crud.work import work_crud
from app.database.connection import get_db
from app.models.user import User
from app.schemas.work import WorkCreate, WorkRead, WorkUpdate

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/catalog",
    tags=["catalog"],
)


@router.get("/", response_model=list[WorkRead])
def list_works(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> list[WorkRead]:
    """
    **Listar obras** — listado público del catálogo.

    ## Parámetros de consulta
    - **skip**: registros a saltar (paginación)
    - **limit**: número máximo de resultados
    """
    works = work_crud.get_multi(db, skip=skip, limit=limit)
    return [WorkRead.model_validate(w) for w in works]


@router.get("/{work_id}", response_model=WorkRead)
def get_work(
    work_id: int,
    db: Session = Depends(get_db),
) -> WorkRead:
    """
    **Obtener obra por ID**.
    """
    work = work_crud.get_by_id(db, work_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Obra no encontrada.",
        )
    return WorkRead.model_validate(work)


@router.post("/", response_model=WorkRead, status_code=status.HTTP_201_CREATED)
def create_work(
    payload: WorkCreate,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> WorkRead:
    """
    **Crear obra** — requiere rol de administrador.

    ## Respuestas
    - **201**: Obra creada
    - **403**: No eres administrador
    """
    work = work_crud.create(db, payload)
    return WorkRead.model_validate(work)


@router.put("/{work_id}", response_model=WorkRead)
def update_work(
    work_id: int,
    payload: WorkUpdate,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> WorkRead:
    """
    **Actualizar obra** — requiere rol de administrador.
    """
    work = work_crud.get_by_id(db, work_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Obra no encontrada.",
        )
    work = work_crud.update(db, work, payload)
    return WorkRead.model_validate(work)


@router.delete("/{work_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work(
    work_id: int,
    _: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> None:
    """
    **Eliminar obra** — requiere rol de administrador.

    También elimina las reseñas asociadas (cascade).
    """
    work = work_crud.get_by_id(db, work_id)
    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Obra no encontrada.",
        )
    work_crud.delete(db, work)
